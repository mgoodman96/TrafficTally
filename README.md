# TrafficTally 🚦  

**Automated Traffic Analysis Using Computer Vision**  

**Project by Michael Goodman in part with the Applied Data Science Program at The University of Chicago**

TrafficTally is a computer vision-powered solution designed to automate and streamline urban traffic studies. By leveraging **YOLOv11 Nano with ByteTrack**, the system efficiently detects and tracks pedestrians, bicycles, and vehicles in traffic footage, significantly reducing manual review time.

## 📌 Project Overview  

Traditional traffic analysis involves manually reviewing hours of footage to count and classify road users. This process is:  
✅ **Time-Consuming** – Reviewing footage is tedious and resource-intensive.  
✅ **Inconsistent** – Manual tracking can lead to human errors.  
✅ **Limited in Scalability** – Analyzing large-scale traffic patterns is impractical without automation.  

TrafficTally solves these challenges by:  
🚀 **Automatically detecting and counting objects** in traffic videos.  
⚡ Optional **Processing videos in parallel** using GPUs.  
📊 **Providing structured output** for urban planning and research.  

---

## 🎥 Data Collection  

Partnered with the **University of Wisconsin-Milwaukee** to analyze **72 hours of traffic footage** from **three intersections** in Milwaukee. The dataset includes:  
- **Diverse conditions**: Variations in lighting, weather, and traffic density.  
- **Multiple object types**: Pedestrians, bicycles, and vehicles.  
- **24 FPS video quality**: Standard footage from traffic cameras.  

---

## ⚙️ How It Works  

TrafficTally automates the analysis of long-duration traffic videos through **YOLOv11 Nano** and **ByteTrack** for object detection and tracking. The system is optimized for:  

1. **Object Detection** – Identifies pedestrians, bicycles, and vehicles.  
2. **Multi-Object Tracking (MOT)** – Ensures accurate tallies by avoiding duplicate counts across frames.  
3. **Output Generation** – Produces structured counts and tracking data for further research.  

---

## 🚀 Quick Start  

### 🔧 Installation  

Clone the repository and install dependencies:  
```bash
git clone https://github.com/mgoodman96/TrafficTally.git
cd TrafficTally
pip install -r requirements.txt
streamlit run TrafficTally.py
```


