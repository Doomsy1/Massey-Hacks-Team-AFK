# 2AK-Bot

<p align="center">
  <img src="assets/images/2AK-BOT Logo.png" alt="2AK-Bot logo" width="220">
</p>

ESP32-powered tank-drive rover with a Bluetooth pygame controller, a servo-driven
picker arm, and three ESP32-CAM streams fed through YOLO v3 for live object
detection. Built at Massey Hacks by Team AFK.

![Controller UI](assets/images/MasseyHacks%20UI.png)

## What it does

- **Tank drive** with two motors per side, driven by an ESP32 receiving speed
  commands over Bluetooth serial.
- **Picker arm** built from 3D-printed parts: a turret servo, an arm servo, and
  a gripper servo assisted by sticky pads.
- **Vision** from three ESP32-CAM modules hosting `/cam-lo.jpg` endpoints, read
  in parallel threads and run through YOLO v3 (COCO classes) to flag objects of
  interest (notably people, sheep, cows, giraffes, zebras).

## Tech stack

- **Firmware (ESP32):** Arduino C++ via `bluetoothsocket.ino` (motor + servo
  control) and `esp32Cam.io` (per-camera JPEG web server). Libraries:
  `ESP32Servo`, `esp32cam`, `WebServer`, `WiFi`.
- **Controller host (Python):** `src/main.py` is a pygame UI that reads keyboard
  or joystick input and sends `left_speed,right_speed,turret,arm,gripper` lines
  over Bluetooth RFCOMM (`pybluez`).
- **Vision host (Python):** `esp32cam.py` fetches the three camera streams and
  runs OpenCV DNN + YOLO v3 inference on each frame.

## Hardware (bill of materials)

- 1 x ESP32 dev board (motor + servo + Bluetooth brain)
- 3 x ESP32-CAM modules (front/side/rear vision)
- 4 x DC motors (tank-drive, two per side)
- 3 x servos (turret rotation, arm lift, gripper)
- Motor driver board, USB power bank, 3D-printed chassis + arm + gripper pads

## Setup

### 1. Python host

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install opencv-python numpy pygame pybluez

# YOLO v3 weights are large and gitignored; download separately:
#   https://pjreddie.com/media/files/yolov3.weights
```

### 2. Flash the ESP32 firmware

1. Open `bluetoothsocket.ino` in the Arduino IDE (or PlatformIO) and flash it
   to the motor/servo ESP32. It advertises itself as **AFK ESP**.
2. For each ESP32-CAM: copy `secrets.h.example` to `secrets.h`, fill in your
   WiFi SSID and password, then open and flash `esp32Cam.io`. The camera prints
   its assigned IP and endpoints (`/cam-lo.jpg`, `/cam-mid.jpg`, `/cam-hi.jpg`)
   to serial. Keep `secrets.h` out of git (it is gitignored).

### 3. Run

```bash
# Controller UI (keyboard: WASD drive, arrows arm, Q/E gripper)
python src/main.py

# Vision feed (override camera IPs for your own LAN)
CAM1_URL=http://<cam1-ip>/cam-lo.jpg \
CAM2_URL=http://<cam2-ip>/cam-lo.jpg \
CAM3_URL=http://<cam3-ip>/cam-lo.jpg \
python esp32cam.py
```

To enable the Bluetooth link, uncomment the `setupBluetooth` / `bt_socket.send`
lines in `src/main.py` (kept commented by default so the UI runs without a
paired rover).

## Project context

This was a hackathon build: the rover is fully assembled and drivable, and the
camera + detection pipeline is functional. Full autonomy (driving toward
detected objects and picking them up) is the next step. Many components were
fried during assembly, which cut into the time we had planned to spend training
a custom detection model.

## License

[MIT](LICENSE).
