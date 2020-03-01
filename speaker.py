import playsound
from gtts import gTTS
from io import BytesIO


def read(fname):
    f = open(fname)
    file = f.readlines()
    shopping = []
    for i in file:
        if i.strip() != "":
            shopping.append(i.strip())
    return shopping


def synth(text, fname):
    mp3_fp = BytesIO()
    tts = gTTS(text=text, lang="en")
    tts.save(fname+".mp3")
    tts.write_to_fp(mp3_fp)
    playsound.playsound(fname+".mp3")


def read_shopping(fname):
    shopping = read(fname)
    for ingredient in shopping:
        synth(ingredient, "ingredient")
    synth("See you soon!", "utt")


if __name__ == "__main__":
    read_shopping("./shopping_list.txt")
