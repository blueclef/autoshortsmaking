import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.services.generator_image import generate_image
from app.services.generator_tts import synthesize_tts

class TestApiGenerators(unittest.TestCase):

    @patch('app.services.generator_image.requests.post')
    @patch('app.services.generator_image.GEMINI_API_KEY', 'fake-api-key')
    def test_generate_image_success(self, mock_post):
        """Tests successful image generation with a mocked API key."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        with patch('builtins.open', mock_open()):
            generate_image("a test prompt", "fake_path/test.png")
            mock_post.assert_called_once()

    @patch('app.services.generator_tts.requests.post')
    @patch('app.services.generator_tts.GEMINI_API_KEY', 'fake-api-key')
    def test_synthesize_tts_success(self, mock_post):
        """Tests successful TTS generation with a mocked API key."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b'fake_audio_content'
        mock_post.return_value = mock_response

        with patch('builtins.open', mock_open()) as mocked_file:
            synthesize_tts("hello world", "fake_path/test.mp3")
            mock_post.assert_called_once()
            mocked_file.assert_called_with('fake_path/test.mp3', 'wb')
            mocked_file().write.assert_called_once_with(b'fake_audio_content')

    @patch('app.services.generator_image.create_placeholder_image')
    @patch('app.services.generator_image.requests.post')
    @patch('app.services.generator_image.GEMINI_API_KEY', 'fake-api-key')
    def test_generate_image_api_failure(self, mock_post, mock_placeholder):
        """Tests the fallback mechanism when the image API call fails."""
        mock_post.side_effect = requests.exceptions.RequestException("API is down")
        generate_image("a test prompt", "fake_path/test.png")
        mock_post.assert_called_once()
        mock_placeholder.assert_called_once_with("a test prompt", "fake_path/test.png")

    @patch('app.services.generator_image.create_placeholder_image')
    @patch('app.services.generator_image.GEMINI_API_KEY', None)
    def test_generate_image_no_api_key(self, mock_placeholder):
        """Tests the fallback mechanism when the API key is not set."""
        generate_image("a test prompt", "fake_path/test.png")
        mock_placeholder.assert_called_once_with("a test prompt", "fake_path/test.png")

if __name__ == '__main__':
    unittest.main()