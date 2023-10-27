import json
import struct

import ffmpeg
import vosk

class Vosk:
    def __init__(self, model_path):
        model = vosk.Model(model_path)
        self.kaldi = vosk.KaldiRecognizer(model, 16000)

    def transcriber(self, path_audio):
        text = ""
        with open(path_audio, "rb") as wf:
            wf.read(44)  # skip header

            while True:
                data = wf.read(4000)
                if len(data) == 0:
                    break
                if self.kaldi.AcceptWaveform(data):
                    res = json.loads(self.kaldi.Result())
                    text += res["text"] + ". "

            res = json.loads(self.kaldi.FinalResult())
            text += res["text"]

        return text

    #Почти всегда нужно будет преоброзовывать файл в нужный формат
    def convert_audio(self, input_file, output_file):
        try:
            input_stream = ffmpeg.input(input_file)
            output_stream = ffmpeg.output(input_stream, output_file, acodec='pcm_s16le', ar=16000, ac=1)
            ffmpeg.run(output_stream)
            # print(f'Аудиофайл успешно преобразован в {output_file}')
        except ffmpeg.Error as e:
            print(f'Ошибка при конвертации аудио: {e}')

    """Этот метод получает запись микрофона. В данном проекте не нужен"""
    def speech_to_text(self, pcm):
        struct_pcm = struct.pack("h" * len(pcm), *pcm)
        if self.kaldi.AcceptWaveform(struct_pcm):
            letter = json.loads(self.kaldi.Result())["text"]

            if (len(letter) > 3):
                print("\rРаспознано: ", end="")
                print(f"{letter}", end=" ")
                return letter

