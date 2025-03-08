TrafficTally 🚦
Automated Traffic Analysis Using Computer Vision

TrafficTally is a computer vision-powered solution designed to automate and streamline urban traffic studies. By leveraging YOLOv11 Nano with ByteTrack, the system efficiently detects and tracks pedestrians, bicycles, and vehicles in traffic footage, significantly reducing manual review time.

📌 Project Overview
Traditional traffic analysis involves manually reviewing hours of footage to count and classify road users. This process is:
✅ Time-Consuming – Reviewing footage is tedious and resource-intensive.
✅ Inconsistent – Manual tracking can lead to human errors.
✅ Limited in Scalability – Analyzing large-scale traffic patterns is impractical without automation.

TrafficTally solves these challenges by:
🚀 Automatically detecting and counting objects in traffic videos.
⚡ Processing videos in parallel chunks using GPU acceleration.
📊 Providing structured output for urban planning and research.

🎥 Data Collection
We partnered with the University of Wisconsin-Milwaukee to analyze 72 hours of traffic footage from three intersections in Milwaukee. The dataset includes:

Diverse conditions: Variations in lighting, weather, and traffic density.
Multiple object types: Pedestrians, bicycles, and vehicles.
24 FPS video quality: Standard footage from traffic cameras.
⚙️ How It Works
TrafficTally automates the analysis of long-duration traffic videos through YOLOv11 Nano and ByteTrack for object detection and tracking. The system is optimized for:

Object Detection – Identifies pedestrians, bicycles, and vehicles.
Multi-Object Tracking (MOT) – Ensures accurate tallies by avoiding duplicate counts across frames.
Parallel Processing – GPU acceleration enables video processing in parallel chunks, speeding up analysis.
Output Generation – Produces structured counts and tracking data for further research.
🚀 Quick Start
🔧 Installation
Clone the repository and install dependencies:

bash
Copy
Edit
git clone https://github.com/mgoodman96/TrafficTally.git
cd TrafficTally
pip install -r requirements.txt
Ensure you have a compatible GPU with CUDA support for optimal performance.

▶️ Running the Model
To process a video:

bash
Copy
Edit
python process_video.py --input path/to/video.mp4 --output results.json --gpu
--gpu enables parallel processing using GPU.
Output is stored as JSON, detailing object counts over time.
📝 Sample Output
json
Copy
Edit
{
  "timestamp": "00:05:00",
  "pedestrians": 12,
  "bicycles": 3,
  "vehicles": 45
}