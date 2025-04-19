"""
Domain classification functionality for the AI Prompt Generator.

This module provides domain classification capabilities, allowing the system to
determine the most likely domain for a user objective.
"""

from typing import Dict, List, Tuple, Any, Optional
import re
from collections import Counter
import logging

# Setup logger
logger = logging.getLogger(__name__)

class BaseClassifier:
    """
    Base classifier implementing the Template Method Pattern for domain classification.
    
    This abstract base class defines the skeleton of the classification algorithm,
    with specific steps implemented by concrete subclasses.
    """
    
    def classify_domain(self, objective: str) -> Tuple[str, float]:
        """
        Template method that defines the classification algorithm.
        
        Args:
            objective: The user objective to classify
            
        Returns:
            A tuple of (domain_name, confidence_score)
        """
        # Handle empty or whitespace-only input
        if not objective or not objective.strip():
            return "general", 0.0
            
        # 1. Preprocess the objective
        processed_text = self._preprocess_text(objective)
        
        # 2. Extract relevant features
        features = self._extract_features(processed_text)
        
        # 3. Calculate domain scores
        domain_scores = self._calculate_domain_scores(features)
        
        # 4. Determine the most likely domain
        domain, confidence = self._determine_domain(domain_scores)
        
        logger.info(f"Classified objective as domain '{domain}' with confidence {confidence:.2f}")
        return domain, confidence
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess the input text for feature extraction.
        
        Args:
            text: Raw input text
            
        Returns:
            Preprocessed text
        """
        # Convert to lowercase and normalize whitespace
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        
        # Add common variations of terms
        text = text.replace('metrics', 'metric')  # Handle singular/plural
        text = text.replace('analyze', 'analysis')  # Handle verb/noun forms
        text = text.replace('analyzing', 'analysis')
        text = text.replace('visualize', 'visualization')
        text = text.replace('visualizing', 'visualization')
        text = text.replace('document', 'documentation')
        text = text.replace('documenting', 'documentation')
        
        # Store the processed text for domain determination
        self._last_processed_text = text
        
        return text
    
    def _extract_features(self, text: str) -> Dict[str, Any]:
        """
        Extract relevant features from preprocessed text.
        
        Args:
            text: Preprocessed input text
            
        Returns:
            Dictionary of extracted features
        """
        # To be implemented by subclasses
        raise NotImplementedError("Feature extraction must be implemented by subclasses")
    
    def _calculate_domain_scores(self, features: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate scores for each domain based on extracted features.
        
        Args:
            features: Extracted features
            
        Returns:
            Dictionary mapping domain names to confidence scores
        """
        # To be implemented by subclasses
        raise NotImplementedError("Domain scoring must be implemented by subclasses")
    
    def _determine_domain(self, domain_scores: Dict[str, float]) -> Tuple[str, float]:
        """
        Determine the most likely domain based on scores.
        
        Args:
            domain_scores: Dictionary mapping domain names to confidence scores
            
        Returns:
            Tuple of (most_likely_domain, confidence_score)
        """
        max_score = max(domain_scores.values())
        if max_score == 0:
            return "general", 0.0

        # Get all domains within 80% of max score (more lenient)
        threshold = max_score * 0.80
        top_domains = [(domain, score) for domain, score in domain_scores.items() if score >= threshold]
        
        if len(top_domains) == 1:
            domain, score = top_domains[0]
            return domain, score

        # Special handling for overlapping domains with priorities
        domain_priorities = {
            # Technical documentation takes precedence over software when documentation-related
            ("technical_documentation", "software"): lambda text: (
                "technical_documentation" if any(word in text.lower() for word in 
                ["documentation", "manual", "guide", "spec", "reference", "architecture", "document"]) 
                else "software"
            ),
            ("software", "technical_documentation"): lambda text: (
                "technical_documentation" if any(word in text.lower() for word in 
                ["documentation", "manual", "guide", "spec", "reference", "architecture", "document"]) 
                else "software"
            ),
            # Data analysis takes precedence over business for analytical tasks
            ("data_analysis", "business"): lambda text: (
                "data_analysis" if any(word in text.lower() for word in 
                ["analysis", "analytics", "metrics", "data", "dashboard", "visualization",
                 "analyze", "patterns", "behavior", "churn", "customer behavior", "website traffic"]) 
                else "business"
            ),
            ("business", "data_analysis"): lambda text: (
                "data_analysis" if any(word in text.lower() for word in 
                ["analysis", "analytics", "metrics", "data", "dashboard", "visualization",
                 "analyze", "patterns", "behavior", "churn", "customer behavior", "website traffic"]) 
                else "business"
            ),
            # Business takes precedence over content for business-specific terms
            ("business", "content"): lambda text: (
                "business" if any(word in text.lower() for word in 
                ["business plan", "market", "sales", "strategy", "investor", "startup", "revenue",
                 "business model", "pitch deck", "stakeholder"]) 
                else "content"
            ),
            ("content", "business"): lambda text: (
                "business" if any(word in text.lower() for word in 
                ["business plan", "market", "sales", "strategy", "investor", "startup", "revenue",
                 "business model", "pitch deck", "stakeholder"]) 
                else "content"
            )
        }

        # Sort by score descending
        top_domains.sort(key=lambda x: x[1], reverse=True)
        domain1, score1 = top_domains[0]
        domain2, score2 = top_domains[1] if len(top_domains) > 1 else (None, 0)

        # Check domain priorities if scores are close
        if domain2 and score2 >= score1 * 0.85:  # More lenient comparison
            # Special case: if both domains are business and data_analysis
            if {"business", "data_analysis"} == {domain1, domain2}:
                # Check for strong business indicators first
                if any(word in self._last_processed_text.lower() for word in 
                      ["business plan", "market analysis", "investor", "pitch deck", "stakeholder"]):
                    return "business", domain_scores["business"]
                # Then check for strong data analysis indicators
                if any(word in self._last_processed_text.lower() for word in 
                      ["data analysis", "analytics", "dashboard", "visualization", "patterns"]):
                    return "data_analysis", domain_scores["data_analysis"]

            # Try both orderings of the domain pair
            pair = (domain1, domain2)
            if pair in domain_priorities:
                chosen_domain = domain_priorities[pair](self._last_processed_text)
                return chosen_domain, domain_scores[chosen_domain]
            pair = (domain2, domain1)
            if pair in domain_priorities:
                chosen_domain = domain_priorities[pair](self._last_processed_text)
                return chosen_domain, domain_scores[chosen_domain]

        return domain1, score1


class DomainClassifier(BaseClassifier):
    """
    A classifier that uses keyword matching for domain classification.
    """
    
    def __init__(self):
        # Initialize domain-specific keywords with weights
        self.domain_keywords = {
            "software": {
                "code": 1.0, "programming": 1.0, "algorithm": 0.9, "function": 0.8,
                "class": 0.8, "api": 0.9, "database": 0.8, "framework": 0.9,
                "software": 1.0, "development": 0.8, "application": 0.8,
                "unit test": 1.0, "debugging": 1.0, "implementation": 0.8,
                "code review": 1.0, "refactor": 1.0, "optimization": 0.8,
                "git": 0.9, "repository": 0.8, "backend": 0.9, "frontend": 0.9,
                "web": 0.8, "python": 1.0, "react": 1.0, "flask": 1.0,
                "component": 0.8, "rest": 0.9, "authentication": 0.8
            },
            "content": {
                "article": 1.0, "blog post": 1.0, "content": 0.9, "writing": 1.0,
                "editorial": 1.0, "story": 0.9, "newsletter": 1.0, "social media": 1.0,
                "marketing copy": 1.0, "creative": 0.8, "engaging": 0.8,
                "seo": 0.9, "headline": 1.0, "content strategy": 1.0,
                "content calendar": 1.0, "blog": 1.0, "copywriting": 1.0,
                "youtube": 0.9, "video script": 1.0, "email": 0.8,
                "subscribers": 0.9, "post": 0.8, "write": 0.9, "edit": 0.8
            },
            "business": {
                "business plan": 1.2, "market analysis": 1.2, "strategy": 1.0,
                "sales": 1.0, "marketing strategy": 1.2, "investor": 1.2,
                "startup": 1.2, "revenue": 1.2, "business model": 1.2,
                "competitive analysis": 1.2, "market research": 1.2,
                "pitch deck": 1.2, "business development": 1.2,
                "growth strategy": 1.2, "business metrics": 1.2,
                "stakeholder": 1.2, "business case": 1.2,
                "industry": 1.0, "trends": 0.8, "q4": 0.8,
                "business": 1.2, "market": 1.0, "sales strategy": 1.2
            },
            "data_analysis": {
                "data analysis": 1.2, "analytics": 1.2, "dashboard": 1.0,
                "metrics": 1.0, "visualization": 1.0, "dataset": 1.2,
                "statistical": 1.2, "predictive model": 1.2, "machine learning": 1.2,
                "data science": 1.2, "data mining": 1.2, "regression": 1.2,
                "correlation": 1.2, "data cleaning": 1.2, "data pipeline": 1.2,
                "data visualization": 1.2, "data transformation": 1.2,
                "data insights": 1.2, "data trends": 1.2, "patterns": 1.0,
                "behavior": 0.9, "traffic": 0.9, "churn": 1.0, "sales metrics": 1.2,
                "analyze": 1.0, "analysis": 1.0, "customer": 0.9,
                "customer behavior": 1.2, "website traffic": 1.2
            },
            "technical_documentation": {
                "documentation": 1.2, "technical spec": 1.2, "api reference": 1.2,
                "user guide": 1.2, "technical manual": 1.2, "system architecture": 1.2,
                "technical requirements": 1.2, "specification document": 1.2,
                "technical design": 1.2, "integration guide": 1.2,
                "technical documentation": 1.2, "implementation guide": 1.2,
                "developer guide": 1.2, "technical overview": 1.2,
                "architecture document": 1.2, "technical reference": 1.2,
                "endpoints": 1.0, "manual": 1.0, "architecture": 1.0,
                "specifications": 1.2, "features": 0.9, "document": 1.0,
                "api": 1.0, "guide": 1.0, "docs": 1.2, "spec": 1.2
            }
        }
    
    def _extract_features(self, text: str) -> Dict[str, Any]:
        """
        Extract keyword-based features from the text.
        
        Args:
            text: Preprocessed text
            
        Returns:
            Dictionary with keyword counts by domain
        """
        features = {"keyword_counts": {}, "total_words": len(text.split())}
        
        # Count occurrences of each domain's keywords
        for domain, keywords in self.domain_keywords.items():
            domain_count = 0
            for keyword in keywords:
                # Count occurrences of the keyword
                count = len(re.findall(rf'\b{re.escape(keyword)}\b', text))
                # Apply keyword weight if defined
                weight = self.domain_keywords[domain].get(keyword, 1.0)
                domain_count += count * weight
            
            features["keyword_counts"][domain] = domain_count
        
        return features
    
    def _calculate_domain_scores(self, features: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate domain scores based on keyword counts.
        
        Args:
            features: Extracted features with keyword counts
            
        Returns:
            Dictionary mapping domain names to confidence scores
        """
        keyword_counts = features.get("keyword_counts", {})
        total_words = features.get("total_words", 1)  # Avoid division by zero
        
        # Calculate normalized scores
        scores = {}
        max_count = max(keyword_counts.values()) if keyword_counts else 0
        
        for domain, count in keyword_counts.items():
            # Base score from keyword frequency
            base_score = count / total_words if total_words > 0 else 0
            
            # Normalize relative to the maximum count
            relative_score = count / max_count if max_count > 0 else 0
            
            # Combine scores with weights
            scores[domain] = 0.7 * base_score + 0.3 * relative_score
            
            # Apply sigmoid-like normalization to keep scores between 0 and 1
            scores[domain] = min(1.0, scores[domain] * 4.0)  # Increased scaling factor
        
        # If no significant scores, return general domain with very low confidence
        if max(scores.values()) < 0.15:  # Lowered threshold
            return {"general": 0.1}
            
        return scores

    def _determine_domain(self, domain_scores: Dict[str, float]) -> Tuple[str, float]:
        """
        Determine the most likely domain based on scores.
        
        Args:
            domain_scores: Dictionary mapping domain names to confidence scores
            
        Returns:
            Tuple of (most_likely_domain, confidence_score)
        """
        max_score = max(domain_scores.values())
        if max_score == 0:
            return "general", 0.0

        # Get all domains within 80% of max score (more lenient)
        threshold = max_score * 0.80
        top_domains = [(domain, score) for domain, score in domain_scores.items() if score >= threshold]
        
        if len(top_domains) == 1:
            domain, score = top_domains[0]
            return domain, score

        # Special handling for overlapping domains with priorities
        domain_priorities = {
            # Technical documentation takes precedence over software when documentation-related
            ("technical_documentation", "software"): lambda text: (
                "technical_documentation" if any(word in text.lower() for word in 
                ["documentation", "manual", "guide", "spec", "reference", "architecture", "document"]) 
                else "software"
            ),
            ("software", "technical_documentation"): lambda text: (
                "technical_documentation" if any(word in text.lower() for word in 
                ["documentation", "manual", "guide", "spec", "reference", "architecture", "document"]) 
                else "software"
            ),
            # Data analysis takes precedence over business for analytical tasks
            ("data_analysis", "business"): lambda text: (
                "data_analysis" if any(word in text.lower() for word in 
                ["analysis", "analytics", "metrics", "data", "dashboard", "visualization",
                 "analyze", "patterns", "behavior", "churn", "customer behavior", "website traffic"]) 
                else "business"
            ),
            ("business", "data_analysis"): lambda text: (
                "data_analysis" if any(word in text.lower() for word in 
                ["analysis", "analytics", "metrics", "data", "dashboard", "visualization",
                 "analyze", "patterns", "behavior", "churn", "customer behavior", "website traffic"]) 
                else "business"
            ),
            # Business takes precedence over content for business-specific terms
            ("business", "content"): lambda text: (
                "business" if any(word in text.lower() for word in 
                ["business plan", "market", "sales", "strategy", "investor", "startup", "revenue",
                 "business model", "pitch deck", "stakeholder"]) 
                else "content"
            ),
            ("content", "business"): lambda text: (
                "business" if any(word in text.lower() for word in 
                ["business plan", "market", "sales", "strategy", "investor", "startup", "revenue",
                 "business model", "pitch deck", "stakeholder"]) 
                else "content"
            )
        }

        # Sort by score descending
        top_domains.sort(key=lambda x: x[1], reverse=True)
        domain1, score1 = top_domains[0]
        domain2, score2 = top_domains[1] if len(top_domains) > 1 else (None, 0)

        # Check domain priorities if scores are close
        if domain2 and score2 >= score1 * 0.85:  # More lenient comparison
            # Special case: if both domains are business and data_analysis
            if {"business", "data_analysis"} == {domain1, domain2}:
                # Check for strong business indicators first
                if any(word in self._last_processed_text.lower() for word in 
                      ["business plan", "market analysis", "investor", "pitch deck", "stakeholder"]):
                    return "business", domain_scores["business"]
                # Then check for strong data analysis indicators
                if any(word in self._last_processed_text.lower() for word in 
                      ["data analysis", "analytics", "dashboard", "visualization", "patterns"]):
                    return "data_analysis", domain_scores["data_analysis"]

            # Try both orderings of the domain pair
            pair = (domain1, domain2)
            if pair in domain_priorities:
                chosen_domain = domain_priorities[pair](self._last_processed_text)
                return chosen_domain, domain_scores[chosen_domain]
            pair = (domain2, domain1)
            if pair in domain_priorities:
                chosen_domain = domain_priorities[pair](self._last_processed_text)
                return chosen_domain, domain_scores[chosen_domain]

        return domain1, score1


# Default instance for convenience
default_classifier = DomainClassifier()


def classify_domain(objective: str) -> Tuple[str, float]:
    """
    Convenience function to classify an objective using the default classifier.
    
    Args:
        objective: The user objective to classify
        
    Returns:
        A tuple of (domain_name, confidence_score)
    """
    return default_classifier.classify_domain(objective) 