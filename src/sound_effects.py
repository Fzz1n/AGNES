import pyvolume
import playsound

def adjust_sound(value):
    if value <= 100 and value >= 0:
        pyvolume.custom(percent=value)
        return f"The volume is set to {value}"
    return f"{value}, is not a valid input"

def play_mp3(soundname):
    dir = "src/mp3_files/"
    playsound.playsound(dir + soundname + ".mp3")