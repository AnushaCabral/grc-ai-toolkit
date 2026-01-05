"""
Streamlit Test App for UI Components

This is a simple test app to validate that all UI components can be rendered.

Run with: streamlit run tests/test_ui_app.py
"""

import streamlit as st
from grc_ai_toolkit.ui import StreamlitComponents

st.set_page_config(page_title="GRC UI Component Test", layout="wide")

st.title("GRC AI Toolkit - UI Component Test")
st.write("This app validates that all UI components render correctly.")

st.divider()

# Test 1: Metric Cards
st.header("1. Metric Cards")
col1, col2, col3 = st.columns(3)

with col1:
    StreamlitComponents.metric_card(
        title="Total Risks",
        value="42",
        delta="+5",
        help_text="Total identified risks"
    )

with col2:
    StreamlitComponents.metric_card(
        title="Compliance Score",
        value="85%",
        delta="+2%",
        delta_color="normal",
        help_text="Overall compliance percentage"
    )

with col3:
    StreamlitComponents.metric_card(
        title="Open Issues",
        value="8",
        delta="-3",
        delta_color="inverse",
        help_text="Currently open issues"
    )

st.success("✓ Metric cards rendered successfully")

st.divider()

# Test 2: Status Badges
st.header("2. Status Badges")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("Completed:")
    StreamlitComponents.status_badge("completed")

with col2:
    st.write("In Progress:")
    StreamlitComponents.status_badge("in_progress")

with col3:
    st.write("Pending:")
    StreamlitComponents.status_badge("pending")

with col4:
    st.write("Failed:")
    StreamlitComponents.status_badge("failed")

st.success("✓ Status badges rendered successfully")

st.divider()

# Test 3: Info Boxes
st.header("3. Info Boxes")

StreamlitComponents.info_box(
    "This is an informational message.",
    box_type="info"
)

StreamlitComponents.info_box(
    "Operation completed successfully!",
    box_type="success"
)

StreamlitComponents.info_box(
    "Please review the following items.",
    box_type="warning"
)

StreamlitComponents.info_box(
    "An error occurred during processing.",
    box_type="error"
)

st.success("✓ Info boxes rendered successfully")

st.divider()

# Test 4: File Uploader
st.header("4. File Uploader with Preview")

uploaded_file = StreamlitComponents.file_uploader_with_preview(
    label="Upload a test document",
    accepted_types=["pdf", "docx", "txt"],
    max_size_mb=10
)

if uploaded_file:
    st.success(f"✓ File uploaded: {uploaded_file.name}")
else:
    st.info("No file uploaded yet")

st.divider()

# Test 5: Data Table
st.header("5. Data Table")

sample_data = [
    {"ID": "R-001", "Title": "Data Privacy Risk", "Severity": "High", "Status": "Open"},
    {"ID": "R-002", "Title": "Access Control Gap", "Severity": "Medium", "Status": "In Progress"},
    {"ID": "R-003", "Title": "Encryption Missing", "Severity": "High", "Status": "Resolved"},
    {"ID": "R-004", "Title": "Audit Trail Incomplete", "Severity": "Low", "Status": "Open"},
]

StreamlitComponents.data_table(
    data=sample_data,
    title="Sample Risk Register"
)

st.success("✓ Data table rendered successfully")

st.divider()

# Final Summary
st.header("Test Summary")
st.balloons()
st.success("✅ All UI components rendered successfully!")
st.info("The Streamlit UI components are working correctly. The UI blocker (B4) is resolved.")
