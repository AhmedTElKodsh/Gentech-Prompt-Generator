"""
Business domain components for the AI Prompt Generator.

This module provides specialized content generators and domain knowledge
for business strategy, analysis, and planning-related prompts.
"""

from typing import Dict, List, Any, Optional
import logging

# Setup logger
logger = logging.getLogger(__name__)


class BusinessContentStrategy:
    """
    Strategy for generating content for business-related prompts.
    
    Implements the Strategy Pattern for business-specific content population.
    """
    
    def __init__(self):
        """Initialize the business content strategy."""
        # Load business domain knowledge
        self.business_frameworks = self._load_business_frameworks()
        self.analysis_types = self._load_analysis_types()
        self.planning_methodologies = self._load_planning_methodologies()
        self.market_segments = self._load_market_segments()
        self.metrics_and_kpis = self._load_metrics_and_kpis()
    
    def populate(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Populate a template section with business-specific content.
        
        Args:
            section: Template section definition
            context: Content generation context
            
        Returns:
            Generated content for the section
        """
        section_name = section.get("name", "").lower()
        
        # Different generation strategies based on section type
        if section_name in ["context", "background", "introduction"]:
            return self._generate_context_content(section, context)
            
        elif section_name in ["framework", "approach", "methodology"]:
            return self._generate_framework_content(section, context)
            
        elif section_name in ["analysis", "marketanalysis", "industryanalysis"]:
            return self._generate_analysis_content(section, context)
            
        elif section_name in ["metrics", "kpis", "success metrics"]:
            return self._generate_metrics_content(section, context)
            
        elif section_name in ["strategy", "strategicplan", "actionplan"]:
            return self._generate_strategy_content(section, context)
            
        # For other sections, use the template's default content
        return section.get("content_template", "").format(**context)
    
    def _generate_context_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for context/background sections."""
        objective = context.get("objective", "")
        analysis_type = context.get("analysis_type", "general business analysis")
        complexity = context.get("complexity", 3)
        
        # Get details for the analysis type
        analysis_info = self.analysis_types.get(analysis_type.lower(), 
                                              {"description": "a business analysis"})
        
        context_template = """
You are a strategic business consultant tasked with the following assignment:

{objective}

Analysis Details:
- Analysis Type: {analysis_type} - {analysis_description}
- Industry Focus: {industry_focus}
- Scope: {scope}
- Complexity Level: {complexity}/5
        """
        
        return context_template.format(
            objective=objective,
            analysis_type=analysis_type.title(),
            analysis_description=analysis_info.get("description", ""),
            industry_focus=context.get("industry", "General business"),
            scope=context.get("scope", "Comprehensive analysis"),
            complexity=complexity
        )
    
    def _generate_framework_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for framework/methodology sections."""
        analysis_type = context.get("analysis_type", "general").lower()
        complexity = context.get("complexity", 3)
        
        # Select appropriate frameworks based on analysis type and complexity
        recommended_frameworks = []
        for framework_name, framework_info in self.business_frameworks.items():
            suitable_for = framework_info.get("suitable_for", [])
            framework_complexity = framework_info.get("complexity", 3)
            
            # Check if this framework is suitable for the analysis type and complexity level
            if (analysis_type in suitable_for or "all" in suitable_for) and framework_complexity <= complexity:
                recommended_frameworks.append({
                    "name": framework_name,
                    "description": framework_info.get("description", ""),
                    "components": framework_info.get("components", []),
                    "complexity": framework_complexity
                })
        
        # Sort frameworks by relevance (exact match for analysis type first, then by complexity)
        recommended_frameworks.sort(key=lambda x: (0 if analysis_type in x.get("suitable_for", []) else 1, 
                                                 abs(x.get("complexity", 3) - complexity)))
        
        # Take the top 3 most relevant frameworks
        top_frameworks = recommended_frameworks[:3] if recommended_frameworks else []
        
        framework_template = """
Recommended Analytical Frameworks:

{frameworks}

Approach to Applying These Frameworks:
1. Begin by gathering relevant data for each framework
2. Apply the frameworks systematically, documenting insights at each step
3. Cross-reference findings between frameworks to identify patterns
4. Prioritize insights based on strategic importance and actionability
        """
        
        # If no suitable frameworks found, provide a general approach
        if not top_frameworks:
            return """
Analytical Approach:

Given the nature of this task, a custom analytical approach is recommended:

1. Situation Assessment:
   - Gather relevant data about the current state
   - Identify key stakeholders and their interests
   - Document existing challenges and opportunities

2. Analysis:
   - Evaluate internal and external factors
   - Identify patterns and trends
   - Assess strengths, weaknesses, opportunities, and threats

3. Strategic Options:
   - Develop potential courses of action
   - Evaluate each option against key criteria
   - Select the most promising approaches

4. Implementation Planning:
   - Create actionable recommendations
   - Establish metrics for success
   - Outline required resources and timeline
            """
        
        # Format the frameworks section
        frameworks_text = ""
        for i, framework in enumerate(top_frameworks):
            frameworks_text += f"{i+1}. {framework['name']}:\n"
            frameworks_text += f"   Description: {framework['description']}\n"
            frameworks_text += "   Key Components:\n"
            for component in framework.get("components", [])[:3]:  # Limit to top 3 components
                frameworks_text += f"   - {component}\n"
            frameworks_text += "\n"
        
        return framework_template.format(frameworks=frameworks_text)
    
    def _generate_analysis_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for analysis sections."""
        analysis_type = context.get("analysis_type", "general").lower()
        industry = context.get("industry", "general").lower()
        
        # Get specific analysis requirements
        analysis_info = self.analysis_types.get(analysis_type, {})
        key_questions = analysis_info.get("key_questions", [])
        data_sources = analysis_info.get("data_sources", [])
        
        # Get industry-specific considerations
        industry_considerations = []
        for segment, details in self.market_segments.items():
            if segment.lower() == industry or "all" in segment:
                industry_considerations = details.get("considerations", [])
                break
        
        analysis_template = """
Analysis Requirements:

1. Key Questions to Answer:
{key_questions}

2. Data Sources to Consider:
{data_sources}

3. Industry-Specific Considerations:
{industry_considerations}

4. Analysis Structure:
   - Begin with overview of current situation
   - Present key findings organized by theme or importance
   - Support assertions with data and evidence
   - Highlight implications for decision-making
   - Conclude with summary of critical insights
        """
        
        # If no specific key questions found, provide general ones
        if not key_questions:
            key_questions = [
                "What is the current market situation?",
                "What are the key challenges and opportunities?",
                "What competitive advantages exist or could be developed?",
                "What are the critical success factors for this situation?"
            ]
        
        # If no specific data sources found, provide general ones
        if not data_sources:
            data_sources = [
                "Market research reports and industry analyses",
                "Financial data and performance metrics",
                "Customer feedback and surveys",
                "Competitive intelligence",
                "Internal operational data"
            ]
        
        # If no industry considerations found, provide general ones
        if not industry_considerations:
            industry_considerations = [
                "Consider general economic factors affecting this industry",
                "Evaluate regulatory considerations that may impact strategy",
                "Assess technological trends influencing the market",
                "Consider consumer behavior patterns in this sector"
            ]
        
        return analysis_template.format(
            key_questions="\n".join(f"   - {q}" for q in key_questions),
            data_sources="\n".join(f"   - {s}" for s in data_sources),
            industry_considerations="\n".join(f"   - {c}" for c in industry_considerations)
        )
    
    def _generate_metrics_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for metrics/KPIs sections."""
        analysis_type = context.get("analysis_type", "general").lower()
        industry = context.get("industry", "general").lower()
        
        # Get relevant metrics for this analysis type and industry
        relevant_metrics = []
        for metric_category, metrics in self.metrics_and_kpis.items():
            # Check if this category applies to the analysis type
            if analysis_type in metrics.get("relevant_for", []) or "all" in metrics.get("relevant_for", []):
                for metric in metrics.get("metrics", []):
                    # Check if metric applies to the industry
                    if industry in metric.get("industries", []) or "all" in metric.get("industries", []):
                        relevant_metrics.append({
                            "category": metric_category,
                            "name": metric.get("name", ""),
                            "description": metric.get("description", ""),
                            "calculation": metric.get("calculation", "")
                        })
        
        # Group metrics by category
        metrics_by_category = {}
        for metric in relevant_metrics:
            category = metric["category"]
            if category not in metrics_by_category:
                metrics_by_category[category] = []
            metrics_by_category[category].append(metric)
        
        metrics_template = """
Success Metrics and KPIs:

{metrics_content}

Measurement Approach:
- Establish baseline values for each metric before implementation
- Set specific targets with timeframes for improvement
- Implement regular tracking and reporting mechanisms
- Adjust strategy based on metric performance
        """
        
        # If no relevant metrics found, provide general guidance
        if not metrics_by_category:
            return """
Success Metrics and KPIs:

For this analysis, consider these general business metrics:

1. Financial Metrics:
   - Revenue growth
   - Profit margin
   - Return on investment (ROI)
   - Cost reduction

2. Operational Metrics:
   - Efficiency improvements
   - Process cycle times
   - Quality metrics
   - Resource utilization

3. Market/Customer Metrics:
   - Market share
   - Customer acquisition cost
   - Customer retention rate
   - Customer satisfaction scores

Measurement Approach:
- Establish baseline values for each metric before implementation
- Set specific targets with timeframes for improvement
- Implement regular tracking and reporting mechanisms
- Adjust strategy based on metric performance
            """
        
        # Format the metrics content by category
        metrics_content = ""
        for category, metrics in metrics_by_category.items():
            metrics_content += f"{category}:\n"
            for i, metric in enumerate(metrics[:4]):  # Limit to 4 metrics per category
                metrics_content += f"   {i+1}. {metric['name']}: {metric['description']}\n"
                if metric.get("calculation"):
                    metrics_content += f"      Calculation: {metric['calculation']}\n"
            metrics_content += "\n"
        
        return metrics_template.format(metrics_content=metrics_content)
    
    def _generate_strategy_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for strategy/action plan sections."""
        analysis_type = context.get("analysis_type", "general").lower()
        complexity = context.get("complexity", 3)
        
        # Get relevant planning methodology
        planning_methodologies = self.planning_methodologies
        relevant_methodology = None
        for method_name, method_info in planning_methodologies.items():
            if analysis_type in method_info.get("suitable_for", []) or "all" in method_info.get("suitable_for", []):
                if method_info.get("complexity", 3) <= complexity:
                    relevant_methodology = {
                        "name": method_name,
                        "description": method_info.get("description", ""),
                        "steps": method_info.get("steps", [])
                    }
                    break
        
        # If no specific methodology matches, use the general strategic planning approach
        if not relevant_methodology:
            relevant_methodology = {
                "name": "Strategic Planning Approach",
                "description": "A structured approach to developing actionable strategies",
                "steps": [
                    "Situation Assessment: Evaluate current state",
                    "Strategic Direction: Define vision, mission, and goals",
                    "Action Planning: Develop specific initiatives to achieve goals",
                    "Resource Allocation: Assign resources to initiatives",
                    "Implementation Schedule: Create timeline with milestones",
                    "Measurement Plan: Define how success will be evaluated"
                ]
            }
        
        strategy_template = """
Strategic Approach:

Recommended Planning Methodology: {method_name}
{method_description}

Planning Process:
{planning_steps}

Strategy Development Guidelines:
- Ensure alignment with organizational objectives
- Consider resource constraints and implementation capacity
- Balance short-term actions with long-term strategic positioning
- Include contingency plans for key risks
- Assign clear ownership for each action item
        """
        
        return strategy_template.format(
            method_name=relevant_methodology["name"],
            method_description=relevant_methodology["description"],
            planning_steps="\n".join(f"{i+1}. {step}" for i, step in enumerate(relevant_methodology["steps"]))
        )
    
    def _load_business_frameworks(self) -> Dict[str, Any]:
        """Load business analysis frameworks."""
        return {
            "SWOT Analysis": {
                "description": "Evaluates Strengths, Weaknesses, Opportunities, and Threats",
                "suitable_for": ["all", "strategic planning", "market entry", "competitive analysis"],
                "complexity": 1,
                "components": [
                    "Strengths: Internal capabilities and advantages",
                    "Weaknesses: Internal limitations and disadvantages",
                    "Opportunities: External favorable factors",
                    "Threats: External unfavorable factors"
                ]
            },
            "Porter's Five Forces": {
                "description": "Analyzes industry competition and attractiveness",
                "suitable_for": ["industry analysis", "competitive analysis", "market entry"],
                "complexity": 3,
                "components": [
                    "Threat of New Entrants",
                    "Bargaining Power of Suppliers",
                    "Bargaining Power of Buyers",
                    "Threat of Substitute Products",
                    "Competitive Rivalry"
                ]
            },
            "PESTEL Analysis": {
                "description": "Examines macro-environmental factors affecting an organization",
                "suitable_for": ["market analysis", "strategic planning", "risk assessment"],
                "complexity": 2,
                "components": [
                    "Political factors",
                    "Economic factors",
                    "Social factors",
                    "Technological factors",
                    "Environmental factors",
                    "Legal factors"
                ]
            },
            "Business Model Canvas": {
                "description": "Visualizes key components of a business model",
                "suitable_for": ["business model development", "startup planning", "innovation"],
                "complexity": 3,
                "components": [
                    "Key Partners",
                    "Key Activities",
                    "Key Resources",
                    "Value Propositions",
                    "Customer Relationships",
                    "Channels",
                    "Customer Segments",
                    "Cost Structure",
                    "Revenue Streams"
                ]
            },
            "Value Chain Analysis": {
                "description": "Identifies primary and support activities that create value",
                "suitable_for": ["operational analysis", "process improvement", "competitive advantage"],
                "complexity": 3,
                "components": [
                    "Primary Activities (Inbound Logistics, Operations, Outbound Logistics, Marketing & Sales, Service)",
                    "Support Activities (Infrastructure, HR Management, Technology Development, Procurement)",
                    "Margin Analysis",
                    "Value Creation Assessment"
                ]
            },
            "Balanced Scorecard": {
                "description": "Strategic planning and management system aligning business activities to vision and strategy",
                "suitable_for": ["performance management", "strategic planning", "organizational alignment"],
                "complexity": 4,
                "components": [
                    "Financial Perspective",
                    "Customer Perspective",
                    "Internal Business Processes",
                    "Learning and Growth Perspective",
                    "Strategic Objectives and Measures"
                ]
            },
            "BCG Matrix": {
                "description": "Evaluates products or business units based on market growth and market share",
                "suitable_for": ["portfolio analysis", "product strategy", "resource allocation"],
                "complexity": 2,
                "components": [
                    "Stars (High Growth, High Share)",
                    "Cash Cows (Low Growth, High Share)",
                    "Question Marks (High Growth, Low Share)",
                    "Dogs (Low Growth, Low Share)",
                    "Strategic Implications for Each Quadrant"
                ]
            },
            "McKinsey 7S Framework": {
                "description": "Examines seven internal elements for organizational effectiveness",
                "suitable_for": ["organizational analysis", "change management", "alignment assessment"],
                "complexity": 4,
                "components": [
                    "Strategy",
                    "Structure",
                    "Systems",
                    "Shared Values",
                    "Skills",
                    "Style",
                    "Staff"
                ]
            },
            "Blue Ocean Strategy": {
                "description": "Focuses on creating uncontested market space rather than competing in existing markets",
                "suitable_for": ["innovation strategy", "market creation", "differentiation"],
                "complexity": 4,
                "components": [
                    "Eliminate-Reduce-Raise-Create Grid",
                    "Strategy Canvas",
                    "Value Innovation",
                    "Six Paths Framework",
                    "Market-Creating Strategy"
                ]
            }
        }
    
    def _load_analysis_types(self) -> Dict[str, Any]:
        """Load information about different types of business analysis."""
        return {
            "market analysis": {
                "description": "assessment of market size, trends, segments, and opportunities",
                "key_questions": [
                    "What is the current market size and growth trajectory?",
                    "Who are the major players and what are their market shares?",
                    "What are the key market segments and their characteristics?",
                    "What trends are shaping the future of this market?",
                    "What are the entry barriers and success factors in this market?"
                ],
                "data_sources": [
                    "Industry reports and market research",
                    "Customer surveys and interviews",
                    "Competitor financial statements and annual reports",
                    "Trade publications and news sources",
                    "Government economic data"
                ]
            },
            "competitive analysis": {
                "description": "evaluation of competitors, their strategies, strengths, and weaknesses",
                "key_questions": [
                    "Who are the direct and indirect competitors?",
                    "What are each competitor's strengths and weaknesses?",
                    "What strategies are competitors employing?",
                    "How do competitors position themselves in the market?",
                    "What are competitors' pricing strategies?"
                ],
                "data_sources": [
                    "Competitor websites and marketing materials",
                    "Product comparisons and reviews",
                    "Financial reports and statements",
                    "Press releases and news coverage",
                    "Social media presence and customer feedback"
                ]
            },
            "financial analysis": {
                "description": "examination of financial performance, profitability, and financial health",
                "key_questions": [
                    "What are the key financial trends over the past 3-5 years?",
                    "How does profitability compare to industry benchmarks?",
                    "What is the cash flow situation and projection?",
                    "How efficient is capital allocation and utilization?",
                    "What is the financial risk profile of the organization?"
                ],
                "data_sources": [
                    "Balance sheets and income statements",
                    "Cash flow statements",
                    "Financial ratios and benchmarks",
                    "Industry average financial data",
                    "Investor presentations and reports"
                ]
            },
            "business model analysis": {
                "description": "assessment of how an organization creates, delivers, and captures value",
                "key_questions": [
                    "How does the organization create and deliver value to customers?",
                    "What is the revenue generation mechanism?",
                    "What are the key resources, activities, and partnerships?",
                    "How sustainable and scalable is the business model?",
                    "What are potential vulnerabilities in the business model?"
                ],
                "data_sources": [
                    "Strategic plans and business model documentation",
                    "Revenue and cost structure data",
                    "Stakeholder interviews",
                    "Customer value proposition statements",
                    "Partnership and supplier agreements"
                ]
            },
            "operational analysis": {
                "description": "evaluation of operational efficiency, processes, and performance",
                "key_questions": [
                    "What are the key operational processes and their performance?",
                    "Where are the bottlenecks and inefficiencies?",
                    "How does operational performance compare to industry benchmarks?",
                    "What are the quality control measures and their effectiveness?",
                    "How can operational efficiency be improved?"
                ],
                "data_sources": [
                    "Process documentation and flowcharts",
                    "Key performance indicators (KPIs) and metrics",
                    "Quality control data",
                    "Employee feedback and observations",
                    "Capacity utilization reports"
                ]
            },
            "strategic planning": {
                "description": "development of long-term objectives and action plans to achieve them",
                "key_questions": [
                    "What is the organization's vision and mission?",
                    "What are the key strategic objectives for the next 3-5 years?",
                    "What capabilities are needed to achieve these objectives?",
                    "What are the key strategic risks and opportunities?",
                    "How will progress and success be measured?"
                ],
                "data_sources": [
                    "Current strategic plans and mission statements",
                    "Market and competitive analysis reports",
                    "SWOT analysis and other strategic frameworks",
                    "Stakeholder input and priorities",
                    "Historical performance against strategic objectives"
                ]
            }
        }
    
    def _load_planning_methodologies(self) -> Dict[str, Any]:
        """Load strategic planning methodologies."""
        return {
            "OKR (Objectives and Key Results)": {
                "description": "A goal-setting framework that connects measurable results to ambitious objectives",
                "suitable_for": ["strategic planning", "performance management", "goal setting"],
                "complexity": 2,
                "steps": [
                    "Define 3-5 ambitious objectives",
                    "Establish 3-5 measurable key results for each objective",
                    "Cascade objectives throughout the organization",
                    "Implement regular check-ins and progress tracking",
                    "Conduct quarterly reviews and resets"
                ]
            },
            "Hoshin Kanri": {
                "description": "A strategic planning process that aligns organizational goals with tactical execution",
                "suitable_for": ["strategic planning", "organizational alignment", "operational planning"],
                "complexity": 4,
                "steps": [
                    "Establish organization vision and long-term goals",
                    "Develop breakthrough objectives (3-5 year horizon)",
                    "Define annual objectives that support breakthrough objectives",
                    "Cascade goals through 'catchball' process",
                    "Implement regular review cycles",
                    "Conduct annual reflection and adjustment"
                ]
            },
            "Scenario Planning": {
                "description": "Developing multiple plausible future scenarios to inform flexible strategic approaches",
                "suitable_for": ["strategic planning", "risk management", "market entry"],
                "complexity": 5,
                "steps": [
                    "Identify key forces and uncertainties",
                    "Develop 3-5 distinct, plausible future scenarios",
                    "Evaluate implications of each scenario",
                    "Create robust strategies that work across multiple scenarios",
                    "Identify early warning indicators for each scenario",
                    "Develop contingency plans for critical scenarios"
                ]
            },
            "Strategic Intent": {
                "description": "Creating a compelling long-term vision that stretches the organization",
                "suitable_for": ["strategic planning", "innovation", "transformation"],
                "complexity": 3,
                "steps": [
                    "Create a compelling, ambitious long-term vision",
                    "Ensure the vision provides clear direction but allows flexibility",
                    "Develop core capabilities needed to achieve the vision",
                    "Establish interim milestones and challenges",
                    "Align organizational systems to support the strategic intent",
                    "Consistently communicate and reinforce the vision"
                ]
            },
            "Agile Strategy": {
                "description": "Applying agile principles to strategy development for adaptability in changing environments",
                "suitable_for": ["strategic planning", "innovation", "digital transformation"],
                "complexity": 3,
                "steps": [
                    "Establish strategic direction and guardrails",
                    "Break strategy into short strategic sprints (30-90 days)",
                    "Form cross-functional teams for implementation",
                    "Conduct regular reviews and retrospectives",
                    "Adapt strategic priorities based on learning and market changes",
                    "Maintain strategic backlog of opportunities"
                ]
            }
        }
    
    def _load_market_segments(self) -> Dict[str, Any]:
        """Load information about different market segments/industries."""
        return {
            "technology": {
                "considerations": [
                    "Rapid pace of innovation and technological obsolescence",
                    "Intellectual property protection and patent landscapes",
                    "Network effects and platform dynamics",
                    "Technical talent acquisition and retention challenges",
                    "Regulatory considerations around data privacy and security"
                ]
            },
            "financial services": {
                "considerations": [
                    "Strict regulatory environment and compliance requirements",
                    "Technology disruption and fintech competition",
                    "Customer trust and security concerns",
                    "Interest rate sensitivity and economic cycle impacts",
                    "Legacy system integration challenges"
                ]
            },
            "healthcare": {
                "considerations": [
                    "Complex regulatory environment and compliance requirements",
                    "Payment model changes and reimbursement challenges",
                    "Patient privacy and data security concerns",
                    "Aging population and changing demographics",
                    "Integration of new technologies with existing care models"
                ]
            },
            "retail": {
                "considerations": [
                    "Omnichannel integration and digital transformation",
                    "Changing consumer expectations and shopping behaviors",
                    "Supply chain optimization and inventory management",
                    "Direct-to-consumer competition and marketplace dynamics",
                    "Physical footprint optimization and experiential retail"
                ]
            },
            "manufacturing": {
                "considerations": [
                    "Supply chain resilience and globalization impacts",
                    "Industry 4.0 and smart manufacturing adoption",
                    "Sustainability requirements and environmental regulations",
                    "Skilled labor shortages and workforce development",
                    "Total cost of ownership beyond direct manufacturing costs"
                ]
            },
            "all": {
                "considerations": [
                    "Global economic conditions and market volatility",
                    "Sustainability and ESG (Environmental, Social, Governance) considerations",
                    "Digital transformation and technology adoption",
                    "Changing consumer/customer expectations and behaviors",
                    "Talent acquisition, development, and retention"
                ]
            }
        }
    
    def _load_metrics_and_kpis(self) -> Dict[str, Any]:
        """Load business metrics and KPIs."""
        return {
            "Financial Metrics": {
                "relevant_for": ["all", "financial analysis", "strategic planning"],
                "metrics": [
                    {
                        "name": "Revenue Growth Rate",
                        "description": "Year-over-year percentage increase in revenue",
                        "calculation": "(Current Period Revenue - Previous Period Revenue) / Previous Period Revenue × 100%",
                        "industries": ["all"]
                    },
                    {
                        "name": "Gross Profit Margin",
                        "description": "Percentage of revenue that exceeds cost of goods sold",
                        "calculation": "(Revenue - Cost of Goods Sold) / Revenue × 100%",
                        "industries": ["all", "retail", "manufacturing"]
                    },
                    {
                        "name": "EBITDA Margin",
                        "description": "Earnings before interest, taxes, depreciation, and amortization as percentage of revenue",
                        "calculation": "EBITDA / Revenue × 100%",
                        "industries": ["all"]
                    },
                    {
                        "name": "Return on Investment (ROI)",
                        "description": "Measures gain or loss relative to the amount invested",
                        "calculation": "(Net Profit - Investment Cost) / Investment Cost × 100%",
                        "industries": ["all"]
                    },
                    {
                        "name": "Customer Acquisition Cost (CAC)",
                        "description": "Cost of acquiring a new customer",
                        "calculation": "Total Sales & Marketing Expenses / Number of New Customers Acquired",
                        "industries": ["all", "technology", "retail"]
                    }
                ]
            },
            "Market Metrics": {
                "relevant_for": ["market analysis", "competitive analysis", "strategic planning"],
                "metrics": [
                    {
                        "name": "Market Share",
                        "description": "Percentage of total market sales captured by a company",
                        "calculation": "Company Sales / Total Market Sales × 100%",
                        "industries": ["all"]
                    },
                    {
                        "name": "Brand Awareness",
                        "description": "Percentage of target audience that recognizes the brand",
                        "calculation": "Number of People Aware of Brand / Total Survey Respondents × 100%",
                        "industries": ["all", "retail", "consumer goods"]
                    },
                    {
                        "name": "Net Promoter Score (NPS)",
                        "description": "Measure of customer loyalty and likelihood to recommend",
                        "calculation": "Percentage of Promoters - Percentage of Detractors",
                        "industries": ["all", "technology", "retail", "financial services"]
                    },
                    {
                        "name": "Customer Lifetime Value (CLV)",
                        "description": "Total value a customer generates over their relationship with the company",
                        "calculation": "Average Purchase Value × Average Purchase Frequency × Average Customer Lifespan",
                        "industries": ["all", "retail", "financial services", "technology"]
                    }
                ]
            },
            "Operational Metrics": {
                "relevant_for": ["operational analysis", "process improvement"],
                "metrics": [
                    {
                        "name": "Inventory Turnover",
                        "description": "Number of times inventory is sold and replaced in a period",
                        "calculation": "Cost of Goods Sold / Average Inventory",
                        "industries": ["retail", "manufacturing", "consumer goods"]
                    },
                    {
                        "name": "Employee Productivity",
                        "description": "Output per employee",
                        "calculation": "Total Output / Number of Employees",
                        "industries": ["all", "manufacturing", "technology"]
                    },
                    {
                        "name": "Capacity Utilization",
                        "description": "Percentage of potential output that is actually being achieved",
                        "calculation": "Actual Output / Maximum Possible Output × 100%",
                        "industries": ["manufacturing", "healthcare", "transportation"]
                    },
                    {
                        "name": "Defect Rate",
                        "description": "Percentage of products with defects",
                        "calculation": "Number of Defective Units / Total Units Produced × 100%",
                        "industries": ["manufacturing", "technology"]
                    },
                    {
                        "name": "On-Time Delivery Rate",
                        "description": "Percentage of orders delivered on time",
                        "calculation": "Number of On-Time Deliveries / Total Number of Deliveries × 100%",
                        "industries": ["manufacturing", "retail", "transportation"]
                    }
                ]
            },
            "Digital Metrics": {
                "relevant_for": ["digital strategy", "marketing analysis", "business model analysis"],
                "metrics": [
                    {
                        "name": "Conversion Rate",
                        "description": "Percentage of visitors who take a desired action",
                        "calculation": "Number of Conversions / Total Number of Visitors × 100%",
                        "industries": ["technology", "retail", "financial services"]
                    },
                    {
                        "name": "Customer Churn Rate",
                        "description": "Percentage of customers who stop using a product/service",
                        "calculation": "Number of Customers Lost / Total Customers at Start of Period × 100%",
                        "industries": ["technology", "financial services", "subscription businesses"]
                    },
                    {
                        "name": "Monthly Active Users (MAU)",
                        "description": "Number of unique users who engage with a product in a month",
                        "calculation": "Count of unique users with at least one session in a month",
                        "industries": ["technology", "digital platforms"]
                    },
                    {
                        "name": "Customer Engagement Rate",
                        "description": "Measure of how users interact with content or product",
                        "calculation": "Total Engagements / Total Users (or Impressions) × 100%",
                        "industries": ["technology", "media", "retail"]
                    }
                ]
            }
        }


# Default instance for convenience
default_strategy = BusinessContentStrategy()


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