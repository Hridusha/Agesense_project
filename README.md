# AgeSense

A web-based application built using *Flask*, **Pandas**, and *Matplotlib* to analyze and visualize age and gender data.

---

## Features

- Upload and analyze age-based data in CSV format  
- Display uploaded data in a structured table  
- Show key statistics:
  - Average and median age
  - Gender distribution
  - Age group distribution (0–18, 19–35, 36–60, 60+)
- Generate visualizations:
  - Bar chart
  - Pie chart
  - Histogram
- User-friendly and responsive interface

---

## Setup

### Step 1: Install required packages (ensure Python is installed)
```bash
pip install flask pandas matplotlib
```

### Step 2: Run the application
```bash
python app.py
```

### Step 3: Open your browser and go to:
```
http://localhost:5000
```

### Step 4: Upload your CSV file in the following format:
```
Name,Age,Gender
John Doe,28,Male
Jane Smith,34,Female
```

---
