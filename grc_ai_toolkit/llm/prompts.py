"""
Prompt Templates for GRC Applications
"""

from typing import Dict, Any, Optional
from string import Template


class PromptTemplate:
    """
    Template for LLM prompts with variable substitution

    Example:
        template = PromptTemplate(
            name="policy_generator",
            template="Create a {policy_type} policy for {framework} compliance.",
            input_variables=["policy_type", "framework"]
        )
        prompt = template.format(policy_type="Information Security", framework="SOC 2")
    """

    def __init__(
        self,
        name: str,
        template: str,
        input_variables: list[str],
        description: Optional[str] = None,
        system_message: Optional[str] = None
    ):
        self.name = name
        self.template = template
        self.input_variables = input_variables
        self.description = description or ""
        self.system_message = system_message

        # Validate template has all required variables
        self._validate()

    def _validate(self):
        """Validate template contains all input variables"""
        for var in self.input_variables:
            if f"{{{var}}}" not in self.template:
                raise ValueError(f"Template missing required variable: {var}")

    def format(self, **kwargs) -> str:
        """
        Format template with provided variables

        Args:
            **kwargs: Variable name=value pairs

        Returns:
            Formatted prompt string
        """
        # Check all required variables provided
        missing = set(self.input_variables) - set(kwargs.keys())
        if missing:
            raise ValueError(f"Missing required variables: {missing}")

        return self.template.format(**kwargs)

    def __str__(self) -> str:
        return f"PromptTemplate({self.name})"


class PromptLibrary:
    """Library of pre-built GRC prompts"""

    # Policy Generation Prompts
    POLICY_GENERATOR = PromptTemplate(
        name="policy_generator",
        template="""You are a professional GRC policy writer. Create a comprehensive {policy_type} policy for {framework} compliance.

Industry: {industry}
Requirements: {requirements}

The policy should include:
1. Purpose and Scope
2. Definitions
3. Policy Statements
4. Roles and Responsibilities
5. Procedures and Guidelines
6. Compliance and Enforcement
7. Review and Updates

Write in clear, professional language suitable for a {target_audience} audience.
Be specific and actionable. Include relevant citations from industry standards.

Output the policy in markdown format with proper headings and structure.""",
        input_variables=["policy_type", "framework", "industry", "requirements", "target_audience"],
        system_message="You are an expert GRC policy writer with deep knowledge of compliance frameworks and industry best practices.",
        description="Generate comprehensive policy documents"
    )

    # Risk Scenario Prompts
    RISK_SCENARIO_GENERATOR = PromptTemplate(
        name="risk_scenario_generator",
        template="""You are a risk management expert. Create a detailed risk scenario analysis.

Risk Type: {risk_type}
Severity: {severity}/5
Likelihood: {likelihood}/5
Industry: {industry}
Current Controls: {controls}

Create a comprehensive scenario that includes:

1. **Initial Event**: What triggers the scenario (be specific and realistic)
2. **Timeline**: How events unfold over hours/days/weeks
3. **Primary Impacts**:
   - Financial impact (estimated costs and losses)
   - Operational impact (business disruption details)
   - Reputational impact (brand and customer effects)
   - Legal/Regulatory impact (potential consequences)
4. **Cascade Effects**: Secondary and tertiary impacts
5. **Affected Stakeholders**: Who is impacted and how
6. **Mitigation Strategies**: How to prevent or respond
7. **Lessons Learned**: Key takeaways for improvement

Be specific, realistic, and based on actual industry incidents when possible.
Include quantitative estimates where appropriate.""",
        input_variables=["risk_type", "severity", "likelihood", "industry", "controls"],
        system_message="You are a seasoned risk management consultant with expertise in scenario planning and business continuity.",
        description="Generate detailed risk scenarios with impact analysis"
    )

    # Compliance Gap Analysis
    COMPLIANCE_GAP_ANALYSIS = PromptTemplate(
        name="compliance_gap_analysis",
        template="""You are a compliance expert. Analyze the gap between current state and required compliance state.

Framework: {framework}
Current State: {current_state}
Required State: {required_state}

Perform a comprehensive gap analysis:

1. **Control Gaps**: Identify missing or inadequate controls
2. **Documentation Gaps**: Identify missing policies, procedures, or evidence
3. **Process Gaps**: Identify process improvements needed
4. **Technical Gaps**: Identify technical controls or tools needed
5. **Training Gaps**: Identify knowledge or skill gaps in the team

For each gap:
- Describe the specific gap
- Assess the risk level (High/Medium/Low)
- Provide remediation recommendations
- Estimate effort and timeline
- Suggest priority order

Output as a structured gap analysis report in markdown format.""",
        input_variables=["framework", "current_state", "required_state"],
        system_message="You are a compliance auditor with expertise in multiple frameworks and gap analysis methodologies.",
        description="Analyze compliance gaps and provide remediation recommendations"
    )

    # Document Review and Improvement
    DOCUMENT_REVIEWER = PromptTemplate(
        name="document_reviewer",
        template="""You are a professional editor and GRC expert. Review and improve this document.

Document Type: {document_type}
Framework: {framework}
Target Audience: {audience}

Document Content:
{content}

Review for:
1. **Completeness**: Are all required sections present?
2. **Accuracy**: Is the content technically correct?
3. **Clarity**: Is it clear and easy to understand?
4. **Compliance**: Does it meet framework requirements?
5. **Style**: Professional tone, consistent terminology, proper formatting

Provide:
1. **Completeness Score** (0-100)
2. **Specific Issues** with priority (High/Medium/Low)
3. **Suggested Improvements** with before/after examples
4. **Missing Elements** that should be added
5. **Best Practice Recommendations**

Be constructive and specific in your feedback.""",
        input_variables=["document_type", "framework", "audience", "content"],
        system_message="You are an expert technical writer and compliance reviewer with high standards for quality and accuracy.",
        description="Review documents and provide improvement suggestions"
    )

    # Incident Report Generator
    INCIDENT_REPORT_GENERATOR = PromptTemplate(
        name="incident_report_generator",
        template="""You are a security incident response expert. Create a comprehensive incident report.

Incident Type: {incident_type}
Severity: {severity}
Incident Details: {details}

Create a structured incident report including:

1. **Executive Summary**: High-level overview in 2-3 sentences
2. **Incident Details**:
   - Date and time of detection
   - Affected systems/data
   - Discovery method
3. **Timeline of Events**: Chronological sequence
4. **Impact Assessment**:
   - Systems affected
   - Data involved
   - Business impact
   - Financial impact (if applicable)
5. **Response Actions**: What was done to contain and resolve
6. **Root Cause Analysis**: Why it happened
7. **Lessons Learned**: What we learned
8. **Recommendations**: Preventive measures for the future

Use professional language suitable for executive and regulatory audiences.
Be factual, specific, and action-oriented.""",
        input_variables=["incident_type", "severity", "details"],
        system_message="You are a cybersecurity incident response professional with experience in forensics and reporting.",
        description="Generate comprehensive incident reports"
    )

    # Control Narrative Generator
    CONTROL_NARRATIVE_GENERATOR = PromptTemplate(
        name="control_narrative_generator",
        template="""You are a compliance documentation expert. Write a control narrative for audit purposes.

Control ID: {control_id}
Control Name: {control_name}
Framework: {framework}
Control Objective: {objective}

Write a comprehensive control narrative that describes:

1. **Control Description**: What the control does
2. **Control Owner**: Who is responsible
3. **Control Frequency**: How often it operates
4. **Control Activities**: Specific activities performed
5. **Evidence**: What evidence is produced
6. **Exceptions**: How exceptions are handled
7. **Monitoring**: How effectiveness is monitored

The narrative should:
- Be clear and specific
- Demonstrate how the control achieves its objective
- Describe the who, what, when, where, and how
- Be suitable for auditor review
- Include specific examples where helpful

Write in present tense, active voice.""",
        input_variables=["control_id", "control_name", "framework", "objective"],
        system_message="You are a SOC 2 and ISO 27001 auditor who writes excellent control narratives.",
        description="Generate control narratives for audit documentation"
    )

    @classmethod
    def get_template(cls, name: str) -> PromptTemplate:
        """Get template by name"""
        template_map = {
            "policy_generator": cls.POLICY_GENERATOR,
            "risk_scenario_generator": cls.RISK_SCENARIO_GENERATOR,
            "compliance_gap_analysis": cls.COMPLIANCE_GAP_ANALYSIS,
            "document_reviewer": cls.DOCUMENT_REVIEWER,
            "incident_report_generator": cls.INCIDENT_REPORT_GENERATOR,
            "control_narrative_generator": cls.CONTROL_NARRATIVE_GENERATOR,
        }

        if name not in template_map:
            raise ValueError(f"Unknown template: {name}")

        return template_map[name]

    @classmethod
    def list_templates(cls) -> list[str]:
        """List all available templates"""
        return [
            "policy_generator",
            "risk_scenario_generator",
            "compliance_gap_analysis",
            "document_reviewer",
            "incident_report_generator",
            "control_narrative_generator",
        ]
