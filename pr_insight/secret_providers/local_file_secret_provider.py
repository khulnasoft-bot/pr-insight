import hashlib
import hmac
import json
import os
import secrets
import string
from pathlib import Path
from typing import Dict, Optional, Tuple

from pr_insight.config_loader import get_settings
from pr_insight.log import get_logger
from pr_insight.secret_providers.secret_provider import SecretProvider


class LocalFileSecretProvider(SecretProvider):
    """
    A secure local file-based secret provider that uses:
    - Safe ID generation for secret names
    - Key splitting for enhanced security
    - HMAC verification for integrity
    """

    def __init__(self):
        self.logger = get_logger()
        self.secrets_dir = Path(get_settings().get("CONFIG.SECRETS_DIR", "./secrets"))
        self.secrets_dir.mkdir(parents=True, exist_ok=True)
        self.key_parts_file = self.secrets_dir / "key_parts.json"
        self.master_key = self._get_or_create_master_key()

    def _get_or_create_master_key(self) -> bytes:
        """Get or create a master key for encryption/decryption."""
        master_key_file = self.secrets_dir / ".master_key"

        if master_key_file.exists():
            return master_key_file.read_bytes()

        # Generate a new master key
        master_key = secrets.token_bytes(32)
        master_key_file.write_bytes(master_key)
        # Set restrictive permissions
        master_key_file.chmod(0o600)
        return master_key

    def _generate_safe_id(self, client_key: str) -> str:
        """Generate a safe ID from client key using HMAC."""
        safe_id = hmac.new(
            self.master_key,
            client_key.encode(),
            hashlib.sha256
        ).hexdigest()[:16]  # Use first 16 chars for safety
        return safe_id

    def _split_key(self, key: str) -> Tuple[str, str]:
        """Split a key into two parts for enhanced security."""
        if len(key) < 16:
            # Pad short keys
            key = key.ljust(16, secrets.choice(string.ascii_letters + string.digits))

        mid = len(key) // 2
        part1 = key[:mid]
        part2 = key[mid:]

        # Add random padding to each part
        part1 += secrets.token_hex(8)
        part2 += secrets.token_hex(8)

        return part1, part2

    def _combine_key(self, part1: str, part2: str) -> str:
        """Combine two key parts back into the original key."""
        # Remove padding (last 16 chars of each part)
        part1_clean = part1[:-16]
        part2_clean = part2[:-16]
        return part1_clean + part2_clean

    def _save_key_parts(self, safe_id: str, key_parts: Dict[str, str], metadata: Dict):
        """Save key parts to file with metadata."""
        data = {
            "safe_id": safe_id,
            "key_parts": key_parts,
            "metadata": metadata,
            "hmac": self._generate_hmac(key_parts, metadata)
        }

        secrets_file = self.secrets_dir / f"{safe_id}.json"
        with open(secrets_file, 'w') as f:
            json.dump(data, f, indent=2)

        # Set restrictive permissions
        secrets_file.chmod(0o600)

    def _load_key_parts(self, safe_id: str) -> Optional[Dict]:
        """Load key parts from file and verify integrity."""
        secrets_file = self.secrets_dir / f"{safe_id}.json"

        if not secrets_file.exists():
            return None

        try:
            with open(secrets_file, 'r') as f:
                data = json.load(f)

            # Verify HMAC
            expected_hmac = self._generate_hmac(data["key_parts"], data["metadata"])
            if not hmac.compare_digest(data["hmac"], expected_hmac):
                self.logger.error(f"Secret file {safe_id} failed integrity check")
                return None

            return data
        except Exception as e:
            self.logger.error(f"Failed to load secret {safe_id}: {e}")
            return None

    def _generate_hmac(self, key_parts: Dict, metadata: Dict) -> str:
        """Generate HMAC for data integrity verification."""
        data_str = json.dumps({"key_parts": key_parts, "metadata": metadata}, sort_keys=True)
        return hmac.new(self.master_key, data_str.encode(), hashlib.sha256).hexdigest()

    def get_secret(self, client_key: str) -> str:
        """Get secret by client key."""
        safe_id = self._generate_safe_id(client_key)
        data = self._load_key_parts(safe_id)

        if not data:
            return ""

        try:
            combined_key = self._combine_key(
                data["key_parts"]["part1"],
                data["key_parts"]["part2"]
            )
            return combined_key
        except Exception as e:
            self.logger.error(f"Failed to reconstruct secret for {client_key}: {e}")
            return ""

    def store_secret(self, client_key: str, secret_value: str, metadata: Optional[Dict] = None):
        """Store secret with key splitting and safe ID."""
        if metadata is None:
            metadata = {}

        safe_id = self._generate_safe_id(client_key)
        key_part1, key_part2 = self._split_key(secret_value)

        key_parts = {
            "part1": key_part1,
            "part2": key_part2
        }

        # Add metadata
        metadata.update({
            "client_key_hash": hashlib.sha256(client_key.encode()).hexdigest()[:16],
            "created_at": str(Path(self.secrets_dir).stat().st_mtime) if self.secrets_dir.exists() else None,
            "safe_id": safe_id
        })

        try:
            self._save_key_parts(safe_id, key_parts, metadata)
            self.logger.info(f"Secret stored successfully for client: {client_key[:8]}...")
        except Exception as e:
            self.logger.error(f"Failed to store secret for {client_key}: {e}")
            raise e

    def list_secrets(self) -> Dict[str, Dict]:
        """List all stored secrets with metadata (for admin purposes)."""
        secrets = {}

        try:
            for secret_file in self.secrets_dir.glob("*.json"):
                if secret_file.name.startswith("."):
                    continue  # Skip hidden files

                safe_id = secret_file.stem
                data = self._load_key_parts(safe_id)

                if data:
                    secrets[safe_id] = {
                        "metadata": data["metadata"],
                        "file_path": str(secret_file),
                        "file_size": secret_file.stat().st_size
                    }
        except Exception as e:
            self.logger.error(f"Failed to list secrets: {e}")

        return secrets

    def delete_secret(self, client_key: str) -> bool:
        """Delete a secret by client key."""
        safe_id = self._generate_safe_id(client_key)
        secrets_file = self.secrets_dir / f"{safe_id}.json"

        if secrets_file.exists():
            try:
                secrets_file.unlink()
                self.logger.info(f"Secret deleted for client: {client_key[:8]}...")
                return True
            except Exception as e:
                self.logger.error(f"Failed to delete secret for {client_key}: {e}")
                return False
        return False
