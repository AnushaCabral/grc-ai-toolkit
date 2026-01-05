"""
Unit tests for UI components

These tests validate that UI components can be imported and instantiated.
Full rendering tests require running the Streamlit app (test_ui_app.py).
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestUIComponentsImport:
    """Test that UI components can be imported"""

    def test_import_streamlit_components(self):
        """Test StreamlitComponents can be imported"""
        from grc_ai_toolkit.ui import StreamlitComponents

        assert StreamlitComponents is not None

    def test_streamlit_components_has_methods(self):
        """Test StreamlitComponents has expected methods"""
        from grc_ai_toolkit.ui import StreamlitComponents

        # Check all expected methods exist
        expected_methods = [
            'metric_card',
            'status_badge',
            'info_box',
            'progress_tracker',
            'file_uploader_with_preview',
            'data_table',
            'action_buttons',
            'loading_spinner',
            'download_button',
            'collapsible_section',
            'tabs_navigation',
            'confirmation_dialog',
            'timeline_view',
            'key_value_display',
        ]

        for method in expected_methods:
            assert hasattr(StreamlitComponents, method), f"Missing method: {method}"
            assert callable(getattr(StreamlitComponents, method))


class TestUIComponentsWithMock:
    """Test UI components with mocked Streamlit"""

    @pytest.fixture(autouse=True)
    def mock_streamlit(self):
        """Mock streamlit module for all tests"""
        with patch('grc_ai_toolkit.ui.components.st') as mock_st:
            # Configure mocks
            mock_st.metric = Mock()
            mock_st.markdown = Mock()
            mock_st.info = Mock()
            mock_st.success = Mock()
            mock_st.warning = Mock()
            mock_st.error = Mock()
            mock_st.progress = Mock()
            mock_st.file_uploader = Mock()
            mock_st.dataframe = Mock()
            mock_st.button = Mock()
            mock_st.spinner = Mock(return_value=MagicMock(__enter__=Mock(), __exit__=Mock()))
            mock_st.download_button = Mock()
            mock_st.expander = Mock(return_value=MagicMock(__enter__=Mock(), __exit__=Mock()))
            mock_st.tabs = Mock(return_value=[Mock(), Mock(), Mock()])
            mock_st.columns = Mock(return_value=[Mock(), Mock()])

            yield mock_st

    def test_metric_card(self, mock_streamlit):
        """Test metric_card component"""
        from grc_ai_toolkit.ui import StreamlitComponents

        StreamlitComponents.metric_card(
            title="Test Metric",
            value="100",
            delta="+10",
            help_text="Test help"
        )

        # Verify st.metric was called
        mock_streamlit.metric.assert_called_once()
        call_args = mock_streamlit.metric.call_args
        assert call_args.kwargs['label'] == "Test Metric"
        assert call_args.kwargs['value'] == "100"
        assert call_args.kwargs['delta'] == "+10"

    def test_status_badge(self, mock_streamlit):
        """Test status_badge component"""
        from grc_ai_toolkit.ui import StreamlitComponents

        StreamlitComponents.status_badge("completed")

        # Verify st.markdown was called
        mock_streamlit.markdown.assert_called_once()
        call_args = mock_streamlit.markdown.call_args[0][0]
        assert "completed" in call_args
        assert "green" in call_args  # Default color for completed

    def test_status_badge_custom_colors(self, mock_streamlit):
        """Test status_badge with custom colors"""
        from grc_ai_toolkit.ui import StreamlitComponents

        custom_colors = {"custom_status": "purple"}
        StreamlitComponents.status_badge("custom_status", custom_colors=custom_colors)

        mock_streamlit.markdown.assert_called_once()
        call_args = mock_streamlit.markdown.call_args[0][0]
        assert "purple" in call_args

    def test_info_box_types(self, mock_streamlit):
        """Test all info_box types"""
        from grc_ai_toolkit.ui import StreamlitComponents

        # Test info type
        StreamlitComponents.info_box("Info message", box_type="info")
        mock_streamlit.info.assert_called_once()

        # Test success type
        StreamlitComponents.info_box("Success message", box_type="success")
        mock_streamlit.success.assert_called_once()

        # Test warning type
        StreamlitComponents.info_box("Warning message", box_type="warning")
        mock_streamlit.warning.assert_called_once()

        # Test error type
        StreamlitComponents.info_box("Error message", box_type="error")
        mock_streamlit.error.assert_called_once()

    def test_data_table(self, mock_streamlit):
        """Test data_table component"""
        from grc_ai_toolkit.ui import StreamlitComponents

        test_data = [
            {"name": "Item 1", "value": 100},
            {"name": "Item 2", "value": 200},
        ]

        # Mock pandas and text_input
        mock_streamlit.text_input = Mock(return_value="")

        StreamlitComponents.data_table(data=test_data, searchable=False)

        # Verify dataframe was called
        assert mock_streamlit.dataframe.called

    def test_action_buttons(self, mock_streamlit):
        """Test action_buttons component"""
        from grc_ai_toolkit.ui import StreamlitComponents

        # Create proper mock columns with context manager support
        mock_col1 = MagicMock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=False)

        mock_col2 = MagicMock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=False)

        mock_streamlit.columns = Mock(return_value=[mock_col1, mock_col2])
        mock_streamlit.button = Mock(return_value=False)

        buttons = [
            {"label": "Save", "key": "save_btn"},
            {"label": "Cancel", "key": "cancel_btn"},
        ]

        result = StreamlitComponents.action_buttons(buttons)

        # Verify columns was called for horizontal layout
        assert mock_streamlit.columns.called


class TestUIFormsImport:
    """Test that UI forms can be imported"""

    def test_import_ui_forms(self):
        """Test that forms module exists"""
        try:
            from grc_ai_toolkit.ui import forms
            assert forms is not None
        except ImportError:
            # Forms might not be exported, check if file exists
            import os
            forms_path = os.path.join("grc_ai_toolkit", "ui", "forms.py")
            assert os.path.exists(forms_path), "forms.py file should exist"


class TestUILayoutsImport:
    """Test that UI layouts can be imported"""

    def test_import_ui_layouts(self):
        """Test that layouts module exists"""
        try:
            from grc_ai_toolkit.ui import layouts
            assert layouts is not None
        except ImportError:
            # Layouts might not be exported, check if file exists
            import os
            layouts_path = os.path.join("grc_ai_toolkit", "ui", "layouts.py")
            assert os.path.exists(layouts_path), "layouts.py file should exist"


class TestUIIntegration:
    """Integration tests for UI components"""

    def test_ui_module_exports(self):
        """Test that ui module exports expected components"""
        from grc_ai_toolkit import ui

        assert hasattr(ui, 'StreamlitComponents')
        assert ui.StreamlitComponents is not None

    def test_streamlit_dependency_available(self):
        """Test that streamlit is installed"""
        try:
            import streamlit
            assert streamlit is not None
        except ImportError:
            pytest.fail("Streamlit should be installed as a dependency")
