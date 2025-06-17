# Smart Traffic Management System

A system to manage traffic at intersections by detecting vehicles and prioritizing emergency vehicles (like ambulances) using Raspberry Pi, FPGA, and computer vision.

## Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [How It Works](#how-it-works)
- [Circuit Diagram](#circuit-diagram)
- [Setup Instructions](#setup-instructions)
- [Results](#results)
- [Visual Results](#visual-results)
- [Demo](#demo)
- [Documentation](#documentation)
- [License](#license)



## About the Project
This project addresses urban traffic congestion and enables emergency vehicles (such as ambulances) to navigate intersections more efficiently.
- A webcam to count vehicles with YOLO (a computer vision tool).
- A microphone to detect ambulance sirens with YAMNet.
- Raspberry Pi to process data.
- FPGA to control traffic lights in real-time.

We built and tested it on a small model of a traffic junction at Mar Baselios College of Engineering and Technology (2025).

## Features

- 🚦 Counts vehicles to adjust green light times for busy roads.  
- 🚑 Detects ambulance sirens and gives them priority (green light).  
- ⚙️ Uses FPGA for fast and reliable traffic light control.


## Technologies Used
- **Hardware**: Raspberry Pi 4, Basys 3 FPGA, Webcam, Microphone, LED Traffic Lights.
- **Software**: Python, Verilog, YOLOv8, YAMNet, OpenCV, PyAudio.
- **Tools**: Git, Vivado (for FPGA), TensorFlow Lite.

## How It Works
1. Webcam captures traffic and YOLO counts vehicles.
2. Microphone listens for sirens and YAMNet confirms if it’s an ambulance.
3. Raspberry Pi processes the data and sends instructions to the FPGA.
4. FPGA changes traffic lights to reduce congestion or prioritize ambulances.

![Block Diagram](docs/block_diagram.jpg)

## Circuit Diagram
![Circuit Diagram](docs/Circuit_Diagram.jpg)

## Setup Instructions
1. Clone the project:
   ```bash
   git clone https://github.com/your-username/Smart-Traffic-Management-System.git
   cd Smart-Traffic-Management-System
2. Install Python libraries
3. Add YOLO and YAMNet models to models/
4. Program the FPGA with src/verilog/fpga_blink_new.v using Vivado.
5. Run the main script
    python src/python/traffic_control.py

## Results

- Successfully controlled traffic lights based on vehicle count.  
- Detected ambulances using siren sounds and video.  
- Tested on a mini traffic junction model.  
- **Challenge**: Audio processing was hard on Raspberry Pi, so we tested it separately on a laptop.
  
## Visual Results

A few snapshots from our system detecting traffic in real-time:

### 🛣️ Real Road Detection using YOLOv8

![Road Detection 1](assets/screenshots/Road_Detection1.jpeg)  
*Real-world traffic detection using YOLOv8*

![Road Detection 2](assets/screenshots/Road_Detection2.jpg)  
*Bounding boxes generated on live traffic input*

### 🚗 Toy Car Detection in Miniature Setup

![Toy Car Detection](assets/screenshots/Toy_car_detection3.jpg)  
*Testing with toy cars and camera input on a prototype intersection*

## Demo

- 🎥 [Watch the Demo Video](https://drive.google.com/file/d/11muLq86sJkHUUcLF9veugZjnzbw4sB4t/view?usp=drivesdk)


## Documentation

###Project Report
- 📄[Project Report (PDF)](docs/Final%20Report%20new.pdf)


## License
This project is licensed under the MIT License - see [LICENSE](LICENSE).

*Created by students at Mar Baselios College of Engineering and Technology, 2025.*
