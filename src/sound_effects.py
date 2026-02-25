import os
import platform
import subprocess

def adjust_sound(value):
    if not 0 <= value <= 100:
        return "Not a valid input"

    system = platform.system()

    if system == "Windows":
        import pyvolume
        pyvolume.custom(percent=value)

    elif system == "Linux":
        subprocess.run(
            ["amixer", "set", "Master", f"{value}%"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    return f"The volume is set to {value}"


def play_mp3(soundname):
    filename = f"src/mp3_files/{soundname}.mp3"
    system = platform.system()

    if system == "Linux":
        subprocess.run(["mpg123", "-q", filename])

    elif system == "Windows":
        os.startfile(filename)