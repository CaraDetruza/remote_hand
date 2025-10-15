# remote_hand
This project features a 3D-printed robotic hand that is remotely controlled using a glove equipped with flex sensors. The system is divided into two main parts: **client** and **server**, which communicate using **UDP sockets**.

## System Overview

- **Sensor Glove (Client):** An ESP32 reads finger flexion using flex sensors. Each sensor reading is mapped to an angle, then sent via UDP to the server.

- **Robotic Hand (Server):** A Raspberry Pi Zero 2W receives the angle data and controls servo motors connected via a **PCA9685 module**, flexing the 3D-printed fingers accordingly.

##  Technologies & Hardware

- **MicroPython** (used throughout the project)
- **ESP32** (client for reading sensors)
- **Raspberry Pi Zero 2W** (server for controlling servos)
- **PCA9685** (for precise servo control)
- **UDP Sockets** (communication protocol)
- **Flex Sensors**
- **Servo Motors**
- **3D Printing** (structure of the robotic hand)

## Project Structure


## Images / Videos

N/A

## Connection diagrams

N/A

## Installation

### Client (ESP32)

1. Flash MicroPython on your ESP32.
2. Upload `main.py` to the board.
3. Connect the flex sensors to the correct GPIO pins.

### Server (Raspberry Pi)

1. Use MicroPython or standard Python with a compatible PCA9685 library.
2. Connect the PCA9685 to the Raspberry Pi.
3. Run `server.py`.

## Communication Protocol

- **Protocol:** UDP
- The client sends a data packet containing the mapped angle values for each finger.
- The server receives the data and moves the corresponding servos.

## License

Idk feel free to use, modify, and share it :P
