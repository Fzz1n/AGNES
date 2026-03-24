import platform
import subprocess

# Adjusting the sound depending on platform (Linux or Windows)
def adjust_sound(volume):
    # Making sure it's between 0 and 100%
    if not 0 <= volume <= 100:
        return "Not a valid input"

    system = platform.system()

    if system == "Windows":
        import pyvolume
        pyvolume.custom(percent=volume)

    elif system == "Linux":
        subprocess.run(["amixer", "-c", "2", "set", "PCM", f"{volume}%"]) # Replace with yours speaker

    return f"The volume is set to {volume}"

#  Plays MP3 files, dependign on platfrom (Linux or Windows)
def play_mp3(soundname):
    filename = f"src/mp3_files/{soundname}.mp3"
    system = platform.system()

    if system == "Linux":
        subprocess.run(["mpg123", "-q", filename])

    elif system == "Windows":
        import playsound
        playsound.playsound(filename)