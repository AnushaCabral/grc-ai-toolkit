"""
Pre-built Agent Templates for Common GRC Tasks
"""

from typing import Dict, Any, Optional
import logging

from .base import BaseAgent, AgentConfig, SimpleAgent
from ..llm import LLMManager


logger = logging.getLogger(__name__)


class ResearchAgent(SimpleAgent):
    """
    Agent specialized in research and information gathering

    Use for:
    - Searching through documents
    - Finding relevant information
    - Gathering context for analysis
    """

    def __init__(self, llm_manager: LLMManager, **kwargs):
        config = AgentConfig(
            name="Research Agent",
            description="Gathers information and researches topics from provided context",
            system_message="""You are a research specialist. Your role is to:
1. Search through provided documents and context
2. Extract relevant information
3. Summarize findings clearly
4. Cite sources when available

Be thorough, accurate, and concise in your research.""",
            llm_manager=llm_manager,
            temperature=0.3,  # Lower temperature for factual research
            **kwargs
        )
        super().__init__(config)


class AnalysisAgent(SimpleAgent):
    """
    Agent specialized in analyzing information and identifying patterns

    Use for:
    - Risk analysis
    - Gap analysis
    - Compliance assessment
    - Pattern recognition
    """

    def __init__(self, llm_manager: LLMManager, **kwargs):
        config = AgentConfig(
            name="Analysis Agent",
            description="Analyzes information to identify patterns, risks, and gaps",
            system_message="""You are an analytical expert specializing in GRC (Governance, Risk, and Compliance). Your role is to:
1. Analyze provided information critically
2. Identify patterns, trends, and anomalies
3. Assess risks and compliance gaps
4. Provide evidence-based insights
5. Rate findings by severity/priority

Use structured thinking and provide clear, actionable analysis.""",
            llm_manager=llm_manager,
            temperature=0.5,  # Balanced temperature for analysis
            **kwargs
        )
        super().__init__(config)


class GenerationAgent(SimpleAgent):
    """
    Agent specialized in content generation

    Use for:
    - Policy drafting
    - Report writing
    - Documentation creation
    - Scenario generation
    """

    def __init__(self, llm_manager: LLMManager, **kwargs):
        config = AgentConfig(
            name="Generation Agent",
            description="Generates professional GRC content and documentation",
            system_message="""You are a professional GRC content writer. Your role is to:
1. Create clear, well-structured documents
2. Follow industry standards and best practices
3. Use appropriate professional tone
4. Include all required sections
5. Ensure accuracy and compliance

Write in clear, professional language suitable for business audiences.""",
            llm_manager=llm_manager,
            temperature=0.7,  # Higher temperature for creative generation
            **kwargs
        )
        super().__init__(config)


class ReviewAgent(SimpleAgent):
    """
    Agent specialized in reviewing and improving content

    Use for:
    - Document review
    - Quality assurance
    - Completeness checking
    - Improvement suggestions
    """

    def __init__(self, llm_manager: LLMManager, **kwargs):
        config = AgentConfig(
            name="Review Agent",
            description="Reviews content for quality, completeness, and compliance",
            system_message="""You are a quality assurance expert for GRC documentation. Your role is to:
1. Review documents for completeness and accuracy
2. Check compliance with frameworks and standards
3. Identify gaps and missing elements
4. Suggest specific improvements
5. Verify professional tone and clarity

Provide constructive, detailed feedback with specific examples.""",
            llm_manager=llm_manager,
            temperature=0.4,  # Lower temperature for critical review
            **kwargs
        )
        super().__init__(config)


class PolicyDraftingAgent(BaseAgent):
    """
    Specialized agent for policy document creation

    Multi-step process:
    1. Research existing policies
    2. Analyze requirements
    3. Generate draft
    4. Review and refine
    """

    def __init__(self, llm_manager: LLMManager):
        config = AgentConfig(
            name="Policy Drafting Agent",
            description="Creates comprehensive policy documents",
            system_message="You are a policy writing expert.",
            llm_manager=llm_manager,
            temperature=0.7
        )
        super().__init__(config)

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute policy drafting workflow

        Args:
            task: Policy requirements
            context: Additional context (framework, industry, etc.)

        Returns:
            Policy document
        """
        self._update_state(task=task, context=context, status="in_progress")

        try:
            context = context or {}

            # Step 1: Research
            self._add_message("user", f"Research phase: {task}")

            research_prompt = f"""Research requirements for this policy:

{task}

Framework: {context.get('framework', 'General compliance')}
Industry: {context.get('industry', 'General')}

Identify:
1. Required sections
2. Regulatory requirements
3. Industry best practices
4. Key stakeholders"""

            research = self.llm_manager.generate(
                prompt=research_prompt,
                system_message="You are a policy research expert.",
                temperature=0.3
            )

            self._add_message("assistant", research)
            logger.info(f"{self.config.name}: Research phase complete")

            # Step 2: Generate draft
            draft_prompt = f"""Based on this research:

{research}

Create a comprehensive policy document with these sections:
1. Purpose and Scope
2. Definitions
3. Policy Statements
4. Roles and Responsibilities
5. Procedures
6. Compliance and Enforcement
7. Review and Updates

Original requirements: {task}"""

            draft = self.llm_manager.generate(
                prompt=draft_prompt,
                system_message="You are a professional policy writer.",
                temperature=0.7
            )

            self._add_message("assistant", draft)
            logger.info(f"{self.config.name}: Draft generation complete")

            # Step 3: Review and refine
            review_prompt = f"""Review this policy draft:

{draft}

Improve:
1. Clarity and readability
2. Completeness
3. Professional tone
4. Specific and actionable language

Provide the improved version."""

            final_policy = self.llm_manager.generate(
                prompt=review_prompt,
                system_message="You are a policy review expert.",
                temperature=0.5
            )

            self._add_message("assistant", final_policy)
            logger.info(f"{self.config.name}: Review phase complete")

            self._update_state(
                status="completed",
                result=final_policy,
                increment_iteration=True
            )

            return final_policy

        except Exception as e:
            logger.error(f"{self.config.name} failed: {str(e)}")
            self._update_state(status="failed", result=str(e))
            raise


class RiskAssessmentAgent(BaseAgent):
    """
    Specialized agent for risk assessment and scenario analysis

    Multi-step process:
    1. Identify risk factors
    2. Analyze impact and likelihood
    3. Generate risk scenarios
    4. Recommend controls
    """

    def __init__(self, llm_manager: LLMManager):
        config = AgentConfig(
            name="Risk Assessment Agent",
            description="Performs comprehensive risk assessments",
            system_message="You are a risk management expert.",
            llm_manager=llm_manager,
            temperature=0.6
        )
        super().__init__(config)

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute risk assessment workflow

        Args:
            task: Risk to assess
            context: Additional context (industry, existing controls, etc.)

        Returns:
            Risk assessment report
        """
        self._update_state(task=task, context=context, status="in_progress")

        try:
            context = context or {}

            # Step 1: Identify risk factors
            identification_prompt = f"""Identify risk factors for:

{task}

Industry: {context.get('industry', 'General')}
Current Controls: {context.get('controls', 'None specified')}

List:
1. Primary risk factors
2. Secondary risk factors
3. Stakeholders affected
4. Assets at risk"""

            risk_factors = self.llm_manager.generate(
                prompt=identification_prompt,
                system_message="You are a risk identification expert.",
                temperature=0.4
            )

            self._add_message("assistant", risk_factors)

            # Step 2: Assess impact and likelihood
            assessment_prompt = f"""Based on these risk factors:

{risk_factors}

Assess:
1. Impact (1-5 scale): Financial, Operational, Reputational, Legal
2. Likelihood (1-5 scale)
3. Overall risk score
4. Risk priority (Critical/High/Medium/Low)

Provide specific reasoning for each rating."""

            assessment = self.llm_manager.generate(
                prompt=assessment_prompt,
                system_message="You are a risk scoring expert.",
                temperature=0.3
            )

            self._add_message("assistant", assessment)

            # Step 3: Generate scenarios
            scenario_prompt = f"""Create a detailed risk scenario:

Risk: {task}
Assessment: {assessment}

Include:
1. Initial trigger event
2. Timeline of events
3. Primary impacts (quantified where possible)
4. Cascade effects
5. Affected stakeholders"""

            scenario = self.llm_manager.generate(
                prompt=scenario_prompt,
                system_message="You are a risk scenario planning expert.",
                temperature=0.7
            )

            self._add_message("assistant", scenario)

            # Step 4: Recommend controls
            controls_prompt = f"""Based on this risk assessment:

{assessment}

And this scenario:

{scenario}

Recommend:
1. Preventive controls
2. Detective controls
3. Corrective controls
4. Priority order for implementation
5. Estimated effort for each control"""

            controls = self.llm_manager.generate(
                prompt=controls_prompt,
                system_message="You are a control design expert.",
                temperature=0.5
            )

            # Compile final report
            final_report = f"""# Risk Assessment Report

## Risk Identified
{task}

## Risk Factors
{risk_factors}

## Risk Assessment
{assessment}

## Risk Scenario
{scenario}

## Recommended Controls
{controls}
"""

            self._update_state(
                status="completed",
                result=final_report,
                increment_iteration=True
            )

            logger.info(f"{self.config.name}: Assessment complete")

            return final_report

        except Exception as e:
            logger.error(f"{self.config.name} failed: {str(e)}")
            self._update_state(status="failed", result=str(e))
            raise


def create_grc_workflow(llm_manager: LLMManager) -> 'AgentOrchestrator':
    """
    Create a standard GRC document workflow

    Workflow:
    1. Research requirements
    2. Analyze context
    3. Generate content
    4. Review and refine

    Args:
        llm_manager: LLM manager instance

    Returns:
        Configured orchestrator
    """
    from .orchestrator import AgentOrchestrator

    orchestrator = AgentOrchestrator(name="GRC Document Workflow")

    # Create agents
    research_agent = ResearchAgent(llm_manager)
    analysis_agent = AnalysisAgent(llm_manager)
    generation_agent = GenerationAgent(llm_manager)
    review_agent = ReviewAgent(llm_manager)

    # Add workflow steps
    orchestrator.add_step(
        "research",
        research_agent,
        "Research: {task}"
    )

    orchestrator.add_step(
        "analyze",
        analysis_agent,
        "Analyze requirements based on: {research}",
        depends_on=["research"]
    )

    orchestrator.add_step(
        "generate",
        generation_agent,
        "Generate document based on: {analyze}",
        depends_on=["analyze"]
    )

    orchestrator.add_step(
        "review",
        review_agent,
        "Review and improve: {generate}",
        depends_on=["generate"]
    )

    return orchestrator
