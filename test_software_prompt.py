#!/usr/bin/env python3
"""
Test script for the software domain prompt generator.
"""

import os
import yaml
from promptgen.templates.loader import PromptTemplate
from promptgen.domains.software import SoftwareContentStrategy

# Load the software template
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, "promptgen", "templates", "examples", "software_template.yaml")

# Load the template from YAML
with open(template_path, 'r') as f:
    template_data = yaml.safe_load(f)

# Create the template object
template = PromptTemplate.from_dict(template_data)

# Test input
objective = "I want to create a daily joke NextJS web app with tailwind library"

# Create context with all required keys
context = {
    "objective": objective,
    "domain": "software",
    "complexity": 3,
    "technology_stack": "Next.js, React, Tailwind CSS",
    "project_type": "web application",
    "features": "daily joke display, joke categories, user favorites",
    "purpose": "entertainment",
    # Additional required keys from template
    "key_components": "frontend UI, joke API integration, and user management",
    "requirements": "1. NextJS for frontend\n2. Tailwind CSS for styling\n3. External joke API integration\n4. User favorites functionality",
    "quality_attributes": "responsive, fast-loading, and mobile-friendly",
    "architecture_patterns": "MVC, Clean Architecture",
    "language_stack": "JavaScript/TypeScript with NextJS and React",
    "data_entities": "User, Joke, Category, Favorite",
    "usage_example": "A user visits the site, sees the joke of the day, logs in, and saves it to favorites",
    "language": "JavaScript",
    "additional_requirements": "Mobile responsiveness is a key requirement"
}

# Create software strategy
software_strategy = SoftwareContentStrategy()

# Populate the template sections
for section in template.sections:
    section_content = software_strategy.populate(section, context)
    template.set_section_content(section["name"], section_content)

# Render the final prompt
generated_prompt = template.render()

# Print the result
print("\n" + "="*80)
print("INPUT PROMPT:")
print(objective)
print("\n" + "="*80)
print("GENERATED PROMPT:")
print(generated_prompt)
print("="*80) 