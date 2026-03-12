#!/usr/bin/env python3
"""Verify the LuxTTS plugin works correctly."""

import os
import tempfile
from ovos_tts_plugin_lux import LuxTTS

# Use the jfk.wav file as reference
prompt_audio = os.path.join(os.path.dirname(__file__), "test", "jfk.wav")

if not os.path.exists(prompt_audio):
    print(f"Error: Reference audio file not found at {prompt_audio}")
    exit(1)

print(f"Using reference audio: {prompt_audio}")
print("Loading LuxTTS model (this may take a moment)...")

# Create TTS instance with CPU
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
    print("✓ Model loaded successfully!")
    
    # Create a temporary output file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        output_file = f.name
    
    print(f"\nSynthesizing speech to: {output_file}")
    print("Text: 'Hello, this is a test of the LuxTTS plugin'")
    
    # Synthesize speech - this should create the file
    result = tts.get_tts(
        "Hello, this is a test of the LuxTTS plugin",
        output_file
    )
    
    # Verify the result
    if result[0] == output_file:
        print("✓ get_tts returned correct file path")
    
    if os.path.exists(output_file):
        print(f"✓ Output file created successfully")
        print(f"  File size: {os.path.getsize(output_file) / 1024:.2f} KB")
        
        # Verify it's a valid WAV file
        import soundfile as sf
        data, sample_rate = sf.read(output_file)
        print(f"✓ Valid WAV file with sample rate: {sample_rate} Hz")
        print(f"  Audio duration: {len(data) / sample_rate:.2f} seconds")
        
        print(f"\n✓ Plugin verification complete!")
        print(f"\nYou can play the file with:")
        print(f"  ffplay {output_file}")
        print(f"\nOr listen to it with:")
        print(f"  aplay {output_file}")
    else:
        print("✗ Output file was not created")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Clean up
    if 'output_file' in locals() and os.path.exists(output_file):
        try:
            os.unlink(output_file)
        except:
            pass
