from pydub import AudioSegment, effects


def load_sound(file: str) -> AudioSegment:
    ending = file.split('.')[-1]
    return AudioSegment.from_file(file, ending)


def save_sound(in_sound: AudioSegment, file: str, form: str = None):
    if form is None:
        form = file.split('.')[-1]
    in_sound.export(file, format=form)


def normalize(in_sound: AudioSegment):
    return effects.normalize(in_sound)


def add_start_silence(in_sound: AudioSegment, length: int) -> AudioSegment:
    """

    :param in_sound: input AudioSegment to add silence to
    :param length: length of silence in milliseconds
    :return: AudioSegment with silence at the start
    """
    sil = AudioSegment.silent(length)
    return sil + in_sound


def add_end_silence(in_sound: AudioSegment, length: int):
    """

    :param in_sound: input AudioSegment to add silence to
    :param length: length of silence in milliseconds
    :return: AudioSegment with silence at the end
    """
    sil = AudioSegment.silent(length)
    return in_sound + sil


def crop_silence(in_sound: AudioSegment):
    start_trim = detect_leading_silence(in_sound)
    end_trim = detect_leading_silence(in_sound.reverse())
    duration = len(in_sound)
    trimmed_sound = in_sound[start_trim:duration - end_trim]
    return trimmed_sound


def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    """
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    """
    trim_ms = 0  # ms

    assert chunk_size > 0  # to avoid infinite loop
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

