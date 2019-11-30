import platform

WINDOWS_PORT = "COM3"
LINUX_PORT = "/dev/ttyUSB0"

PORT_MAPPING = {
    "Windows": "COM3",
    "Linux": "/dev/ttyUSB0"
}

PORT = PORT_MAPPING.get(platform.system())