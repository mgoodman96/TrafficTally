import streamlit as st
import cv2
import os
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
import datetime

# Load YOLO model
model = YOLO("models/yolo11n.pt")

# Define class IDs for tracking
CLASSES_TO_DETECT = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

# Confidence threshold for counting
CONFIDENCE_THRESHOLD = 0.6

# Track unique objects
track_history = defaultdict(lambda: [])
unique_objects = set()
object_counts = {cls: 0 for cls in CLASSES_TO_DETECT}  # Persistent count

# Streamlit UI
st.title("🚦 TrafficTally - Traffic Activity Monitor for Urban Studies")
st.write("Upload a video file to process and analyze traffic activity.")

uploaded_file = st.file_uploader("📂 Upload a video", type=["mp4", "avi", "mov"])

# Create side-by-side buttons for UI layout
col1, col2 = st.columns(2)

# Buttons for process and stop
process_button = col1.button("▶️ Process Video")
stop_processing = col2.button("🛑 Stop Processing")

if uploaded_file is not None:
    # Save uploaded video to the app directory
    input_video_path = os.path.join(os.getcwd(), uploaded_file.name)
    with open(input_video_path, "wb") as f:
        f.write(uploaded_file.read())

    st.video(input_video_path)  # Show the uploaded video before processing

    if process_button:
        st.write("⏳ Processing video... Click '🛑 Stop Processing' anytime.")

        # Open the video file
        cap = cv2.VideoCapture(input_video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Define output file path in the **current directory**
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        processed_filename = f"{os.path.splitext(uploaded_file.name)[0]}_processed_{timestamp}.mp4"
        processed_video_path = os.path.join(os.getcwd(), processed_filename)

        # Ensure a valid codec is used
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(processed_video_path, fourcc, fps, (width, height))

        if not out.isOpened():
            st.error("⚠️ Error: VideoWriter failed to open. Process aborted.")
            cap.release()
            st.stop()

        # Streamlit UI elements
        progress_bar = st.progress(0)
        frame_placeholder = st.empty()  # Display the processed video frame
        tally_placeholder = st.empty()  # Live tally count updates here

        frame_number = 0
        FRAME_SKIP = 5  # Skip frames for efficiency
        processing_stopped = False

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            if stop_processing:
                processing_stopped = True
                break

            # Skip frames for efficiency
            if frame_number % FRAME_SKIP != 0:
                frame_number += 1
                continue

            # Run YOLO tracking
            results = model.track(frame, persist=True, tracker='bytetrack.yaml')

            # Get detection info
            if results[0].boxes.id is not None:
                boxes = results[0].boxes.xywh.cpu()  # Bounding boxes
                track_ids = results[0].boxes.id.int().cpu().tolist()  # Track IDs
                class_ids = results[0].boxes.cls.int().cpu().tolist()  # Class IDs
                confidences = results[0].boxes.conf.cpu().tolist()  # Confidence scores

                # Track and count unique objects
                for box, track_id, cls, conf in zip(boxes, track_ids, class_ids, confidences):
                    if cls in CLASSES_TO_DETECT and conf >= CONFIDENCE_THRESHOLD:
                        x, y, w, h = box

                        # Only count objects appearing in the lower 2/3 of the frame
                        if y + h / 2 >= height // 3:
                            track = track_history[track_id]
                            track.append((float(x), float(y)))  # Store track points
                            if len(track) > 30:  # Keep the last 30 frames of history
                                track.pop(0)

                            # Ensure unique objects are only counted once
                            if track_id not in unique_objects:
                                unique_objects.add(track_id)
                                object_counts[cls] += 1  # Persistent tally

                            # Draw bounding boxes and labels
                            label = f"{CLASSES_TO_DETECT[cls]} {object_counts[cls]}"
                            color = (0, 255, 0) if cls == 2 else (255, 0, 0) if cls == 1 else (0, 0, 255)
                            cv2.rectangle(frame, (int(x - w/2), int(y - h/2)), (int(x + w/2), int(y + h/2)), color, 2)
                            cv2.putText(frame, label, (int(x - w/2), int(y - h/2) - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Update **single live tally**
            tally_text = (
                f"🚗 Cars: {object_counts[2] + object_counts[3] + object_counts[5] + object_counts[7]} | "
                f"🚴 Bicycles: {object_counts[1]} | 🚶 People: {object_counts[0]}"
            )
            tally_placeholder.markdown(f"### {tally_text}")

            # Update frame in **Streamlit video player**
            frame_placeholder.image(frame, channels="BGR", use_container_width=True)

            # Write processed frame to output video
            out.write(frame)

            # Update progress bar
            progress_bar.progress(frame_number / frame_count)
            frame_number += 1

        # Release resources
        cap.release()
        out.release()

        if processing_stopped:
            st.warning("⚠️ Processing stopped early. The video is still available for download.")
            with open(processed_video_path, "rb") as file:
                st.download_button("📥 Download Partially Processed Video", data=file, file_name=processed_filename, mime="video/mp4")
        else:
            st.success(f"✅ Processing complete! Processed video saved as `{processed_filename}` in the current directory.")

            # Provide download link
            with open(processed_video_path, "rb") as file:
                st.download_button("📥 Download Processed Video", data=file, file_name=processed_filename, mime="video/mp4")
