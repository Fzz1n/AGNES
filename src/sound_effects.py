import platform
import subprocess

# Adjusting the sound depending on platform (Linux or Windows)
def adjust_volume(volume):
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

# Gets the current volume level
def current_volume():
    system = platform.system()

    if system == "Windows":
        from pycaw.pycaw import AudioUtilities
        device = AudioUtilities.GetSpeakers()
        volume = device.EndpointVolume
        volume_level = volume.GetMasterVolumeLevelScalar() * 100
        return int(volume_level)    
    
    elif system == "Linux":
        import alsaaudio
        mixer = alsaaudio.Mixer()
        return int(mixer.getvolume()[0])

#  Plays MP3 files, dependign on platfrom (Linux or Windows)
def play_mp3(soundname):
    filename = f"src/mp3_files/{soundname}.mp3"
    system = platform.system()

    if system == "Linux":
        subprocess.run(["mpg123", "-q", filename])

    elif system == "Windows":
        import playsound
        playsound.playsound(filename)

def play_mp3_with_custom_volume(file, volume_level):
    # Save current volume
    old_volume = current_volume()

    # Change volume
    adjust_volume(volume_level)

    # Play sound
    play_mp3(file)

    # Go back to teh old volume 
    adjust_volume(old_volume)