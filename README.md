# ovos-tts-plugin-lux

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Vibe Coded](https://img.shields.io/badge/Vibe%20Coded-100%25-brightgreen.svg)](https://mistral.ai)

A LuxTTS plugin for the OpenVoiceOS voice assistant platform. LuxTTS is a
[ZipVoice](https://github.com/k2-fsa/ZipVoice)-based text-to-speech model that
clones a voice from a short reference audio clip and generates speech at more
than 150x realtime on a GPU. It needs less than 1 GB of VRAM and also runs on
CPU or Apple Silicon (MPS).

See [CREDITS.md](CREDITS.md) for the model's authorship and generation history.

## Installation

```bash
pip install ovos-tts-plugin-lux
```

## Configuration

The plugin needs a reference audio file for voice cloning. Add this to
`mycroft.conf`:

```yaml
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

## Usage

The plugin clones the voice in the reference audio and generates speech from
it. Use a reference clip of at least 3 seconds for the best results.

## Docker

Run the plugin behind [`ovos-tts-server`](https://github.com/OpenVoiceOS/ovos-tts-server),
which exposes an ElevenLabs-compatible HTTP API on port `9666`. CI builds and
publishes an image to `ghcr.io/openvoiceos/ovos-tts-plugin-lux`.

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

- **Heavy image.** LuxTTS pulls torch/torchaudio (CPU wheels) and the LuxTTS
  fork's LinaCodec/piper-phonemize prerequisites, so the build is large.
- **First-run model download.** The 491 MB `YatharthS/LuxTTS` model downloads
  on first synthesis into `~/.cache`. Mount a named volume, as the compose
  file does, so the download happens only once. Give the container time to
  start.
- **Zero-shot voice cloning.** LuxTTS clones the voice in a reference prompt.
  The image ships with `test/jfk.wav` as the default `prompt_audio`, so it
  works out of the box. Mount your own `mycroft.conf` (and prompt file) to
  clone a different voice. The engine runs on CPU in the container
  (`device: cpu`).

## Supported Languages

- `en-US` - English (United States)

## Requirements

- A reference audio file (WAV or MP3 format)
- At least 3 seconds of reference audio for the best voice cloning
- A GPU (CUDA or MPS) for the best performance

## Tips

- Use at least a 3 second audio file for voice cloning.
- Set `return_smooth = True` if you hear metallic sounds.
- Lower `t_shift` for fewer pronunciation errors, at the cost of quality.
- Lower `ref_duration` to speed up inference.

## Related Projects

- [LuxTTS](https://github.com/ysharma3501/LuxTTS) - the underlying voice cloning model
- [ZipVoice](https://github.com/k2-fsa/ZipVoice) - the TTS architecture LuxTTS builds on
- [OpenVoiceOS/ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager) - the plugin interface this package implements
- [OpenVoiceOS/ovos-tts-server](https://github.com/OpenVoiceOS/ovos-tts-server) - serves this plugin over HTTP

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

## Credits

Developed by [TigreGótico](https://tigregotico.pt) for
[OpenVoiceOS](https://openvoiceos.org).

[![NGI0 Commons Fund](./ngi.png)](https://nlnet.nl/project/OpenVoiceOS)

This project was funded through the [NGI0 Commons Fund](https://nlnet.nl/commonsfund),
a fund established by [NLnet](https://nlnet.nl) with financial support from the
European Commission's [Next Generation Internet](https://ngi.eu) programme, under
the aegis of [DG Communications Networks, Content and Technology](https://commission.europa.eu/about-european-commission/departments-and-executive-agencies/communications-networks-content-and-technology_en)
under grant agreement No [101135429](https://cordis.europa.eu/project/id/101135429).
