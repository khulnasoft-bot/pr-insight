## Repository Metadata Configuration for Enhanced Context

In addition to the automatic metadata injection described above, Pr Merge supports **repository-specific metadata configuration** that provides enhanced context awareness for AI models.

### Configuration Options

Repository metadata can be configured in several ways:

#### 1. Global Configuration File
Add repository metadata settings to your organization's `.pr_insight.toml`:

```toml
[repository_metadata]
enabled = true
repository_type = "application"
technology_stack = "python,fastapi,postgresql,docker"
maturity_level = "development"
complexity_level = "enterprise"
custom_context = "This is a microservices-based application handling financial transactions with high security requirements"

best_practices_file = "docs/best-practices.md"
guidelines_file = "CONTRIBUTING.md"

context_enhancements = [
    "Consider security implications for financial transactions",
    "Follow microservices architecture patterns",
    "Ensure database transaction integrity",
    "Maintain API versioning consistency"
]
```

#### 2. Repository-Specific Configuration
Add metadata configuration to individual repositories via `.pr_insight.toml`:

```toml
[repository_metadata]
repository_type = "library"
technology_stack = "typescript,react,nextjs"
maturity_level = "stable"
complexity_level = "moderate"
custom_context = "React component library for internal UI components"

context_enhancements = [
    "Follow component design system guidelines",
    "Ensure accessibility compliance",
    "Maintain consistent prop interfaces"
]
```

### Repository Metadata Fields

#### Repository Type Classification
Classify your repository for better context understanding:
- `"application"` - Production applications and services
- `"library"` - Reusable component libraries
- `"framework"` - Development frameworks and tools
- `"tool"` - Development and build tools
- `"documentation"` - Documentation repositories
- `"config"` - Configuration management
- `"other"` - Other types of repositories

#### Technology Stack Identification
Specify the technology stack (comma-separated):
```toml
technology_stack = "python,fastapi,postgresql,docker,kubernetes"
```

#### Maturity Level
Indicate repository maturity:
- `"experimental"` - Early stage, unstable
- `"development"` - Active development
- `"stable"` - Production ready, stable
- `"mature"` - Well-established, widely used
- `"legacy"` - Maintenance mode, deprecated features

#### Complexity Level
Indicate project complexity:
- `"simple"` - Small, straightforward projects
- `"moderate"` - Medium complexity with some advanced features
- `"complex"` - Large, complex applications
- `"enterprise"` - Enterprise-scale applications with complex requirements

#### Custom Context
Provide domain-specific context:
```toml
custom_context = "Healthcare application handling patient data with HIPAA compliance requirements"
```

#### Best Practices Integration
Link to repository-specific best practices:
```toml
best_practices_file = "docs/development-best-practices.md"
guidelines_file = "CONTRIBUTING.md"
```

#### Context Enhancements
Custom prompt enhancements for specific repository needs:
```toml
context_enhancements = [
    "Follow healthcare industry security standards",
    "Ensure HIPAA compliance for data handling",
    "Consider patient privacy implications"
]
```

### How Repository Metadata Enhances Analysis

#### 1. Enhanced Prompt Generation
Repository metadata is automatically injected into AI prompts:

```
## Repository Context
- **Type**: application
- **Technology Stack**: python,fastapi,postgresql
- **Maturity Level**: development
- **Complexity Level**: enterprise
- **Custom Context**: Financial transaction processing with high security requirements

## Context Enhancements
- Consider security implications for financial transactions
- Follow microservices architecture patterns
- Ensure database transaction integrity
- Maintain API versioning consistency
```

#### 2. Dynamic Context Discovery
When `auto_discover_context = true`, Pr Merge automatically analyzes repository files to discover:
- Project structure and patterns
- Technology stack verification
- Code organization conventions
- Testing and documentation practices

#### 3. Multi-Stage Analysis Integration
Repository metadata enhances all analysis stages:

- **Describe**: More accurate PR type classification
- **Review**: Context-aware code suggestions
- **Improve**: Repository-specific improvement recommendations
- **Ask**: Better understanding of repository context

#### 4. Best Practices Integration
Repository-specific best practices are automatically incorporated:

- Referenced best practice files are analyzed for context
- Guidelines are used to inform code review standards
- Custom context enhancements improve AI understanding

### Benefits of Repository Metadata

#### 1. **Improved Accuracy**
- AI models better understand repository-specific patterns
- Context-aware suggestions reduce false positives
- Domain-specific knowledge enhances analysis quality

#### 2. **Consistency**
- Standardized approach across different repository types
- Consistent application of best practices
- Unified coding standards enforcement

#### 3. **Efficiency**
- Reduced need for manual context explanation
- Faster analysis with pre-configured context
- Automated best practices integration

#### 4. **Scalability**
- Organization-wide standards application
- Automated context discovery
- Reduced configuration overhead

### Example Configurations

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
    "Follow e-commerce UX patterns"
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
    "Ensure proper data handling and validation"
]
```

### Configuration Precedence

Repository metadata follows the same precedence rules as other configurations:

1. **Repository-specific** (`.pr_insight.toml` in repo)
2. **Organization-level** (from `pr-insight-settings` repo)
3. **Default values**

This ensures that specific repository needs can override organization-wide settings while maintaining sensible defaults.
