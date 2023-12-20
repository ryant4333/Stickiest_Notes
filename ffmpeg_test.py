from pydub import AudioSegment

import os

audio = AudioSegment.from_file("./uploads/file_example_OOG_1MG.ogg", "ogg")
print(type(audio))
wav_path = "test.wav"
audio.export(wav_path, format='wav')