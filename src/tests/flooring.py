import obd
import subprocess

# Try with the specific baudrate
connection = obd.OBD("/dev/rfcomm0", baudrate=38400)

# Check connection status
print("Connection status:", connection.status())

# Initialize variables to track sound playback
idle_sound_process = None
exhaust_sound_process = None

# Define RPM thresholds
IDLE_THRESHOLD = 1000
FLOOR_THRESHOLD = 3000  # Adjust this value based on what you consider "flooring it"

try:
    while True:
        response = connection.query(obd.commands.RPM)
        if response.value is not None:
            rpm = response.value.magnitude  # Get the RPM as a number
            print("RPM:", rpm)

            if rpm < IDLE_THRESHOLD:
                # Play idle/chopping sound if not already playing
                if idle_sound_process is None or idle_sound_process.poll() is not None:
                    # Terminate exhaust sound if it's playing
                    if exhaust_sound_process is not None:
                        exhaust_sound_process.terminate()
                        exhaust_sound_process = None
                    # Start idle sound
                    idle_sound_process = subprocess.Popen(['aplay', '-D', 'plughw:0,0', 'chop.wav'])
            elif rpm > FLOOR_THRESHOLD:
                # Play exhaust sound if not already playing
                if exhaust_sound_process is None or exhaust_sound_process.poll() is not None:
                    # Terminate idle sound if it's playing
                    if idle_sound_process is not None:
                        idle_sound_process.terminate()
                        idle_sound_process = None
                    # Start exhaust sound
                    exhaust_sound_process = subprocess.Popen(['aplay', '-D', 'plughw:0,0', 'exhaust.wav'])
            else:
                # RPM is between idle and floor thresholds, stop all sounds
                if idle_sound_process is not None:
                    idle_sound_process.terminate()
                    idle_sound_process = None
                if exhaust_sound_process is not None:
                    exhaust_sound_process.terminate()
                    exhaust_sound_process = None
        else:
            print("No RPM data available")
except KeyboardInterrupt:
    print("Polling stopped by user.")
    # Clean up any running processes
    if idle_sound_process is not None:
        idle_sound_process.terminate()
    if exhaust_sound_process is not None:
        exhaust_sound_process.terminate()