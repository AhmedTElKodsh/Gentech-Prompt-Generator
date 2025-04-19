"""
Test suite for the ComplexityAnalyzer.

This module contains comprehensive tests for the task complexity analysis functionality,
testing various scenarios and edge cases.
"""

import unittest
from promptgen.core.complexity import ComplexityAnalyzer

class TestComplexityAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.analyzer = ComplexityAnalyzer()
    
    def test_simple_tasks(self):
        """Test analysis of simple tasks."""
        test_cases = [
            ("Create a hello world program", "software"),
            ("Write a blog post about cats", "content"),
            ("Make a simple sales report", "business"),
            ("Create a bar chart", "data_analysis")
        ]
        
        for objective, domain in test_cases:
            level, analysis = self.analyzer.analyze_complexity(objective, domain)
            self.assertLessEqual(level, 2, f"Simple task '{objective}' should have complexity <= 2")
            self.assertIn('components', analysis)
            self.assertIn('technical_terms', analysis)
    
    def test_complex_tasks(self):
        """Test analysis of complex tasks."""
        test_cases = [
            (
                "Design and implement a distributed microservices architecture with "
                "authentication, caching, and load balancing. Integrate with existing "
                "APIs and ensure scalability for high traffic loads. Implement "
                "monitoring and alerting systems.",
                "software"
            ),
            (
                "Develop a comprehensive content strategy incorporating SEO optimization, "
                "audience segmentation, and conversion funnel analysis. Create editorial "
                "guidelines and implement content taxonomy. Monitor engagement metrics "
                "and optimize for retention.",
                "content"
            ),
            (
                "Conduct market analysis for expansion into international markets. "
                "Evaluate regulatory requirements, assess market liquidity, and develop "
                "risk mitigation strategies. Create financial models for ROI forecasting "
                "and prepare valuation reports.",
                "business"
            )
        ]
        
        for objective, domain in test_cases:
            level, analysis = self.analyzer.analyze_complexity(objective, domain)
            self.assertGreaterEqual(level, 4, f"Complex task '{objective}' should have complexity >= 4")
            self.assertTrue(analysis['components'], "Complex tasks should have identified components")
            self.assertTrue(analysis['technical_terms'], "Complex tasks should have technical terms")
    
    def test_component_identification(self):
        """Test identification of components/subtasks."""
        objective = """
        Implement a new user authentication system:
        - Design the database schema
        - Create API endpoints
        - Implement frontend components
        - Write unit tests
        - Deploy to production
        """
        
        level, analysis = self.analyzer.analyze_complexity(objective, "software")
        components = analysis['components']
        
        expected_components = {
            "design database schema",
            "create api endpoints",
            "implement frontend components",
            "write unit tests",
            "deploy production"
        }
        
        # Check that all expected components are found (allowing for some variation in exact wording)
        found_components = set()
        for expected in expected_components:
            for actual in components:
                if all(word in actual.lower() for word in expected.split()):
                    found_components.add(expected)
                    break
        
        self.assertEqual(
            len(found_components),
            len(expected_components),
            f"Not all components were identified. Found: {components}"
        )
    
    def test_dependency_identification(self):
        """Test identification of dependencies between components."""
        objective = """
        Create a data pipeline that requires raw data preprocessing before analysis.
        The visualization dashboard depends on the analyzed data.
        Deploy after testing is complete.
        """
        
        level, analysis = self.analyzer.analyze_complexity(objective, "data_analysis")
        dependencies = analysis['dependencies']
        
        self.assertTrue(dependencies, "Dependencies should be identified")
        self.assertTrue(
            any('preprocessing' in dep[0].lower() or 'preprocessing' in dep[1].lower() 
                for dep in dependencies),
            "Preprocessing dependency should be identified"
        )
        self.assertTrue(
            any('visualization' in dep[0].lower() or 'visualization' in dep[1].lower() 
                for dep in dependencies),
            "Visualization dependency should be identified"
        )
    
    def test_technical_term_identification(self):
        """Test identification of domain-specific technical terms."""
        test_cases = [
            (
                "Implement API authentication and database optimization",
                "software",
                {"api", "authentication", "database", "optimization"}
            ),
            (
                "Analyze customer segmentation and engagement metrics",
                "content",
                {"segmentation", "engagement", "analytics"}
            ),
            (
                "Create correlation analysis and data visualization",
                "data_analysis",
                {"correlation", "visualization"}
            )
        ]
        
        for objective, domain, expected_terms in test_cases:
            level, analysis = self.analyzer.analyze_complexity(objective, domain)
            found_terms = set(analysis['technical_terms'])
            
            # Check that all expected terms are found
            self.assertTrue(
                expected_terms.issubset(found_terms),
                f"Not all technical terms were identified. Expected: {expected_terms}, Found: {found_terms}"
            )
    
    def test_edge_cases(self):
        """Test edge cases and potential error conditions."""
        test_cases = [
            ("", "software"),  # Empty string
            ("   ", "content"),  # Whitespace only
            ("xyz123", "business"),  # Random string
            ("Help me", "data_analysis"),  # Very generic request
            (None, "software")  # None input
        ]
        
        for objective, domain in test_cases:
            try:
                if objective is not None:  # Skip None input
                    level, analysis = self.analyzer.analyze_complexity(objective, domain)
                    self.assertEqual(level, 1, f"Edge case '{objective}' should have minimum complexity")
                    self.assertIn('components', analysis)
                    self.assertIn('technical_terms', analysis)
            except Exception as e:
                if objective is None:
                    # None input should raise an exception
                    self.assertIsInstance(e, (ValueError, TypeError))
                else:
                    raise  # Other exceptions should fail the test
    
    def test_complexity_scaling(self):
        """Test that complexity scales appropriately with task size/difficulty."""
        objectives = [
            # Simple task
            "Create a hello world program",
            
            # Slightly more complex
            "Create a web form with input validation",
            
            # Moderate complexity
            "Build a REST API with database integration",
            
            # High complexity
            "Implement a distributed microservices architecture with authentication",
            
            # Very high complexity
            "Design and implement a scalable cloud-native application with "
            "microservices, event-driven architecture, distributed caching, "
            "and real-time analytics. Include comprehensive monitoring, "
            "automated deployment pipelines, and disaster recovery procedures."
        ]
        
        previous_level = 0
        for objective in objectives:
            level, _ = self.analyzer.analyze_complexity(objective, "software")
            self.assertGreaterEqual(
                level,
                previous_level,
                f"Complexity should increase or stay same. Previous: {previous_level}, Current: {level}"
            )
            previous_level = level
    
    def test_cross_domain_consistency(self):
        """Test that similar complexity tasks in different domains get similar scores."""
        base_task = "Create a {thing} with proper {quality} and {action}"
        
        variations = [
            ("software", "API", "authentication", "testing"),
            ("content", "article", "structure", "editing"),
            ("business", "report", "analysis", "review"),
            ("data_analysis", "dashboard", "visualization", "validation")
        ]
        
        scores = []
        for domain, thing, quality, action in variations:
            objective = base_task.format(thing=thing, quality=quality, action=action)
            level, _ = self.analyzer.analyze_complexity(objective, domain)
            scores.append(level)
        
        # Check that all scores are within 1 level of each other
        self.assertTrue(
            max(scores) - min(scores) <= 1,
            f"Similar tasks in different domains should have similar complexity. Scores: {scores}"
        ) 