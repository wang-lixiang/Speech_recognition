import openai
import pyttsx3
import wave
import pyaudio
import whisper

# 初始化文本到语音引擎
engine = pyttsx3.init()
# 获取openai_key
openai.api_key = "sk-LZc1RDFMruIM0077dWkFf9VleMz6S9cmZkb9korxruGR1KjX"
# 固定提问的时间(s)
Time = 5


# 说出指定文本
def speak_text(text):
    engine.say(text)
    # 阻塞其它语句，等待语音完成播放
    engine.runAndWait()


# 使用OpenAI产生对问题进行回答
def generate_response(question):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    return response["choices"][0]["message"]["content"]


# 处理提问的语音，并返回提问的文本
def generate_question(time=Time):
    # 每次读取的数据块大小
    CHUNK = 1024
    # 音频格式为16位PCM
    FORMAT = pyaudio.paInt16
    # 单通道
    CHANNELS = 1
    # 采样率为16kHZ
    RATE = 16000
    # 录音时长
    RECORD_SECONDS = time
    # 录音文件保存路径及文件名
    WAVE_OUTPUT_FILENAME = "./output.wav"

    # 创建PyAudio对象
    Pyaudio = pyaudio.PyAudio()
    # 打开音频输入流
    stream = Pyaudio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        # 从音频输入流中读取数据
        data = stream.read(CHUNK)
        # 将读取的数据添加到frames列表中
        frames.append(data)
    print("* done recording")

    # 停止音频输入流
    stream.stop_stream()
    # 关闭音频输入流
    stream.close()
    # 终止PyAudio对象
    Pyaudio.terminate()

    # 将录制的音频数据写入WAV文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    # 设置通道数
    wf.setnchannels(CHANNELS)
    # 设置采样位数
    wf.setsampwidth(Pyaudio.get_sample_size(FORMAT))
    # 设置采样率
    wf.setframerate(RATE)
    # 写入音频数据
    wf.writeframes(b''.join(frames))
    # 关闭WAV文件
    wf.close()

    # 加载预训练的语音识别模型
    model = whisper.load_model("base")
    # 通过模型转录音频文件中的语音内容
    result = model.transcribe("output.wav", language="Chinese", fp16=False)
    # 获取转录结果中的文本
    question = result["text"]

    return question


def main():
    while True:
        question = generate_question()
        if question == "":
            speak_text('please speak something')
        else:
            response = generate_response(question)
            print(f'You: {question}')
            print(f'chatGpt: {response}')
            speak_text(response)


if __name__ == '__main__':
    main()
