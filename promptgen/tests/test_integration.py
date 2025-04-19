"""
Integration tests for domain-specific prompt evaluation.
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from promptgen.utils.domain_evaluator import DomainSpecificEvaluator, evaluate_prompt_with_domain
from promptgen.web.app import create_app

# Test prompts
TEST_SOFTWARE_PROMPT = """
Create a Python microservice that handles user authentication with JWT.
The service should provide endpoints for registration, login, password reset,
and token validation. Use Flask and SQLAlchemy for the implementation.
"""

TEST_CONTENT_PROMPT = """
Write a blog post about machine learning for beginners.
Target audience: College students with basic programming knowledge.
Tone: Friendly and educational.
Include code examples in Python.
"""

def test_domain_evaluator_integration():
    """Test that domain evaluator returns correct structure for UI consumption."""
    evaluator = DomainSpecificEvaluator(domain="software")
    results = evaluator.evaluate(TEST_SOFTWARE_PROMPT)
    
    # Check that all required fields for UI are present
    assert "quality_score" in results
    assert "factor_scores" in results
    assert "domain_scores" in results
    assert "domain_quality_score" in results
    assert "combined_quality_score" in results
    assert "domain_suggestions" in results
    
    # Check that the scores are in the expected range
    assert 0 <= results["quality_score"] <= 1
    assert 0 <= results["domain_quality_score"] <= 1
    assert 0 <= results["combined_quality_score"] <= 1
    
    # Check that domain scores contain expected keys
    domain_scores = results["domain_scores"]
    expected_keys = ["technical_accuracy", "implementation_detail", 
                     "security_consideration", "maintainability", "testability"]
    
    for key in expected_keys:
        assert key in domain_scores

@patch('streamlit.sidebar')
@patch('streamlit.columns')
@patch('streamlit.tabs')
@patch('streamlit.text_area')
@patch('streamlit.selectbox')
@patch('streamlit.button')
def test_streamlit_ui_integration(mock_button, mock_selectbox, mock_text_area, 
                                 mock_tabs, mock_columns, mock_sidebar):
    """Test that the Streamlit UI can work with the domain evaluator."""
    # Mock Streamlit components
    mock_button.return_value = True
    mock_selectbox.return_value = "software"
    mock_text_area.return_value = TEST_SOFTWARE_PROMPT
    
    # Mock tabs
    mock_tabs_instance = MagicMock()
    mock_tabs.return_value = [MagicMock(), mock_tabs_instance, MagicMock(), MagicMock()]
    
    # Mock the evaluate_prompt_with_domain function
    with patch('promptgen.utils.domain_evaluator.evaluate_prompt_with_domain') as mock_evaluate:
        # Set up mock evaluation result
        mock_result = {
            "quality_score": 0.85,
            "word_count": 50,
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
        mock_evaluate.return_value = mock_result
        
        # Try to create and run the app
        try:
            with patch('streamlit.title'):
                app = create_app()
                # This is just to trigger the app creation, we're not actually running it
                pass
            
            # Verify that the evaluate function was called with the right parameters
            mock_evaluate.assert_called_once()
        except Exception as e:
            # We expect some exceptions since we're not in a real Streamlit environment
            # Just verify that our mocked function was called
            assert mock_evaluate.called

def test_convenience_function():
    """Test that the convenience function returns expected structure."""
    # Use the convenience function
    result = evaluate_prompt_with_domain(TEST_CONTENT_PROMPT, domain="content")
    
    # Check structure
    assert "quality_score" in result
    assert "domain_scores" in result
    assert "domain" in result
    assert result["domain"] == "content"
    
    # Check content-specific scores
    domain_scores = result["domain_scores"]
    expected_keys = ["audience_focus", "tone_consistency", "engagement_potential", 
                    "content_structure", "seo_consideration"]
    
    for key in expected_keys:
        assert key in domain_scores

def test_pandas_integration():
    """Test integration with pandas for UI visualization."""
    # Get evaluation results
    evaluator = DomainSpecificEvaluator(domain="software")
    results = evaluator.evaluate(TEST_SOFTWARE_PROMPT)
    
    # Try to create a DataFrame from the results
    try:
        factor_df = pd.DataFrame({
            'Factor': list(results["factor_scores"].keys()),
            'Score': list(results["factor_scores"].values())
        })
        
        domain_df = pd.DataFrame({
            'Factor': list(results["domain_scores"].keys()),
            'Score': list(results["domain_scores"].values())
        })
        
        # Check that DataFrames were created correctly
        assert len(factor_df) == len(results["factor_scores"])
        assert len(domain_df) == len(results["domain_scores"])
        
        # Check that column types are as expected
        assert factor_df['Factor'].dtype == 'object'
        assert factor_df['Score'].dtype == 'float64'
        
    except Exception as e:
        pytest.fail(f"Failed to create pandas DataFrame: {e}")

if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 