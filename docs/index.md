# ovos-tts-plugin-lux

A LuxTTS plugin for the OpenVoiceOS voice assistant platform.

## Overview

This plugin integrates LuxTTS, a ZipVoice-based text-to-speech model that
clones a voice and generates speech at more than 150x realtime on a GPU.

## Features

- Voice cloning
- 48kHz speech generation
- High-speed inference (150x realtime on GPU, faster than realtime on CPU)
- Low VRAM requirements (<1GB)

## Installation

```bash
pip install ovos-tts-plugin-lux
```

## Configuration

The plugin needs a reference audio file for voice cloning:

```yaml
# mycroft.conf or configuration
{
  "tts": {
    "module": "ovos-tts-plugin-lux",
    "ovos-tts-plugin-lux": {
      "prompt_audio": "/path/to/reference.wav",
      "device": "cuda",  # or "cpu" or "mps"
      "model_path": "YatharthS/LuxTTS",
      "rms": 0.01,
      "num_steps": 4,
      "t_shift": 0.9,
      "speed": 1.0,
      "return_smooth": false,
      "ref_duration": 5
    }
  }
}
```

## Usage

The plugin uses the reference audio file to clone the voice and generate
speech. Use a reference clip of at least 3 seconds for the best results.

## Supported Languages

- `en-US` - English (United States)

## Requirements

- A reference audio file (WAV or MP3 format)
- At least 3 seconds of reference audio for the best voice cloning
- A GPU (CUDA or MPS) for the best performance

## Technical Details

### Class Reference

#### `LuxTTS`

The main TTS plugin class. It implements the OVOS TTS interface.

**Inherits from:** `ovos_plugin_manager.templates.tts.TTS`

**Methods:**

- `__init__(self, *args, **kwargs)`: Initialize the plugin
- `_encode_prompt(self)`: Encode the reference audio prompt
- `get_tts(self, sentence, wav_file, lang=None, voice=None)`: Generate speech

**Attributes:**

- `model_path`: HuggingFace model path
- `device`: Device to use (cuda/cpu/mps)
- `threads`: Number of threads for CPU
- `prompt_audio`: Path to reference audio file
- `rms`: Volume control
- `num_steps`: Sampling steps
- `t_shift`: Sampling parameter
- `speed`: Speed control
- `return_smooth`: Smooth output flag
- `ref_duration`: Reference duration

#### `LuxTTSValidator`

The validator for the LuxTTS plugin.

**Inherits from:** `ovos_plugin_manager.templates.tts.TTSValidator`

**Methods:**

- `validate_lang(self)`: Validate language support
- `validate_dependencies(self)`: Validate dependencies
- `get_tts_class(self)`: Return TTS class

## Configuration Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_path` | str | "YatharthS/LuxTTS" | HuggingFace model path |
| `device` | str | "cuda" | Device to use (cuda/cpu/mps) |
| `threads` | int | 4 | Number of threads for CPU |
| `prompt_audio` | str | None | Path to reference audio file (required) |
| `rms` | float | 0.01 | Volume control (0.01 recommended) |
| `num_steps` | int | 4 | Sampling steps (3-4 recommended) |
| `t_shift` | float | 0.9 | Sampling parameter (higher can sound better but worse WER) |
| `speed` | float | 1.0 | Speed control (lower=slower) |
| `return_smooth` | bool | False | Makes output smoother but less clean |
| `ref_duration` | int | 5 | Reference duration in seconds |

## Tips

- Use at least a 3 second audio file for voice cloning.
- Set `return_smooth = True` if you hear metallic sounds.
- Lower `t_shift` for fewer pronunciation errors, at the cost of quality.
- Lower `ref_duration` to speed up inference.

## See Also

- [LuxTTS GitHub](https://github.com/ysharma3501/LuxTTS)
- [ZipVoice](https://github.com/k2-fsa/ZipVoice)
- [OVOS Plugin Manager](https://github.com/OpenVoiceOS/ovos-plugin-manager)
