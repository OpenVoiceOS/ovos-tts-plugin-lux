# ovos-tts-plugin-lux Quick Facts

**Package Name:** ovos-tts-plugin-lux
**Version:** 0.1.0
**License:** Apache-2.0
**Author:** OpenVoiceOS
**Description:** LuxTTS plugin for OpenVoiceOS

## Key Classes
- `LuxTTS` - Main TTS plugin class
- `LuxTTSValidator` - Validator for LuxTTS plugin

## Dependencies
- ovos-plugin-manager>=0.0.1
- zipvoice>=0.0.11
- soundfile

## Configuration Options
- `model_path`: HuggingFace model path (default: "YatharthS/LuxTTS")
- `device`: Device to use (default: "cuda")
- `threads`: Number of threads for CPU (default: 4)
- `prompt_audio`: Path to reference audio file (required)
- `rms`: Volume control (default: 0.01)
- `num_steps`: Sampling steps (default: 4)
- `t_shift`: Sampling parameter (default: 0.9)
- `speed`: Speed control (default: 1.0)
- `return_smooth`: Smooth output (default: False)
- `ref_duration`: Reference duration (default: 5)

## Supported Languages
- en-US (English - United States)
