import cv2
import re
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

videos = ['police_cctv.mp4', 'municipal_cctv.mp4', 'gsrtc_cctv.mp4', 'health_cctv.mp4', 'panchayat_cctv.mp4']
for v in videos:
    cap = cv2.VideoCapture('frontend/public/videos/' + v)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f'=== Analyzing {v} (total {total} frames) ===')
    for fno in [10, 25, 40, 55, 70]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, min(fno, total-1))
        ret, frame = cap.read()
        if not ret: continue
        res = reader.readtext(frame)
        for (bbox, text, conf) in res:
            clean = re.sub(r'[^A-Z0-9]', '', text.upper())
            if len(clean) >= 4 and any(c.isdigit() for c in clean) and any(c.isalpha() for c in clean):
                pts = bbox
                x1 = min(p[0] for p in pts)
                y1 = min(p[1] for p in pts)
                x2 = max(p[0] for p in pts)
                y2 = max(p[1] for p in pts)
                h, w = frame.shape[:2]
                print(f'Frame {fno}: OCR="{text}" Clean="{clean}" Conf={round(conf, 2)} Pos: top={round(y1/h*100, 1)}% left={round(x1/w*100, 1)}% w={round((x2-x1)/w*100, 1)}% h={round((y2-y1)/h*100, 1)}%')
    cap.release()
