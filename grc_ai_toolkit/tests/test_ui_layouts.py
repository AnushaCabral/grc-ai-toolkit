"""
Comprehensive tests for UI layouts module

These tests verify all layout functions work correctly with mocked Streamlit.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from grc_ai_toolkit.ui import layouts


class TestCreateHeader:
    """Test create_header layout function"""

    @pytest.fixture(autouse=True)
    def mock_streamlit(self):
        """Mock streamlit module for all tests"""
        with patch('grc_ai_toolkit.ui.layouts.st') as mock_st:
            mock_st.title = Mock()
            mock_st.markdown = Mock()
            mock_st.divider = Mock()
            yield mock_st

    def test_create_header_basic(self, mock_streamlit):
        """Test basic header creation"""
        layouts.create_header("Test Title")

        mock_streamlit.title.assert_called_once_with("Test Title")
        mock_streamlit.divider.assert_called_once()

    def test_create_header_with_icon(self, mock_streamlit):
        """Test header with icon"""
        layouts.create_header("Test Title", icon="📊")

        mock_streamlit.title.assert_called_once_with("📊 Test Title")

    def test_create_header_with_subtitle(self, mock_streamlit):
        """Test header with subtitle"""
        layouts.create_header("Test Title", subtitle="Test Subtitle")

        mock_streamlit.markdown.assert_called_once_with("*Test Subtitle*")

    def test_create_header_no_divider(self, mock_streamlit):
        """Test header without divider"""
        layouts.create_header("Test Title", show_divider=False)

        mock_streamlit.divider.assert_not_called()

    def test_create_header_all_options(self, mock_streamlit):
        """Test header with all options"""
        layouts.create_header(
            "Test Title",
            subtitle="Test Subtitle",
            icon="🔒",
            show_divider=True
        )

        mock_streamlit.title.assert_called_once_with("🔒 Test Title")
        mock_streamlit.markdown.assert_called_once_with("*Test Subtitle*")
        mock_streamlit.divider.assert_called_once()


class TestCreateSidebar:
    """Test create_sidebar layout function"""

    @pytest.fixture(autouse=True)
    def mock_streamlit(self):
        """Mock streamlit module for all tests"""
        with patch('grc_ai_toolkit.ui.layouts.st') as mock_st:
            # Create proper sidebar context manager mock
            mock_sidebar = MagicMock()
            mock_sidebar.__enter__ = Mock(return_value=mock_sidebar)
            mock_sidebar.__exit__ = Mock(return_value=False)
            mock_st.sidebar = mock_sidebar

            mock_st.header = Mock()
            mock_st.subheader = Mock()
            mock_st.divider = Mock()
            mock_st.button = Mock(return_value=False)
            mock_st.caption = Mock()

            yield mock_st

    def test_create_sidebar_basic(self, mock_streamlit):
        """Test basic sidebar creation"""
        result = layouts.create_sidebar("Test App")

        mock_streamlit.header.assert_called_once_with("Test App")
        assert result is None

    def test_create_sidebar_with_navigation(self, mock_streamlit):
        """Test sidebar with navigation items"""
        nav_items = {"Home": "🏠", "Dashboard": "📊", "Settings": "⚙️"}

        layouts.create_sidebar("Test App", navigation_items=nav_items)

        mock_streamlit.subheader.assert_called_once_with("Navigation")
        assert mock_streamlit.button.call_count == 3

    def test_create_sidebar_navigation_selected(self, mock_streamlit):
        """Test sidebar navigation returns selected item"""
        nav_items = {"Home": "🏠", "Dashboard": "📊"}

        # Mock button to return True for Dashboard
        mock_streamlit.button.side_effect = [False, True]

        result = layouts.create_sidebar("Test App", navigation_items=nav_items)

        assert result == "Dashboard"

    def test_create_sidebar_show_info(self, mock_streamlit):
        """Test sidebar with app info"""
        layouts.create_sidebar("Test App", show_info=True)

        # Check that caption was called with app info
        caption_calls = [call[0][0] for call in mock_streamlit.caption.call_args_list]
        assert "Powered by GRC AI Toolkit" in caption_calls
        assert "v1.0.0" in caption_calls

    def test_create_sidebar_hide_info(self, mock_streamlit):
        """Test sidebar without app info"""
        layouts.create_sidebar("Test App", show_info=False)

        mock_streamlit.caption.assert_not_called()


class TestCreateFooter:
    """Test create_footer layout function"""

    @pytest.fixture(autouse=True)
    def mock_streamlit(self):
        """Mock streamlit module for all tests"""
        with patch('grc_ai_toolkit.ui.layouts.st') as mock_st:
            # Create column mocks
            mock_col1 = MagicMock()
            mock_col1.__enter__ = Mock(return_value=mock_col1)
            mock_col1.__exit__ = Mock(return_value=False)

            mock_col2 = MagicMock()
            mock_col2.__enter__ = Mock(return_value=mock_col2)
            mock_col2.__exit__ = Mock(return_value=False)

            mock_st.columns = Mock(return_value=[mock_col1, mock_col2])
            mock_st.divider = Mock()
            mock_st.caption = Mock()
            mock_st.markdown = Mock()

            yield mock_st

    def test_create_footer_default(self, mock_streamlit):
        """Test footer with default copyright"""
        layouts.create_footer()

        mock_streamlit.divider.assert_called_once()
        mock_streamlit.caption.assert_called_once()
        assert "© 2025 GRC AI Toolkit" in mock_streamlit.caption.call_args[0][0]

    def test_create_footer_custom_copyright(self, mock_streamlit):
        """Test footer with custom copyright"""
        layouts.create_footer(copyright_text="© 2025 Custom Corp")

        caption_arg = mock_streamlit.caption.call_args[0][0]
        assert "Custom Corp" in caption_arg

    def test_create_footer_with_links(self, mock_streamlit):
        """Test footer with links"""
        links = {"Privacy": "https://example.com/privacy", "Terms": "https://example.com/terms"}

        layouts.create_footer(links=links)

        mock_streamlit.markdown.assert_called_once()
        markdown_arg = mock_streamlit.markdown.call_args[0][0]
        assert "Privacy" in markdown_arg
        assert "Terms" in markdown_arg
        assert "https://example.com/privacy" in markdown_arg


class TestTwoColumnLayout:
    """Test two_column_layout function"""

    @pytest.fixture(autouse=True)
    def mock_streamlit(self):
        """Mock streamlit module for all tests"""
        with patch('grc_ai_toolkit.ui.layouts.st') as mock_st:
            # Create column mocks
            mock_col1 = MagicMock()
            mock_col1.__enter__ = Mock(return_value=mock_col1)
            mock_col1.__exit__ = Mock(return_value=False)

            mock_col2 = MagicMock()
            mock_col2.__enter__ = Mock(return_value=mock_col2)
            mock_col2.__exit__ = Mock(return_value=False)

            mock_st.columns = Mock(return_value=[mock_col1, mock_col2])

            yield mock_st

    def test_two_column_layout_equal(self, mock_streamlit):
        """Test two-column layout with equal widths"""
        left_called = False
        right_called = False

        def left_content():
            nonlocal left_called
            left_called = True

        def right_content():
            nonlocal right_called
            right_called = True

        layouts.two_column_layout(left_content, right_content)

        assert left_called
        assert right_called
        mock_streamlit.columns.assert_called_once_with([1, 1])

    def test_two_column_layout_custom_widths(self, mock_streamlit):
        """Test two-column layout with custom widths"""
        layouts.two_column_layout(lambda: None, lambda: None, left_width=2, right_width=1)

        mock_streamlit.columns.assert_called_once_with([2, 1])


class TestThreeColumnLayout:
    """Test three_column_layout function"""

    @pytest.fixture(autouse=True)
    def mock_streamlit(self):
        """Mock streamlit module for all tests"""
        with patch('grc_ai_toolkit.ui.layouts.st') as mock_st:
            # Create column mocks
            mock_cols = []
            for _ in range(3):
                mock_col = MagicMock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=False)
                mock_cols.append(mock_col)

            mock_st.columns = Mock(return_value=mock_cols)

            yield mock_st

    def test_three_column_layout_equal(self, mock_streamlit):
        """Test three-column layout with equal widths"""
        call_counts = {"left": 0, "center": 0, "right": 0}

        def left_content():
            call_counts["left"] += 1

        def center_content():
            call_counts["center"] += 1

        def right_content():
            call_counts["right"] += 1

        layouts.three_column_layout(left_content, center_content, right_content)

        assert call_counts["left"] == 1
        assert call_counts["center"] == 1
        assert call_counts["right"] == 1
        mock_streamlit.columns.assert_called_once_with((1, 1, 1))

    def test_three_column_layout_custom_widths(self, mock_streamlit):
        """Test three-column layout with custom widths"""
        layouts.three_column_layout(
            lambda: None, lambda: None, lambda: None,
            widths=(2, 1, 1)
        )

        mock_streamlit.columns.assert_called_once_with((2, 1, 1))


class TestDashboardLayout:
    """Test dashboard_layout function"""

    @pytest.fixture(autouse=True)
    def mock_streamlit(self):
        """Mock streamlit module for all tests"""
        with patch('grc_ai_toolkit.ui.layouts.st') as mock_st:
            # Create sidebar and column mocks
            mock_sidebar = MagicMock()
            mock_sidebar.__enter__ = Mock(return_value=mock_sidebar)
            mock_sidebar.__exit__ = Mock(return_value=False)
            mock_st.sidebar = mock_sidebar

            # Create column mocks
            mock_cols = []
            for _ in range(3):
                mock_col = MagicMock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=False)
                mock_cols.append(mock_col)

            mock_st.columns = Mock(return_value=mock_cols)
            mock_st.metric = Mock()
            mock_st.divider = Mock()

            yield mock_st

    def test_dashboard_layout_basic(self, mock_streamlit):
        """Test basic dashboard layout"""
        metrics = {"Users": 100, "Revenue": "$50k"}
        main_called = False

        def main_content():
            nonlocal main_called
            main_called = True

        layouts.dashboard_layout(metrics, main_content)

        assert main_called
        assert mock_streamlit.metric.call_count == 2

    def test_dashboard_layout_with_sidebar(self, mock_streamlit):
        """Test dashboard layout with sidebar"""
        sidebar_called = False

        def sidebar_content():
            nonlocal sidebar_called
            sidebar_called = True

        layouts.dashboard_layout({}, lambda: None, sidebar_content=sidebar_content)

        assert sidebar_called

    def test_dashboard_layout_metrics_with_delta(self, mock_streamlit):
        """Test dashboard metrics with delta tuples"""
        metrics = {"Users": (100, "+10"), "Revenue": ("$50k", "+$5k")}

        layouts.dashboard_layout(metrics, lambda: None)

        # Verify metric calls
        calls = mock_streamlit.metric.call_args_list
        assert len(calls) == 2


class TestWizardLayout:
    """Test wizard_layout function"""

    @pytest.fixture(autouse=True)
    def mock_streamlit(self):
        """Mock streamlit module for all tests"""
        with patch('grc_ai_toolkit.ui.layouts.st') as mock_st:
            # Create column mocks
            mock_cols = []
            for _ in range(3):
                mock_col = MagicMock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=False)
                mock_cols.append(mock_col)

            mock_st.columns = Mock(return_value=mock_cols)
            mock_st.progress = Mock()
            mock_st.markdown = Mock()
            mock_st.divider = Mock()

            yield mock_st

    def test_wizard_layout_first_step(self, mock_streamlit):
        """Test wizard layout on first step"""
        steps = ["Step 1", "Step 2", "Step 3"]
        content_called = False

        def step_content():
            nonlocal content_called
            content_called = True

        layouts.wizard_layout(steps, current_step=0, step_content=step_content)

        assert content_called
        mock_streamlit.progress.assert_called_once_with(1/3)

    def test_wizard_layout_middle_step(self, mock_streamlit):
        """Test wizard layout on middle step"""
        steps = ["Step 1", "Step 2", "Step 3"]

        layouts.wizard_layout(steps, current_step=1, step_content=lambda: None)

        mock_streamlit.progress.assert_called_once_with(2/3)

    def test_wizard_layout_last_step(self, mock_streamlit):
        """Test wizard layout on last step"""
        steps = ["Step 1", "Step 2", "Step 3"]

        layouts.wizard_layout(steps, current_step=2, step_content=lambda: None)

        mock_streamlit.progress.assert_called_once_with(1.0)


class TestFormLayout:
    """Test form_layout function"""

    @pytest.fixture(autouse=True)
    def mock_streamlit(self):
        """Mock streamlit module for all tests"""
        with patch('grc_ai_toolkit.ui.layouts.st') as mock_st:
            # Create form context manager mock
            mock_form = MagicMock()
            mock_form.__enter__ = Mock(return_value=mock_form)
            mock_form.__exit__ = Mock(return_value=False)
            mock_st.form = Mock(return_value=mock_form)

            mock_st.subheader = Mock()
            mock_st.text_input = Mock(return_value="test")
            mock_st.text_area = Mock(return_value="test")
            mock_st.number_input = Mock(return_value=42)
            mock_st.selectbox = Mock(return_value="option1")
            mock_st.multiselect = Mock(return_value=["option1"])
            mock_st.checkbox = Mock(return_value=True)
            mock_st.date_input = Mock(return_value="2025-01-01")
            mock_st.slider = Mock(return_value=50)
            mock_st.form_submit_button = Mock(return_value=False)
            mock_st.error = Mock()

            yield mock_st

    def test_form_layout_text_field(self, mock_streamlit):
        """Test form with text field"""
        fields = {
            "name": {"type": "text", "label": "Name", "default": "John"}
        }

        layouts.form_layout("Test Form", fields)

        mock_streamlit.text_input.assert_called_once()

    def test_form_layout_textarea_field(self, mock_streamlit):
        """Test form with textarea field"""
        fields = {
            "description": {"type": "textarea", "label": "Description"}
        }

        layouts.form_layout("Test Form", fields)

        mock_streamlit.text_area.assert_called_once()

    def test_form_layout_number_field(self, mock_streamlit):
        """Test form with number field"""
        fields = {
            "age": {"type": "number", "label": "Age", "min": 0, "max": 120}
        }

        layouts.form_layout("Test Form", fields)

        mock_streamlit.number_input.assert_called_once()

    def test_form_layout_select_field(self, mock_streamlit):
        """Test form with select field"""
        fields = {
            "country": {"type": "select", "label": "Country", "options": ["US", "UK"]}
        }

        layouts.form_layout("Test Form", fields)

        mock_streamlit.selectbox.assert_called_once()

    def test_form_layout_multiselect_field(self, mock_streamlit):
        """Test form with multiselect field"""
        fields = {
            "tags": {"type": "multiselect", "label": "Tags", "options": ["A", "B", "C"]}
        }

        layouts.form_layout("Test Form", fields)

        mock_streamlit.multiselect.assert_called_once()

    def test_form_layout_checkbox_field(self, mock_streamlit):
        """Test form with checkbox field"""
        fields = {
            "agree": {"type": "checkbox", "label": "I agree"}
        }

        layouts.form_layout("Test Form", fields)

        mock_streamlit.checkbox.assert_called_once()

    def test_form_layout_date_field(self, mock_streamlit):
        """Test form with date field"""
        fields = {
            "birthday": {"type": "date", "label": "Birthday"}
        }

        layouts.form_layout("Test Form", fields)

        mock_streamlit.date_input.assert_called_once()

    def test_form_layout_slider_field(self, mock_streamlit):
        """Test form with slider field"""
        fields = {
            "priority": {"type": "slider", "label": "Priority", "min": 1, "max": 10}
        }

        layouts.form_layout("Test Form", fields)

        mock_streamlit.slider.assert_called_once()

    def test_form_layout_submit_returns_data(self, mock_streamlit):
        """Test form submission returns data"""
        mock_streamlit.form_submit_button.return_value = True
        mock_streamlit.text_input.return_value = "Test Name"

        fields = {
            "name": {"type": "text", "label": "Name"}
        }

        result = layouts.form_layout("Test Form", fields)

        assert result is not None
        assert "name" in result

    def test_form_layout_required_validation(self, mock_streamlit):
        """Test form required field validation"""
        mock_streamlit.form_submit_button.return_value = True
        mock_streamlit.text_input.return_value = ""  # Empty required field

        fields = {
            "name": {"type": "text", "label": "Name", "required": True}
        }

        result = layouts.form_layout("Test Form", fields)

        assert result is None
        mock_streamlit.error.assert_called_once()

    def test_form_layout_callback(self, mock_streamlit):
        """Test form with callback function"""
        mock_streamlit.form_submit_button.return_value = True
        callback_called = False
        callback_data = None

        def on_submit(data):
            nonlocal callback_called, callback_data
            callback_called = True
            callback_data = data

        fields = {
            "name": {"type": "text", "label": "Name"}
        }

        layouts.form_layout("Test Form", fields, on_submit=on_submit)

        assert callback_called
        assert callback_data is not None


class TestResultsDisplayLayout:
    """Test results_display_layout function"""

    @pytest.fixture(autouse=True)
    def mock_streamlit(self):
        """Mock streamlit module for all tests"""
        with patch('grc_ai_toolkit.ui.layouts.st') as mock_st:
            # Create column mocks
            mock_cols = []
            for _ in range(3):
                mock_col = MagicMock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=False)
                mock_cols.append(mock_col)

            mock_st.columns = Mock(return_value=mock_cols)
            mock_st.subheader = Mock()
            mock_st.markdown = Mock()
            mock_st.divider = Mock()
            mock_st.download_button = Mock()
            mock_st.button = Mock(return_value=False)

            yield mock_st

    def test_results_display_basic(self, mock_streamlit):
        """Test basic results display"""
        layouts.results_display_layout("Test result content")

        mock_streamlit.subheader.assert_called_once_with("Results")
        mock_streamlit.markdown.assert_called_once_with("Test result content")

    def test_results_display_custom_title(self, mock_streamlit):
        """Test results display with custom title"""
        layouts.results_display_layout("Test content", title="Custom Results")

        mock_streamlit.subheader.assert_called_once_with("Custom Results")

    def test_results_display_with_download(self, mock_streamlit):
        """Test results display with download button"""
        layouts.results_display_layout("Test content", show_download=True)

        mock_streamlit.download_button.assert_called_once()

    def test_results_display_without_download(self, mock_streamlit):
        """Test results display without download button"""
        layouts.results_display_layout("Test content", show_download=False)

        mock_streamlit.download_button.assert_not_called()

    def test_results_display_with_actions(self, mock_streamlit):
        """Test results display with action buttons"""
        action_called = False

        def test_action(result):
            nonlocal action_called
            action_called = True

        actions = {"Copy": test_action, "Share": lambda r: None}

        layouts.results_display_layout("Test content", actions=actions)

        # Verify buttons were created
        assert mock_streamlit.button.call_count == 2

    def test_results_display_custom_filename(self, mock_streamlit):
        """Test results display with custom download filename"""
        layouts.results_display_layout(
            "Test content",
            download_filename="custom_result.txt"
        )

        # Check download button was called with custom filename
        call_args = mock_streamlit.download_button.call_args
        assert call_args.kwargs["file_name"] == "custom_result.txt"
