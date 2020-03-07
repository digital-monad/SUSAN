import speech_recognition as sr  # Needs PyAudio as pre-requisite for microphone recognition


def recognise():
    recog = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Listening...")
        recog.adjust_for_ambient_noise(source)
        inp = recog.listen(source)
    print("Recognising...")
    result = recog.recognize_google(inp)
    return result


if __name__ == "__main__":
    recognise()
