import unittest
from unittest.mock import patch, Mock

from app.services import llm_client


class TestLLMClient(unittest.TestCase):
    @patch('app.services.llm_client.requests.post')
    def test_generate_insights_via_hf_parses_generated_text(self, mock_post):
        mock_resp = Mock()
        mock_resp.raise_for_status.return_value = None
        # HF returns a list with generated_text key
        mock_resp.json.return_value = [{'generated_text': '[{"type":"info","icon":"lightbulb","title":"T","message":"M"}]'}]
        mock_post.return_value = mock_resp

        # Temporarily set a fake API key
        with patch.dict('os.environ', {'HF_API_KEY': 'fake-key'}):
            out = llm_client.generate_insights_via_hf({'total_sessions': 1})
            self.assertIsInstance(out, list)
            self.assertEqual(out[0]['type'], 'info')

    @patch('app.services.llm_client.requests.post')
    def test_generate_insights_parses_google_candidates(self, mock_post):
        mock_resp = Mock()
        mock_resp.raise_for_status.return_value = None
        # Google returns a dict with candidates -> first candidate has 'output'
        mock_resp.json.return_value = {'candidates': [{'output': '[{"type":"tip","icon":"lightbulb","title":"G","message":"N"}]'}]}
        mock_post.return_value = mock_resp

        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'fake-google-key'}):
            out = llm_client.generate_insights_via_hf({'total_sessions': 2})
            self.assertIsInstance(out, list)
            self.assertEqual(out[0]['type'], 'tip')


if __name__ == '__main__':
    unittest.main()
