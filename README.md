# AI Prompt Generator

A sophisticated system for generating specialized prompts tailored to different domains and use cases.

## Overview

The AI Prompt Generator creates structured, domain-specific prompts based on user objectives. It uses template-based generation with domain-specific content strategies to produce high-quality prompts that follow best practices for each domain.

## Features

- Domain-specific prompt generation
- Template-based structure with conditional sections
- Role-based personalization
- Integrated prompting techniques
- Customizable templates
- Prompt quality evaluation
- Streamlit-based web interface
- Visual prompt quality metrics

## Web Interface

The system now provides a modern, user-friendly Streamlit interface with:

- **Generate Tab**: Create new prompts with domain-specific optimization
- **Evaluate Tab**: Assess prompt quality and get improvement suggestions
- **Templates Tab**: Browse sample templates for different domains
- **Learn Tab**: Educational resources about prompt engineering techniques

### Prompt Evaluation

The system includes a sophisticated prompt evaluation module that:

- Analyzes prompt quality across multiple dimensions (clarity, specificity, structure, etc.)
- Provides a numerical quality score (0-1)
- Generates specific improvement suggestions
- Allows comparison between different prompt versions
- Visualizes quality metrics for better understanding

## Domains Supported

The system currently supports the following domains:

- **Software Development**: Programming, application architecture, debugging, etc.
- **Content Creation**: Writing, blogging, copywriting, etc.
- **Business Strategy**: Market analysis, planning, metrics, etc.
- **Data Analysis**: Data exploration, visualization, statistical analysis, etc.
- **Video Editing**: Post-production, editing techniques, etc.

## Role-Based Prompt Generation

The AI Prompt Generator now supports role-based prompt customization. Users can specify their professional role at the beginning of their input, and the system will:

1. Automatically detect the role
2. Map it to the appropriate domain
3. Generate a domain-specific prompt tailored to that professional context

### Supported Roles

The system recognizes roles in the following categories:

#### Software Development
- Software Developer
- Programmer
- Web Developer
- Backend Developer
- Frontend Developer
- Full Stack Developer
- DevOps Engineer

#### Digital Marketing
- Digital Marketer
- Marketing Specialist
- SEO Specialist
- Social Media Manager
- PPC Specialist
- Email Marketer
- Marketing Analyst
- Growth Hacker

#### Content Creation
- Content Creator
- Content Writer
- Copywriter
- Blogger
- Journalist
- Editor
- Content Strategist
- Technical Writer

#### Video Editing
- Video Editor
- Videographer
- Film Editor
- Motion Graphics Designer
- Video Producer

### How to Use Role-Based Prompts

To use the role-based functionality, simply start your input with your role, followed by a colon, comma, dash, or space:

```
Software Developer: I need to create an authentication system for a React application
```

```
Video Editor - Need to create smooth transitions between interview segments
```

```
As a Content Writer, I need to create an engaging blog post about AI technologies
```

```
Digital Marketer: How to optimize Google Ads for higher conversion rates
```

The system will automatically detect your role, remove it from the input, and use the appropriate domain-specific template to generate a tailored prompt.

## Getting Started

### Prerequisites

- Python 3.11+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prompt-generator.git
cd prompt-generator
```

2. Create and activate the virtual environment:
```bash
python -m venv venv311
```

3. Activate the virtual environment:
   - On Windows:
   ```bash
   venv311\Scripts\activate
   ```
   - On macOS/Linux:
   ```bash
   source venv311/bin/activate
   ```

4. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development and testing
```

Note: All required packages are already installed in the venv311 environment. If you need to recreate the environment, follow the steps above.

5. Set up environment variables:
```bash
cp .env.example .env
```
Then edit the `.env` file with your LLM API credentials.

### Running the Application

#### Flask Interface
```bash
python -m promptgen.main
```
Access the Flask web interface at http://localhost:5000

#### Streamlit Interface (Recommended)
```bash
streamlit run streamlit_app.py
```
Access the Streamlit web interface at http://localhost:8501

## Advanced Prompt Engineering Techniques

The system supports several advanced prompt engineering techniques:

### Chain of Thought
Guides the AI through step-by-step reasoning to improve complex problem-solving.

### Role Prompting
Assigns the AI a specific role to set context and expectations for the response.

### Few-Shot Examples
Demonstrates the desired pattern with examples before asking for a new response.

### Tree of Thoughts
Explores multiple reasoning paths simultaneously for complex problems.

### ReAct (Reasoning + Acting)
Combines reasoning with specific actions to solve multi-step problems.

### Emotional Stimuli
Uses phrases that have been shown to improve AI performance like "This is very important to my career" or "Take a deep breath and work through this step-by-step."

## Project Structure

```
prompt-generator/
├── promptgen/              # Main package
│   ├── __init__.py
│   ├── main.py             # Flask application entry point
│   ├── core/               # Core functionality
│   │   ├── __init__.py
│   │   ├── classifier.py   # Domain classification
│   │   ├── generator.py    # Prompt generation
│   │   ├── refiner.py      # Prompt refinement
│   │   └── technique_selector.py # Technique selection
│   ├── domains/            # Domain-specific components
│   │   ├── __init__.py
│   │   ├── software.py     # Software development prompts
│   │   ├── content.py      # Content creation prompts 
│   │   ├── business.py     # Business strategy prompts
│   │   └── data_analysis.py # Data analysis prompts
│   ├── templates/          # Prompt templates
│   │   ├── __init__.py
│   │   └── loader.py       # Template loading utilities
│   ├── techniques/         # Prompting techniques
│   │   ├── __init__.py
│   │   ├── library.py      # Core technique library
│   │   └── advanced.py     # Advanced techniques
│   ├── utils/              # Utility functions
│   │   ├── __init__.py
│   │   ├── llm.py          # LLM API integration
│   │   └── evaluator.py    # Prompt evaluation utilities
│   └── web/                # Web interfaces
│       ├── __init__.py
│       └── app.py          # Streamlit application
├── streamlit_app.py        # Streamlit launcher
├── tests/                  # Test suite
├── requirements.txt        # Dependencies
├── .env.example            # Example environment variables
└── README.md               # This file
```

## License

MIT 

## References & Acknowledgments

We would like to express our gratitude to the following projects, libraries, and resources that have inspired or contributed to the development of this prompt generator:

### Core Libraries
- [Streamlit](https://streamlit.io/) - The powerful framework behind our web interface
- [Flask](https://flask.palletsprojects.com/) - Alternative web framework for the API interface
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - For managing environment variables

### LLM & AI Integration
- [OpenAI](https://openai.com/) - For API integration with GPT models
- [Marimo](https://github.com/marimo-team/marimo) - Reactive notebook inspiration for testing and evaluation
- [PromptTools](https://github.com/hegelai/prompttools) - Inspired our experimental testing frameworks
- [Microsoft Prompt-Engine](https://github.com/microsoft/prompt-engine) - Influenced our prompt architecture design
- [Promptfoo](https://github.com/promptfoo/promptfoo) - Inspired our evaluation methodologies

### Prompt Engineering Resources
- [Awesome-Prompt-Engineering](https://github.com/promptslab/Awesome-Prompt-Engineering) - Comprehensive resource for prompt techniques
- [Dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) - Excellent educational materials
- [Promptify](https://github.com/promptslab/Promptify) - For NLP-specific prompt patterns

### Testing Frameworks
- [Pytest](https://docs.pytest.org/) - For comprehensive testing suite
- [Preset-io/Promptimize](https://github.com/preset-io/promptimize) - Evaluation toolkit concepts

### UI/UX
- [Cursor](https://github.com/bmadcode/cursor-custom-agents-rules-generator) - Integration concepts for IDE enhancement

This project stands on the shoulders of these remarkable open-source projects. We are grateful to their developers and contributors for making their work available to the community.

# Configuration System Tests

This repository contains tests for the configuration management system.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## Running Tests

Run all tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=./ --cov-report=html
```

## Test Structure

The test suite covers:
- Default configuration values
- Environment variable overrides
- Dynamic configuration updates
- Notification settings
- UI configuration
- Configuration persistence

Each test case is documented with assertions and expected behaviors. 