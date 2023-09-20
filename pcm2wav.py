import wave
import numpy as np
import sys


def pcm2wav(pcm_file, wav_file, channels=1, bits=16, sample_rate=16000):
    """
    PCM转为WAV格式
    :param pcm_file: pcm文件路径
    :param wav_file: wav文件路径
    :param channels: 声道数
    :param bits: 比特率
    :param sample_rate: 采样率
    :return:
    """
    data = open(pcm_file, 'rb').read()
    # 如果位深度为16位，那么需要进行short转换
    if bits == 16:
        data = np.frombuffer(data, dtype=np.short)
    data = data.tobytes()

    if bits % 8 != 0:
        return

    wav = wave.open(wav_file, 'wb')
    wav.setnchannels(channels)
    wav.setsampwidth(bits // 8)
    wav.setframerate(sample_rate)
    wav.writeframes(data)
    wav.close()


pcm2wav(sys.argv[1],sys.argv[2])
