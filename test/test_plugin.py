"""Test cases for ovos-tts-plugin-lux."""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch


class TestLuxTTSPlugin(unittest.TestCase):
    """Test cases for LuxTTS plugin."""

    def tearDown(self):
        """Clean up test fixtures."""
        pass

    def setUp(self):
        """Set up test fixtures."""
        import os
        
        # Use the jfk.wav file from the test directory
        self.test_audio_file = os.path.join(os.path.dirname(__file__), "jfk.wav")
        
        self.config = {
            "prompt_audio": self.test_audio_file,
            "device": "cpu",
            "model_path": "YatharthS/LuxTTS",
        }

    @patch('ovos_tts_plugin_lux.LuxTTS._encode_prompt')
    @patch('zipvoice.luxvoice.LuxTTS')
    def test_init(self, mock_lux_tts, mock_encode_prompt):
        """Test plugin initialization."""
        from ovos_tts_plugin_lux import LuxTTS

        mock_lux_tts_instance = MagicMock()
        mock_lux_tts.return_value = mock_lux_tts_instance

        tts = LuxTTS(config=self.config)

        self.assertEqual(tts.model_path, "YatharthS/LuxTTS")
        self.assertEqual(tts.device, "cpu")
        self.assertTrue(tts.prompt_audio.endswith("jfk.wav"))
        self.assertIsNotNone(tts.lux_tts)

    @patch('zipvoice.luxvoice.LuxTTS')
    def test_encode_prompt(self, mock_lux_tts):
        """Test prompt encoding."""
        from ovos_tts_plugin_lux import LuxTTS

        mock_lux_tts_instance = MagicMock()
        mock_lux_tts.return_value = mock_lux_tts_instance
        mock_lux_tts_instance.encode_prompt.return_value = {"test": "encoded"}

        # Create TTS without calling _encode_prompt
        tts = LuxTTS(config={**self.config, "prompt_audio": None})
        tts.prompt_audio = self.test_audio_file
        
        # Call _encode_prompt directly to test it
        tts._encode_prompt()

        # The mock should have been called
        mock_lux_tts_instance.encode_prompt.assert_called_once()
        self.assertIsNotNone(tts.encoded_prompt)

    @patch('ovos_tts_plugin_lux.LuxTTS._encode_prompt')
    @patch('zipvoice.luxvoice.LuxTTS')
    def test_get_tts(self, mock_lux_tts, mock_encode_prompt):
        """Test speech generation."""
        from ovos_tts_plugin_lux import LuxTTS
        import numpy as np

        mock_lux_tts_instance = MagicMock()
        mock_lux_tts.return_value = mock_lux_tts_instance
        mock_encode_prompt.return_value = {"test": "encoded"}

        # Create a mock audio output
        mock_audio = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        mock_lux_tts_instance.generate_speech.return_value = mock_audio

        tts = LuxTTS(config=self.config)
        tts.encoded_prompt = {"test": "encoded"}

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wav_file = f.name

        try:
            result = tts.get_tts("Hello world", wav_file)
            self.assertEqual(result[0], wav_file)
            self.assertIsNone(result[1])
            self.assertTrue(os.path.exists(wav_file))
        finally:
            if os.path.exists(wav_file):
                os.unlink(wav_file)

    def test_validator(self):
        """Test validator."""
        from ovos_tts_plugin_lux import LuxTTSValidator

        validator = LuxTTSValidator(None)
        self.assertIsNotNone(validator)

    def test_config(self):
        """Test plugin configuration."""
        from ovos_tts_plugin_lux import LuxTTSPluginConfig

        self.assertIn("en-US", LuxTTSPluginConfig)
        self.assertEqual(len(LuxTTSPluginConfig["en-US"]), 1)


if __name__ == "__main__":
    unittest.main()
