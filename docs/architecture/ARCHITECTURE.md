# LuxTTS Plugin Architecture

## Overview

This document explains the architecture of the OVOS TTS plugin for LuxTTS, including how it integrates with OpenVoiceOS and the underlying LuxTTS model.

## Plugin Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                    OVOS TTS Plugin for LuxTTS                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │  LuxTTS      │    │  Validator  │    │  Configuration   │  │
│  │  Implementation│    │  Logic      │    │  Management      │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
│        │                  │                  │               │
│        ▼                  ▼                  ▼               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                 OVOS TTS Interface                     │  │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │  │
│  │  │ get_tts()   │    │ validate()  │    │  config     │  │  │
│  │  └─────────────┘    └─────────────┘    └─────────────┘  │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. LuxTTS Class

The main plugin class that implements the OVOS TTS interface.

```python
class LuxTTS(TTS):
    """Main TTS plugin implementing OVOS interface"""
```

**Key Responsibilities:**
- Initialize LuxTTS model with configuration
- Load and encode reference audio
- Generate speech from text
- Handle audio file creation and management

**Main Methods:**

#### `__init__(self, *args, **kwargs)`
Initializes the plugin and loads the LuxTTS model.

**Parameters:**
- `config`: Dictionary containing plugin configuration
  - `prompt_audio`: Path to reference audio file (required)
  - `device`: Device to use (cuda/cpu/mps)
  - `model_path`: HuggingFace model path
  - `threads`: Number of CPU threads
  - `num_steps`: Sampling steps
  - `t_shift`: Sampling parameter
  - `speed`: Speed control
  - `return_smooth`: Smooth output flag
  - `ref_duration`: Reference duration
  - `rms`: Volume control

**Process:**
1. Call parent `TTS.__init__()` with audio_ext="wav" and validator
2. Store configuration parameters
3. Import and initialize LuxTTS model
4. Encode reference audio if provided

#### `get_tts(self, sentence, wav_file, lang=None, voice=None)`
Generates speech and saves it to a WAV file.

**Parameters:**
- `sentence`: Text to synthesize
- `wav_file`: Output file path
- `lang`: Language code (unused, for compatibility)
- `voice`: Voice identifier (unused, for compatibility)

**Returns:**
- `tuple`: `(wav_file, None)` where wav_file is the output path

**Process:**
1. Check if encoded prompt is available
2. Generate speech using LuxTTS
3. Convert audio to numpy array
4. Save as WAV file using soundfile
5. Return file path and None for phonemes

#### `_encode_prompt(self)`
Encodes the reference audio for voice cloning.

**Process:**
1. Check if prompt audio file exists
2. Call LuxTTS `encode_prompt()` method
3. Store encoded prompt for later use

### 2. LuxTTSValidator Class

Validates plugin configuration and dependencies.

```python
class LuxTTSValidator(TTSValidator):
    """Validates plugin configuration"""
```

**Key Responsibilities:**
- Validate language support
- Validate required dependencies
- Ensure proper plugin configuration

**Main Methods:**

#### `validate_lang(self)`
Validates that the requested language is supported.

**Process:**
1. Get list of supported languages from config
2. Check if requested language is in list
3. Raise assertion error if not supported

#### `validate_dependencies(self)`
Validates that required dependencies are installed.

**Process:**
1. Try to import LuxTTS from zipvoice
2. Raise ImportError if not available

#### `get_tts_class(self)`
Returns the TTS class.

**Returns:**
- `LuxTTS`: The main plugin class

## Configuration

### Configuration Structure

```yaml
{
  "tts": {
    "module": "ovos-tts-plugin-lux",
    "ovos-tts-plugin-lux": {
      "prompt_audio": "/path/to/reference.wav",
      "device": "cuda",
      "model_path": "YatharthS/LuxTTS",
      "threads": 4,
      "num_steps": 4,
      "t_shift": 0.9,
      "speed": 1.0,
      "return_smooth": false,
      "ref_duration": 5,
      "rms": 0.01
    }
  }
}
```

### Configuration Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt_audio` | str | Yes | None | Path to reference audio file for voice cloning |
| `device` | str | No | "cuda" | Device to use (cuda/cpu/mps) |
| `model_path` | str | No | "YatharthS/LuxTTS" | HuggingFace model path |
| `threads` | int | No | 4 | Number of CPU threads |
| `num_steps` | int | No | 4 | Sampling steps (3-4 recommended) |
| `t_shift` | float | No | 0.9 | Sampling parameter (higher = better quality, worse WER) |
| `speed` | float | No | 1.0 | Speed control (lower = slower) |
| `return_smooth` | bool | No | False | Makes output smoother but less clean |
| `ref_duration` | int | No | 5 | Reference duration in seconds |
| `rms` | float | No | 0.01 | Volume control (0.01 recommended) |

## LuxTTS Model Integration

### LuxTTS Overview

LuxTTS is a lightweight zipvoice-based text-to-speech model designed for:
- High-quality voice cloning
- 48kHz speech generation
- High-speed inference (150x realtime on GPU)
- Low VRAM requirements (<1GB)

### Integration Details

```python
from zipvoice.luxvoice import LuxTTS as LuxTTSModel

self.lux_tts = LuxTTSModel(
    model_path=self.model_path,
    device=self.device,
    threads=self.threads
)
```

### Key LuxTTS Methods Used

#### `encode_prompt(prompt_audio, duration=5, rms=0.001)`
Encodes reference audio for voice cloning.

**Parameters:**
- `prompt_audio`: Path to reference audio file
- `duration`: Duration to extract (seconds)
- `rms`: Target RMS level for volume control

**Returns:**
- `dict`: Dictionary containing encoded prompt data

#### `generate_speech(text, encode_dict, num_steps=4, guidance_scale=3.0, t_shift=0.5, speed=1.0, return_smooth=False)`
Generates speech using the encoded prompt.

**Parameters:**
- `text`: Text to synthesize
- `encode_dict`: Encoded prompt dictionary
- `num_steps`: Number of sampling steps
- `guidance_scale`: Guidance scale for diffusion
- `t_shift`: Sampling temperature parameter
- `speed`: Speed control
- `return_smooth`: Return smooth output

**Returns:**
- `torch.Tensor`: Generated audio waveform

## Audio Processing Pipeline

### Speech Synthesis Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Speech Synthesis Pipeline                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │  Text Input │───▶│  LuxTTS      │───▶│  Audio Waveform  │  │
│  │  (sentence) │    │  Model       │    │  (torch.Tensor)  │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
│        │                  │                  │               │
│        │                  ▼                  ▼               │
│        │            ┌─────────────┐    ┌─────────────┐      │
│        │            │  Prompt     │    │  NumPy       │      │
│        │            │  Encoding   │───▶│  Conversion  │      │
│        │            └─────────────┘    └─────────────┘      │
│        │                  │                  │               │
│        │                  ▼                  ▼               │
│        │            ┌─────────────┐    ┌─────────────┐      │
│        │            │  Reference  │    │  WAV File    │      │
│        │            │  Audio      │───▶│  Output      │      │
│        │            └─────────────┘    └─────────────┘      │
│        │                  │                  │               │
│        └──────────────────┘                  ▼               │
│                                      ┌─────────────┐        │
│                                      │  Return     │        │
│                                      │  (wav_file, │        │
│                                      │   None)     │        │
│                                      └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Process

1. **Input Text**: User provides text to synthesize
2. **Prompt Encoding**: Reference audio is encoded (done once during initialization)
3. **Speech Generation**: LuxTTS generates audio waveform using:
   - Text input
   - Encoded prompt
   - Sampling parameters (num_steps, t_shift, etc.)
4. **Tensor Conversion**: Convert torch tensor to numpy array
5. **Audio Save**: Save as 48kHz WAV file using soundfile
6. **Return Result**: Return file path and None for phonemes

## OVOS Integration

### Plugin Registration

The plugin registers with OVOS using entry points in `setup.py`:

```python
entry_points={'opm.tts': PLUGIN_ENTRY_POINT,
              'opm.tts.config': SAMPLE_CONFIGS}
```

Where:
- `PLUGIN_ENTRY_POINT = 'ovos-tts-plugin-lux = ovos_tts_plugin_lux:LuxTTS'`
- `SAMPLE_CONFIGS = 'ovos-tts-plugin-lux.config = ovos_tts_plugin_lux:LuxTTSPluginConfig'`

### OVOS TTS Interface

The plugin implements the standard OVOS TTS interface:

```python
class LuxTTS(TTS):
    """Inherits from ovos_plugin_manager.templates.tts.TTS"""
```

**Required Methods:**
- `__init__(self, *args, **kwargs)`: Initialize plugin
- `get_tts(self, sentence, wav_file, lang=None, voice=None)`: Generate speech
- `available_languages`: Class property returning supported languages

**Optional Methods:**
- Any additional helper methods

### Language Support

```python
@classproperty
def available_languages(cls) -> set:
    """Return languages supported by LuxTTS"""
    return set(LuxTTSPluginConfig.keys())
```

Current supported languages:
- `en-US`: English (United States)

## Error Handling

### Error Handling Strategy

The plugin implements robust error handling at multiple levels:

1. **Initialization Errors**:
   - Missing dependencies
   - Invalid configuration
   - Model loading failures

2. **Runtime Errors**:
   - Missing reference audio
   - Audio generation failures
   - File I/O errors

3. **Validation Errors**:
   - Unsupported languages
   - Invalid parameters

### Example Error Handling

```python
try:
    # Generate speech
    final_wav = self.lux_tts.generate_speech(...)
    
    # Convert to numpy and save
    if hasattr(final_wav, 'numpy'):
        final_wav = final_wav.numpy().squeeze()
    else:
        final_wav = final_wav.squeeze()
    sf.write(wav_file, final_wav, 48000)
    
    return wav_file, None
except Exception as e:
    LOG.error(f"Failed to generate speech: {e}")
    raise
```

## Performance Considerations

### Model Loading
- LuxTTS model is loaded during plugin initialization
- Model loading can take several seconds
- Model is kept in memory for subsequent syntheses

### Speech Generation
- Generation time depends on:
  - `num_steps`: Higher values = better quality, longer time
  - `device`: GPU (cuda) is much faster than CPU
  - Text length: Longer text = longer generation

### Memory Usage
- LuxTTS requires <1GB VRAM
- CPU mode requires more memory
- Audio files are ~300-400KB for typical sentences

## Best Practices

### Configuration
- Use GPU (cuda) for best performance
- Start with `num_steps=4` for good quality
- Use `t_shift=0.9` for balance of quality and accuracy
- Provide at least 3 seconds of reference audio

### Reference Audio
- Use high-quality WAV or MP3 files
- Minimum 3 seconds for good voice cloning
- 48kHz sample rate recommended
- Clear, clean audio without background noise

### Production Use
- Pre-load the model at startup
- Cache encoded prompts for reuse
- Monitor memory usage
- Handle errors gracefully

## Testing

### Test Strategy

The plugin includes comprehensive tests covering:

1. **Initialization**: Plugin loads correctly
2. **Prompt Encoding**: Reference audio encoded properly
3. **Speech Generation**: Audio files created correctly
4. **Validation**: Configuration validated
5. **Configuration**: Plugin config accessible

### Test Coverage

```python
class TestLuxTTSPlugin(unittest.TestCase):
    def test_init():
        """Test plugin initialization"""
    
    def test_encode_prompt():
        """Test prompt encoding"""
    
    def test_get_tts():
        """Test speech generation"""
    
    def test_validator():
        """Test validator functionality"""
    
    def test_config():
        """Test plugin configuration"""
```

All tests pass (5/5).

## Future Enhancements

### Potential Improvements

1. **Multiple Voices**: Support multiple reference voices
2. **Dynamic Voice Switching**: Change voices at runtime
3. **SSML Support**: Basic SSML tag parsing
4. **Batch Processing**: Generate multiple utterances at once
5. **Model Caching**: Cache models for faster loading
6. **Advanced Configuration**: More tuning parameters

### Architecture Extensions

```
┌─────────────────────────────────────────────────────────────┐
│                    Future Architecture                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │  Voice       │    │  SSML       │    │  Batch          │  │
│  │  Management  │    │  Parser     │    │  Processing     │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
│        │                  │                  │               │
│        ▼                  ▼                  ▼               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                 OVOS TTS Interface                     │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Conclusion

This architecture provides a solid foundation for voice cloning in OpenVoiceOS. The plugin:
- Integrates seamlessly with OVOS TTS interface
- Leverages LuxTTS for high-quality voice cloning
- Provides flexible configuration options
- Implements robust error handling
- Includes comprehensive testing

The design allows for future extensions while maintaining simplicity and reliability.
