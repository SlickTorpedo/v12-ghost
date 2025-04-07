import obd
import subprocess

# Try with the specific baudrate
connection = obd.OBD("/dev/rfcomm0", baudrate=38400)

# Check connection status
print("Connection status:", connection.status())

# Initialize variables to track sound playback
sound_process = None

try:
    while True:
        response = connection.query(obd.commands.RPM)
        if response.value is not None:
            rpm = response.value.magnitude  # Get the RPM as a number
            print("RPM:", rpm)

            if rpm < 1000:
                # Start playing sound if not already playing
                if sound_process is None or sound_process.poll() is not None:
                    sound_process = subprocess.Popen(['aplay', '-D', 'plughw:0,0', 'chop.wav'])
            else:
                # Stop the sound if RPM is above 1000
                if sound_process is not None:
                    sound_process.terminate()
                    sound_process = None
        else:
            print("No RPM data available")
except KeyboardInterrupt:
    print("Polling stopped by user.")
    if sound_process is not None:
        sound_process.terminate()