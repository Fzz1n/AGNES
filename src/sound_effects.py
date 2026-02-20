import playsound

def play_mp3(soundname):
    dir = "src/mp3_files/"
    playsound.playsound(dir + soundname + ".mp3")