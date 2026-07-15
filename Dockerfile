# LuxTTS (Luxembourgish zero-shot voice cloning, ZipVoice) served through
# ovos-tts-server's ElevenLabs-compatible API on port 9666. Any client that speaks
# the ovos-tts-server / ElevenLabs API can hit it, and it can be A/B-tested against
# other ovos-tts-server voices by pointing at a different port.
#
# Heavy image: the engine pulls torch/torchaudio (CPU wheels here) plus the LuxTTS
# fork's LinaCodec/piper-phonemize prerequisites. The ~491 MB YatharthS/LuxTTS model
# downloads on first use into the mounted cache volume, so it is not baked in.
FROM python:3.11-slim

# libsndfile1 for soundfile; git + build-essential for the git/source wheels the
# LuxTTS fork and its prerequisites need.
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        libsndfile1 \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# The `zipvoice.luxvoice` module lives in the ysharma3501/LuxTTS fork (distribution
# "Zipvoice" 0.0.11), NOT the empty PyPI `zipvoice`. That fork declares non-PyPI
# sources (LinaCodec via git, piper-phonemize via the icefall find-links) that plain
# pip cannot resolve transitively, so they are installed explicitly first, followed
# by the fork itself (which then finds them satisfied), and finally this plugin.
# - CPU-only torch first so the multi-GB CUDA wheels never land in this CPU image.
# - setuptools<81 keeps ovos-plugin-manager's pkg_resources usage working.
# - ovos-tts-server>=1.13.5a1 floor lets pip resolve the prerelease without --pre.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir "linacodec @ git+https://github.com/ysharma3501/LinaCodec.git" \
    && ( pip install --no-cache-dir piper-phonemize -f https://k2-fsa.github.io/icefall/piper_phonemize.html \
         || pip install --no-cache-dir piper-phonemize-cross ) \
    && pip install --no-cache-dir "git+https://github.com/ysharma3501/LuxTTS.git" \
    && pip install --no-cache-dir "setuptools<81" "." "ovos-tts-server>=1.13.5a1"

# LuxTTS is a zero-shot voice-cloning engine: it needs a reference prompt to clone
# and runs on CPU here. The bundled test/jfk.wav is used as the default reference so
# the container synthesises out of the box; mount your own mycroft.conf to override.
ARG LUX_LANG=en-US
RUN useradd -m -u 1000 ovos \
    && mkdir -p /home/ovos/.config/mycroft \
    && printf '{\n  "tts": {\n    "module": "ovos-tts-plugin-lux",\n    "lang": "%s",\n    "ovos-tts-plugin-lux": {\n      "lang": "%s",\n      "device": "cpu",\n      "prompt_audio": "/app/test/jfk.wav"\n    }\n  }\n}\n' "${LUX_LANG}" "${LUX_LANG}" \
        > /home/ovos/.config/mycroft/mycroft.conf \
    && chown -R 1000:1000 /home/ovos/.config
USER 1000

EXPOSE 9666

# --cache persists synthesized audio across restarts. The model download lands under
# ~/.cache (mount a named volume so the ~491 MB model is fetched only once).
ENTRYPOINT ["ovos-tts-server", "--engine", "ovos-tts-plugin-lux", \
            "--host", "0.0.0.0", "--port", "9666", "--cache"]
