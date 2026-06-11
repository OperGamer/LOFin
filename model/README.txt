# Model Information

This directory contains the TensorFlow Lite model used by LOFin (Lost Object Finder) for object detection on the Raspberry Pi.

## Files

* `detect.tflite` – TensorFlow Lite object detection model.
* `labels.txt` – Label map corresponding to the model classes.

## Purpose

The model is used to identify and locate user-requested objects in frames captured by the Raspberry Pi camera. When the requested object is detected, the system uploads the detection result to Supabase and displays it through the web interface.

## Model Format

* Framework: TensorFlow Lite
* File format: `.tflite`
* Inference device: Raspberry Pi
* Input: Camera frames captured by the Raspberry Pi
* Output: Detected object labels with confidence scores and bounding boxes.

## Replacing the Model

To use a different model:

1. Export the new model in TensorFlow Lite (`.tflite`) format.
2. Replace `detect.tflite` with the new model file.
3. Update `labels.txt` so that it matches the classes used during training.
4. Ensure the Raspberry Pi detection script references the correct file names.

## Notes

* The model included in this repository was intended for educational and demonstration purposes.
* Detection accuracy depends on factors such as lighting conditions, camera quality, and the diversity of the training dataset.
