"""
GRC-Specific Form Builders
"""

from typing import Dict, Any, Optional, List
import streamlit as st


class GRCFormBuilder:
    """
    Form builder for common GRC use cases

    Provides pre-built forms for:
    - Policy generation
    - Risk assessment
    - Compliance gap analysis
    - Incident reporting
    """

    @staticmethod
    def policy_generation_form() -> Optional[Dict[str, Any]]:
        """
        Form for policy generation parameters

        Returns:
            Form data if submitted, else None
        """
        st.subheader("📝 Policy Generation Parameters")

        with st.form("policy_generation_form"):
            # Policy type
            policy_type = st.selectbox(
                "Policy Type *",
                [
                    "Information Security",
                    "Data Privacy",
                    "Access Control",
                    "Incident Response",
                    "Business Continuity",
                    "Acceptable Use",
                    "Change Management",
                    "Vendor Management",
                    "Other",
                ],
                help="Select the type of policy to generate"
            )

            if policy_type == "Other":
                policy_type = st.text_input("Specify Policy Type *")

            # Framework
            framework = st.selectbox(
                "Compliance Framework *",
                [
                    "SOC 2",
                    "ISO 27001",
                    "NIST CSF",
                    "GDPR",
                    "HIPAA",
                    "PCI DSS",
                    "CCPA",
                    "General Compliance",
                ],
                help="Primary compliance framework to align with"
            )

            # Industry
            industry = st.selectbox(
                "Industry *",
                [
                    "Technology/SaaS",
                    "Healthcare",
                    "Financial Services",
                    "Retail/E-commerce",
                    "Manufacturing",
                    "Education",
                    "Government",
                    "Professional Services",
                    "Other",
                ]
            )

            # Requirements
            requirements = st.text_area(
                "Specific Requirements",
                placeholder="Enter any specific requirements or sections to include...",
                help="Optional: Specific elements to include in the policy"
            )

            # Target audience
            target_audience = st.selectbox(
                "Target Audience",
                ["All Employees", "IT Staff", "Management", "Specific Department"]
            )

            # Additional context
            additional_context = st.text_area(
                "Additional Context",
                placeholder="Any additional context or considerations...",
                help="Optional: Additional information to help generate the policy"
            )

            # Submit
            submitted = st.form_submit_button("Generate Policy", type="primary")

            if submitted:
                if not policy_type or not framework or not industry:
                    st.error("Please fill in all required fields (*)")
                    return None

                return {
                    "policy_type": policy_type,
                    "framework": framework,
                    "industry": industry,
                    "requirements": requirements,
                    "target_audience": target_audience,
                    "additional_context": additional_context,
                }

        return None

    @staticmethod
    def risk_assessment_form() -> Optional[Dict[str, Any]]:
        """
        Form for risk assessment parameters

        Returns:
            Form data if submitted, else None
        """
        st.subheader("⚠️ Risk Assessment Parameters")

        with st.form("risk_assessment_form"):
            # Risk name/description
            risk_description = st.text_area(
                "Risk Description *",
                placeholder="Describe the risk to assess...",
                help="Detailed description of the risk"
            )

            # Risk category
            risk_type = st.selectbox(
                "Risk Category *",
                [
                    "Cybersecurity",
                    "Data Privacy",
                    "Operational",
                    "Financial",
                    "Compliance/Legal",
                    "Reputational",
                    "Strategic",
                    "Third-Party",
                    "Other",
                ]
            )

            # Severity and likelihood
            col1, col2 = st.columns(2)

            with col1:
                severity = st.slider(
                    "Severity (Impact) *",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="1 = Minimal, 5 = Critical"
                )

            with col2:
                likelihood = st.slider(
                    "Likelihood *",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="1 = Rare, 5 = Almost Certain"
                )

            # Industry context
            industry = st.selectbox(
                "Industry *",
                [
                    "Technology/SaaS",
                    "Healthcare",
                    "Financial Services",
                    "Retail/E-commerce",
                    "Manufacturing",
                    "Education",
                    "Government",
                    "Professional Services",
                    "Other",
                ]
            )

            # Current controls
            controls = st.text_area(
                "Current Controls",
                placeholder="Describe existing controls or mitigation measures...",
                help="Optional: What controls are already in place?"
            )

            # Scenario detail level
            detail_level = st.select_slider(
                "Analysis Detail Level",
                options=["Basic", "Standard", "Comprehensive"],
                value="Standard"
            )

            # Submit
            submitted = st.form_submit_button("Assess Risk", type="primary")

            if submitted:
                if not risk_description or not risk_type:
                    st.error("Please fill in all required fields (*)")
                    return None

                return {
                    "risk_description": risk_description,
                    "risk_type": risk_type,
                    "severity": severity,
                    "likelihood": likelihood,
                    "industry": industry,
                    "controls": controls or "None specified",
                    "detail_level": detail_level,
                }

        return None

    @staticmethod
    def compliance_gap_analysis_form() -> Optional[Dict[str, Any]]:
        """
        Form for compliance gap analysis

        Returns:
            Form data if submitted, else None
        """
        st.subheader("📊 Compliance Gap Analysis")

        with st.form("gap_analysis_form"):
            # Framework
            framework = st.selectbox(
                "Framework/Standard *",
                [
                    "SOC 2 Type II",
                    "ISO 27001:2022",
                    "NIST CSF 2.0",
                    "GDPR",
                    "HIPAA",
                    "PCI DSS 4.0",
                    "CCPA",
                    "Custom Framework",
                ]
            )

            if framework == "Custom Framework":
                framework = st.text_input("Specify Framework *")

            # Current state
            current_state = st.text_area(
                "Current State Description *",
                placeholder="Describe your current compliance posture...",
                help="What controls and processes are currently in place?"
            )

            # Required state
            required_state = st.text_area(
                "Required State Description",
                placeholder="Describe the target compliance state...",
                help="Optional: Specific requirements or target state"
            )

            # Scope
            scope_areas = st.multiselect(
                "Scope Areas",
                [
                    "Access Control",
                    "Data Protection",
                    "Network Security",
                    "Incident Management",
                    "Business Continuity",
                    "Vendor Management",
                    "Change Management",
                    "Risk Management",
                    "Compliance Monitoring",
                    "Training & Awareness",
                ],
                help="Select areas to analyze"
            )

            # Priority focus
            priority = st.radio(
                "Priority Focus",
                ["Quick Wins", "High-Risk Gaps", "Comprehensive Analysis"],
                help="Focus area for gap analysis"
            )

            # Submit
            submitted = st.form_submit_button("Analyze Gaps", type="primary")

            if submitted:
                if not framework or not current_state:
                    st.error("Please fill in all required fields (*)")
                    return None

                return {
                    "framework": framework,
                    "current_state": current_state,
                    "required_state": required_state or "Full compliance with " + framework,
                    "scope_areas": scope_areas,
                    "priority": priority,
                }

        return None

    @staticmethod
    def incident_report_form() -> Optional[Dict[str, Any]]:
        """
        Form for incident report generation

        Returns:
            Form data if submitted, else None
        """
        st.subheader("🚨 Incident Report Details")

        with st.form("incident_report_form"):
            # Incident type
            incident_type = st.selectbox(
                "Incident Type *",
                [
                    "Data Breach",
                    "Ransomware Attack",
                    "Phishing Incident",
                    "System Outage",
                    "Unauthorized Access",
                    "Data Loss",
                    "Policy Violation",
                    "Third-Party Incident",
                    "Other Security Incident",
                ]
            )

            # Severity
            severity = st.select_slider(
                "Severity Level *",
                options=["Low", "Medium", "High", "Critical"],
                value="Medium"
            )

            # Incident details
            details = st.text_area(
                "Incident Details *",
                placeholder="Provide detailed description of the incident...",
                help="What happened, when, how was it discovered, etc."
            )

            # Impact areas
            col1, col2 = st.columns(2)

            with col1:
                systems_affected = st.text_input(
                    "Systems Affected",
                    placeholder="e.g., CRM, Email Server"
                )

            with col2:
                data_involved = st.text_input(
                    "Data Involved",
                    placeholder="e.g., Customer PII, Financial Data"
                )

            # Timeline
            col3, col4 = st.columns(2)

            with col3:
                detection_date = st.date_input("Detection Date *")

            with col4:
                resolution_date = st.date_input(
                    "Resolution Date",
                    help="Leave blank if ongoing"
                )

            # Response actions
            response_actions = st.text_area(
                "Response Actions Taken",
                placeholder="Describe actions taken to contain and resolve...",
                help="What steps were taken to respond to the incident?"
            )

            # Report format
            report_format = st.radio(
                "Report Format",
                ["Executive Summary", "Detailed Technical Report", "Regulatory Filing"],
                help="Choose the appropriate format for your audience"
            )

            # Submit
            submitted = st.form_submit_button("Generate Report", type="primary")

            if submitted:
                if not incident_type or not details:
                    st.error("Please fill in all required fields (*)")
                    return None

                return {
                    "incident_type": incident_type,
                    "severity": severity,
                    "details": details,
                    "systems_affected": systems_affected,
                    "data_involved": data_involved,
                    "detection_date": str(detection_date),
                    "resolution_date": str(resolution_date) if resolution_date else "Ongoing",
                    "response_actions": response_actions,
                    "report_format": report_format,
                }

        return None

    @staticmethod
    def document_review_form() -> Optional[Dict[str, Any]]:
        """
        Form for document review parameters

        Returns:
            Form data if submitted, else None
        """
        st.subheader("🔍 Document Review Settings")

        with st.form("document_review_form"):
            # Document type
            document_type = st.selectbox(
                "Document Type *",
                [
                    "Policy Document",
                    "Procedure Manual",
                    "Risk Assessment",
                    "Compliance Report",
                    "Audit Report",
                    "Contract/Agreement",
                    "Technical Documentation",
                    "Other",
                ]
            )

            # Review framework
            framework = st.selectbox(
                "Review Framework",
                [
                    "SOC 2",
                    "ISO 27001",
                    "NIST",
                    "GDPR",
                    "General Best Practices",
                    "Custom Criteria",
                ]
            )

            # Target audience
            audience = st.selectbox(
                "Target Audience",
                ["Technical Staff", "Management", "All Employees", "External Stakeholders"]
            )

            # Review focus
            review_focus = st.multiselect(
                "Review Focus Areas",
                [
                    "Completeness",
                    "Accuracy",
                    "Clarity",
                    "Compliance",
                    "Style & Formatting",
                    "Technical Correctness",
                ],
                default=["Completeness", "Accuracy", "Clarity"]
            )

            # Depth of review
            review_depth = st.radio(
                "Review Depth",
                ["Quick Scan", "Standard Review", "Comprehensive Analysis"],
                index=1
            )

            # Submit
            submitted = st.form_submit_button("Review Document", type="primary")

            if submitted:
                if not document_type:
                    st.error("Please fill in all required fields (*)")
                    return None

                return {
                    "document_type": document_type,
                    "framework": framework,
                    "audience": audience,
                    "review_focus": review_focus,
                    "review_depth": review_depth,
                }

        return None
