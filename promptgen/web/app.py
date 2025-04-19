"""
Streamlit web application for the AI Prompt Generator.

This module provides a user-friendly interface for generating,
refining, and managing AI prompts.
"""

import streamlit as st
import logging
from typing import Dict, List, Any, Optional
import json
import os
import pandas as pd
import altair as alt
import time

from promptgen.core.classifier import DomainClassifier
from promptgen.core.generator import PromptGenerator
from promptgen.core.refiner import PromptRefiner
from promptgen.core.technique_selector import TechniqueSelector
from promptgen.domains import get_domain_service
from promptgen.utils.evaluator import PromptEvaluator
from promptgen.utils.domain_evaluator import DomainSpecificEvaluator, evaluate_prompt_with_domain

# Setup logger
logger = logging.getLogger(__name__)

class NotificationManager:
    """Manages notifications and alerts in the application."""
    
    @staticmethod
    def success(message: str, duration: int = 3) -> None:
        """Show a success notification."""
        st.toast(f"✅ {message}", icon="✅")
    
    @staticmethod
    def error(message: str, duration: int = 5) -> None:
        """Show an error notification."""
        st.toast(f"❌ {message}", icon="❌")
    
    @staticmethod
    def info(message: str, duration: int = 3) -> None:
        """Show an info notification."""
        st.toast(f"ℹ️ {message}", icon="ℹ️")
    
    @staticmethod
    def warning(message: str, duration: int = 4) -> None:
        """Show a warning notification."""
        st.toast(f"⚠️ {message}", icon="⚠️")
    
    @staticmethod
    def processing(message: str) -> None:
        """Show a processing status."""
        return st.status(f"⏳ {message}", expanded=True)

def create_app():
    """Configure the Streamlit application."""
    # Initialize components
    classifier = DomainClassifier()
    generator = PromptGenerator()
    refiner = PromptRefiner()
    technique_selector = TechniqueSelector()
    evaluator = PromptEvaluator()
    notifications = NotificationManager()
    
    # Main application
    def run():
        st.title("🚀 AI Prompt Generator")
        st.subheader("Create optimized prompts for any purpose")
        
        # Sidebar for advanced options
        with st.sidebar:
            st.header("Options")
            view_mode = st.radio("View Mode", ["Basic", "Advanced"], index=0)
            
            if view_mode == "Advanced":
                st.subheader("Advanced Settings")
                selected_domain = st.selectbox(
                    "Domain",
                    ["Auto-detect", "Software Development", "Content Creation", "Business Strategy", "Data Analysis"],
                    index=0
                )
                
                complexity = st.slider(
                    "Complexity Level",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="Higher values generate more sophisticated prompts"
                )
                
                apply_techniques = st.multiselect(
                    "Apply Techniques",
                    [
                        "Chain of Thought", 
                        "Role Prompting", 
                        "Few-Shot Examples",
                        "Step-by-Step",
                        "Self-Consistency",
                        "Tree of Thoughts",
                        "XML Tagging",
                        "ReAct"
                    ],
                    default=["Role Prompting", "Step-by-Step"]
                )
                
                include_phrases = st.multiselect(
                    "Include Special Phrases",
                    [
                        "Take a deep breath and work on this problem step-by-step",
                        "This is very important to my career",
                        "You are a world-class expert",
                        "Let's think about this logically"
                    ],
                    default=[]
                )
                
                output_format = st.selectbox(
                    "Output Format",
                    ["Markdown", "Plain Text", "JSON"],
                    index=0
                )
            
            st.header("About")
            st.markdown("""
            **AI Prompt Generator** helps you create effective prompts for AI models.
            
            Features:
            - Domain-specific optimization
            - Advanced prompting techniques
            - Refinement suggestions
            """)
        
        # Main tabs
        tabs = st.tabs(["Generate", "Evaluate", "Templates", "Learn"])
        
        # Generate Tab
        with tabs[0]:
            st.header("Generate Prompt")
            user_input = st.text_area("Enter your objective:", height=100)
            
            if st.button("Generate Prompt"):
                with notifications.processing("Generating optimized prompt...") as status:
                    try:
                        # Domain Classification
                        status.update(label="Detecting domain...")
                        time.sleep(0.5)  # Simulate processing
                        detected_domain = classifier.classify(user_input)
                        notifications.info(f"Detected domain: {detected_domain}")
                        
                        # Technique Selection
                        status.update(label="Selecting techniques...")
                        time.sleep(0.5)  # Simulate processing
                        selected_techniques = technique_selector.select(user_input, detected_domain)
                        
                        # Generate Prompt
                        status.update(label="Generating prompt...")
                        time.sleep(0.5)  # Simulate processing
                        generated_prompt = generator.generate(
                            user_input,
                            domain=detected_domain,
                            techniques=selected_techniques
                        )
                        
                        # Display Results
                        st.text_area("Generated Prompt:", value=generated_prompt, height=200)
                        notifications.success("Prompt generated successfully!")
                        
                        # Copy button
                        if st.button("📋 Copy to Clipboard"):
                            st.write("Copied to clipboard!")
                            
                    except Exception as e:
                        logger.error(f"Error generating prompt: {str(e)}")
                        notifications.error(f"Error generating prompt: {str(e)}")
                        status.update(label="Error occurred!", state="error")
        
        # Evaluate Tab
        with tabs[1]:
            st.header("Evaluate Prompt")
            
            # Create two columns for input area
            col1, col2 = st.columns([3, 1])
            
            with col1:
                eval_input = st.text_area("Enter prompt to evaluate:", height=200)
            
            with col2:
                # Add domain selection dropdown
                domain = st.selectbox(
                    "Select domain for evaluation:",
                    ["general", "software", "content", "business", "creative", "education"],
                    index=0
                )
                
                # Add option to run LLM-based evaluation
                run_llm_eval = st.checkbox("Run LLM-based evaluation", value=False)
                
                # Add a notice about LLM evaluation
                if run_llm_eval:
                    st.info("LLM evaluation makes API calls to test your prompt. This may take a moment.")
                
                # Evaluation button
                evaluate_button = st.button("Evaluate Prompt")
            
            if evaluate_button and eval_input:
                with st.spinner("Evaluating prompt..."):
                    try:
                        # Use domain-specific evaluation if a domain is selected
                        if domain != "general":
                            # Initialize LLM client if needed
                            llm_client = None
                            if run_llm_eval:
                                from promptgen.utils.llm import get_default_llm_client
                                llm_client = get_default_llm_client()
                            
                            # Use domain-specific evaluator
                            evaluation = evaluate_prompt_with_domain(eval_input, domain, llm_client)
                            
                            # Create tabs for different evaluation views
                            eval_tabs = st.tabs(["Overview", "General Metrics", "Domain Metrics", "Suggestions"])
                            
                            # Overview tab - show key metrics
                            with eval_tabs[0]:
                                st.subheader("Quality Scores")
                                
                                # Create metrics display
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("General Quality", f"{evaluation['quality_score']:.2f}")
                                with col2:
                                    st.metric(f"{domain.capitalize()} Quality", f"{evaluation['domain_quality_score']:.2f}")
                                with col3:
                                    st.metric("Combined Score", f"{evaluation['combined_quality_score']:.2f}")
                                
                                # Display word count
                                st.metric("Word Count", evaluation["word_count"])
                                
                                # Create radar chart for factor scores
                                if evaluation["factor_scores"] and evaluation.get("domain_scores"):
                                    import pandas as pd
                                    import plotly.graph_objects as go
                                    
                                    # Combine general and domain scores
                                    all_scores = {**evaluation["factor_scores"], **evaluation.get("domain_scores", {})}
                                    
                                    # Create radar chart data
                                    categories = list(all_scores.keys())
                                    values = list(all_scores.values())
                                    
                                    fig = go.Figure()
                                    
                                    fig.add_trace(go.Scatterpolar(
                                        r=values,
                                        theta=categories,
                                        fill='toself',
                                        name='Score'
                                    ))
                                    
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
                            
                            # General metrics tab
                            with eval_tabs[1]:
                                st.subheader("General Quality Factors")
                                
                                # Show general factor scores
                                factor_scores = evaluation["factor_scores"]
                                
                                # Convert to DataFrame for better display
                                df = pd.DataFrame({
                                    'Factor': list(factor_scores.keys()),
                                    'Score': list(factor_scores.values())
                                })
                                
                                # Create horizontal bar chart
                                fig = go.Figure(go.Bar(
                                    x=df['Score'],
                                    y=df['Factor'],
                                    orientation='h',
                                    marker_color='steelblue'
                                ))
                                
                                fig.update_layout(
                                    title='General Quality Factors',
                                    xaxis_title='Score',
                                    yaxis_title='Factor',
                                    xaxis=dict(range=[0, 1])
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                            
                            # Domain-specific metrics tab
                            with eval_tabs[2]:
                                st.subheader(f"{domain.capitalize()} Domain Factors")
                                
                                # Show domain-specific factor scores
                                domain_scores = evaluation.get("domain_scores", {})
                                
                                if domain_scores:
                                    # Convert to DataFrame for better display
                                    df = pd.DataFrame({
                                        'Factor': list(domain_scores.keys()),
                                        'Score': list(domain_scores.values())
                                    })
                                    
                                    # Create horizontal bar chart
                                    fig = go.Figure(go.Bar(
                                        x=df['Score'],
                                        y=df['Factor'],
                                        orientation='h',
                                        marker_color='indianred'
                                    ))
                                    
                                    fig.update_layout(
                                        title=f'{domain.capitalize()} Domain Factors',
                                        xaxis_title='Score',
                                        yaxis_title='Factor',
                                        xaxis=dict(range=[0, 1])
                                    )
                                    
                                    st.plotly_chart(fig, use_container_width=True)
                                else:
                                    st.info("No domain-specific metrics available.")
                            
                            # Suggestions tab
                            with eval_tabs[3]:
                                st.subheader("Improvement Suggestions")
                                
                                # Display general suggestions
                                st.write("**General Suggestions:**")
                                for suggestion in evaluation.get("suggestions", []):
                                    st.markdown(f"- {suggestion}")
                                
                                # Display domain-specific suggestions
                                domain_suggestions = evaluation.get("domain_suggestions", [])
                                if domain_suggestions:
                                    st.write(f"**{domain.capitalize()} Domain Suggestions:**")
                                    for suggestion in domain_suggestions:
                                        st.markdown(f"- {suggestion}")
                        
                        else:
                            # Use standard evaluator for "general" domain
                            evaluation = evaluator.evaluate(eval_input)
                            
                            # Display metrics
                            st.subheader("Quality Metrics")
                            
                            col1, col2, col3, col4, col5 = st.columns(5)
                            with col1:
                                st.metric("Clarity", f"{evaluation['factor_scores']['clarity']:.2f}")
                            with col2:
                                st.metric("Specificity", f"{evaluation['factor_scores']['specificity']:.2f}")
                            with col3:
                                st.metric("Structure", f"{evaluation['factor_scores']['structure']:.2f}")
                            with col4:
                                st.metric("Context", f"{evaluation['factor_scores']['context']:.2f}")
                            with col5:
                                st.metric("Actionability", f"{evaluation['factor_scores']['actionability']:.2f}")
                            
                            # Overall quality
                            st.metric("Overall Quality", f"{evaluation['quality_score']:.2f}")
                            
                            # Create radar chart for factor scores
                            import pandas as pd
                            import plotly.graph_objects as go
                            
                            factor_scores = evaluation["factor_scores"]
                            categories = list(factor_scores.keys())
                            values = list(factor_scores.values())
                            
                            fig = go.Figure()
                            
                            fig.add_trace(go.Scatterpolar(
                                r=values,
                                theta=categories,
                                fill='toself',
                                name='Score'
                            ))
                            
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
                            
                            # Display suggestions
                            st.subheader("Improvement Suggestions")
                            for suggestion in evaluation.get("suggestions", []):
                                st.markdown(f"- {suggestion}")
                        
                        # If LLM evaluation was run, show response metrics
                        if run_llm_eval and "response_consistency" in evaluation:
                            st.subheader("LLM Response Metrics")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Response Consistency", f"{evaluation.get('response_consistency', 0):.2f}")
                            with col2:
                                st.metric("Avg Response Length", evaluation.get("response_length", 0))
                            with col3:
                                st.metric("Avg Response Time", f"{evaluation.get('response_time', 0):.2f}s")
                            
                            # Show sample responses
                            if "sample_responses" in evaluation:
                                st.subheader("Sample Responses")
                                for i, response in enumerate(evaluation["sample_responses"]):
                                    with st.expander(f"Response {i+1} (Length: {response.get('length', 0)})"):
                                        st.text(response.get("text", ""))
                    
                    except Exception as e:
                        st.error(f"Error evaluating prompt: {str(e)}")
        
        # Templates Tab
        with tabs[2]:
            st.header("Prompt Templates")
            # Template content here
            
        # Learn Tab
        with tabs[3]:
            st.header("Learn Prompt Engineering")
            # Learning content here

    # Return the run function    
    return run

def main():
    """Run the Streamlit application."""
    app = create_app()
    app()

if __name__ == "__main__":
    main() 