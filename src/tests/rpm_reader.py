import obd

# Try with the specific baudrate
connection = obd.OBD("/dev/rfcomm0", baudrate=38400)

# Check connection status
print("Connection status:", connection.status())

# Try a basic command
response = connection.query(obd.commands.RPM)
print("Response:", response.value)