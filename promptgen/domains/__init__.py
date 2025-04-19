"""
Domain-specific components for the prompt generator.
"""

from .software import SoftwareContentStrategy, populate_section as populate_software_section
from .content import ContentCreationStrategy, populate_section as populate_content_section
from .business import BusinessContentStrategy, populate_section as populate_business_section
from .data_analysis import DataAnalysisContentStrategy, populate_section as populate_data_analysis_section

# Import the domain service after all domain strategies are imported
from .domain_service import DomainService, default_service, populate_section

def get_domain_service() -> DomainService:
    """
    Get the default domain service instance.
    
    Returns:
        The default domain service
    """
    return default_service

# Export the default service instance for easy access
__all__ = [
    'SoftwareContentStrategy', 'ContentCreationStrategy', 'BusinessContentStrategy', 
    'DataAnalysisContentStrategy', 'DomainService', 'default_service', 'populate_section',
    'get_domain_service'
] 