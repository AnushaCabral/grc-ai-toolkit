"""
Common Layout Templates for Streamlit Apps
"""

from typing import Optional, Dict, Any
import streamlit as st


def create_header(
    title: str,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    show_divider: bool = True
):
    """
    Create standardized header

    Args:
        title: Page title
        subtitle: Optional subtitle
        icon: Optional icon emoji
        show_divider: Whether to show divider line
    """
    if icon:
        st.title(f"{icon} {title}")
    else:
        st.title(title)

    if subtitle:
        st.markdown(f"*{subtitle}*")

    if show_divider:
        st.divider()


def create_sidebar(
    app_name: str,
    navigation_items: Optional[Dict[str, str]] = None,
    show_info: bool = True
) -> Optional[str]:
    """
    Create standardized sidebar

    Args:
        app_name: Application name
        navigation_items: Dict of page names and icons
        show_info: Whether to show app info

    Returns:
        Selected navigation item or None
    """
    with st.sidebar:
        st.header(app_name)
        st.divider()

        selected = None

        # Navigation
        if navigation_items:
            st.subheader("Navigation")

            for page, icon in navigation_items.items():
                if st.button(f"{icon} {page}", use_container_width=True):
                    selected = page

            st.divider()

        # App info
        if show_info:
            st.caption("Powered by GRC AI Toolkit")
            st.caption("v1.0.0")

        return selected


def create_footer(
    copyright_text: Optional[str] = None,
    links: Optional[Dict[str, str]] = None
):
    """
    Create standardized footer

    Args:
        copyright_text: Copyright text
        links: Dict of link text and URLs
    """
    st.divider()

    cols = st.columns([3, 1])

    with cols[0]:
        if copyright_text:
            st.caption(copyright_text)
        else:
            st.caption("© 2025 GRC AI Toolkit. All rights reserved.")

    with cols[1]:
        if links:
            link_html = " | ".join(
                [f'<a href="{url}" target="_blank">{text}</a>' for text, url in links.items()]
            )
            st.markdown(link_html, unsafe_allow_html=True)


def two_column_layout(
    left_content: callable,
    right_content: callable,
    left_width: int = 1,
    right_width: int = 1
):
    """
    Create two-column layout

    Args:
        left_content: Function to render left column
        right_content: Function to render right column
        left_width: Relative width of left column
        right_width: Relative width of right column
    """
    col1, col2 = st.columns([left_width, right_width])

    with col1:
        left_content()

    with col2:
        right_content()


def three_column_layout(
    left_content: callable,
    center_content: callable,
    right_content: callable,
    widths: tuple = (1, 1, 1)
):
    """
    Create three-column layout

    Args:
        left_content: Function to render left column
        center_content: Function to render center column
        right_content: Function to render right column
        widths: Tuple of relative widths
    """
    col1, col2, col3 = st.columns(widths)

    with col1:
        left_content()

    with col2:
        center_content()

    with col3:
        right_content()


def dashboard_layout(
    metrics: Dict[str, Any],
    main_content: callable,
    sidebar_content: Optional[callable] = None
):
    """
    Create dashboard layout with metrics at top

    Args:
        metrics: Dict of metric name to (value, delta) tuples
        main_content: Function to render main content
        sidebar_content: Optional function for sidebar
    """
    # Sidebar
    if sidebar_content:
        with st.sidebar:
            sidebar_content()

    # Metrics row
    if metrics:
        cols = st.columns(len(metrics))

        for i, (name, data) in enumerate(metrics.items()):
            with cols[i]:
                if isinstance(data, tuple):
                    value, delta = data
                    st.metric(name, value, delta)
                else:
                    st.metric(name, data)

        st.divider()

    # Main content
    main_content()


def wizard_layout(
    steps: list,
    current_step: int,
    step_content: callable
):
    """
    Create wizard/stepper layout

    Args:
        steps: List of step names
        current_step: Current step index (0-based)
        step_content: Function to render current step content
    """
    # Progress indicator
    st.progress((current_step + 1) / len(steps))

    # Step indicator
    step_cols = st.columns(len(steps))

    for i, step in enumerate(steps):
        with step_cols[i]:
            if i < current_step:
                st.markdown(f"✅ {step}")
            elif i == current_step:
                st.markdown(f"**🔹 {step}**")
            else:
                st.markdown(f"⚪ {step}")

    st.divider()

    # Current step content
    step_content()


def form_layout(
    title: str,
    fields: Dict[str, Dict[str, Any]],
    submit_label: str = "Submit",
    on_submit: Optional[callable] = None
) -> Optional[Dict[str, Any]]:
    """
    Create standardized form layout

    Args:
        title: Form title
        fields: Dict of field name to field config
        submit_label: Submit button label
        on_submit: Optional callback function

    Returns:
        Form data if submitted, else None
    """
    st.subheader(title)

    with st.form(key=f"form_{id(fields)}"):
        form_data = {}

        for field_name, config in fields.items():
            field_type = config.get("type", "text")
            label = config.get("label", field_name)
            default = config.get("default", None)
            help_text = config.get("help", None)
            required = config.get("required", False)

            # Render field based on type
            if field_type == "text":
                value = st.text_input(label, value=default or "", help=help_text)

            elif field_type == "textarea":
                value = st.text_area(label, value=default or "", help=help_text)

            elif field_type == "number":
                value = st.number_input(
                    label,
                    value=default or 0,
                    min_value=config.get("min", None),
                    max_value=config.get("max", None),
                    help=help_text
                )

            elif field_type == "select":
                options = config.get("options", [])
                value = st.selectbox(label, options, help=help_text)

            elif field_type == "multiselect":
                options = config.get("options", [])
                value = st.multiselect(label, options, default=default, help=help_text)

            elif field_type == "checkbox":
                value = st.checkbox(label, value=default or False, help=help_text)

            elif field_type == "date":
                value = st.date_input(label, value=default, help=help_text)

            elif field_type == "slider":
                value = st.slider(
                    label,
                    min_value=config.get("min", 0),
                    max_value=config.get("max", 100),
                    value=default or 50,
                    help=help_text
                )

            else:
                value = st.text_input(label, value=default or "", help=help_text)

            form_data[field_name] = value

        # Submit button
        submitted = st.form_submit_button(submit_label, type="primary")

        if submitted:
            # Validate required fields
            missing = [
                name for name, config in fields.items()
                if config.get("required") and not form_data.get(name)
            ]

            if missing:
                st.error(f"Required fields missing: {', '.join(missing)}")
                return None

            # Call callback if provided
            if on_submit:
                on_submit(form_data)

            return form_data

    return None


def results_display_layout(
    result: str,
    title: str = "Results",
    show_download: bool = True,
    download_filename: str = "result.txt",
    actions: Optional[Dict[str, callable]] = None
):
    """
    Display results with actions

    Args:
        result: Result text to display
        title: Results title
        show_download: Whether to show download button
        download_filename: Filename for download
        actions: Dict of action name to callback function
    """
    st.subheader(title)

    # Display result
    st.markdown(result)

    st.divider()

    # Actions
    action_cols = []

    if show_download:
        action_cols.append("download")

    if actions:
        action_cols.extend(actions.keys())

    if action_cols:
        cols = st.columns(len(action_cols))

        col_idx = 0

        # Download button
        if show_download:
            with cols[col_idx]:
                st.download_button(
                    "⬇️ Download",
                    data=result,
                    file_name=download_filename,
                    mime="text/plain",
                    type="primary",
                    use_container_width=True
                )
            col_idx += 1

        # Action buttons
        if actions:
            for action_name, callback in actions.items():
                with cols[col_idx]:
                    if st.button(action_name, use_container_width=True):
                        callback(result)
                col_idx += 1
