import cv2
import numpy as np

def create_sample_traffic_video(output_path="traffic_sample.mp4", width=800, height=450, fps=25, duration_sec=14):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    total_frames = fps * duration_sec

    # Multiple vehicles driving simultaneously in different lanes!
    vehicles = [
        # Scene 1: Two vehicles side-by-side in Upper and Lower lanes
        {"start_frame": 10, "end_frame": 150, "plate": "GJ01AB1234", "color": (50, 50, 200), "lane": "upper", "label": "WANTED SUSPECT"},
        {"start_frame": 20, "end_frame": 160, "plate": "MH12AB3456", "color": (200, 60, 40), "lane": "lower", "label": "CROSS-STATE SUV"},
        
        # Scene 2: Next two vehicles in both lanes
        {"start_frame": 170, "end_frame": 310, "plate": "GJ03XX5555", "color": (30, 160, 210), "lane": "upper", "label": "LOCAL TRAFFIC"},
        {"start_frame": 185, "end_frame": 325, "plate": "DL01AB4321", "color": (40, 180, 70), "lane": "lower", "label": "COMMUTER SEDAN"}
    ]

    for frame_idx in range(total_frames):
        # Road asphalt
        frame = np.full((height, width, 3), (32, 35, 40), dtype=np.uint8)
        
        # Multi-lane highway markings
        cv2.rectangle(frame, (0, 70), (width, height - 30), (45, 48, 54), -1)
        # Yellow edge barriers
        cv2.line(frame, (0, 75), (width, 75), (0, 210, 255), 3)
        cv2.line(frame, (0, height - 35), (width, height - 35), (0, 210, 255), 3)
        
        # White dashed center dividing line
        dash_offset = (frame_idx * 14) % 60
        for x in range(-dash_offset, width, 60):
            cv2.line(frame, (x, height // 2), (x + 35, height // 2), (240, 240, 240), 2)

        # Header overlay
        cv2.putText(frame, "GUJARAT POLICE SCRB - MULTI-LANE CCTV CAM #01 (SG HIGHWAY)", (15, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.58, (0, 240, 255), 2)
        cv2.putText(frame, f"REC [LIVE] - FRAME {frame_idx:04d} - DUAL LANE ANPR INGEST", (15, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (170, 170, 170), 1)

        # Draw each vehicle in its lane
        for v in vehicles:
            if v["start_frame"] <= frame_idx <= v["end_frame"]:
                progress = (frame_idx - v["start_frame"]) / (v["end_frame"] - v["start_frame"])
                car_x = int(-200 + progress * (width + 280))
                
                # Lane positioning (Upper vs Lower lane)
                if v["lane"] == "upper":
                    car_y = 110
                else:
                    car_y = 250
                    
                car_w = 210
                car_h = 75

                # Main chassis
                cv2.rectangle(frame, (car_x, car_y), (car_x + car_w, car_y + car_h), v["color"], -1)
                cv2.rectangle(frame, (car_x, car_y), (car_x + car_w, car_y + car_h), (255, 255, 255), 2)

                # Cabin roof
                roof_x1 = car_x + 45
                roof_x2 = car_x + car_w - 40
                roof_y1 = car_y - 28
                roof_y2 = car_y
                pts = np.array([[roof_x1 - 15, roof_y2], [roof_x1 + 10, roof_y1], [roof_x2 - 10, roof_y1], [roof_x2 + 15, roof_y2]], np.int32)
                cv2.fillPoly(frame, [pts], (20, 24, 28))
                cv2.polylines(frame, [pts], True, (200, 200, 200), 1)

                # Wheels
                cv2.circle(frame, (car_x + 50, car_y + car_h), 18, (12, 12, 12), -1)
                cv2.circle(frame, (car_x + car_w - 45, car_y + car_h), 18, (12, 12, 12), -1)
                cv2.circle(frame, (car_x + 50, car_y + car_h), 7, (190, 190, 190), -1)
                cv2.circle(frame, (car_x + car_w - 45, car_y + car_h), 7, (190, 190, 190), -1)

                # License plate white rectangle
                plate_x1 = car_x + 55
                plate_y1 = car_y + car_h - 32
                plate_x2 = car_x + 155
                plate_y2 = car_y + car_h - 8
                cv2.rectangle(frame, (plate_x1, plate_y1), (plate_x2, plate_y2), (255, 255, 255), -1)
                cv2.rectangle(frame, (plate_x1, plate_y1), (plate_x2, plate_y2), (0, 0, 0), 2)
                
                # IND blue strip
                cv2.rectangle(frame, (plate_x1, plate_y1), (plate_x1 + 12, plate_y2), (210, 50, 0), -1)

                # License plate text
                cv2.putText(frame, v["plate"], (plate_x1 + 15, plate_y2 - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)

        out.write(frame)

    out.release()
    print(f"[+] Multi-lane multi-vehicle traffic video generated: {output_path}")

if __name__ == "__main__":
    create_sample_traffic_video()
