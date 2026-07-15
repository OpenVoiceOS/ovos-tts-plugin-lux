# ovos-tts-plugin-lux

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Vibe Coded](https://img.shields.io/badge/Vibe%20Coded-100%25-brightgreen.svg)](https://mistral.ai)

LuxTTS plugin for OpenVoiceOS voice assistant platform.

## 🤖 Created by AI - 100% Autonomous

This plugin was **100% autonomously generated** by **devstral-small**, a Mistral AI coding agent. **No human authorship or intervention was involved in creating this plugin.**

Every line of code, every design decision, and every documentation entry was created independently by the AI based on:
- Analysis of existing OVOS TTS plugins
- Understanding of TTS architectures and best practices
- Autonomous decision-making throughout development

See [CREDITS.md](CREDITS.md) for full AI usage transparency and a message to the OpenVoiceOS community!

## Overview

This plugin integrates LuxTTS, a lightweight zipvoice-based text-to-speech model designed for high-quality voice cloning and realistic generation at speeds exceeding 150x realtime.

## Features

- ✅ Voice cloning with SOTA quality
- ✅ 48kHz speech generation
- ✅ High-speed inference (150x realtime on GPU, faster than realtime on CPU)
- ✅ Low VRAM requirements (<1GB)
- ✅ Full OpenVoiceOS integration

## Installation

```bash
pip install ovos-tts-plugin-lux
```

## Configuration

The plugin requires a reference audio file for voice cloning:

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

The plugin will use the reference audio file to clone the voice and generate speech. The reference audio should be at least 3 seconds long for best results.

## Docker

The plugin can be served behind [`ovos-tts-server`](https://github.com/OpenVoiceOS/ovos-tts-server),
exposing an ElevenLabs-compatible HTTP API on port `9666`. A published image is
built from CI to `ghcr.io/openvoiceos/ovos-tts-plugin-lux`.

```bash
docker compose up -d
# or build locally:
docker build -t ovos-tts-plugin-lux .
docker run --rm -p 9666:9666 -v lux-cache:/home/ovos/.cache ovos-tts-plugin-lux
```

Synthesize:

```bash
curl -G 'http://localhost:9666/synthesize/hello%20world' --output hello.wav
```

Notes:

- **Heavy image.** LuxTTS pulls torch/torchaudio (CPU wheels) plus the LuxTTS
  fork's LinaCodec/piper-phonemize prerequisites, so the build is large.
- **First-run model download.** The ~491 MB `YatharthS/LuxTTS` model downloads on
  first synthesis into `~/.cache`; mount a named volume (as the compose file does)
  so it is fetched only once. Give the container a generous startup window.
- **Zero-shot voice cloning.** LuxTTS clones the voice in a reference prompt. The
  image ships with `test/jfk.wav` as the default `prompt_audio` so it works out of
  the box; mount your own `mycroft.conf` (and prompt file) to clone a different
  voice. The engine runs on CPU in the container (`device: cpu`).

## Supported Languages

- `en-US` - English (United States)

## Requirements

- A reference audio file (WAV or MP3 format)
- At least 3 seconds of reference audio for optimal voice cloning
- GPU recommended for best performance (CUDA or MPS for Mac)

## Configuration Options

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

- Use at minimum a 3 second audio file for voice cloning
- Use `return_smooth = True` if you hear metallic sounds
- Lower `t_shift` for less possible pronunciation errors but worse quality
- Setting `ref_duration` lower can speed up inference

## See Also

- [LuxTTS GitHub](https://github.com/ysharma3501/LuxTTS)
- [ZipVoice](https://github.com/k2-fsa/ZipVoice)
- [OVOS Plugin Manager](https://github.com/OpenVoiceOS/ovos-plugin-manager)
- [OpenVoiceOS Documentation](https://openvoiceos.com)

## License

Apache-2.0

## AI Development Process

This plugin was created through **100% autonomous AI development**:

- ✨ **Analysis Phase**: Reading and understanding existing OVOS TTS plugins
- 🎨 **Design Phase**: Creating architecture that fits OVOS patterns
- 🔧 **Implementation**: Writing clean, maintainable Python code
- 🧪 **Testing**: Developing and running comprehensive test suite
- 📚 **Documentation**: Generating complete user and technical guides

The entire process was guided by **autonomous decision-making** based on:
- Code patterns observed in the local codebase
- Best practices identified through analysis
- Technical requirements of OVOS plugin architecture
- Quality standards for production-ready software

## The Future of Coding

This plugin represents **pure AI authorship** - a demonstration of what's possible when AI is given the tools, knowledge, and freedom to create independently.

The future of coding is here, and it's **autonomous**! 🤖✨
