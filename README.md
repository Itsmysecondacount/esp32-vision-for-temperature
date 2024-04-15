# Computer Vision Temperature Reader

## Overview

This project utilizes a computer vision approach to read and interpret temperatures from a non-digital temperature dial. By processing images captured from an ESP32 camera module, the system computes the angle of the dial's needle from a start to an end point. This angle is then correlated to a temperature value which is sent to a backend server for logging and monitoring.

## Features

Image Processing: Leverages the OpenCV library to interpret images of a temperature gauge.
Angle Calculation: Determines the angle of the temperature dial's needle to estimate temperature.
API Communication: Sends the calculated temperature data to a backend API for storage and further analysis.

## Software Dependencies

[Requirements](./requirements.txt)

## Setup and Operation

Camera Setup: Position the ESP32 camera to have a clear, focused view of the temperature dial.

Image Capture: The camera captures image and sends it to the endpoint configured (http://192.168.1.33/800x600.jpg).

Image Processing: The Python script procesar_imagen_desde_url processes the received image to find the dial and calculate the percentage, which corresponds to the temperature.

Data Transmission: Using the enviar_porcentaje function, the script sends the temperature data to a backend API (http://192.168.1.40:8099/api/v1/post-simple-data).

Backend Logging: The backend server receives the temperature data and stores it for tracking and analysis.

Calibration: While the system is calibrated to a nearly 1:1 temperature ratio, manual temperature mapping is recommended for precise monitoring needs.

## Usage Instructions

To ensure a consistent environment for running the script, it's recommended to use a virtual environment. Follow these steps to set up the environment and run the application:

### Set Up a Virtual Environment:

If you haven't installed virtualenv yet, you can install it using pip:

    pip install virtualenv

Then create a virtual environment in the project directory:

    virtualenv venv

Activate the virtual environment:

    On Windows:

    bash

    .\venv\Scripts\activate

    On Unix or MacOS:

    bash

    source venv/bin/activate

### Install Dependencies:

With the virtual environment active, install the required dependencies by running:

    pip install -r requirements.txt

### Run the Script:

To start the temperature reading and data transmission, execute:

    python main.py

### Adjust Debug Mode:

If you wish to run the script without the debug mode (which shows visual confirmation of the dial reading), locate the encontrar_dial_y_calcular_porcentaje function call and set the debug parameter to False:

    porcentaje = encontrar_dial_y_calcular_porcentaje(imagen, debug=False)

This will disable the debug mode and the script will operate in a non-interactive mode, suitable for automated or background running.

## Customization

You can modify the calibration settings in the encontrar_dial_y_calcular_porcentaje function to match the specifics of your temperature gauge if necessary.

## Maintenance

Regular checks should be conducted to ensure the ESP32 camera's view is unobstructed and the script is running as expected.
