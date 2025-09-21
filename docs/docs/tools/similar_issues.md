## Overview
The similar issue tool retrieves the most similar issues to the current issue.
It can be invoked manually by commenting on any PR:
```
/similar_issue
```


## Example usage

![similar_issue_original_issue](https://khulnasoft/images/pr_insight/similar_issue_original_issue.png){width=768}

![similar_issue_comment](https://khulnasoft/images/pr_insight/similar_issue_comment.png){width=768}

![similar_issue](https://khulnasoft/images/pr_insight/similar_issue.png){width=768}

Note that to perform retrieval, the `similar_issue` tool indexes all the repo previous issues (once).

### Selecting a Vector Database
Configure your preferred database by changing the `pr_similar_issue` parameter in `configuration.toml` file.

#### Available Options
Choose from the following Vector Databases:

1. LanceDB
2. Pinecone
3. **Qdrant** *(New!)*

#### Pinecone Configuration
To use Pinecone with the `similar issue` tool, add these credentials to `.secrets.toml` (or set as environment variables):

```
[pinecone]
api_key = "..."
environment = "..."
```
These parameters can be obtained by registering to [Pinecone](https://app.pinecone.io/?sessionType=signup/).

#### Qdrant Configuration
To use Qdrant with the `similar issue` tool, add these credentials to `.secrets.toml` (or set as environment variables):

```
[qdrant]
url = "http://localhost:6333"  # Your Qdrant server URL
# api_key = "your-api-key"  # Optional, for Qdrant Cloud
```

**Installation:**
```bash
pip install qdrant-client
```

**Qdrant Setup Options:**

1. **Local Installation:**
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

2. **Qdrant Cloud:**
   - Sign up at [Qdrant Cloud](https://cloud.qdrant.io/)
   - Create a new cluster
   - Use the provided connection URL and API key

3. **Self-hosted:**
   - Install Qdrant following the [official documentation](https://qdrant.tech/documentation/install/)
   - Configure the server URL in your configuration

**Performance Benefits:**
- **High Performance**: Optimized for vector similarity search
- **Flexible Filtering**: Advanced filtering capabilities for repository-specific searches
- **Scalable**: Handles large collections efficiently
- **RESTful API**: Easy integration with existing infrastructure

**Configuration Example:**
```toml
[pr_similar_issue]
vectordb = "qdrant"
max_issues_to_scan = 500

[qdrant]
url = "https://your-cluster.cloud.qdrant.io"
api_key = "your-qdrant-api-key"
```


## How to use
- To invoke the 'similar issue' tool from **CLI**, run:
`python3 cli.py --issue_url=... similar_issue`

- To invoke the 'similar' issue tool via online usage, [comment](https://github.com/Khulnasoft/pr-insight/issues/178#issuecomment-1716934893) on a PR:
`/similar_issue`

- You can also enable the 'similar issue' tool to run automatically when a new issue is opened, by adding it to the [pr_commands list in the github_app section](https://github.com/Khulnasoft/pr-insight/blob/main/pr_insight/settings/configuration.toml#L66)
