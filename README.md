# BMI-Calculator-Made-Using-Python-With-GUI-Desktop-App

# 🫀 BMI Calculator

A clean, modern **Body Mass Index (BMI) Calculator** desktop application built with Python and Tkinter. Supports both Metric and Imperial units with a live color-coded gauge bar.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-informational)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 What is BMI?

**Body Mass Index (BMI)** is a numerical value calculated from a person's **weight and height**. It is widely used as a simple screening tool to indicate whether a person is underweight, normal weight, overweight, or obese.

### Formula

| Unit System | Formula |
|---|---|
| **Metric** | BMI = weight (kg) ÷ height² (m) |
| **Imperial** | BMI = 703 × weight (lb) ÷ height² (in) |

### BMI Categories

| BMI Range | Category |
|---|---|
| Below 18.5 | 🔵 Underweight |
| 18.5 – 24.9 | 🟢 Normal weight |
| 25.0 – 29.9 | 🟡 Overweight |
| 30.0 – 34.9 | 🟠 Obese (Class I) |
| 35.0 – 39.9 | 🔴 Obese (Class II) |
| 40.0 and above | 🔴 Obese (Class III) |

> ⚠️ BMI is a general screening tool and does not account for factors like muscle mass, bone density, age, or gender. Always consult a healthcare professional for medical advice.

---

## ✨ Features

- 🔄 Toggle between **Metric (kg / cm)** and **Imperial (lb / ft / in)** units
- 🎨 Color-coded **BMI gauge bar** with a live needle indicator
- 🏷️ Displays **BMI category** with matching color
- 📊 Shows your **healthy weight range** and how far you are from it
- ⌨️ Keyboard shortcut — press **Enter** to calculate
- 🌑 Clean dark-themed UI
- 🖼️ Custom app icon

---

## 🛠️ Requirements

- **Python 3.8 or higher**
- **Tkinter** — comes built into Python by default (no extra install needed)

To verify Python is installed:
```bash
python --version
```

To verify Tkinter is available:
```bash
python -m tkinter
```
> A small test window should pop up if Tkinter is working correctly.

---

## 📁 Project Structure

```
BMI-Calculator/
│
├── bmi_calculator.py   # Main application file
├── bmi_icon.ico        # App icon
└── README.md           # Project documentation
```

> ⚠️ Make sure `bmi_icon.ico` is in the **same folder** as `bmi_calculator.py`, otherwise the app will throw an error on launch.

---

## 🚀 How to Run

### Option 1 — Run directly with Python

1. Clone or download this repository:
```bash
git clone https://github.com/your-username/bmi-calculator.git
```

2. Navigate to the project folder:
```bash
cd bmi-calculator
```

3. Run the script:
```bash
python bmi_calculator.py
```

The application window will open immediately. No extra libraries needed.

---

### Option 2 — Build a standalone `.exe` (Windows)

Want to run it by just **double-clicking** without needing Python installed?

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller --onefile --windowed --icon=bmi_icon.ico bmi_calculator.py
```

3. Open the `dist/` folder that gets created — your `bmi_calculator.exe` will be inside. Double-click to launch.

> 💡 **Windows Defender note:** Windows may flag the `.exe` as a false positive. This is a known issue with PyInstaller builds. Go to **Windows Security → Protection History** and click **Allow** to run it.

---

## 👤 Author

Made by **AA** — Self-Made Python Project
