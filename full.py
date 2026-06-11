import time
import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter
from supabase import create_client
from datetime import datetime

# ---------------- SUPABASE SETUP ----------------
SUPABASE_URL = "https://qugxfdmhllswhsjmvwqb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF1Z3hmZG1obGxzd2hzam12d3FiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAwNzM0NDEsImV4cCI6MjA5NTY0OTQ0MX0.uoPkzZZHX9M3yptUrcYm_ds7EdeB2jfH0wT8QnfE7FY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- MODEL SETUP ----------------
MODEL_PATH = "detect.tflite"
LABELS_PATH = "labels.txt"

interpreter = Interpreter(MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
print("MODEL DTYPE =", input_details[0]["dtype"])
output_details = interpreter.get_output_details()

with open(LABELS_PATH, "r") as f:
    labels = [line.strip() for line in f.readlines()]

# ---------------- CAMERA SETUP ----------------
cap = cv2.VideoCapture(0
)
print("Camera opened:", cap.isOpened())
last_seen_image = None  # Stores the last detected frame before command

# ---------------- FUNCTIONS ----------------
def detect_objects(frame):
    h, w = input_details[0]['shape'][1], input_details[0]['shape'][2]
    img = cv2.resize(frame, (w, h))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    input_data = np.expand_dims(img_rgb, axis=0).astype(np.uint8)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]

    detected = False
    confidence = 0.0
    for i in range(len(scores)):
        if scores[i] > 0.5 and labels[int(classes[i])] == "bottle":
            ymin, xmin, ymax, xmax = boxes[i]
            ymin, xmin, ymax, xmax = int(ymin * frame.shape[0]), int(xmin * frame.shape[1]), int(ymax * frame.shape[0]), int(xmax * frame.shape[1])
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            detected = True
            confidence = float(scores[i])
            break

    return detected, confidence, frame

def get_pending_command():
    res = supabase.table("commands").select("*").eq("status", "pending").order("created_at").limit(1).execute()
    if res.data and len(res.data) > 0:
        return res.data[0]
    return None

def upload_detection(command_id, found, confidence, image=None, last_seen=False):
    image_url = None
    if image is not None:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"bottle_{timestamp}.jpg"
        cv2.imwrite(filename, image)
        with open(filename, "rb") as f:
            supabase.storage.from_("detections").upload(filename, f)
        image_url = f"{SUPABASE_URL}/storage/v1/object/public/detections/{filename}"

    if last_seen:
        status_text = "last_seen"
    else:
        status_text = "detected" if found else "no image detected"

    supabase.table("detections").insert({
        "command_id": command_id,
        "found": found,
        "confidence": confidence,
        "image_url": image_url,
        "status": status_text
    }).execute()

    supabase.table("commands").update({"status": "done"}).eq("id", command_id).execute()

# ---------------- MAIN LOOP ----------------
try:
    poll_count = 0
    print("Lost Object Finder running...")

    while True:
        poll_count += 1
        print(f"[Polling {poll_count}] Updating last seen before checking commands...")

        # ---------------- Faster last_seen update ----------------
        # Capture multiple frames for 1 second to reduce lag
        start_time = time.time()
        while time.time() - start_time < 1:  # 1-second window
            ret, frame = cap.read()
            if ret:
                detected, _, output_frame = detect_objects(frame)
                if detected:
                    last_seen_image = output_frame.copy()
                    print("[Last Seen] Object detected, updated last_seen_image.")

        # ---------------- Check for commands ----------------
        command = get_pending_command()
        if command:
            print(f"[Command received] Processing command {command['id']}")

            ret, frame = cap.read()
            if not ret:
                print("Camera error, skipping command...")
                time.sleep(1)
                continue

            detected, confidence, output_frame = detect_objects(frame)

            if detected:
                print(f"[Detection] Object detected in current frame. Confidence: {confidence:.2f}")
                upload_detection(command['id'], True, confidence, output_frame)
            else:
                if last_seen_image is not None:
                    print("[Detection] Object not detected. Using last seen image before command.")
                    upload_detection(command['id'], True, 0.0, last_seen_image, last_seen=True)
                else:
                    print("[Detection] Object not detected and no last seen image available.")
                    upload_detection(command['id'], False, 0.0, None)

        else:
            print("No new commands. Waiting...")
            time.sleep(0.5)  # faster polling

except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
    print("Exited")
