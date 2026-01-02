"""
Tests for sample data generators
"""

import pytest
from grc_ai_toolkit.sample_data import (
    RiskDataGenerator,
    PolicyDataGenerator,
    IncidentDataGenerator,
    VendorDataGenerator,
    ComplianceDataGenerator,
    generate_sample_dataset,
)


class TestRiskDataGenerator:
    """Tests for RiskDataGenerator"""

    def test_generate_single_risk(self):
        """Test generating a single risk"""
        risk = RiskDataGenerator.generate_risk(1)

        assert "risk_id" in risk
        assert "risk_type" in risk
        assert "severity" in risk
        assert "likelihood" in risk
        assert "risk_score" in risk

        # Validate data types and ranges
        assert isinstance(risk["severity"], int)
        assert 1 <= risk["severity"] <= 5
        assert isinstance(risk["likelihood"], int)
        assert 1 <= risk["likelihood"] <= 5
        assert risk["risk_score"] == risk["severity"] * risk["likelihood"]

    def test_generate_multiple_risks(self):
        """Test generating multiple risks"""
        risks = RiskDataGenerator.generate_risks(count=10)

        assert len(risks) == 10
        assert all("risk_id" in r for r in risks)

        # Check IDs are unique
        ids = [r["risk_id"] for r in risks]
        assert len(ids) == len(set(ids))

    def test_risk_id_format(self):
        """Test risk ID formatting"""
        risk = RiskDataGenerator.generate_risk(5)

        assert risk["risk_id"] == "RISK-0005"


class TestPolicyDataGenerator:
    """Tests for PolicyDataGenerator"""

    def test_generate_single_policy(self):
        """Test generating a single policy"""
        policy = PolicyDataGenerator.generate_policy(1)

        assert "policy_id" in policy
        assert "policy_name" in policy
        assert "version" in policy
        assert "status" in policy
        assert "applicable_frameworks" in policy

        # Check frameworks is a list
        assert isinstance(policy["applicable_frameworks"], list)
        assert len(policy["applicable_frameworks"]) >= 1

    def test_generate_multiple_policies(self):
        """Test generating multiple policies"""
        policies = PolicyDataGenerator.generate_policies(count=20)

        assert len(policies) == 20

        # Verify all have required fields
        for policy in policies:
            assert "policy_id" in policy
            assert "created_date" in policy
            assert "next_review_date" in policy


class TestIncidentDataGenerator:
    """Tests for IncidentDataGenerator"""

    def test_generate_single_incident(self):
        """Test generating a single incident"""
        incident = IncidentDataGenerator.generate_incident(1)

        assert "incident_id" in incident
        assert "incident_type" in incident
        assert "severity" in incident
        assert "detection_date" in incident

        # Check severity is valid
        assert incident["severity"] in ["Low", "Medium", "High", "Critical"]

    def test_generate_multiple_incidents(self):
        """Test generating multiple incidents"""
        incidents = IncidentDataGenerator.generate_incidents(count=15)

        assert len(incidents) == 15

        # Check all incidents have numeric affected systems
        for incident in incidents:
            assert isinstance(incident["affected_systems"], int)
            assert incident["affected_systems"] >= 0


class TestVendorDataGenerator:
    """Tests for VendorDataGenerator"""

    def test_generate_single_vendor(self):
        """Test generating a single vendor"""
        vendor = VendorDataGenerator.generate_vendor(1)

        assert "vendor_id" in vendor
        assert "vendor_name" in vendor
        assert "vendor_type" in vendor
        assert "risk_level" in vendor

        # Check certifications are boolean
        assert isinstance(vendor["soc2_certified"], bool)
        assert isinstance(vendor["iso27001_certified"], bool)

    def test_generate_multiple_vendors(self):
        """Test generating multiple vendors"""
        vendors = VendorDataGenerator.generate_vendors(count=25)

        assert len(vendors) == 25

        # Check risk levels are valid
        valid_risk_levels = ["Low", "Medium", "High", "Critical"]
        for vendor in vendors:
            assert vendor["risk_level"] in valid_risk_levels


class TestComplianceDataGenerator:
    """Tests for ComplianceDataGenerator"""

    def test_generate_single_control(self):
        """Test generating a single control"""
        control = ComplianceDataGenerator.generate_control(1)

        assert "control_id" in control
        assert "control_name" in control
        assert "framework" in control
        assert "domain" in control
        assert "implementation_status" in control

        # Check evidence is boolean
        assert isinstance(control["evidence_collected"], bool)

    def test_generate_multiple_controls(self):
        """Test generating multiple controls"""
        controls = ComplianceDataGenerator.generate_controls(count=30)

        assert len(controls) == 30

        # Check all have valid frameworks
        valid_frameworks = ["SOC 2", "ISO 27001", "NIST CSF", "GDPR", "HIPAA"]
        for control in controls:
            assert control["framework"] in valid_frameworks

    def test_generate_gap_analysis(self):
        """Test generating gap analysis data"""
        gap_analysis = ComplianceDataGenerator.generate_gap_analysis()

        assert "framework" in gap_analysis
        assert "total_controls" in gap_analysis
        assert "implemented" in gap_analysis
        assert "in_progress" in gap_analysis
        assert "not_started" in gap_analysis
        assert "compliance_percentage" in gap_analysis

        # Validate percentages
        assert 0 <= gap_analysis["compliance_percentage"] <= 100


class TestGenerateSampleDataset:
    """Tests for generate_sample_dataset function"""

    def test_generate_risks_dataset(self):
        """Test generating risks dataset"""
        dataset = generate_sample_dataset("risks", count=5)

        assert len(dataset) == 5
        assert all("risk_id" in item for item in dataset)

    def test_generate_policies_dataset(self):
        """Test generating policies dataset"""
        dataset = generate_sample_dataset("policies", count=8)

        assert len(dataset) == 8
        assert all("policy_id" in item for item in dataset)

    def test_generate_incidents_dataset(self):
        """Test generating incidents dataset"""
        dataset = generate_sample_dataset("incidents", count=12)

        assert len(dataset) == 12
        assert all("incident_id" in item for item in dataset)

    def test_generate_vendors_dataset(self):
        """Test generating vendors dataset"""
        dataset = generate_sample_dataset("vendors", count=6)

        assert len(dataset) == 6
        assert all("vendor_id" in item for item in dataset)

    def test_generate_controls_dataset(self):
        """Test generating controls dataset"""
        dataset = generate_sample_dataset("controls", count=15)

        assert len(dataset) == 15
        assert all("control_id" in item for item in dataset)

    def test_invalid_dataset_type(self):
        """Test error handling for invalid dataset type"""
        with pytest.raises(ValueError, match="Unknown dataset type"):
            generate_sample_dataset("invalid_type", count=10)


class TestDataConsistency:
    """Tests for data consistency across generators"""

    def test_risk_score_calculation(self):
        """Test that risk scores are calculated correctly"""
        risks = RiskDataGenerator.generate_risks(count=100)

        for risk in risks:
            expected_score = risk["severity"] * risk["likelihood"]
            assert risk["risk_score"] == expected_score

    def test_date_formats(self):
        """Test that dates are in consistent format"""
        incidents = IncidentDataGenerator.generate_incidents(count=10)

        for incident in incidents:
            # Detection date should be in YYYY-MM-DD HH:MM format
            assert len(incident["detection_date"]) >= 16

    def test_id_uniqueness(self):
        """Test that generated IDs are unique"""
        risks = RiskDataGenerator.generate_risks(count=50)

        risk_ids = [r["risk_id"] for r in risks]
        assert len(risk_ids) == len(set(risk_ids)), "Risk IDs are not unique"

        policies = PolicyDataGenerator.generate_policies(count=50)
        policy_ids = [p["policy_id"] for p in policies]
        assert len(policy_ids) == len(set(policy_ids)), "Policy IDs are not unique"
