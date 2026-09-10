import cv2
import os
import subprocess
import imageio_ffmpeg
import PIL.Image

exe = imageio_ffmpeg.get_ffmpeg_exe()
base_dir = r"d:\Hackathon\Hackathon"
frontend_out = os.path.join(base_dir, 'frontend', 'public', 'videos')
backend_out = os.path.join(base_dir, 'backend', 'static', 'videos')
os.makedirs(frontend_out, exist_ok=True)
os.makedirs(backend_out, exist_ok=True)

configs = [
    {
        'name': 'police_cctv',
        'src': os.path.join(base_dir, 'scratch_plate_license_plate.mp4'),
        'start_frame': 5,
        'frame_count': 90
    },
    {
        'name': 'municipal_cctv',
        'src': os.path.join(base_dir, 'scratch_anpr_mycarplate.mp4'),
        'start_frame': 35,
        'frame_count': 90
    },
    {
        'name': 'gsrtc_cctv',
        'src': os.path.join(base_dir, 'scratch_anpr_mycarplate.mp4'),
        'start_frame': 185,
        'frame_count': 65
    },
    {
        'name': 'health_cctv',
        'src': os.path.join(base_dir, 'scratch_plate_license_plate.mp4'),
        'start_frame': 45,
        'frame_count': 90
    },
    {
        'name': 'panchayat_cctv',
        'src': os.path.join(base_dir, 'scratch_anpr_mycarplate.mp4'),
        'start_frame': 110,
        'frame_count': 90
    }
]

for cfg in configs:
    name = cfg['name']
    src = cfg['src']
    start_frame = cfg['start_frame']
    frame_count = cfg['frame_count']
    print(f"Extracting clean 720p HD footage for {name} from {src}...")

    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        print(f"Error opening {src}")
        continue

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frames = []
    f_idx = 0

    while cap.isOpened() and f_idx < frame_count:
        ret, frame = cap.read()
        if not ret:
            break
        # Resize to clean standard 720p HD (1280x720) - completely unblemished, pure real video
        frame_hd = cv2.resize(frame, (1280, 720))
        frames.append(frame_hd)
        f_idx += 1

    cap.release()

    if not frames:
        print(f"No frames read for {name}")
        continue

    # Write temporary AVI
    temp_avi = os.path.join(base_dir, f"temp_clean_{name}.avi")
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(temp_avi, fourcc, 22, (1280, 720))
    for fr in frames:
        out.write(fr)
    out.release()

    # Transcode to high-efficiency, clean H.264 MP4
    mp4_out = os.path.join(frontend_out, f"{name}.mp4")
    cmd = [
        exe, '-y',
        '-i', temp_avi,
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-profile:v', 'baseline',
        '-preset', 'fast',
        '-crf', '21',
        '-movflags', '+faststart',
        '-an',
        mp4_out
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    # Save clean animated WebP fallback
    webp_out = os.path.join(frontend_out, f"{name}.webp")
    pil_frames = [PIL.Image.fromarray(cv2.cvtColor(cv2.resize(fr, (854, 480)), cv2.COLOR_BGR2RGB)) for fr in frames]
    pil_frames[0].save(webp_out, save_all=True, append_images=pil_frames[1:], duration=45, loop=0, quality=85)

    # Copy to backend static directory
    import shutil
    shutil.copyfile(mp4_out, os.path.join(backend_out, f"{name}.mp4"))
    shutil.copyfile(webp_out, os.path.join(backend_out, f"{name}.webp"))

    if os.path.exists(temp_avi):
        os.remove(temp_avi)

    print(f"DONE: {name} clean video generated (MP4: {os.path.getsize(mp4_out)//1024} KB, WebP: {os.path.getsize(webp_out)//1024} KB)")

print("\nAll 5 clean real-world surveillance video feeds generated successfully without any burned-in graphics!")
