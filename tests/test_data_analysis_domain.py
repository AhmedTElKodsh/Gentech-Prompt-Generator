import unittest
from promptgen.domains.domain_service import DomainService
from promptgen.domains.data_analysis import DataAnalysisContentStrategy

class TestDataAnalysisDomain(unittest.TestCase):
    """Tests for the Data Analysis domain functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.domain_service = DomainService()
        self.data_analysis_strategy = DataAnalysisContentStrategy()
    
    def test_domain_registration(self):
        """Test that the data analysis domain is properly registered."""
        # Check that data domain is in available domains
        self.assertIn("data", self.domain_service.get_available_domains())
        
        # Check that data analysis-related roles are properly mapped
        data_roles = ["data analyst", "data scientist", "business analyst", "statistician"]
        for role in data_roles:
            self.assertEqual("data", self.domain_service.role_to_domain.get(role.lower()))
    
    def test_role_detection(self):
        """Test that the domain is correctly detected from role prefixes."""
        test_cases = [
            ("As a data analyst, I need to analyze customer churn", "data", "I need to analyze customer churn"),
            ("Data Scientist: Looking for patterns in user behavior", "data", "Looking for patterns in user behavior"),
            ("Business Analyst - Create a dashboard for sales metrics", "data", "Create a dashboard for sales metrics")
        ]
        
        for input_text, expected_domain, expected_objective in test_cases:
            domain, cleaned_objective = self.domain_service.extract_role_from_objective(input_text)
            self.assertEqual(expected_domain, domain)
            self.assertEqual(expected_objective, cleaned_objective)
    
    def test_section_population(self):
        """Test that sections are correctly populated with data analysis content."""
        # Create a test section
        test_section = {
            "name": "Analysis Approach",
            "content_template": "Default template content"
        }
        
        # Create test context
        test_context = {
            "domain": "data",
            "objective": "Analyze customer churn and identify key factors",
            "data_type": "customer data",
            "complexity": 3
        }
        
        # Populate the section and verify it's not just the default content
        populated_content = self.domain_service.populate_section(test_section, test_context)
        self.assertNotEqual("Default template content", populated_content)
        self.assertIn("Analysis Approach", populated_content)
        self.assertIn("Methodology", populated_content)
        
    def test_visualization_section(self):
        """Test that visualization sections are correctly populated."""
        # Create a test visualization section
        test_section = {
            "name": "Visualization",
            "content_template": "Default visualization content"
        }
        
        # Create test context
        test_context = {
            "domain": "data",
            "objective": "Visualize sales trends over time",
            "data_type": "time series",
            "complexity": 3
        }
        
        # Populate the section and verify it contains visualization guidance
        populated_content = self.data_analysis_strategy._generate_visualization_content(test_section, test_context)
        self.assertIn("Visualization", populated_content)
        self.assertIn("Recommended Visualization Techniques", populated_content)
        self.assertIn("Best Practices", populated_content)
        
    def test_statistical_methods_section(self):
        """Test that statistical methods sections are correctly populated."""
        # Create a test statistical section
        test_section = {
            "name": "Statistical Methods",
            "content_template": "Default statistical content"
        }
        
        # Create test context
        test_context = {
            "domain": "data",
            "objective": "Test hypothesis about customer demographics",
            "complexity": 3
        }
        
        # Populate the section and verify it contains statistical guidance
        populated_content = self.data_analysis_strategy._generate_statistical_methods_content(test_section, test_context)
        self.assertIn("Statistical Methods", populated_content)
        self.assertIn("Recommended Statistical Approaches", populated_content)
        self.assertIn("Implementation Considerations", populated_content)


if __name__ == "__main__":
    unittest.main() 