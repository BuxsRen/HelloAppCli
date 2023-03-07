import pyaudio # Windows：到 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio 下载对应的版本(cp37 表示python37) 然后pip install 文件名 | MacOS： brew install portaudio;pip install pyaudio

class Audio:
    play = None
    chunk_size = 1024  # 512
    audio_format = pyaudio.paInt16  # 采样位数
    channels = 1  # 通道
    rate = 16000  # 采样率

    # 初始化
    def new(self):
        try:
            self.play = pyaudio.PyAudio()
            self.playing_stream = self.play.open(format=self.audio_format, channels=self.channels, rate=self.rate,
                                                 output=True, frames_per_buffer=self.chunk_size)
            self.recording_stream = self.play.open(format=self.audio_format, channels=self.channels, rate=self.rate,
                                                   input=True, frames_per_buffer=self.chunk_size)
            return True
        except Exception as e:
            print("麦克风或输出设备不可用")
            return False

    # 播放音频流
    def receive(self,data):
        self.playing_stream.write(data)

    # 捕获音频流
    def send(self):
        while True:
            data = self.recording_stream.read(1024)
            print(data)