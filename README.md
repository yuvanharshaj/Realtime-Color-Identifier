# Real-Time Color Identification Using OpenCV (Python)

A real-time color detection project built in Python using OpenCV.  
The system captures live video from the webcam, detects the color inside a sampling region, and displays the closest matching color name along with its RGB values — all in real-time.

This project is ideal for:
- Computer vision beginners
- OpenCV learning projects
- VTU mini-projects / lab submissions
- Real-time color sampling applications

---

## Features

### 1. Real-time webcam color detection  
Continuously reads frames from your webcam and extracts the color inside a small sampling box.

### 2. LAB color space matching  
More accurate than raw RGB matching — closer to how humans perceive color.

### 3. ΔE2000 (CIEDE2000) color difference  
Industry-standard formula for high-precision color comparison.

### 4. Clean minimal UI  
- Small sampling box  
- Color dot preview  
- Text label with detected color name + RGB values  

### 5. Reliable window closing  
The program exits cleanly when the user presses `Q` or clicks the window close (X) button.

### 6. 138-color dataset included  
Matches against a wide range of real-world colors.

---

## Project Structure
```bash
RealTime-Color-Identification/
│
├── src/
│ └── color_detector.py # Main program
│
├── data/
│ └── color_data.csv # 138-color dataset
│
├── assets/ # (Optional) Screenshots / output images
│
├── README.md # Project documentation
└── .gitignore # Ignore venv, cache, etc.
```
---


---

## Requirements

Install the following Python packages:

```bash
pip install opencv-python numpy pandas
```
Python 3.8+ recommended

---

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/<your-username>/RealTime-Color-Identification.git
```

2. Move into the project folder:
```bash
cd RealTime-Color-Identification
```

3. Run the script:
```bash
python src/color_detector.py
```

4. Controls:
```bash
Q → Quit the program
X button → Also quits safely
```

---

## How it Works

1. Capture frame
OpenCV captures frames from your webcam.

2. Sampling Region
A small 8×8 square at the center of the frame is used to calculate the average color.

3. Convert to LAB
The average BGR value is converted to LAB color space.

4. Color Matching
The detected LAB value is compared against all 138 colors in the dataset using the ΔE2000 formula:
```bash
Smaller ΔE2000 = more accurate match
```
5. Display UI
- Small colored dot (preview)
- Color name
- RGB values

---

## Application

1. Object color recognition
2. Color picking tool for designers
3. Robotics (color-based navigation)
4. Educational CV demonstrations
5. Real-time color-based automation

---

## Author

Yuvan Harshaj
Real-Time Color Identification Project (Python + OpenCV)

Feel free to reach out for issues or contributions!

---