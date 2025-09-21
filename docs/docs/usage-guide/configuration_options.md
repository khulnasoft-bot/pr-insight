The different tools and sub-tools used by Pr Merge are adjustable via the **[configuration file](https://github.com/Khulnasoft/pr-insight/blob/main/pr_insight/settings/configuration.toml)**.

In addition to general configuration options, each tool has its own configurations. For example, the `review` tool will use parameters from the [pr_reviewer](https://github.com/Khulnasoft/pr-insight/blob/main/pr_insight/settings/configuration.toml#L16) section in the configuration file.
See the [Tools Guide](https://pr-insight-docs.khulnasoft.com/tools/) for a detailed description of the different tools and their configurations.

There are three ways to set persistent configurations:

1. Wiki configuration page 💎
2. Local configuration file
3. Global configuration file 💎

In terms of precedence, wiki configurations will override local configurations, and local configurations will override global configurations.

!!! tip "Tip1: edit only what you need"
    Your configuration file should be minimal, and edit only the relevant values. Don't copy the entire configuration options, since it can lead to legacy problems when something changes.
!!! tip "Tip2: show relevant configurations"
    If you set `config.output_relevant_configurations=true`, each tool will also output in a collapsible section its relevant configurations. This can be useful for debugging, or getting to know the configurations better.

## Wiki configuration file 💎

`Platforms supported: GitHub, GitLab, Bitbucket`

With Pr Merge, you can set configurations by creating a page called `.pr_insight.toml` in the [wiki](https://github.com/Khulnasoft/pr-insight/wiki/pr_insight.toml) of the repo.
The advantage of this method is that it allows to set configurations without needing to commit new content to the repo - just edit the wiki page and **save**.


![wiki_configuration](https://khulnasoft/images/pr_insight/wiki_configuration.png){width=512}

Click [here](https://khulnasoft/images/pr_insight/wiki_configuration_pr_insight.mp4) to see a short instructional video. We recommend surrounding the configuration content with triple-quotes (or \`\`\`toml), to allow better presentation when displayed in the wiki as markdown.
An example content:

```toml
[pr_description]
generate_ai_title=true
```

Pr Merge will know to remove the surrounding quotes when reading the configuration content.

## Local configuration file

`Platforms supported: GitHub, GitLab, Bitbucket, Azure DevOps`


By uploading a local `.pr_insight.toml` file to the root of the repo's default branch, you can edit and customize any configuration parameter. Note that you need to upload `.pr_insight.toml` prior to creating a PR, in order for the configuration to take effect.

For example, if you set in `.pr_insight.toml`:

```
[pr_reviewer]
extra_instructions="""\
- instruction a
- instruction b
...
"""
```

Then you can give a list of extra instructions to the `review` tool.


## Global configuration file 💎

`Platforms supported: GitHub, GitLab, Bitbucket`

If you create a repo called `pr-insight-settings` in your **organization**, its configuration file `.pr_insight.toml` will be used as a global configuration file for any other repo that belongs to the same organization.
Parameters from a local `.pr_insight.toml` file, in a specific repo, will override the global configuration parameters.

For example, in the GitHub organization `Khulnasoft`:

- The file [`https://github.com/Khulnasoft/pr-insight-settings/.pr_insight.toml`](https://github.com/Khulnasoft/pr-insight-settings/blob/main/.pr_insight.toml)  serves as a global configuration file for all the repos in the GitHub organization `Khulnasoft`.

- The repo [`https://github.com/Khulnasoft/pr-insight`](https://github.com/Khulnasoft/pr-insight/blob/main/.pr_insight.toml) inherits the global configuration file from `pr-insight-settings`.

## Repository Metadata Configuration 💎

Repository metadata configuration allows you to provide enhanced context awareness for AI models by specifying repository-specific information such as technology stack, maturity level, and custom context.

### Configuration Structure

Add the `[repository_metadata]` section to your configuration file:

```toml
[repository_metadata]
enabled = true
repository_type = "application"
technology_stack = "python,fastapi,postgresql,docker"
maturity_level = "development"
complexity_level = "enterprise"
custom_context = "Financial transaction processing application"

best_practices_file = "docs/best-practices.md"
guidelines_file = "CONTRIBUTING.md"

context_enhancements = [
    "Consider security implications for financial transactions",
    "Follow microservices architecture patterns",
    "Ensure database transaction integrity"
]
```

### Configuration Options

#### Basic Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable repository metadata injection |
| `repository_type` | string | `"other"` | Repository classification (see options below) |
| `technology_stack` | string | `""` | Comma-separated technology list |
| `maturity_level` | string | `"development"` | Repository maturity (see options below) |
| `complexity_level` | string | `"moderate"` | Project complexity (see options below) |
| `custom_context` | string | `""` | Domain-specific context description |

#### Repository Type Options
- `"application"` - Production applications and services
- `"library"` - Reusable component libraries
- `"framework"` - Development frameworks and tools
- `"tool"` - Development and build tools
- `"documentation"` - Documentation repositories
- `"config"` - Configuration management
- `"other"` - Other types of repositories

#### Maturity Level Options
- `"experimental"` - Early stage, unstable
- `"development"` - Active development
- `"stable"` - Production ready, stable
- `"mature"` - Well-established, widely used
- `"legacy"` - Maintenance mode, deprecated features

#### Complexity Level Options
- `"simple"` - Small, straightforward projects
- `"moderate"` - Medium complexity with some advanced features
- `"complex"` - Large, complex applications
- `"enterprise"` - Enterprise-scale applications with complex requirements

#### Advanced Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `auto_discover_context` | boolean | `true` | Enable automatic context discovery |
| `max_context_files` | integer | `50` | Maximum files to analyze for context |
| `best_practices_file` | string | `""` | Path to best practices file |
| `guidelines_file` | string | `""` | Path to guidelines file |
| `context_enhancements` | array | `[]` | Custom prompt enhancements |

### Configuration Examples

#### E-commerce Application
```toml
[repository_metadata]
repository_type = "application"
technology_stack = "nodejs,react,postgresql,redis,docker"
maturity_level = "stable"
complexity_level = "enterprise"
custom_context = "E-commerce platform with payment processing and inventory management"

context_enhancements = [
    "Consider payment security implications",
    "Ensure inventory consistency across services",
    "Follow e-commerce UX patterns",
    "Maintain shopping cart state integrity"
]
```

#### Machine Learning Library
```toml
[repository_metadata]
repository_type = "library"
technology_stack = "python,tensorflow,pytorch,scikit-learn"
maturity_level = "development"
complexity_level = "complex"
custom_context = "Deep learning library for computer vision applications"

context_enhancements = [
    "Follow machine learning best practices",
    "Consider model performance optimization",
    "Ensure proper data handling and validation",
    "Maintain backward compatibility for API changes"
]
```

#### Microservices Framework
```toml
[repository_metadata]
repository_type = "framework"
technology_stack = "go,kubernetes,grpc,protobuf,istio"
maturity_level = "mature"
complexity_level = "enterprise"
custom_context = "Microservices framework for cloud-native applications"

best_practices_file = "docs/framework-best-practices.md"
guidelines_file = "CONTRIBUTING.md"

context_enhancements = [
    "Follow microservices architecture principles",
    "Ensure service mesh compatibility",
    "Consider distributed system challenges",
    "Maintain API contract consistency"
]
```

### Benefits

1. **Enhanced Context Awareness**: AI models receive repository-specific context
2. **Improved Accuracy**: Better understanding of project patterns and conventions
3. **Consistency**: Standardized approach across different repository types
4. **Domain Expertise**: Custom context for specialized domains
5. **Best Practices Integration**: Automatic incorporation of repository guidelines

### Configuration Precedence

Repository metadata follows the standard configuration precedence:

1. **Repository-specific** settings (`.pr_insight.toml` in repo)
2. **Organization-level** settings (from `pr-insight-settings` repo)
3. **Default values**

This ensures flexibility while maintaining sensible defaults across your organization.
