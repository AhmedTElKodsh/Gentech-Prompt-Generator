"""
Streamlit application for the prompt generator and evaluator.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import sys
import traceback
from promptgen.utils.domain_evaluator import evaluate_prompt_with_domain
from promptgen.templates.loader import TemplateLibrary, PromptGenerator
from promptgen.utils.prompt_helper import extract_context_from_description

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="Prompt Evaluator",
        page_icon="🚀",
        layout="wide"
    )
    
    # Initialize template library and prompt generator
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "examples")
    st.session_state.debug_info = f"Loading templates from: {templates_dir}"
    
    # Check if template directory exists
    if not os.path.exists(templates_dir):
        st.error(f"Template directory not found: {templates_dir}")
        template_library = TemplateLibrary()
    else:
        template_library = TemplateLibrary(templates_dir)
        # List all templates for debugging
        st.session_state.templates = template_library.list_templates()
    
    prompt_generator = PromptGenerator(template_library)
    
    # Initialize session state variables if they don't exist
    if 'evaluate_prompt' not in st.session_state:
        st.session_state.evaluate_prompt = ""
    if 'evaluate_domain' not in st.session_state:
        st.session_state.evaluate_domain = "software"
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 0  # Default to first tab
    if 'debug_mode' not in st.session_state:
        st.session_state.debug_mode = False
    
    # Create tabs for different functionality
    tabs = st.tabs(["Prompt Evaluator", "Prompt Generator", "Debug"])
    
    # Check if we should auto-select the first tab based on session state
    if st.session_state.active_tab == 0:
        with tabs[0]:  # Prompt Evaluator tab
            st.title("Prompt Evaluator 🚀")
            st.markdown("""
            Evaluate the quality of your AI prompts with domain-specific metrics.
            """)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Auto-fill from session state if available
                prompt = st.text_area("Enter your prompt:", value=st.session_state.evaluate_prompt, height=200)
                
            with col2:
                # Pre-select domain from session state if available
                domain = st.selectbox(
                    "Select domain:", 
                    ["software", "content", "business", "creative", "education"],
                    index=["software", "content", "business", "creative", "education"].index(st.session_state.evaluate_domain)
                )
                run_llm_eval = st.checkbox("Use LLM for evaluation (slower but more accurate)")
                
                st.markdown("### Instructions")
                st.markdown("""
                1. Enter your prompt in the text area
                2. Select the domain for specialized evaluation
                3. Click 'Evaluate Prompt' to get detailed metrics
                """)
            
            eval_button = st.button("Evaluate Prompt", type="primary")
            
            if eval_button and prompt:
                with st.spinner("Evaluating prompt..."):
                    try:
                        llm = None  # We would set this if run_llm_eval is True
                        result = evaluate_prompt_with_domain(prompt, domain, llm)
                        
                        # Create tabs for different evaluation aspects
                        gen_tab, domain_tab, viz_tab, sugg_tab = st.tabs([
                            "General Metrics", 
                            f"{domain.capitalize()} Metrics",
                            "Visualization",
                            "Suggestions"
                        ])
                        
                        with gen_tab:
                            # Display general metrics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Quality Score", f"{result['quality_score']:.2f}")
                            with col2:
                                st.metric("Domain Score", f"{result['domain_quality_score']:.2f}")
                            with col3:
                                st.metric("Combined Score", f"{result['combined_quality_score']:.2f}")
                            
                            st.markdown("### General Metrics Details")
                            factor_df = pd.DataFrame({
                                'Factor': list(result["factor_scores"].keys()),
                                'Score': list(result["factor_scores"].values())
                            })
                            st.dataframe(factor_df, use_container_width=True)
                        
                        with domain_tab:
                            st.markdown(f"### {domain.capitalize()} Domain Metrics")
                            domain_df = pd.DataFrame({
                                'Factor': list(result["domain_scores"].keys()),
                                'Score': list(result["domain_scores"].values())
                            })
                            st.dataframe(domain_df, use_container_width=True)
                        
                        with viz_tab:
                            st.markdown("### Visualization of All Metrics")
                            # Create a radar chart with all scores
                            all_scores = {
                                **result["factor_scores"],
                                **result["domain_scores"]
                            }
                            
                            # Create categories and values lists
                            categories = list(all_scores.keys())
                            values = list(all_scores.values())
                            
                            # Create a radar chart
                            fig = go.Figure()
                            fig.add_trace(go.Scatterpolar(
                                r=values,
                                theta=categories,
                                fill='toself',
                                name='Score'
                            ))
                            
                            # Update layout
                            fig.update_layout(
                                polar=dict(
                                    radialaxis=dict(
                                        visible=True,
                                        range=[0, 1]
                                    )
                                ),
                                showlegend=False
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with sugg_tab:
                            st.markdown("### General Suggestions")
                            for sugg in result["suggestions"]:
                                st.write(f"- {sugg}")
                            
                            st.markdown(f"### {domain.capitalize()} Domain Suggestions")
                            for sugg in result["domain_suggestions"]:
                                st.write(f"- {sugg}")
                    
                    except Exception as e:
                        st.error(f"Error evaluating prompt: {str(e)}")
                        if st.session_state.debug_mode:
                            st.error(traceback.format_exc())
    
    if st.session_state.active_tab == 1 or 'active_tab' not in st.session_state:
        with tabs[1]:  # Prompt Generator tab
            st.title("Prompt Generator 🧠")
            st.markdown("""
            Generate high-quality prompts from simple descriptions. Select a domain and describe what you want to achieve.
            """)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                user_description = st.text_area("Describe what you want to achieve:", 
                                            placeholder="Example: Create a web application for tracking daily water intake",
                                            height=150)
                
            with col2:
                generator_domain = st.selectbox(
                    "Select domain:",
                    ["software", "content", "business", "creative", "education"],
                    key="generator_domain"
                )
                
                complexity = st.slider(
                    "Complexity level:",
                    1, 5, 3,
                    help="Higher complexity will generate more detailed prompts"
                )
                
                st.markdown("### Instructions")
                st.markdown("""
                1. Select the relevant domain
                2. Describe what you want to achieve
                3. Adjust complexity as needed
                4. Click 'Generate Prompt' button
                """)
            
            generate_button = st.button("Generate Prompt", type="primary", key="generate_prompt")
            
            if generate_button and user_description:
                with st.spinner("Generating prompt..."):
                    try:
                        # Extract context from user description
                        context = extract_context_from_description(user_description, generator_domain)
                        
                        # Set complexity from UI
                        context["complexity"] = complexity
                        
                        # Find all suitable templates
                        suitable_templates = template_library.find_templates(generator_domain, complexity)
                        if not suitable_templates:
                            template_names = ", ".join([f"{t.name} (range: {t.complexity_range})" 
                                                       for t in template_library.templates.values()])
                            st.error(f"No suitable template found for {generator_domain} domain with complexity {complexity}.")
                            st.error(f"Available templates: {template_names}")
                            raise ValueError(f"No suitable template found for {generator_domain} domain with complexity {complexity}")
                        
                        # Generate the prompt
                        generated_prompt, template_used = prompt_generator.generate_prompt(
                            objective=user_description,
                            domain=generator_domain,
                            task=context.get("task", "implementation" if generator_domain == "software" else "creation"),
                            complexity=complexity,
                            context=context
                        )
                        
                        if template_used is None:
                            st.error("Failed to select a template. Please try a different domain or complexity level.")
                            if st.session_state.debug_mode:
                                st.error(f"Generated prompt: {generated_prompt}")
                                st.error(f"Available templates: {template_library.list_templates()}")
                                st.error(f"Templates for {generator_domain} domain with complexity {complexity}: {[t.name for t in suitable_templates]}")
                        else:
                            st.success("Prompt generated successfully!")
                            
                            # Display the generated prompt
                            st.markdown("### Generated Prompt")
                            st.code(generated_prompt, language="markdown")
                            
                            # Add buttons for actions
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if st.button("Copy to Clipboard", type="secondary", key="copy_button"):
                                    st.write("Copied prompt to clipboard!")
                                    # Note: The actual clipboard functionality happens on frontend
                            
                            with col2:
                                # Create a function to handle the evaluation redirect
                                def evaluate_generated_prompt():
                                    st.session_state.evaluate_prompt = generated_prompt
                                    st.session_state.evaluate_domain = generator_domain
                                    st.session_state.active_tab = 0  # Switch to first tab
                                    st.rerun()
                                
                                if st.button("Evaluate This Prompt", type="secondary", key="evaluate_button", on_click=evaluate_generated_prompt):
                                    pass  # The action is in the on_click function
                            
                            # Show template information
                            with st.expander("Template Information"):
                                st.markdown(f"**Template Name:** {template_used.name}")
                                st.markdown(f"**Description:** {template_used.description}")
                                st.markdown("**Template Sections:**")
                                for section in template_used.sections:
                                    st.markdown(f"- {section['name']}")
                            
                            # Show extracted context
                            with st.expander("Extracted Context from Description"):
                                st.markdown("### Extracted Information")
                                for key, value in context.items():
                                    if key not in ["complexity", "task", "objective"]:
                                        st.markdown(f"**{key.replace('_', ' ').title()}:**")
                                        st.markdown(f"{value}")
                    
                    except Exception as e:
                        st.error(f"Error generating prompt: {str(e)}")
                        st.error("Please try adjusting your description or selecting a different domain.")
                        if st.session_state.debug_mode:
                            st.error(traceback.format_exc())
    
    # Debug tab
    with tabs[2]:
        st.title("Debug Information")
        st.warning("This tab is for debugging purposes only.")
        
        # Toggle debug mode
        st.session_state.debug_mode = st.checkbox("Enable detailed error messages", value=st.session_state.debug_mode)
        
        # Show template information
        st.subheader("Templates")
        st.write(f"Templates directory: {templates_dir}")
        st.write(f"Directory exists: {os.path.exists(templates_dir)}")
        
        if hasattr(st.session_state, 'templates'):
            st.write(f"Available templates: {st.session_state.templates}")
        
        # Show all templates and their details
        st.subheader("Template Details")
        for template_name, template in template_library.templates.items():
            with st.expander(f"{template_name} (Domain: {template.domain}, Complexity: {template.complexity_range})"):
                st.write(f"**Description:** {template.description}")
                st.write(f"**Tags:** {', '.join(template.tags)}")
                st.write("**Sections:**")
                for section in template.sections:
                    st.write(f"- {section['name']} (Required: {section.get('required', True)})")
        
        # System information
        st.subheader("System Information")
        st.write(f"Python version: {sys.version}")
        st.write(f"Current directory: {os.getcwd()}")
        st.write(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")
        
        # Session state
        st.subheader("Session State")
        st.write(st.session_state)

if __name__ == "__main__":
    main() 