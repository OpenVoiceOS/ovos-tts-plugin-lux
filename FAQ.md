# FAQ - ovos-tts-plugin-lux

## General Questions

### What is LuxTTS?
LuxTTS is a lightweight zipvoice-based text-to-speech model designed for high-quality voice cloning and realistic generation at speeds exceeding 150x realtime.

### What makes LuxTTS different from other TTS models?
- Voice cloning quality on par with models 10x larger
- 48kHz speech generation (unlike most TTS models limited to 24kHz)
- High speed (150x realtime on GPU, faster than realtime on CPU)
- Low VRAM requirements (<1GB)

### Do I need a GPU to use this plugin?
No, but it's highly recommended. LuxTTS can run on CPU, but performance will be significantly slower. MPS (Metal Performance Shaders) is also supported for Mac users.

## Installation

### How do I install the plugin?
```bash
pip install ovos-tts-plugin-lux
```

### What are the dependencies?
- ovos-plugin-manager>=0.0.1
- zipvoice>=0.0.11
- soundfile

### How do I configure the plugin?
You need to provide a reference audio file for voice cloning:

```yaml
{
  "tts": {
    "module": "ovos-tts-plugin-lux",
    "ovos-tts-plugin-lux": {
      "prompt_audio": "/path/to/reference.wav"
    }
  }
}
```

## Usage

### What format should the reference audio be?
The reference audio should be WAV or MP3 format, at least 3 seconds long for optimal voice cloning.

### How do I change the voice quality?
You can adjust several parameters:
- `num_steps`: Higher values (3-4) sound better but take longer
- `t_shift`: Higher values can sound better but may have worse WER
- `rms`: Controls volume (0.01 recommended)
- `speed`: Controls playback speed (1.0 = normal)
- `return_smooth`: Set to True if you hear metallic sounds

### Can I use multiple voices?
Currently, the plugin uses a single reference voice. You would need to create separate configurations with different reference audio files.

## Performance

### How fast is LuxTTS?
- 150x realtime on GPU
- Faster than realtime on CPU
- Float16 inference should be almost 2x faster than float32

### What are the hardware requirements?
- GPU with at least 1GB VRAM (recommended)
- CPU with multiple threads (4+ recommended)
- At least 3 seconds of reference audio

## Troubleshooting

### I get an error "No encoded prompt available"
This means you haven't provided a valid `prompt_audio` path in your configuration, or the file doesn't exist.

### The voice sounds robotic/metallic
Try setting `return_smooth = True` in your configuration.

### Speech has pronunciation errors
Try lowering the `t_shift` parameter (e.g., 0.7 instead of 0.9).

### Inference is too slow
- Make sure you're using a GPU (CUDA or MPS)
- Reduce `num_steps` to 3
- Reduce `ref_duration` if possible
- Try using float16 inference (not yet implemented in this plugin)

### I get CUDA errors
Make sure you have CUDA toolkit installed and your GPU is supported. You can switch to CPU by setting `device: "cpu"` in configuration.

## Advanced

### Can I use a custom model?
Yes, set `model_path` to your custom HuggingFace model path or local path.

### How do I use multiple threads on CPU?
Set `threads` to the number of threads you want to use (default is 4).

### Can I change the sample rate?
LuxTTS outputs at 48kHz. This is currently not configurable.

## Configuration Examples

### Basic configuration
```yaml
{
  "tts": {
    "module": "ovos-tts-plugin-lux",
    "ovos-tts-plugin-lux": {
      "prompt_audio": "/home/user/voice_reference.wav"
    }
  }
}
```

### GPU configuration with quality settings
```yaml
{
  "tts": {
    "module": "ovos-tts-plugin-lux",
    "ovos-tts-plugin-lux": {
      "prompt_audio": "/home/user/voice_reference.wav",
      "device": "cuda",
      "num_steps": 4,
      "t_shift": 0.9,
      "rms": 0.01,
      "return_smooth": false
    }
  }
}
```

### CPU configuration
```yaml
{
  "tts": {
    "module": "ovos-tts-plugin-lux",
    "ovos-tts-plugin-lux": {
      "prompt_audio": "/home/user/voice_reference.wav",
      "device": "cpu",
      "threads": 8,
      "num_steps": 3
    }
  }
}
```

### Mac MPS configuration
```yaml
{
  "tts": {
    "module": "ovos-tts-plugin-lux",
    "ovos-tts-plugin-lux": {
      "prompt_audio": "/home/user/voice_reference.wav",
      "device": "mps"
    }
  }
}
```

## See Also

- [LuxTTS GitHub Repository](https://github.com/ysharma3501/LuxTTS)
- [ZipVoice](https://github.com/k2-fsa/ZipVoice)
- [OVOS Documentation](https://openvoiceos.com)
