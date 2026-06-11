# LOFin

AI-powered lost object finder using Raspberry Pi, TensorFlow Lite, Supabase, and a web interface.

## Features

- Voice/text-based object search
- TensorFlow Lite object detection
- Supabase integration
- Web dashboard
- Last-seen image capture
- Raspberry Pi buzzer indication

## Tech Stack

- Raspberry Pi
- TensorFlow Lite
- Python
- Supabase
- HTML/CSS/JavaScript
  ```bash
  pip install -r requirements.txt
## SETUP:
  ## Place your TFLite model in:
  model/model.tflite
  ## Run:  
    ```bash
    python raspberry_pi/main.py

## SUPABASE SETUP:
A Detections table and a Commands table with following configs
<img width="979" height="481" alt="image" src="https://github.com/user-attachments/assets/d0e27131-1911-468c-bd9e-886b3124b9a5" />


SQL Query for above:
  ```bash
  CREATE TABLE commands (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    object_name TEXT NOT NULL,
    status TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
  );

  CREATE TABLE detections (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    command_id BIGINT REFERENCES commands(id),
    confidence DOUBLE PRECISION,
    image_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    status TEXT,
    found BOOLEAN
  );
```


  
