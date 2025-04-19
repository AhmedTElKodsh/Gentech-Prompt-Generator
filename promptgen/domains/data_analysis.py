"""
Data Analysis domain components for the AI Prompt Generator.

This module provides specialized content generators and domain knowledge
for data analysis, statistics, and visualization-related prompts.
"""

from typing import Dict, List, Any, Optional
import logging

# Setup logger
logger = logging.getLogger(__name__)


class DataAnalysisContentStrategy:
    """
    Strategy for generating content for data analysis prompts.
    
    Implements the Strategy Pattern for data analysis-specific content population.
    """
    
    def __init__(self):
        """Initialize the data analysis content strategy."""
        # Load best practices and domain knowledge
        self.data_analysis_methods = self._load_analysis_methods()
        self.visualization_techniques = self._load_visualization_techniques()
        self.statistical_methods = self._load_statistical_methods()
        self.data_preparation_techniques = self._load_data_preparation_techniques()
        self.insight_frameworks = self._load_insight_frameworks()
    
    def populate(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Populate a template section with data analysis-specific content.
        
        Args:
            section: Template section definition
            context: Content generation context
            
        Returns:
            Generated content for the section
        """
        section_name = section.get("name", "").lower()
        
        # Different generation strategies based on section type
        if section_name in ["context", "background", "introduction", "data description"]:
            return self._generate_context_content(section, context)
            
        elif section_name in ["data preparation", "preprocessing", "data cleaning"]:
            return self._generate_data_preparation_content(section, context)
            
        elif section_name in ["analysis approach", "methodology", "techniques"]:
            return self._generate_analysis_approach_content(section, context)
            
        elif section_name in ["statistical methods", "statistical analysis"]:
            return self._generate_statistical_methods_content(section, context)
            
        elif section_name in ["visualization", "visualizations", "data visualization"]:
            return self._generate_visualization_content(section, context)
            
        elif section_name in ["insights", "findings", "interpretation"]:
            return self._generate_insights_content(section, context)
            
        # For other sections, use the template's default content
        return section.get("content_template", "").format(**context)
    
    def _generate_context_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for context/background sections."""
        objective = context.get("objective", "")
        data_type = context.get("data_type", "dataset")
        complexity = context.get("complexity", 3)
        
        context_template = """
You are a data analysis expert tasked with the following analytical challenge:

{objective}

Data Environment:
- Data Type: {data_type}
- Analysis Scope: {analysis_scope}
- Complexity Level: {complexity}/5

The data to be analyzed includes {data_dimensions} with information about {data_subjects}.
        """
        
        return context_template.format(
            objective=objective,
            data_type=data_type,
            analysis_scope=context.get("analysis_scope", "Exploratory Data Analysis"),
            complexity=complexity,
            data_dimensions=context.get("data_dimensions", "multiple variables"),
            data_subjects=context.get("data_subjects", "the subject matter")
        )
    
    def _generate_data_preparation_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for data preparation sections."""
        data_type = context.get("data_type", "").lower()
        
        # Select appropriate preparation techniques based on data type
        preparation_steps = []
        
        # Common preparation steps for most data types
        common_steps = [
            "Import and load the dataset",
            "Examine the data structure and basic properties",
            "Check for missing values and decide on appropriate handling strategy",
            "Identify and address outliers or anomalous values",
            "Verify data types and convert if necessary"
        ]
        
        preparation_steps.extend(common_steps)
        
        # Data type specific steps
        if "time series" in data_type or "temporal" in data_type:
            preparation_steps.extend([
                "Ensure proper datetime formatting",
                "Check for and handle seasonality",
                "Consider resampling or interpolation for irregular time intervals"
            ])
        elif "categorical" in data_type or "survey" in data_type:
            preparation_steps.extend([
                "Encode categorical variables appropriately",
                "Consider dimensionality reduction for high-cardinality categories",
                "Check for and address class imbalance issues"
            ])
        elif "text" in data_type or "nlp" in data_type:
            preparation_steps.extend([
                "Perform text cleaning (remove special characters, normalize case)",
                "Tokenize text data",
                "Consider stemming or lemmatization",
                "Remove stopwords if appropriate"
            ])
        
        preparation_template = """
Data Preparation:

1. Essential Preparation Steps:
{preparation_steps}

2. Quality Assurance Considerations:
   - Verify data consistency and integrity
   - Document any assumptions made during preprocessing
   - Create reproducible data preparation pipeline
   - Consider creating derived features if beneficial

3. Preprocessing Code Framework:
   Use appropriate libraries and functions for efficient data manipulation
   Document each preparation step for transparency
        """
        
        return preparation_template.format(
            preparation_steps="\n".join(f"   - {step}" for step in preparation_steps)
        )
    
    def _generate_analysis_approach_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for analysis approach sections."""
        objective = context.get("objective", "")
        data_type = context.get("data_type", "").lower()
        complexity = context.get("complexity", 3)
        
        # Select appropriate analysis methods based on context
        potential_methods = []
        for method, details in self.data_analysis_methods.items():
            method_complexity = details.get("complexity", 3)
            keywords = details.get("keywords", [])
            
            # Check if method applies to this task
            if (method_complexity <= complexity and 
                any(keyword in objective.lower() for keyword in keywords)):
                potential_methods.append(method)
        
        # If no methods match, suggest general exploratory approach
        if not potential_methods:
            potential_methods = ["Exploratory Data Analysis"]
        
        approach_template = """
Analysis Approach:

1. Recommended Methodology:
   Consider using {primary_method} as your primary approach.
   This method is suitable because {method_reason}.

2. Analysis Steps:
{analysis_steps}

3. Key Considerations:
   - Ensure analysis aligns with the original objective
   - Document assumptions and limitations
   - Consider alternative approaches if initial results are inconclusive
   - Validate findings through multiple analytical techniques when possible
        """
        
        # Get details for the first suggested method
        method_details = self.data_analysis_methods.get(potential_methods[0], {})
        
        return approach_template.format(
            primary_method=potential_methods[0],
            method_reason=method_details.get("description", "it provides structured insights into the data patterns"),
            analysis_steps="\n".join(f"   - {step}" for step in method_details.get("steps", ["Explore data distributions", "Identify patterns and relationships", "Test hypotheses"]))
        )
    
    def _generate_statistical_methods_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for statistical methods sections."""
        objective = context.get("objective", "")
        complexity = context.get("complexity", 3)
        
        # Select appropriate statistical methods based on context
        potential_stats = []
        for method, details in self.statistical_methods.items():
            method_complexity = details.get("complexity", 3)
            keywords = details.get("keywords", [])
            
            # Check if method applies to this task
            if (method_complexity <= complexity and 
                any(keyword in objective.lower() for keyword in keywords)):
                potential_stats.append((method, details))
        
        # Limit to top 3 most relevant methods
        if len(potential_stats) > 3:
            potential_stats = potential_stats[:3]
        elif not potential_stats:
            # Fallback if no specific methods found
            potential_stats = [(key, self.statistical_methods[key]) for key in list(self.statistical_methods.keys())[:3]]
        
        stats_template = """
Statistical Methods:

1. Recommended Statistical Approaches:
{statistical_approaches}

2. Implementation Considerations:
   - Verify assumptions required for each statistical test
   - Consider confidence intervals and significance levels
   - Document statistical rationale for chosen methods
   - Be mindful of multiple testing problems if applicable

3. Result Interpretation:
   - Clearly distinguish between correlation and causation
   - Acknowledge limitations of statistical inferences
   - Consider practical significance alongside statistical significance
        """
        
        approaches_text = ""
        for i, (method, details) in enumerate(potential_stats):
            approaches_text += f"   {i+1}. {method}: {details.get('description', '')}\n"
            approaches_text += f"      When to use: {details.get('when_to_use', 'When appropriate')}\n"
            approaches_text += f"      Implementation: {details.get('implementation', 'Use appropriate libraries')}\n"
        
        return stats_template.format(statistical_approaches=approaches_text)
    
    def _generate_visualization_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for visualization sections."""
        data_type = context.get("data_type", "").lower()
        objective = context.get("objective", "")
        
        # Select appropriate visualization techniques based on data type and objective
        viz_techniques = []
        
        for viz, details in self.visualization_techniques.items():
            data_types = details.get("data_types", [])
            purposes = details.get("purposes", [])
            
            # Check if visualization applies to this data type and purpose
            if (any(dt in data_type for dt in data_types) or not data_types) and \
               (any(purpose.lower() in objective.lower() for purpose in purposes) or not purposes):
                viz_techniques.append((viz, details))
        
        # Limit to top 4 most relevant visualizations
        if len(viz_techniques) > 4:
            viz_techniques = viz_techniques[:4]
        elif not viz_techniques:
            # Fallback if no specific visualizations found
            viz_techniques = [(key, self.visualization_techniques[key]) for key in list(self.visualization_techniques.keys())[:4]]
        
        viz_template = """
Data Visualization Guidelines:

1. Recommended Visualization Techniques:
{visualization_techniques}

2. Visualization Best Practices:
   - Ensure visualizations directly support analytical objectives
   - Maintain simplicity and clarity in design
   - Use appropriate color schemes and accessibility considerations
   - Include proper labels, titles, and legends
   - Consider the intended audience when designing visualizations

3. Visualization Tools Recommendation:
   Use appropriate libraries such as Matplotlib, Seaborn, Plotly, or ggplot2
   Consider interactive visualizations for complex relationships
        """
        
        techniques_text = ""
        for i, (viz, details) in enumerate(viz_techniques):
            techniques_text += f"   {i+1}. {viz}: {details.get('description', '')}\n"
            techniques_text += f"      Best for: {details.get('best_for', 'Various data types')}\n"
            if "example" in details:
                techniques_text += f"      Example usage: {details.get('example', '')}\n"
        
        return viz_template.format(visualization_techniques=techniques_text)
    
    def _generate_insights_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for insights/findings sections."""
        objective = context.get("objective", "")
        
        # Select appropriate insight frameworks
        insight_types = list(self.insight_frameworks.keys())[:3]  # Take top 3 frameworks
        
        insights_template = """
Insights and Interpretation Guidelines:

1. Types of Insights to Extract:
{insight_types}

2. Interpretation Framework:
   - Connect findings back to the original business or research questions
   - Distinguish between descriptive, predictive, and prescriptive insights
   - Acknowledge limitations and potential biases in the analysis
   - Suggest follow-up questions or analyses when appropriate

3. Actionable Recommendations:
   - Transform analytical findings into clear, actionable recommendations
   - Prioritize insights based on impact and feasibility
   - Support recommendations with data-driven evidence
   - Consider multiple stakeholder perspectives when presenting findings
        """
        
        types_text = ""
        for i, insight_type in enumerate(insight_types):
            details = self.insight_frameworks.get(insight_type, {})
            types_text += f"   {i+1}. {insight_type}: {details.get('description', '')}\n"
            if "questions" in details:
                types_text += f"      Key questions: {', '.join(details.get('questions', [])[:2])}\n"
        
        return insights_template.format(insight_types=types_text)
    
    def _load_analysis_methods(self) -> Dict[str, Any]:
        """Load data analysis methodologies."""
        return {
            "Exploratory Data Analysis (EDA)": {
                "description": "Systematic approach to understand data characteristics before formal modeling",
                "complexity": 2,
                "keywords": ["explore", "understand", "initial", "examine"],
                "steps": [
                    "Summarize main characteristics of the data",
                    "Create visualizations to understand distributions and relationships",
                    "Identify patterns, anomalies, and interesting structures",
                    "Formulate hypotheses for further investigation"
                ]
            },
            "Hypothesis Testing": {
                "description": "Statistical approach to test specific assumptions about the data",
                "complexity": 3,
                "keywords": ["test", "hypothesis", "significance", "compare", "difference"],
                "steps": [
                    "Formulate null and alternative hypotheses",
                    "Select appropriate statistical tests",
                    "Execute tests and analyze results",
                    "Draw conclusions based on significance levels"
                ]
            },
            "Regression Analysis": {
                "description": "Modeling the relationship between variables to understand influence and make predictions",
                "complexity": 3,
                "keywords": ["predict", "relate", "influence", "impact", "model", "regression"],
                "steps": [
                    "Identify dependent and independent variables",
                    "Explore variable relationships",
                    "Develop and validate regression models",
                    "Interpret coefficients and make predictions"
                ]
            },
            "Cluster Analysis": {
                "description": "Grouping similar objects to identify natural segments or patterns",
                "complexity": 4,
                "keywords": ["group", "segment", "cluster", "similar", "categories"],
                "steps": [
                    "Prepare data and select appropriate features",
                    "Choose clustering algorithm and determine optimal number of clusters",
                    "Execute clustering and validate results",
                    "Characterize and interpret the identified clusters"
                ]
            },
            "Time Series Analysis": {
                "description": "Analyzing data points collected or ordered by time to extract meaningful patterns",
                "complexity": 4,
                "keywords": ["time", "trend", "seasonal", "forecast", "predict", "temporal"],
                "steps": [
                    "Analyze trends, seasonality, and cyclic patterns",
                    "Test for stationarity and transform if necessary",
                    "Build appropriate time series models",
                    "Generate forecasts and confidence intervals"
                ]
            },
            "Text Mining and NLP": {
                "description": "Extracting meaningful patterns and insights from textual data",
                "complexity": 5,
                "keywords": ["text", "language", "words", "documents", "sentiment", "nlp"],
                "steps": [
                    "Preprocess and clean text data",
                    "Apply text representation techniques",
                    "Extract features and patterns from text",
                    "Interpret findings in context of original objective"
                ]
            }
        }
    
    def _load_visualization_techniques(self) -> Dict[str, Any]:
        """Load data visualization techniques."""
        return {
            "Histogram": {
                "description": "Visualizes the distribution of a single continuous variable",
                "data_types": ["numeric", "continuous"],
                "purposes": ["distribution", "explore"],
                "best_for": "Understanding data distributions and identifying patterns",
                "example": "hist(data['column'], bins=20)"
            },
            "Scatter Plot": {
                "description": "Displays relationship between two continuous variables",
                "data_types": ["numeric", "continuous"],
                "purposes": ["correlation", "relationship", "pattern"],
                "best_for": "Identifying relationships, patterns, and outliers",
                "example": "scatter(data['x'], data['y'])"
            },
            "Bar Chart": {
                "description": "Compares categorical data with rectangular bars",
                "data_types": ["categorical", "nominal", "ordinal"],
                "purposes": ["compare", "rank", "count"],
                "best_for": "Comparing values across categories or groups",
                "example": "bar(categories, values)"
            },
            "Line Chart": {
                "description": "Shows trends in data over time or sequence",
                "data_types": ["time series", "sequential"],
                "purposes": ["trend", "time", "change"],
                "best_for": "Visualizing trends, changes over time, and continuous sequences",
                "example": "plot(time_data, values)"
            },
            "Heatmap": {
                "description": "Represents data values as colors in a matrix",
                "data_types": ["matrix", "correlation", "categorical"],
                "purposes": ["pattern", "correlation", "matrix"],
                "best_for": "Visualizing correlations, matrices, and complex relationships",
                "example": "heatmap(correlation_matrix)"
            },
            "Box Plot": {
                "description": "Displays distribution summary with quartiles and outliers",
                "data_types": ["numeric", "continuous"],
                "purposes": ["distribution", "compare", "outlier"],
                "best_for": "Comparing distributions and identifying outliers",
                "example": "boxplot(data, by=grouping_variable)"
            },
            "Pie Chart": {
                "description": "Shows composition of a whole into parts",
                "data_types": ["categorical", "proportion"],
                "purposes": ["proportion", "composition", "part-to-whole"],
                "best_for": "Showing composition when there are few categories (less than 7)",
                "example": "pie(values, labels=categories)"
            },
            "Geographic Map": {
                "description": "Visualizes spatial data on a geographic map",
                "data_types": ["geographic", "spatial"],
                "purposes": ["geographic", "spatial", "location"],
                "best_for": "Analyzing geographic patterns and regional comparisons",
                "example": "choropleth_map(regions, values)"
            }
        }
    
    def _load_statistical_methods(self) -> Dict[str, Any]:
        """Load statistical methods and tests."""
        return {
            "t-test": {
                "description": "Tests if means of two groups are significantly different",
                "complexity": 2,
                "keywords": ["compare", "mean", "difference", "groups"],
                "when_to_use": "Comparing means between two groups or samples",
                "implementation": "Use scipy.stats.ttest_ind for independent samples"
            },
            "ANOVA": {
                "description": "Tests differences among multiple group means",
                "complexity": 3,
                "keywords": ["multiple", "groups", "compare", "variance"],
                "when_to_use": "Comparing means across more than two groups",
                "implementation": "Use scipy.stats.f_oneway for one-way ANOVA"
            },
            "Chi-Square Test": {
                "description": "Tests association between categorical variables",
                "complexity": 2,
                "keywords": ["categorical", "frequency", "association"],
                "when_to_use": "Analyzing relationships between categorical variables",
                "implementation": "Use scipy.stats.chi2_contingency for contingency tables"
            },
            "Correlation Analysis": {
                "description": "Measures strength and direction of relationship between variables",
                "complexity": 2,
                "keywords": ["relationship", "association", "correlation"],
                "when_to_use": "Quantifying linear relationships between variables",
                "implementation": "Use numpy.corrcoef or pandas.DataFrame.corr"
            },
            "Linear Regression": {
                "description": "Models relationship between dependent and independent variables",
                "complexity": 3,
                "keywords": ["predict", "relationship", "model", "regression"],
                "when_to_use": "Modeling continuous outcomes based on predictors",
                "implementation": "Use statsmodels.api.OLS or sklearn.linear_model.LinearRegression"
            },
            "Logistic Regression": {
                "description": "Models probability of binary outcomes based on predictors",
                "complexity": 4,
                "keywords": ["binary", "classification", "probability", "odds"],
                "when_to_use": "Predicting binary outcomes or class membership",
                "implementation": "Use statsmodels.api.Logit or sklearn.linear_model.LogisticRegression"
            },
            "Time Series Decomposition": {
                "description": "Splits time series into trend, seasonal, and residual components",
                "complexity": 3,
                "keywords": ["time", "series", "seasonal", "trend"],
                "when_to_use": "Understanding time series components before forecasting",
                "implementation": "Use statsmodels.tsa.seasonal.seasonal_decompose"
            }
        }
    
    def _load_data_preparation_techniques(self) -> Dict[str, Any]:
        """Load data preparation techniques."""
        return {
            "Missing Value Imputation": {
                "description": "Techniques to handle missing data in datasets",
                "methods": [
                    "Mean/Median/Mode Imputation",
                    "Regression Imputation",
                    "K-Nearest Neighbors Imputation",
                    "Multiple Imputation"
                ],
                "considerations": [
                    "Mechanism of missingness (MCAR, MAR, MNAR)",
                    "Impact on distributions and relationships",
                    "Potential for bias introduction"
                ]
            },
            "Outlier Detection and Handling": {
                "description": "Methods to identify and address extreme values",
                "methods": [
                    "Z-score method",
                    "IQR method",
                    "DBSCAN clustering",
                    "Isolation Forest"
                ],
                "considerations": [
                    "Domain-specific definition of outliers",
                    "Distinguish between errors and valid extreme values",
                    "Impact of removal on analysis"
                ]
            },
            "Feature Scaling": {
                "description": "Normalizing feature ranges for algorithm compatibility",
                "methods": [
                    "Min-Max Scaling",
                    "Standardization (Z-score)",
                    "Robust Scaling",
                    "Log Transformation"
                ],
                "considerations": [
                    "Algorithm requirements",
                    "Presence of outliers",
                    "Interpretability of scaled features"
                ]
            },
            "Feature Engineering": {
                "description": "Creating new features to improve model performance",
                "methods": [
                    "Polynomial Features",
                    "Interaction Terms",
                    "Domain-specific Derivations",
                    "Dimensionality Reduction"
                ],
                "considerations": [
                    "Domain knowledge incorporation",
                    "Balance between complexity and interpretability",
                    "Risk of overfitting"
                ]
            }
        }
    
    def _load_insight_frameworks(self) -> Dict[str, Any]:
        """Load insight generation frameworks."""
        return {
            "Descriptive Insights": {
                "description": "Understanding what has happened in the data",
                "questions": [
                    "What patterns exist in the data?",
                    "How are variables distributed?",
                    "What relationships exist between variables?",
                    "Are there any anomalies or outliers?"
                ]
            },
            "Diagnostic Insights": {
                "description": "Understanding why something happened",
                "questions": [
                    "What factors contributed to observed outcomes?",
                    "What are the root causes of patterns?",
                    "How do different variables interact?",
                    "What conditions lead to specific results?"
                ]
            },
            "Predictive Insights": {
                "description": "Forecasting what might happen in the future",
                "questions": [
                    "What trends can be extrapolated from the data?",
                    "How will key metrics likely change?",
                    "What scenarios are most probable?",
                    "What factors will influence future outcomes?"
                ]
            },
            "Prescriptive Insights": {
                "description": "Recommending actions based on analysis",
                "questions": [
                    "What actions should be taken based on the findings?",
                    "How can outcomes be optimized?",
                    "What strategies would address identified issues?",
                    "What trade-offs exist between different approaches?"
                ]
            },
            "Comparative Insights": {
                "description": "Contrasting between different groups or time periods",
                "questions": [
                    "How do different segments compare?",
                    "What has changed over time?",
                    "Which factors drive differences between groups?",
                    "What benchmarks are relevant for comparison?"
                ]
            }
        }


# Default instance for convenience
default_strategy = DataAnalysisContentStrategy()


def populate_section(section: Dict[str, Any], context: Dict[str, Any]) -> str:
    """
    Convenience function to populate a section using the default strategy.
    
    Args:
        section: Section definition
        context: Content generation context
        
    Returns:
        Generated content
    """
    return default_strategy.populate(section, context) 