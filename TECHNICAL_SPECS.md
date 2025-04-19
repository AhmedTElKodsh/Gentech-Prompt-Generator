# AI Prompt Generator Technical Specifications

## 1. System Architecture

### 1.1 Overview

The AI Prompt Generator is built as a layered application with clear separation of concerns, integrated with Marimo reactive notebooks for testing and iteration:

```
┌─────────────────────────────────────────────┐    ┌─────────────────────────────────────────────┐
│                Web Interface                │◄───►│            Marimo Integration              │
└───────────────────────┬─────────────────────┘    └─────────────────┬───────────────────────────┘
                        │                                            │
┌───────────────────────▼─────────────────────┐                      │
│                 Core Services               │                      │
├─────────────────┬─────────────┬─────────────┤                      │
│   Classifier    │  Generator  │   Refiner   │◄─────────────────────┘
└─────────────────┴──────┬──────┴─────────────┘
                         │
┌────────────────────────▼────────────────────┐
│               Domain Services               │
├─────────────────┬─────────────┬─────────────┤
│    Software     │   Content   │  Business   │
└─────────────────┴──────┬──────┴─────────────┘
                         │
┌────────────────────────▼────────────────────┐
│              Template Services              │
├─────────────────┬─────────────┬─────────────┤
│  Base Templates │  Structures │ Components  │
└─────────────────┴──────┬──────┴─────────────┘
                         │
┌────────────────────────▼────────────────────┐
│               Utility Services              │
├─────────────────┬─────────────┬─────────────┤
│   LLM Clients   │   Parsers   │   Helpers   │
└─────────────────┴─────────────┴─────────────┘
```

### 1.2 Component Descriptions

#### 1.2.1 Web Interface
- Flask-based web application
- REST API endpoints
- HTML/CSS/JavaScript frontend
- Integration buttons for Marimo testing

#### 1.2.2 Core Services
- Domain classification engine
- Prompt generation system
- Prompt refinement capabilities

#### 1.2.3 Domain Services
- Domain-specific content generation
- Specialized knowledge bases
- Domain heuristics and best practices

#### 1.2.4 Template Services
- Template class hierarchy
- Section definitions and composition
- Structure patterns for different prompt types

#### 1.2.5 Utility Services
- LLM API integrations
- Input/output parsing
- Helper functions and common utilities

#### 1.2.6 Marimo Integration
- Reactive notebook environment
- Multi-model testing capabilities
- Prompt iteration and version control
- Collaborative prompt repository

## 2. Data Flow

### 2.1 Prompt Generation Flow

```
User Input → Classification → Template Selection → Content Population → Formatting → Output
```

1. **User Input**: User provides high-level objective
2. **Classification**: System identifies domain, complexity, and components
3. **Template Selection**: Appropriate template structure is selected
4. **Content Population**: Template is filled with domain-specific content
5. **Formatting**: Final prompt is formatted for the target LLM
6. **Output**: Structured prompt is presented to the user

### 2.2 Prompt Refinement Flow

```
Existing Prompt → Parsing → Analysis → Enhancement → Formatting → Output
```

1. **Existing Prompt**: User provides an existing prompt
2. **Parsing**: System extracts structure and content
3. **Analysis**: Quality assessment and gap identification
4. **Enhancement**: Improvements are generated
5. **Formatting**: Enhanced prompt is formatted
6. **Output**: Improved prompt is presented to the user

### 2.3 Marimo Testing Flow

```
Generated Prompt → Marimo Export → Multi-Model Testing → Comparison → Iteration → Version Control
```

1. **Generated Prompt**: User generates prompt using the main application
2. **Marimo Export**: Prompt is exported to Marimo notebook environment
3. **Multi-Model Testing**: Prompt is tested against multiple LLM providers
4. **Comparison**: Results are compared and visualized
5. **Iteration**: User refines the prompt based on insights
6. **Version Control**: Changes are tracked and stored in the repository

## 3. Key Design Patterns

### 3.1 Factory Pattern
Used for creating different types of templates and prompt structures based on the input requirements.

```python
class TemplateFactory:
    @staticmethod
    def create_template(domain_type, complexity, components):
        if domain_type == "software":
            return SoftwareTemplate(complexity, components)
        elif domain_type == "content":
            return ContentTemplate(complexity, components)
        elif domain_type == "business":
            return BusinessTemplate(complexity, components)
        else:
            return GenericTemplate(complexity, components)
```

### 3.2 Strategy Pattern
Used for implementing different content population strategies for various domains.

```python
class ContentPopulationStrategy:
    def populate(self, template, context):
        pass

class SoftwareContentStrategy(ContentPopulationStrategy):
    def populate(self, template, context):
        # Software-specific content population
        pass

class ContentCreationStrategy(ContentPopulationStrategy):
    def populate(self, template, context):
        # Content creation-specific population
        pass
```

### 3.3 Composite Pattern
Used for building complex prompt structures from reusable components.

```python
class PromptComponent:
    def render(self):
        pass

class PromptSection(PromptComponent):
    def __init__(self, title, content):
        self.title = title
        self.content = content
    
    def render(self):
        return f"# {self.title}\n{self.content}"

class PromptContainer(PromptComponent):
    def __init__(self):
        self.children = []
    
    def add(self, component):
        self.children.append(component)
    
    def render(self):
        return "\n\n".join(child.render() for child in self.children)
```

### 3.4 Template Method Pattern
Used for defining the skeleton of prompt generation algorithms, with specific steps implemented by subclasses.

```python
class BaseGenerator:
    def generate_prompt(self, objective):
        domain_type = self.classify_domain(objective)
        template = self.select_template(domain_type, objective)
        self.populate_template(template, objective)
        return self.format_output(template)
    
    def classify_domain(self, objective):
        # To be implemented by subclasses
        pass
    
    def select_template(self, domain_type, objective):
        # To be implemented by subclasses
        pass
    
    def populate_template(self, template, objective):
        # To be implemented by subclasses
        pass
    
    def format_output(self, template):
        # Common implementation
        return template.render()
```

### 3.5 Observer Pattern
Used for implementing reactive updates in the Marimo integration.

```python
class PromptObserver:
    def update(self, prompt, results):
        pass

class MarimoDashboard(PromptObserver):
    def update(self, prompt, results):
        # Update the dashboard with new results
        self.render_comparison(results)
        self.update_metrics(prompt, results)
```

## 4. Data Models

### 4.1 Domain

```python
class Domain:
    def __init__(self, name, keywords, techniques, best_practices):
        self.name = name
        self.keywords = keywords
        self.techniques = techniques
        self.best_practices = best_practices
```

### 4.2 Template

```python
class Template:
    def __init__(self, name, sections, required_components=None):
        self.name = name
        self.sections = sections
        self.required_components = required_components or []
        self.content = {section: "" for section in sections}
    
    def set_content(self, section, content):
        if section in self.sections:
            self.content[section] = content
    
    def render(self):
        result = []
        for section in self.sections:
            if self.content[section]:
                result.append(f"# {section}\n{self.content[section]}")
        return "\n\n".join(result)
```

### 4.3 Prompt

```python
class Prompt:
    def __init__(self, template, domain, complexity):
        self.template = template
        self.domain = domain
        self.complexity = complexity
        self.generated_text = ""
        self.versions = []  # For version tracking
    
    def set_generated_text(self, text):
        self.generated_text = text
        self.versions.append({"timestamp": datetime.now(), "text": text})
    
    def to_dict(self):
        return {
            "domain": self.domain.name,
            "complexity": self.complexity,
            "template": self.template.name,
            "content": self.generated_text,
            "versions": self.versions
        }
```

### 4.4 PromptVersion

```python
class PromptVersion:
    def __init__(self, prompt_id, text, timestamp, metrics=None):
        self.prompt_id = prompt_id
        self.text = text
        self.timestamp = timestamp
        self.metrics = metrics or {}
        self.model_results = {}
    
    def add_model_result(self, model_name, result, metrics):
        self.model_results[model_name] = {
            "result": result,
            "metrics": metrics
        }
```

## 5. API Endpoints

### 5.1 Prompt Generation

```
POST /api/generate
```

**Request Body:**
```json
{
  "objective": "Create a daily joke web app",
  "domain": "software",  // Optional, if known
  "complexity": "medium",  // Optional
  "additional_context": "Should include user authentication and voting on jokes"
}
```

**Response:**
```json
{
  "prompt": "# Task Description\nCreate a daily joke web app with user authentication and voting capabilities.\n\n# Technical Requirements\n...",
  "structure": {
    "sections": ["Task Description", "Technical Requirements", "User Stories", "Constraints", "Expected Output"]
  },
  "domain": "software",
  "complexity": "medium"
}
```

### 5.2 Prompt Refinement

```
POST /api/refine
```

**Request Body:**
```json
{
  "existing_prompt": "Create a web app that shows a new joke every day and lets users vote...",
  "objective": "Make it more specific for a React and Node.js stack",
  "desired_improvements": ["Technical detail", "Architecture guidance"]
}
```

**Response:**
```json
{
  "original_prompt": "Create a web app that shows a new joke every day and lets users vote...",
  "refined_prompt": "# Task Description\nCreate a daily joke web app using React for the frontend and Node.js for the backend...\n\n# Technical Architecture\n...",
  "improvements": [
    {
      "type": "Added section",
      "section": "Technical Architecture",
      "reason": "To provide specific guidance on React and Node.js implementation"
    }
  ]
}
```

### 5.3 Marimo Export

```
POST /api/export/marimo
```

**Request Body:**
```json
{
  "prompt_id": "12345",
  "models": ["gpt-4", "claude-3", "gemini-pro"]  // Optional, models to test against
}
```

**Response:**
```json
{
  "notebook_url": "http://localhost:8000/notebooks/prompt-12345",
  "prompt_id": "12345",
  "models": ["gpt-4", "claude-3", "gemini-pro"]
}
```

### 5.4 Model Comparison

```
POST /api/compare
```

**Request Body:**
```json
{
  "prompt_id": "12345",
  "models": ["gpt-4", "claude-3", "gemini-pro"],
  "metrics": ["relevance", "specificity", "coherence"]
}
```

**Response:**
```json
{
  "prompt_id": "12345",
  "results": {
    "gpt-4": {
      "response": "...",
      "metrics": {
        "relevance": 0.92,
        "specificity": 0.85,
        "coherence": 0.89
      }
    },
    "claude-3": {
      "response": "...",
      "metrics": {
        "relevance": 0.88,
        "specificity": 0.91,
        "coherence": 0.87
      }
    },
    "gemini-pro": {
      "response": "...",
      "metrics": {
        "relevance": 0.84,
        "specificity": 0.79,
        "coherence": 0.82
      }
    }
  },
  "comparison_summary": "Claude-3 provided the most specific response, while GPT-4 scored highest on relevance and coherence."
}
```

## 6. Storage Schema

### 6.1 Template Storage

Templates are stored as YAML files in the `templates` directory:

```yaml
name: "Software Development Basic"
domain: "software"
complexity_range: [1, 3]
sections:
  - name: "Task Description"
    required: true
    position: 1
  - name: "Technical Requirements"
    required: true
    position: 2
  - name: "Constraints"
    required: false
    position: 3
  - name: "Expected Output"
    required: true
    position: 4
```

### 6.2 Domain Knowledge Storage

Domain-specific knowledge is stored in structured YAML files:

```yaml
domain: "software"
keywords:
  - web app
  - website
  - software
  - application
techniques:
  - name: "Specific technology stack prompt"
    description: "Specify languages, frameworks, and tools to ensure appropriate code output"
    template: "Use {technology_stack} to implement this solution."
best_practices:
  - name: "Testing reminder"
    description: "Remind the model to include testing approaches"
    template: "Include appropriate testing strategies such as unit tests, integration tests, and end-to-end tests."
```

### 6.3 Prompt Repository Storage

Prompt versions and testing results are stored in a structured database:

```json
{
  "prompt_id": "12345",
  "original_text": "# Task\nCreate a web app...",
  "domain": "software",
  "created_at": "2023-05-15T14:30:00Z",
  "user_id": "user_789",
  "versions": [
    {
      "version_id": "v1",
      "text": "# Task\nCreate a web app...",
      "timestamp": "2023-05-15T14:30:00Z",
      "model_results": {
        "gpt-4": {
          "response": "...",
          "metrics": {
            "relevance": 0.85,
            "specificity": 0.78
          }
        }
      }
    },
    {
      "version_id": "v2",
      "text": "# Task\nCreate a React web app...",
      "timestamp": "2023-05-15T15:20:00Z",
      "model_results": {
        "gpt-4": {
          "response": "...",
          "metrics": {
            "relevance": 0.91,
            "specificity": 0.86
          }
        }
      }
    }
  ],
  "tags": ["web", "react", "frontend"]
}
```

## 7. Error Handling

### 7.1 Input Validation

- All user inputs are validated for format and content
- Malformed inputs trigger specific error responses
- Maximum input lengths are enforced

### 7.2 Error Responses

All API errors follow a consistent format:

```json
{
  "error": {
    "code": "INVALID_OBJECTIVE",
    "message": "The objective must be a non-empty string.",
    "details": {
      "field": "objective",
      "constraint": "non-empty string"
    }
  }
}
```

### 7.3 Logging

- All errors are logged with timestamps and request context
- Critical errors trigger alerts
- Request/response pairs are logged for debugging

## 8. Performance Considerations

### 8.1 Caching

- Template selection results are cached to reduce processing time
- Domain classification results are cached for similar objectives
- Common prompt patterns are cached for quick retrieval

### 8.2 Async Processing

- Long-running operations like complex prompt generation use asynchronous processing
- Users receive immediate feedback on request receipt
- Webhook notifications when processing is complete

### 8.3 Scaling

- Stateless design allows horizontal scaling
- Resource-intensive operations (classification, LLM calls) can be offloaded to worker processes
- Rate limiting protects against abuse

## 9. Marimo Integration

### 9.1 Reactive Notebook Architecture

The Marimo integration leverages reactive notebooks for interactive prompt testing and iteration:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Marimo Notebook                             │
│                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │
│  │  Prompt Import  │───►│  Model Testing  │───►│ Result Analysis │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘  │
│           │                      │                       │          │
│           ▼                      ▼                       ▼          │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │
│  │ Interactive     │    │ Multi-Model     │    │ Visualization &  │  │
│  │ Prompt Editor   │◄──►│ Comparison      │◄──►│ Metrics          │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘  │
│           │                      │                       │          │
│           └──────────────────────┼───────────────────────┘          │
│                                  │                                  │
│                                  ▼                                  │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │
│  │ Version Control │◄──►│ Prompt Repository│◄──►│ Export Options  │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Prompt Generator Core                          │
└─────────────────────────────────────────────────────────────────────┘
```

### 9.2 Multi-Model Testing

The system supports testing prompts against multiple language models simultaneously:

- **Model Integration**: Unified API for connecting to various LLM providers
- **Parallel Testing**: Simultaneous prompt execution across multiple models
- **Result Comparison**: Side-by-side comparison of model outputs
- **Metric Calculation**: Automated quality metrics for each response
- **Visualization**: Interactive charts and tables for comparing results

### 9.3 Version Control System

The version control system tracks prompt iterations and their performance:

- **History Tracking**: Maintains a complete history of prompt changes
- **Diff Visualization**: Highlights changes between versions
- **Performance Comparison**: Tracks quality metrics across versions
- **Metadata**: Stores context, model preferences, and annotations
- **Branching**: Supports experimental branches for prompt development

### 9.4 Prompt Repository

The prompt repository provides a collaborative space for prompt management:

- **Organization**: Categorization by domain, technique, and purpose
- **Searchability**: Full-text and metadata-based search capabilities
- **Sharing**: Controlled access for team collaboration
- **Templates**: Conversion of successful prompts into reusable templates
- **Analytics**: Usage tracking and effectiveness metrics

### 9.5 Integration APIs

The following APIs facilitate the connection between the main application and Marimo notebooks:

#### 9.5.1 Prompt Export API
Exports prompts from the main application to Marimo notebooks

#### 9.5.2 Result Import API
Imports testing results from Marimo back to the main application

#### 9.5.3 Repository Access API
Provides access to the shared prompt repository

#### 9.5.4 Version Control API
Interfaces with the version tracking system

### 9.6 Reactive UI Components

The system includes reactive UI components for real-time prompt editing and testing:

- **Interactive Editor**: Real-time prompt editing with syntax highlighting
- **Results Dashboard**: Live-updating results from multiple models
- **Metric Panels**: Dynamic visualization of quality metrics
- **Suggestion System**: Real-time improvement suggestions
- **Comparison Sliders**: Interactive tools for comparing outputs

### 9.7 Technical Implementation

The Marimo integration is implemented using:

- **Python-Based Notebooks**: Pure Python implementation for easy version control
- **Reactive Execution Engine**: Automatic dependency tracking and cell execution
- **Web Components**: Interactive UI elements with responsive design
- **API Integration Layer**: Secure connection to multiple LLM providers
- **Database Backend**: Storage for prompt versions and test results 