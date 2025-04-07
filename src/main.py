import obd

# Try with the specific baudrate
connection = obd.OBD("/dev/rfcomm0", baudrate=38400)

# Check connection status
print("Connection status:", connection.status())

# Continuously poll RPM as fast as possible
try:
    while True:
        response = connection.query(obd.commands.RPM)
        if response.value is not None:
            print("RPM:", response.value)
        else:
            print("No RPM data available")
except KeyboardInterrupt:
    print("Polling stopped by user.")