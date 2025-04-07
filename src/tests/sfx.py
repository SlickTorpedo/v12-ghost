import subprocess
import time

# Set the volume using the numid references
try:
    # Main playback volume (numid=10)
    subprocess.run(['amixer', '-c', '0', 'cset', 'numid=10', '100%'])
    # Speaker playback volume (numid=13)
    subprocess.run(['amixer', '-c', '0', 'cset', 'numid=13', '100%'])
    # Headphone playback volume (numid=11)
    subprocess.run(['amixer', '-c', '0', 'cset', 'numid=11', '100%'])
    
    print("Volume set to maximum")
except Exception as e:
    print(f"Error setting volume: {e}")
    print("Please use alsamixer to adjust volume manually")

# Play the sound
process = subprocess.Popen(['aplay', '-D', 'plughw:0,0', 'chop.wav'])

print("Sound is playing. Press Ctrl+C to stop.")
try:
    time.sleep(14) #Because the audio is 14 seconds long
except KeyboardInterrupt:
    process.terminate()
    print("Sound stopped.")