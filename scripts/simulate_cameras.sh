#!/bin/bash

# simulate_cameras.sh
# This script simulates the Gujarat Police Hackathon test case by streaming
# a sample looping video to the local MediaMTX server to mimic 50 cameras.

# Create a dummy video file if one doesn't exist (10 seconds of noise/test pattern)
if [ ! -f "sample.mp4" ]; then
    echo "Creating a sample video file..."
    # Generates a 10-second test video at 720p 25fps
    ffmpeg -f lavfi -i testsrc=duration=10:size=1280x720:rate=25 -c:v libx264 -preset ultrafast -t 10 sample.mp4
fi

echo "Starting MediaMTX simulated streams..."
echo "MediaMTX should already be running via 'docker-compose up -d'"
echo ""

# For demonstration, we will spin up 5 simulated cameras instead of 50 to save local CPU.
# In a real stress test, change this to 50.
NUM_CAMERAS=5

for i in $(seq 1 $NUM_CAMERAS); do
    CAM_ID=$(printf "cam_%03d" $i)
    echo "Starting stream for $CAM_ID (rtsp://localhost:8554/stream/$CAM_ID)..."
    
    # Push looping video to MediaMTX in the background
    # -stream_loop -1 loops the video infinitely
    ffmpeg -re -stream_loop -1 -i sample.mp4 -c copy -f rtsp -rtsp_transport tcp rtsp://localhost:8554/stream/$CAM_ID > /dev/null 2>&1 &
done

echo ""
echo "✅ Started $NUM_CAMERAS simulated camera streams."
echo "To view a stream in VLC: rtsp://localhost:8554/stream/cam_001"
echo "To view via WebRTC (browser): http://localhost:8889/stream/cam_001/whep"
echo ""
echo "To stop the streams later, run: pkill -f 'ffmpeg -re -stream_loop'"
