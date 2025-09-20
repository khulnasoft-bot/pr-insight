from abc import ABC, abstractmethod
from typing import Dict, Optional


class SecretProvider(ABC):
    @abstractmethod
    def get_secret(self, secret_name: str) -> str:
        pass

    @abstractmethod
    def store_secret(self, secret_name: str, secret_value: str, metadata: Optional[Dict] = None):
        pass

    def list_secrets(self) -> Dict[str, Dict]:
        """List all stored secrets (default implementation for providers that don't support this)."""
        return {}

    def delete_secret(self, secret_name: str) -> bool:
        """Delete a secret (default implementation for providers that don't support this)."""
        return False
