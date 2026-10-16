"""Offline regression tests for PDF executable discovery and error handling."""

import unittest
from unittest.mock import mock_open, patch

import main


class PdfConfigurationTests(unittest.TestCase):
    def run_without_ai(self, configuration_error=None):
        with patch.object(main, 'ShouldUseAI', return_value=False), \
             patch('builtins.open', mock_open(read_data='{"name": "Test"}')), \
             patch.object(main, 'render_template', return_value='<p>Test</p>'), \
             patch.object(main.pdfkit, 'configuration',
                          side_effect=configuration_error) as configure, \
             patch.object(main, 'save_pdf') as save, \
             patch('builtins.print') as output:
            main.main()
        return configure, save, output

    def test_pdf_configuration_uses_path_discovery(self):
        configure, save, output = self.run_without_ai()
        configure.assert_called_once_with()
        save.assert_called_once_with(
            '<p>Test</p>', 'Nir-Tuttnauer-Resume.pdf',
            config=configure.return_value,
        )
        output.assert_called_once_with(
            'Resume has been successfully generated and saved to '
            'Nir-Tuttnauer-Resume.pdf'
        )

    def test_missing_executable_reports_error_without_saving(self):
        configure, save, output = self.run_without_ai(
            OSError('No wkhtmltopdf executable found')
        )
        configure.assert_called_once_with()
        save.assert_not_called()
        output.assert_called_once_with(
            'An error occurred: No wkhtmltopdf executable found'
        )


if __name__ == '__main__':
    unittest.main()
