import cv2
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

for src_name in ['scratch_plate_license_plate.mp4', 'scratch_anpr_mycarplate.mp4', 'traffic_sample.mp4']:
    cap = cv2.VideoCapture(src_name)
    print(f"\n=================== {src_name} ===================")
    for fn in [15, 30, 45, 60]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, fn)
        ret, frame = cap.read()
        if not ret: continue
        res = reader.readtext(frame)
        for (bbox, text, conf) in res:
            t_clean = text.strip()
            if len(t_clean) >= 4 and any(c.isdigit() for c in t_clean):
                print(f"Frame {fn}: \"{text}\" (conf: {round(conf, 2)})")
    cap.release()
