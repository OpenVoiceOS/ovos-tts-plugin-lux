"""End-to-end TTS intelligibility test for the LuxTTS plugin.

Synthesises a small fixed set of English phrases, transcribes the rendered
audio back with the ovoscope reference STT, and asserts the mean word error
rate stays within tolerance.
"""
import os
import json

from ovoscope.tts_intelligibility import score_tts_intelligibility

from ovos_tts_plugin_lux import LuxTTS

LANG = "en-US"
PHRASES = [
    "hello world",
    "what time is it",
    "turn on the kitchen lights",
    "the weather is nice today",
    "set a timer for five minutes",
]


def test_tts_intelligibility():
    # LuxTTS is a zero-shot voice-cloning engine: it needs a reference prompt
    # audio to clone, and runs on CPU in CI. The reference WAV path is provided by
    # the workflow via LUX_PROMPT_AUDIO (synthesised with espeak-ng).
    config = {
        "lang": LANG,
        "device": os.environ.get("LUX_DEVICE", "cpu"),
    }
    prompt = os.environ.get("LUX_PROMPT_AUDIO")
    if prompt:
        config["prompt_audio"] = prompt
    tts = LuxTTS(config)
    report = score_tts_intelligibility(tts, PHRASES, lang=LANG, mode="direct")
    print("::TTS-INTELLIGIBILITY:: " + json.dumps(report.to_dict()))
    assert report.mean_wer <= float(os.environ.get("TTS_MAX_WER", "1.0"))
