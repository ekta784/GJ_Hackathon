import cv2
import json
import urllib.request
import time
import argparse
import sys

# Attempt to load YOLO and EasyOCR
try:
    from ultralytics import YOLO
except ImportError:
    print("Error: ultralytics is not installed. Please run: pip install ultralytics")
    sys.exit(1)

try:
    import easyocr
except ImportError:
    print("Error: easyocr is not installed. Please run: pip install easyocr")
    sys.exit(1)

API_URL = "http://127.0.0.1:8000/api/simulate/sighting"
CAMERA_NAME = "Live Camera 1"

def post_detection(plate_text, confidence):
    data = {
        "camera_name": CAMERA_NAME,
        "plate_number": plate_text,
        "confidence": confidence
    }
    
    req = urllib.request.Request(API_URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req)
        print(f"[+] Posted detection {plate_text} (Conf: {confidence:.2f}) to dashboard! Status: {response.getcode()}")
    except Exception as e:
        print(f"[-] Failed to post detection to {API_URL}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Live Video AI Pipeline for SETU Sentinel")
    parser.add_argument("--source", type=str, default="0", help="Video source: '0' for webcam, or path to an .mp4 file or RTSP stream")
    args = parser.parse_args()

    print("[*] Initializing AI Models...")
    # Load YOLOv8 nano model (downloads automatically if missing)
    model = YOLO("yolov8n.pt") 
    
    # Initialize EasyOCR reader (English). Uses CPU by default on Windows unless CUDA is perfectly configured
    reader = easyocr.Reader(['en'], gpu=False)
    
    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source)
    
    if not cap.isOpened():
        print(f"[!] Error: Could not open video source {source}")
        sys.exit(1)
        
    print(f"[*] Connected to video source {source}. Starting inference...")
    print("[*] Press 'q' to quit.")

    frame_skip = 5 # Process every 5th frame to avoid lag
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[*] End of video stream.")
            break
            
        frame_count += 1
        
        # Display the live feed
        cv2.imshow("SETU Sentinel - Live Feed", frame)

        if frame_count % frame_skip == 0:
            # Run YOLO inference
            results = model(frame, verbose=False)
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls_id = int(box.cls[0])
                    # In COCO dataset: 2=car, 3=motorcycle, 5=bus, 7=truck
                    if cls_id in [2, 3, 5, 7]:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        
                        # Crop the detected vehicle
                        vehicle_crop = frame[y1:y2, x1:x2]
                        
                        if vehicle_crop.size == 0:
                            continue
                            
                        # Run OCR on the vehicle crop to find any text (license plate)
                        # In a real production system, you would use a dedicated License Plate Detector YOLO model before OCR
                        ocr_results = reader.readtext(vehicle_crop)
                        
                        for (bbox, text, prob) in ocr_results:
                            # Filter for strings that resemble license plates (alphanumeric, reasonable length)
                            clean_text = "".join(c for c in text if c.isalnum()).upper()
                            
                            if len(clean_text) >= 4 and prob > 0.5:
                                # Draw a bounding box and text on the frame
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, clean_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                                cv2.imshow("SETU Sentinel - Live Feed", frame)
                                
                                # Send to backend
                                post_detection(clean_text, prob)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
