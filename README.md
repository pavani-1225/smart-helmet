# AI-Based Smart Helmet for Industrial Workers

## Project Overview

The AI-Based Smart Helmet is a safety and communication system designed for industrial and construction workers operating in high-noise environments.

The system combines real-time digital noise reduction, voice enhancement, fall detection, GPS-based location reporting, and emergency communication.

The current software prototype is developed and tested on Windows using Python. Hardware deployment is planned using a Raspberry Pi 4.

---

## Key Features

- Real-time software-based noise reduction
- Voice enhancement
- Continuous audio processing
- Fall detection using accelerometer data
- Free-fall and impact sequence detection
- GPS location simulation
- Emergency alert generation
- Communication module simulation
- Modular Python architecture
- Raspberry Pi deployment support

---

## System Architecture

```text
             INMP441 Microphone
                    |
                    v
             Raspberry Pi 4
                    |
                    v
        Real-Time Audio Processing
          /                    \
         v                      v
 Noise Reduction          Voice Enhancement
         |                      |
         +----------+-----------+
                    |
                    v
            USB Sound Card
                    |
                    v
             PAM8403 Amplifier
                    |
                    v
             3W Speakers


        MPU6050 Accelerometer
                    |
                    v
             Fall Detection
                    |
                    v
            Emergency Trigger
                    |
             +------+------+
             |             |
             v             v
            GPS       Communication
             |             |
             +------+------+
                    |
                    v
             Emergency Alert

Software Modules
Audio Processing

The audio processing module performs real-time digital noise reduction and voice enhancement.

Processing parameters:

Sampling rate: 44.1 kHz
FFT size: 1024
Hop size: 512 samples
Mono audio processing
Frequency-domain spectral processing
Overlap-add reconstruction

The current implementation is a software-based noise reduction prototype and should not be described as validated active noise cancellation (ANC).

Fall Detection

The fall detection module uses accelerometer data from the MPU6050.

The prototype detects a sequence consisting of:

Possible free-fall
Strong impact
Post-impact state
Fall confirmation

The current Windows implementation uses simulated accelerometer data for testing.

GPS

The GPS module currently uses simulated coordinates to demonstrate location retrieval and emergency-alert integration.

Communication

The communication module currently simulates transmission of an emergency message.

The prototype demonstrates the software flow from fall detection to emergency notification.

Hardware Architecture

Planned hardware components include:

Raspberry Pi 4 Model B
32 GB microSD card
INMP441 I2S microphone
CM108 USB sound card
PAM8403 audio amplifier
Two 3 W, 4 Ω speakers
MPU6050 accelerometer
NEO-6M GPS module
Bluetooth communication modules
Jumper wires and supporting components
Planned Audio Path
INMP441
   |
   v
Raspberry Pi 4
   |
   v
Python Audio Processing
   |
   v
CM108 USB Sound Card
   |
   v
PAM8403 Amplifier
   |
   v
3W Speakers
Project Structure
smarthelmet/
│
├── smart_helmet.py
├── main.py
├── requirements.txt
├── README.md
│
├── audio/
│   ├── realtime_noise_reduction_v3_1.py
│   ├── noise_reduction.py
│   ├── audio_test.py
│   ├── audio_analysis.py
│   ├── realtime_audio.py
│   ├── realtime_noise_reduction.py
│   ├── realtime_noise_reduction_v2.py
│   ├── realtime_noise_reduction_v3.py
│   ├── realtime_performance.py
│   └── audio_performance_test.py
│
├── sensors/
│   ├── __init__.py
│   ├── mpu6050.py
│   ├── mpu6050_simulation.py
│   └── gps_simulation.py
│
├── safety/
│   └── emergency.py
│
├── communication/
│   └── communication_simulation.py
│
├── tests/
│
└── recordings/
    ├── original_voice.wav
    └── cleaned_voice.wav
Python Environment

The current Windows prototype uses:

Python 3.10
NumPy 2.2.6
SciPy 1.15.3
SoundDevice 0.5.6

Install the required Python packages using:

pip install -r requirements.txt
Running the Integrated System

From the project root:

python smart_helmet.py

The integrated system starts:

Real-time audio processing
Voice enhancement
Fall detection simulation
GPS simulation
Emergency communication simulation

The integrated software test completed successfully without import errors or runtime traceback.

Audio Performance

Experimental testing was performed using a 44.1 kHz sampling rate.

One recorded test produced:

Parameter	Before	After
Noise RMS	0.000025	0.000020
Speech RMS	0.004997	0.004995
SNR	45.91 dB	48.04 dB
Estimated SNR Improvement

2.14 dB

The speech RMS remained nearly unchanged during this test, indicating that the processing preserved the measured speech signal while reducing the estimated background noise.

These results represent the current software prototype and are not laboratory-validated ANC performance measurements.

Real-Time Processing Performance

The real-time processing prototype was tested using:

Sampling rate: 44.1 kHz
Block size: 1024 samples

Measured processing time:

Average processing time: approximately 0.257 ms
Maximum measured processing time: approximately 10.709 ms
Audio block duration: approximately 23.22 ms

The average processing time was substantially below the duration of an audio block during the test.

Current Testing Status
Completed
Python environment setup
Basic audio capture
Audio playback
Offline noise reduction
Real-time audio pass-through
Real-time noise reduction
Voice enhancement
Audio performance testing
MPU6050 fall-detection simulation
GPS simulation
Emergency communication simulation
Integrated system testing
Project folder organization
Current Status

The complete software prototype has been integrated and tested successfully on Windows.

Hardware integration and Raspberry Pi deployment remain part of the next stage.

Limitations

The current prototype has the following limitations:

Audio noise reduction is software-based and is not validated active noise cancellation.
MPU6050 input is simulated on Windows.
GPS coordinates are simulated.
Emergency communication is simulated.
Raspberry Pi hardware deployment has not yet been completed.
Final real-world performance depends on hardware integration and environmental testing.
Future Work

Future development can include:

Raspberry Pi deployment
Real INMP441 I2S microphone integration
Real MPU6050 sensor integration
Real NEO-6M GPS integration
Wireless emergency communication
Hardware-level audio optimization
Improved noise suppression algorithms
Real-world industrial noise testing
Helmet enclosure and final hardware integration
Project Objective

The primary objective is to develop a smart safety helmet that improves worker communication in high-noise environments while providing automated fall detection and emergency location reporting.

The project combines embedded systems, digital signal processing, sensors, communication, and Python-based software development into a single safety-oriented system.