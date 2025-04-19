"""
Integration tests for the Streamlit UI with domain-specific evaluator.
"""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import plotly.graph_objects as go

from promptgen.utils.domain_evaluator import DomainSpecificEvaluator, evaluate_prompt_with_domain

@pytest.fixture
def mock_evaluation_result():
    """Fixture for a mock evaluation result."""
    return {
        "quality_score": 0.85,
        "word_count": 150,
        "factor_scores": {
            "clarity": 0.9,
            "specificity": 0.8,
            "structure": 0.7,
            "context": 0.6,
            "actionability": 0.9
        },
        "suggestions": ["Add more context"],
        "domain": "software",
        "domain_scores": {
            "technical_accuracy": 0.8,
            "implementation_detail": 0.7,
            "security_consideration": 0.6,
            "maintainability": 0.5,
            "testability": 0.4
        },
        "domain_quality_score": 0.75,
        "combined_quality_score": 0.81,
        "domain_suggestions": ["Add security considerations"]
    }

def test_evaluation_result_structure():
    """Test that the evaluation structure is correct for UI display."""
    # Create a basic evaluator
    evaluator = DomainSpecificEvaluator(domain="software")
    
    # Use a simple test prompt
    test_prompt = "Create a Python function to parse JSON data."
    
    # Get evaluation results
    results = evaluator.evaluate(test_prompt)
    
    # Check structure required for UI
    assert "quality_score" in results
    assert "factor_scores" in results
    assert "domain" in results
    assert "domain_scores" in results
    assert "domain_quality_score" in results
    assert "combined_quality_score" in results
    
    # Domain scores should contain expected keys for software domain
    domain_scores = results["domain_scores"]
    expected_keys = ["technical_accuracy", "implementation_detail", 
                    "security_consideration", "maintainability", "testability"]
    
    for key in expected_keys:
        assert key in domain_scores
    
    # Test creating pandas DataFrame for UI display
    factor_df = pd.DataFrame({
        'Factor': list(results["factor_scores"].keys()),
        'Score': list(results["factor_scores"].values())
    })
    
    domain_df = pd.DataFrame({
        'Factor': list(results["domain_scores"].keys()),
        'Score': list(results["domain_scores"].values())
    })
    
    # Check that DataFrames have the right structure
    assert len(factor_df) == len(results["factor_scores"])
    assert len(domain_df) == len(results["domain_scores"])
    assert 'Factor' in factor_df.columns
    assert 'Score' in factor_df.columns

@patch('plotly.graph_objects.Figure')
@patch('plotly.graph_objects.Scatterpolar')
def test_plotly_visualization(mock_scatterpolar, mock_figure, mock_evaluation_result):
    """Test that we can create Plotly visualizations from evaluation results."""
    # Create a mock figure
    mock_fig = MagicMock()
    mock_figure.return_value = mock_fig
    
    # Create a mock scatter polar trace
    mock_trace = MagicMock()
    mock_scatterpolar.return_value = mock_trace
    
    # Get the evaluation data
    all_scores = {
        **mock_evaluation_result["factor_scores"],
        **mock_evaluation_result["domain_scores"]
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
    
    # Verify that the Figure constructor was called
    assert mock_figure.called
    
    # Verify that add_trace was called
    assert mock_fig.add_trace.called
    
    # Verify that update_layout was called
    assert mock_fig.update_layout.called

if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 