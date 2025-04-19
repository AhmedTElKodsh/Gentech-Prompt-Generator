#!/usr/bin/env python3
"""
Test script that directly creates a prompt for a software development task.
"""

# Import the necessary modules
from promptgen.domains.domain_service import default_service
import sys

# Turn on debugging
print("Python version:", sys.version)
print("Available domains:", default_service.get_available_domains())
print("Available roles:", default_service.get_supported_roles())

# Define our test input with an explicit software developer role
test_input = "As a software developer, I want to create a daily joke NextJS web app with Tailwind CSS"

# Extract the domain and clean objective
domain, clean_objective = default_service.extract_role_from_objective(test_input)

print(f"Detected domain: {domain}")
print(f"Clean objective: {clean_objective}")

# Create context with necessary details for a software project
context = {
    "objective": clean_objective,
    "domain": domain,
    "complexity": 3,
    "technology_stack": "Next.js, React, Tailwind CSS",
    "project_type": "web application",
    "features": "daily joke display, joke categories, user favorites",
    "purpose": "entertainment",
    "apis": "jokes API",
    "user_stories": [
        "As a user, I want to see a new joke every day",
        "As a user, I want to save my favorite jokes",
        "As a user, I want to browse jokes by category"
    ]
}

# Define sections that should be populated for a software project
sections = [
    {
        "name": "Task Description",
        "content_template": "You are tasked with building {objective}. This will involve creating a {project_type} using {technology_stack}."
    },
    {
        "name": "Technical Requirements",
        "content_template": "Please implement this with the following technical requirements:\n\n- {technology_stack}\n- Feature set: {features}\n- Integration with {apis}\n\nThe solution should be responsive, intuitive, and visually appealing."
    },
    {
        "name": "Architecture Overview",
        "content_template": "Design a clean architecture for this {project_type} that separates concerns:\n\n1. Frontend/UI layer built with Next.js and Tailwind CSS\n2. API integration layer for fetching jokes\n3. State management for user preferences\n4. Data persistence for saved jokes"
    },
    {
        "name": "Implementation Approach",
        "content_template": "Implement this solution using the following approach:\n\n1. Set up a Next.js project with Tailwind CSS\n2. Create the main layout and page structure\n3. Implement the joke fetching and display logic\n4. Add user preference and favorite saving functionality\n5. Ensure responsive design across all device sizes"
    }
]

# Generate content for each section
print("\n" + "="*80)
print("GENERATED PROMPT:")
print("="*80)

for section in sections:
    print(f"Processing section: {section['name']}")
    try:
        populated_content = default_service.populate_section(section, context)
        print(f"\n# {section['name']}")
        print(populated_content)
    except Exception as e:
        print(f"Error populating section {section['name']}: {str(e)}")

print("="*80) 