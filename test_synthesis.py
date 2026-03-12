#!/usr/bin/env python3
"""Test script to synthesize speech using LuxTTS plugin."""

import os
import tempfile
from ovos_tts_plugin_lux import LuxTTS

# Use the jfk.wav file as reference
prompt_audio = os.path.join(os.path.dirname(__file__), "test", "jfk.wav")

if not os.path.exists(prompt_audio):
    print(f"Error: Reference audio file not found at {prompt_audio}")
    exit(1)

print(f"Using reference audio: {prompt_audio}")
print("Loading LuxTTS model...")

# Create TTS instance with CPU (faster for testing)
config = {
    "prompt_audio": prompt_audio,
    "device": "cpu",
    "threads": 4,
    "model_path": "YatharthS/LuxTTS",
    "num_steps": 3,  # Lower for faster testing
    "t_shift": 0.7,
    "rms": 0.01,
    "ref_duration": 3
}

try:
    tts = LuxTTS(config=config)
    print("Model loaded successfully!")
    
    # Create output file
    output_file = os.path.join(tempfile.gettempdir(), "lux_tts_output.wav")
    
    # Synthesize speech
    print("Synthesizing speech...")
    print("Text: 'Hello, this is a test of the LuxTTS plugin for OpenVoiceOS'")
    
    tts.get_tts(
        "Hello, this is a test of the LuxTTS plugin for OpenVoiceOS",
        output_file
    )
    
    print(f"\nSpeech synthesized successfully!")
    print(f"Output file: {output_file}")
    print(f"File size: {os.path.getsize(output_file) / 1024:.2f} KB")
    
    # Try to play the audio
    try:
        import simpleaudio as sa
        wave_obj = sa.WaveObject.from_wave_file(output_file)
        print("\nPlaying audio...")
        play_obj = wave_obj.play()
        play_obj.wait_done()
        print("Audio playback complete!")
    except ImportError:
        print("\nNote: simpleaudio not installed. Install it with:")
        print("  pip install simpleaudio")
        print(f"\nYou can play the file manually with:")
        print(f"  ffplay {output_file}")
    except Exception as e:
        print(f"\nCould not play audio automatically: {e}")
        print(f"You can play the file manually with:")
        print(f"  ffplay {output_file}")
        
except Exception as e:
    print(f"Error during synthesis: {e}")
    import traceback
    traceback.print_exc()
