"""
Sample Data Generators for GRC Applications
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import random


class RiskDataGenerator:
    """Generate sample risk assessment data"""

    RISK_TYPES = [
        "Cybersecurity Threat",
        "Data Privacy Breach",
        "Third-Party Vendor Risk",
        "Operational Disruption",
        "Regulatory Non-Compliance",
        "Financial Fraud",
        "Reputational Damage",
        "Natural Disaster",
        "Insider Threat",
        "Technology Failure",
    ]

    RISK_DESCRIPTIONS = {
        "Cybersecurity Threat": [
            "Ransomware attack targeting critical infrastructure",
            "Phishing campaign compromising employee credentials",
            "DDoS attack on customer-facing services",
            "Zero-day vulnerability in core application",
        ],
        "Data Privacy Breach": [
            "Unauthorized access to customer PII database",
            "Accidental exposure of sensitive data in public repository",
            "Third-party breach affecting shared customer data",
            "Misconfigured cloud storage exposing confidential files",
        ],
        "Third-Party Vendor Risk": [
            "Critical vendor experiencing financial difficulties",
            "Vendor security breach affecting our data",
            "Key vendor acquired by competitor",
            "Vendor non-compliance with contractual SLAs",
        ],
    }

    @staticmethod
    def generate_risk(risk_id: int = 1) -> Dict[str, Any]:
        """
        Generate a single risk record

        Returns:
            Risk data dictionary
        """
        risk_type = random.choice(RiskDataGenerator.RISK_TYPES)
        severity = random.randint(1, 5)
        likelihood = random.randint(1, 5)
        risk_score = severity * likelihood

        return {
            "risk_id": f"RISK-{risk_id:04d}",
            "risk_type": risk_type,
            "severity": severity,
            "likelihood": likelihood,
            "risk_score": risk_score,
            "status": random.choice(["Open", "In Progress", "Mitigated", "Accepted"]),
            "owner": random.choice([
                "Security Team",
                "IT Operations",
                "Compliance Team",
                "Legal Department",
                "Executive Management",
            ]),
            "identified_date": (
                datetime.now() - timedelta(days=random.randint(1, 180))
            ).strftime("%Y-%m-%d"),
            "last_review_date": (
                datetime.now() - timedelta(days=random.randint(1, 30))
            ).strftime("%Y-%m-%d"),
        }

    @staticmethod
    def generate_risks(count: int = 10) -> List[Dict[str, Any]]:
        """
        Generate multiple risk records

        Args:
            count: Number of risks to generate

        Returns:
            List of risk dictionaries
        """
        return [RiskDataGenerator.generate_risk(i + 1) for i in range(count)]


class PolicyDataGenerator:
    """Generate sample policy data"""

    POLICY_TYPES = [
        "Information Security Policy",
        "Data Privacy Policy",
        "Acceptable Use Policy",
        "Access Control Policy",
        "Incident Response Policy",
        "Business Continuity Policy",
        "Change Management Policy",
        "Vendor Management Policy",
        "Data Retention Policy",
        "Remote Work Policy",
    ]

    @staticmethod
    def generate_policy(policy_id: int = 1) -> Dict[str, Any]:
        """
        Generate a single policy record

        Returns:
            Policy data dictionary
        """
        created_date = datetime.now() - timedelta(days=random.randint(30, 730))
        review_date = created_date + timedelta(days=365)

        return {
            "policy_id": f"POL-{policy_id:04d}",
            "policy_name": random.choice(PolicyDataGenerator.POLICY_TYPES),
            "version": f"{random.randint(1, 5)}.{random.randint(0, 9)}",
            "status": random.choice(["Draft", "Under Review", "Approved", "Published"]),
            "owner": random.choice([
                "CISO",
                "Compliance Officer",
                "Legal Team",
                "IT Director",
                "COO",
            ]),
            "created_date": created_date.strftime("%Y-%m-%d"),
            "last_updated": (created_date + timedelta(days=random.randint(30, 365))).strftime(
                "%Y-%m-%d"
            ),
            "next_review_date": review_date.strftime("%Y-%m-%d"),
            "applicable_frameworks": random.sample(
                ["SOC 2", "ISO 27001", "NIST CSF", "GDPR", "HIPAA"], k=random.randint(1, 3)
            ),
        }

    @staticmethod
    def generate_policies(count: int = 10) -> List[Dict[str, Any]]:
        """
        Generate multiple policy records

        Args:
            count: Number of policies to generate

        Returns:
            List of policy dictionaries
        """
        return [PolicyDataGenerator.generate_policy(i + 1) for i in range(count)]


class IncidentDataGenerator:
    """Generate sample incident data"""

    INCIDENT_TYPES = [
        "Phishing Attack",
        "Malware Infection",
        "Data Breach",
        "Unauthorized Access",
        "System Outage",
        "DDoS Attack",
        "Insider Threat",
        "Lost/Stolen Device",
        "Configuration Error",
        "Third-Party Breach",
    ]

    SEVERITIES = ["Low", "Medium", "High", "Critical"]

    @staticmethod
    def generate_incident(incident_id: int = 1) -> Dict[str, Any]:
        """
        Generate a single incident record

        Returns:
            Incident data dictionary
        """
        detection_date = datetime.now() - timedelta(days=random.randint(1, 90))
        resolution_days = random.randint(1, 30)
        resolution_date = detection_date + timedelta(days=resolution_days)

        status = random.choice(["Open", "Investigating", "Contained", "Resolved", "Closed"])

        return {
            "incident_id": f"INC-{incident_id:04d}",
            "incident_type": random.choice(IncidentDataGenerator.INCIDENT_TYPES),
            "severity": random.choice(IncidentDataGenerator.SEVERITIES),
            "status": status,
            "detection_date": detection_date.strftime("%Y-%m-%d %H:%M"),
            "resolution_date": resolution_date.strftime("%Y-%m-%d %H:%M")
            if status == "Closed"
            else "Ongoing",
            "affected_systems": random.randint(1, 20),
            "affected_users": random.randint(0, 500),
            "responder": random.choice([
                "SOC Team",
                "Incident Response Team",
                "Security Analyst",
                "IT Support",
                "External Consultant",
            ]),
            "estimated_cost": f"${random.randint(1000, 100000):,}",
        }

    @staticmethod
    def generate_incidents(count: int = 10) -> List[Dict[str, Any]]:
        """
        Generate multiple incident records

        Args:
            count: Number of incidents to generate

        Returns:
            List of incident dictionaries
        """
        return [IncidentDataGenerator.generate_incident(i + 1) for i in range(count)]


class VendorDataGenerator:
    """Generate sample vendor/third-party data"""

    VENDOR_TYPES = [
        "Cloud Service Provider",
        "SaaS Application",
        "Data Processor",
        "Payment Processor",
        "Consulting Services",
        "Managed Security Services",
        "Infrastructure Provider",
        "Software Developer",
    ]

    RISK_LEVELS = ["Low", "Medium", "High", "Critical"]

    @staticmethod
    def generate_vendor(vendor_id: int = 1) -> Dict[str, Any]:
        """
        Generate a single vendor record

        Returns:
            Vendor data dictionary
        """
        return {
            "vendor_id": f"VEN-{vendor_id:04d}",
            "vendor_name": f"Vendor {vendor_id} Inc.",
            "vendor_type": random.choice(VendorDataGenerator.VENDOR_TYPES),
            "risk_level": random.choice(VendorDataGenerator.RISK_LEVELS),
            "data_access": random.choice([
                "Customer PII",
                "Financial Data",
                "Employee Data",
                "Intellectual Property",
                "No Sensitive Data",
            ]),
            "contract_status": random.choice(["Active", "Expiring Soon", "Under Review", "Terminated"]),
            "last_assessment_date": (
                datetime.now() - timedelta(days=random.randint(1, 365))
            ).strftime("%Y-%m-%d"),
            "next_assessment_date": (
                datetime.now() + timedelta(days=random.randint(30, 365))
            ).strftime("%Y-%m-%d"),
            "compliance_status": random.choice(["Compliant", "Pending Review", "Non-Compliant"]),
            "soc2_certified": random.choice([True, False]),
            "iso27001_certified": random.choice([True, False]),
        }

    @staticmethod
    def generate_vendors(count: int = 10) -> List[Dict[str, Any]]:
        """
        Generate multiple vendor records

        Args:
            count: Number of vendors to generate

        Returns:
            List of vendor dictionaries
        """
        return [VendorDataGenerator.generate_vendor(i + 1) for i in range(count)]


class ComplianceDataGenerator:
    """Generate sample compliance control data"""

    FRAMEWORKS = ["SOC 2", "ISO 27001", "NIST CSF", "GDPR", "HIPAA"]

    CONTROL_DOMAINS = [
        "Access Control",
        "Network Security",
        "Data Protection",
        "Incident Management",
        "Risk Management",
        "Business Continuity",
        "Change Management",
        "Vendor Management",
    ]

    @staticmethod
    def generate_control(control_id: int = 1) -> Dict[str, Any]:
        """
        Generate a single compliance control record

        Returns:
            Control data dictionary
        """
        return {
            "control_id": f"CTRL-{control_id:04d}",
            "control_name": f"Control {control_id}",
            "framework": random.choice(ComplianceDataGenerator.FRAMEWORKS),
            "domain": random.choice(ComplianceDataGenerator.CONTROL_DOMAINS),
            "implementation_status": random.choice([
                "Not Started",
                "In Progress",
                "Implemented",
                "Needs Improvement",
            ]),
            "effectiveness": random.choice(["Effective", "Partially Effective", "Not Effective"]),
            "testing_frequency": random.choice(["Continuous", "Monthly", "Quarterly", "Annual"]),
            "last_tested_date": (
                datetime.now() - timedelta(days=random.randint(1, 90))
            ).strftime("%Y-%m-%d"),
            "next_test_date": (
                datetime.now() + timedelta(days=random.randint(30, 365))
            ).strftime("%Y-%m-%d"),
            "owner": random.choice([
                "Security Team",
                "IT Operations",
                "Compliance Team",
                "Engineering",
            ]),
            "evidence_collected": random.choice([True, False]),
        }

    @staticmethod
    def generate_controls(count: int = 10) -> List[Dict[str, Any]]:
        """
        Generate multiple control records

        Args:
            count: Number of controls to generate

        Returns:
            List of control dictionaries
        """
        return [ComplianceDataGenerator.generate_control(i + 1) for i in range(count)]

    @staticmethod
    def generate_gap_analysis() -> Dict[str, Any]:
        """
        Generate sample gap analysis data

        Returns:
            Gap analysis dictionary
        """
        return {
            "framework": random.choice(ComplianceDataGenerator.FRAMEWORKS),
            "assessment_date": datetime.now().strftime("%Y-%m-%d"),
            "total_controls": random.randint(50, 150),
            "implemented": random.randint(30, 100),
            "in_progress": random.randint(10, 30),
            "not_started": random.randint(5, 20),
            "compliance_percentage": random.randint(60, 95),
            "high_priority_gaps": random.randint(3, 10),
            "medium_priority_gaps": random.randint(5, 15),
            "low_priority_gaps": random.randint(2, 8),
        }


def generate_sample_dataset(dataset_type: str, count: int = 10) -> List[Dict[str, Any]]:
    """
    Generate sample dataset of specified type

    Args:
        dataset_type: Type of data ("risks", "policies", "incidents", "vendors", "controls")
        count: Number of records to generate

    Returns:
        List of data dictionaries

    Raises:
        ValueError: If unknown dataset type
    """
    generators = {
        "risks": RiskDataGenerator.generate_risks,
        "policies": PolicyDataGenerator.generate_policies,
        "incidents": IncidentDataGenerator.generate_incidents,
        "vendors": VendorDataGenerator.generate_vendors,
        "controls": ComplianceDataGenerator.generate_controls,
    }

    if dataset_type not in generators:
        raise ValueError(
            f"Unknown dataset type: {dataset_type}. "
            f"Available types: {', '.join(generators.keys())}"
        )

    return generators[dataset_type](count)
