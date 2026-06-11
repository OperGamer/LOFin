# Raspberry Pi Setup

This guide explains how to configure the Raspberry Pi for the LOFin (Lost Object Finder) project.

## Hardware Used

* Raspberry Pi 4 Model B
* USB Webcam
* MicroSD Card (16 GB or larger)
* Power Supply
* Buzzer/LED (optional)

## Operating System

The project was developed and tested on:

* **Raspberry Pi OS (64-bit)**
* Debian Bookworm based release

## Initial Setup

1. Flash Raspberry Pi OS to the microSD card using Raspberry Pi Imager.
2. During the imaging process, enable:

   * SSH
   * Wi-Fi configuration
   * Username and password setup
3. Insert the microSD card into the Raspberry Pi and boot the device.

## Update the System

```bash
sudo apt update
sudo apt upgrade -y
```

## Install Required Packages

```bash
sudo apt install python3-pip python3-venv git -y
```

## Clone the Repository

```bash
git clone https://github.com/<your-username>/LOFin.git
cd LOFin
```

## Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file containing the required Supabase credentials:

```text
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Running the Project

```bash
python raspberry_pi/full.py
```

## Notes

* Ensure the USB webcam is connected before running the application.
* Verify that the TensorFlow Lite model and labels file are placed in the correct directory.
* The Raspberry Pi must have internet access to communicate with Supabase.
* SSH can be used to manage the Raspberry Pi remotely.
