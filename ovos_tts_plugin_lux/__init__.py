"""LuxTTS plugin for OpenVoiceOS."""

import logging
import os
import tempfile
from pathlib import Path

import soundfile as sf
from ovos_plugin_manager.templates.tts import TTS, TTSValidator
from ovos_utils import classproperty

LOG = logging.getLogger(__name__)


class LuxTTS(TTS):
    """LuxTTS plugin for OpenVoiceOS."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            audio_ext="wav",
            validator=LuxTTSValidator(self),
        )

        # Load LuxTTS model
        self.model_path = self.config.get("model_path", "YatharthS/LuxTTS")
        self.device = self.config.get("device", "cuda")
        self.threads = self.config.get("threads", 4)
        self.prompt_audio = self.config.get("prompt_audio")
        self.rms = self.config.get("rms", 0.01)
        self.num_steps = self.config.get("num_steps", 4)
        self.t_shift = self.config.get("t_shift", 0.9)
        self.speed = self.config.get("speed", 1.0)
        self.return_smooth = self.config.get("return_smooth", False)
        self.ref_duration = self.config.get("ref_duration", 5)

        try:
            from zipvoice.luxvoice import LuxTTS as LuxTTSModel
            self.lux_tts = LuxTTSModel(
                model_path=self.model_path,
                device=self.device,
                threads=self.threads
            )
            LOG.info(f"LuxTTS model loaded successfully on {self.device}")
        except ImportError as e:
            LOG.error(f"Failed to import LuxTTS: {e}")
            raise
        except Exception as e:
            LOG.error(f"Failed to load LuxTTS model: {e}")
            raise

        # Initialize prompt encoding if prompt_audio is provided
        self.encoded_prompt = None
        if self.prompt_audio:
            self._encode_prompt()

    def _encode_prompt(self):
        """Encode the reference audio prompt."""
        if not self.prompt_audio or not os.path.exists(self.prompt_audio):
            LOG.warning(f"Prompt audio file not found: {self.prompt_audio}")
            return

        try:
            self.encoded_prompt = self.lux_tts.encode_prompt(
                self.prompt_audio,
                duration=self.ref_duration,
                rms=self.rms
            )
            LOG.info("Prompt audio encoded successfully")
        except Exception as e:
            LOG.error(f"Failed to encode prompt audio: {e}")
            raise

    def get_tts(self, sentence, wav_file, lang=None, voice=None):
        """Generate speech using LuxTTS.

        Args:
            sentence: Text to synthesize
            wav_file: Output file path
            lang: Language code (unused, for compatibility)
            voice: Voice identifier (unused, for compatibility)

        Returns:
            tuple: (wav_file, phonemes) where phonemes is None
        """
        if not self.encoded_prompt:
            LOG.error("No encoded prompt available. Please provide a prompt_audio in config.")
            raise ValueError("No encoded prompt available")

        try:
            # Generate speech
            final_wav = self.lux_tts.generate_speech(
                text=sentence,
                encode_dict=self.encoded_prompt,
                num_steps=self.num_steps,
                t_shift=self.t_shift,
                speed=self.speed,
                return_smooth=self.return_smooth
            )

            # Convert to numpy and save
            # final_wav might already be a numpy array or a torch tensor
            if hasattr(final_wav, 'numpy'):
                final_wav = final_wav.numpy().squeeze()
            else:
                final_wav = final_wav.squeeze()
            sf.write(wav_file, final_wav, 48000)

            return wav_file, None
        except Exception as e:
            LOG.error(f"Failed to generate speech: {e}")
            raise

    @classproperty
    def available_languages(cls) -> set:
        """Return languages supported by LuxTTS.

        Returns:
            set: supported languages
        """
        return set(LuxTTSPluginConfig.keys())


class LuxTTSValidator(TTSValidator):
    """Validator for LuxTTS plugin."""

    def __init__(self, tts):
        super().__init__(tts)

    def validate_lang(self):
        """Validate that the language is supported."""
        langs = [l.lower() for l in LuxTTSPluginConfig.keys()]
        assert self.tts.lang.lower() in langs

    def validate_dependencies(self):
        """Validate that required dependencies are installed."""
        try:
            from zipvoice.luxvoice import LuxTTS
        except ImportError as exc:
            raise ImportError(
                "LuxTTS dependencies not installed, please run pip install zipvoice"
            ) from exc

    def get_tts_class(self):
        """Return the TTS class."""
        return LuxTTS


# Configuration for supported languages and voices
LuxTTSPluginConfig = {
    "en-US": [
        {
            "voice": "default",
            "lang": "en-US",
            "meta": {
                "display_name": "Default",
                "offline": False,
                "gender": "unknown",
                "priority": 40,
            },
        }
    ],
}
