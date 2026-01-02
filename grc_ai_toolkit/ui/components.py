"""
Reusable Streamlit Components for GRC Applications
"""

from typing import Dict, Any, List, Optional, Callable
import streamlit as st
from datetime import datetime


class StreamlitComponents:
    """
    Collection of reusable Streamlit components for GRC tools

    Provides consistent UI elements across all GRC applications.
    """

    @staticmethod
    def metric_card(
        title: str,
        value: str,
        delta: Optional[str] = None,
        delta_color: str = "normal",
        help_text: Optional[str] = None
    ):
        """
        Display a metric card

        Args:
            title: Metric title
            value: Metric value
            delta: Optional change indicator
            delta_color: "normal", "inverse", or "off"
            help_text: Optional help tooltip
        """
        st.metric(
            label=title,
            value=value,
            delta=delta,
            delta_color=delta_color,
            help=help_text
        )

    @staticmethod
    def status_badge(
        status: str,
        custom_colors: Optional[Dict[str, str]] = None
    ):
        """
        Display a colored status badge

        Args:
            status: Status text
            custom_colors: Optional color mapping
        """
        # Default color scheme
        colors = {
            "completed": "green",
            "in_progress": "blue",
            "pending": "orange",
            "failed": "red",
            "active": "green",
            "inactive": "gray",
            "high": "red",
            "medium": "orange",
            "low": "green",
        }

        # Override with custom colors
        if custom_colors:
            colors.update(custom_colors)

        color = colors.get(status.lower(), "gray")

        st.markdown(
            f'<span style="background-color:{color};color:white;padding:4px 12px;'
            f'border-radius:12px;font-size:14px;">{status}</span>',
            unsafe_allow_html=True
        )

    @staticmethod
    def info_box(
        message: str,
        box_type: str = "info",
        icon: bool = True
    ):
        """
        Display an info/warning/error box

        Args:
            message: Message text
            box_type: "info", "success", "warning", or "error"
            icon: Whether to show icon
        """
        if box_type == "info":
            st.info(message, icon="ℹ️" if icon else None)
        elif box_type == "success":
            st.success(message, icon="✅" if icon else None)
        elif box_type == "warning":
            st.warning(message, icon="⚠️" if icon else None)
        elif box_type == "error":
            st.error(message, icon="🚨" if icon else None)

    @staticmethod
    def progress_tracker(
        current: int,
        total: int,
        label: Optional[str] = None
    ):
        """
        Display a progress bar with percentage

        Args:
            current: Current progress
            total: Total items
            label: Optional label
        """
        percentage = (current / total) * 100 if total > 0 else 0

        if label:
            st.write(label)

        st.progress(percentage / 100)
        st.caption(f"{current}/{total} ({percentage:.1f}%)")

    @staticmethod
    def file_uploader_with_preview(
        label: str,
        accepted_types: Optional[List[str]] = None,
        max_size_mb: int = 10,
        show_stats: bool = True
    ):
        """
        File uploader with preview and stats

        Args:
            label: Uploader label
            accepted_types: List of accepted file extensions
            max_size_mb: Maximum file size in MB
            show_stats: Whether to show file statistics

        Returns:
            Uploaded file object or None
        """
        accepted_types = accepted_types or ["pdf", "docx", "txt", "csv"]

        uploaded_file = st.file_uploader(
            label,
            type=accepted_types,
            help=f"Maximum file size: {max_size_mb}MB"
        )

        if uploaded_file is not None:
            # Check file size
            file_size_mb = uploaded_file.size / (1024 * 1024)

            if file_size_mb > max_size_mb:
                st.error(f"File too large ({file_size_mb:.2f}MB). Maximum: {max_size_mb}MB")
                return None

            if show_stats:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Filename", uploaded_file.name)

                with col2:
                    st.metric("Size", f"{file_size_mb:.2f} MB")

                with col3:
                    st.metric("Type", uploaded_file.type)

        return uploaded_file

    @staticmethod
    def data_table(
        data: List[Dict[str, Any]],
        columns: Optional[List[str]] = None,
        searchable: bool = True,
        sortable: bool = True
    ):
        """
        Display an interactive data table

        Args:
            data: List of data dictionaries
            columns: Optional column names to display
            searchable: Enable search functionality
            sortable: Enable column sorting
        """
        if not data:
            st.info("No data to display")
            return

        # Search functionality
        if searchable:
            search = st.text_input("🔍 Search", key=f"search_{id(data)}")
            if search:
                data = [
                    row for row in data
                    if any(search.lower() in str(v).lower() for v in row.values())
                ]

        # Display as dataframe
        import pandas as pd
        df = pd.DataFrame(data)

        if columns:
            df = df[columns]

        st.dataframe(df, use_container_width=True)

    @staticmethod
    def action_buttons(
        buttons: List[Dict[str, Any]],
        layout: str = "horizontal"
    ) -> Optional[str]:
        """
        Display a set of action buttons

        Args:
            buttons: List of button configs with 'label', 'type', 'icon' keys
            layout: "horizontal" or "vertical"

        Returns:
            Label of clicked button or None
        """
        if layout == "horizontal":
            cols = st.columns(len(buttons))

            for i, button_config in enumerate(buttons):
                with cols[i]:
                    label = button_config.get("label", f"Button {i}")
                    button_type = button_config.get("type", "secondary")
                    icon = button_config.get("icon", "")

                    display_label = f"{icon} {label}" if icon else label

                    if st.button(
                        display_label,
                        type=button_type,
                        key=f"btn_{id(buttons)}_{i}",
                        use_container_width=True
                    ):
                        return label

        else:  # vertical
            for i, button_config in enumerate(buttons):
                label = button_config.get("label", f"Button {i}")
                button_type = button_config.get("type", "secondary")
                icon = button_config.get("icon", "")

                display_label = f"{icon} {label}" if icon else label

                if st.button(
                    display_label,
                    type=button_type,
                    key=f"btn_{id(buttons)}_{i}",
                    use_container_width=True
                ):
                    return label

        return None

    @staticmethod
    def loading_spinner(
        message: str = "Processing...",
        func: Optional[Callable] = None,
        *args,
        **kwargs
    ):
        """
        Display loading spinner while executing function

        Args:
            message: Loading message
            func: Function to execute
            *args, **kwargs: Function arguments

        Returns:
            Function result if func provided, else None
        """
        with st.spinner(message):
            if func:
                return func(*args, **kwargs)

    @staticmethod
    def download_button(
        label: str,
        data: str,
        filename: str,
        mime: str = "text/plain",
        icon: str = "⬇️"
    ):
        """
        Styled download button

        Args:
            label: Button label
            data: Data to download
            filename: Download filename
            mime: MIME type
            icon: Button icon
        """
        st.download_button(
            label=f"{icon} {label}",
            data=data,
            file_name=filename,
            mime=mime,
            type="primary"
        )

    @staticmethod
    def collapsible_section(
        title: str,
        content: Callable,
        expanded: bool = False
    ):
        """
        Create a collapsible section

        Args:
            title: Section title
            content: Function that renders content
            expanded: Whether to start expanded
        """
        with st.expander(title, expanded=expanded):
            content()

    @staticmethod
    def tabs_navigation(
        tabs: List[str],
        render_functions: List[Callable]
    ):
        """
        Create tabbed navigation

        Args:
            tabs: List of tab names
            render_functions: List of functions to render each tab
        """
        selected_tabs = st.tabs(tabs)

        for i, tab in enumerate(selected_tabs):
            with tab:
                render_functions[i]()

    @staticmethod
    def confirmation_dialog(
        message: str,
        confirm_label: str = "Confirm",
        cancel_label: str = "Cancel"
    ) -> bool:
        """
        Display confirmation dialog

        Args:
            message: Confirmation message
            confirm_label: Confirm button label
            cancel_label: Cancel button label

        Returns:
            True if confirmed, False otherwise
        """
        st.warning(message)

        col1, col2 = st.columns(2)

        confirmed = False

        with col1:
            if st.button(confirm_label, type="primary", use_container_width=True):
                confirmed = True

        with col2:
            if st.button(cancel_label, use_container_width=True):
                confirmed = False

        return confirmed

    @staticmethod
    def timeline_view(
        events: List[Dict[str, Any]],
        date_field: str = "date",
        title_field: str = "title",
        description_field: str = "description"
    ):
        """
        Display events in timeline format

        Args:
            events: List of event dictionaries
            date_field: Field name for date
            title_field: Field name for title
            description_field: Field name for description
        """
        for event in events:
            date = event.get(date_field, "Unknown date")
            title = event.get(title_field, "Untitled")
            description = event.get(description_field, "")

            st.markdown(f"**{date}** - {title}")
            if description:
                st.caption(description)
            st.markdown("---")

    @staticmethod
    def key_value_display(
        data: Dict[str, Any],
        columns: int = 2
    ):
        """
        Display key-value pairs in columns

        Args:
            data: Dictionary of key-value pairs
            columns: Number of columns
        """
        cols = st.columns(columns)

        for i, (key, value) in enumerate(data.items()):
            with cols[i % columns]:
                st.markdown(f"**{key}:**")
                st.write(value)
