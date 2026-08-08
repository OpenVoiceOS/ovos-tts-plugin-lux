#!/usr/bin/env python3
import os

from setuptools import setup

PLUGIN_ENTRY_POINT = 'ovos-tts-plugin-lux = ovos_tts_plugin_lux:LuxTTS'
SAMPLE_CONFIGS = 'ovos-tts-plugin-lux.config = ovos_tts_plugin_lux:LuxTTSPluginConfig'

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    """ Find the version of the package"""
    version_file = f'{BASEDIR}/ovos_tts_plugin_lux/version.py'
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version


setup(
    name='ovos-tts-plugin-lux',
    version=get_version(),
    description='LuxTTS plugin for OpenVoiceOS',
    url='https://github.com/OpenVoiceOS/ovos-tts-plugin-lux',
    author='OpenVoiceOS',
    author_email='contact@openvoiceos.com',
    license='Apache-2.0',
    packages=['ovos_tts_plugin_lux'],
    install_requires=[
        'ovos-plugin-manager>=0.0.1',
        'zipvoice>=0.0.11',
        'soundfile',
    ],
    extras_require={'test': ['ovoscope[tts]', 'pytest']},
    zip_safe=True,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
    keywords='OpenVoiceOS mycroft neon chatterbox plugin tts',
    entry_points={'mycroft.plugin.tts': PLUGIN_ENTRY_POINT,
                  'mycroft.plugin.tts.config': SAMPLE_CONFIGS}
)
