# ⚡ WDS Scheduling Engine (Weighted Dynamic Scoring)

> **A Next-Generation Non-Preemptive CPU Scheduler Comparison Tool.** > Built with **Python (Flask)**, **JavaScript**, and **Chart.js**.

![Home Page Screenshot](image_b141eb.jpg)

## 📖 Overview
The **WDS (Weighted Dynamic Scoring)** Engine is a custom CPU scheduling algorithm designed to solve the flaws of standard non-preemptive algorithms like **FCFS** (First-Come-First-Serve) and **SJF** (Shortest Job First).

While FCFS suffers from the **Convoy Effect** and SJF suffers from **Starvation**, WDS uses a hybrid formula to balance **Efficiency (Speed)**, **Fairness (Aging)**, and **Urgency (Priority)** dynamically at every time step.

## 🧮 The Core Algorithm
At every time quantum, the scheduler calculates a score for every waiting process. The process with the highest score wins the CPU.

$$Score = (W_{wait} \times \text{WaitTime}) + (W_{burst} \times \frac{1}{\text{BurstTime}}) + (W_{prio} \times \text{Priority})$$

* **$W_{wait}$ (Aging Factor):** Prevents starvation by boosting the score of old jobs.
* **$W_{burst}$ (Efficiency Factor):** Mimics SJF by favoring short jobs to maximize throughput.
* **$W_{prio}$ (Urgency Factor):** Allows critical/VIP tasks to cut the line immediately.

---

## 🚀 Features

### 1. Interactive Demo Mode ("The VS Battle")
* Runs 4 pre-built scenarios (Convoy Effect, VIP Emergency, Starvation, etc.).
* **Smart Commentary Engine:** Explains *why* WDS made a specific choice compared to FCFS/SJF (e.g., *"FCFS wanted the slow job, but WDS picked the fast one"*).
* **Visual Ready Queue:** A real-time timeline showing exactly who is in the CPU and who is waiting.

### 2. Custom Workload Designer
* Input your own list of processes (Arrival Time, Burst Time, Priority).
* Generates instant Gantt Charts and "VS Battle" logs for your custom data.

### 3. Real-World Case Studies (2025 Era)
* Explains how WDS applies to modern tech:
    * 🤖 **AI Training Clusters:** Handling Checkpoints vs. Epochs.
    * 📡 **5G Edge Gateways:** Prioritizing Health Alerts over Video Streaming.
    * 🚗 **Autonomous Vehicles:** Lidar Obstacle Detection vs. Map Downloads.
* Includes **clickable references** to real research papers (Google Scholar/IEEE).

---

## 🛠️ Installation & Usage

### Prerequisites
* Python 3.x
* Pip

### Steps
1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/wds-scheduler.git](https://github.com/your-username/wds-scheduler.git)
    cd wds-scheduler
    ```

2.  **Install Dependencies**
    ```bash
    pip install flask
    ```

3.  **Run the Application**
    ```bash
    python app.py
    ```

4.  **Open in Browser**
    Visit `http://127.0.0.1:5000` to see the dashboard.

---

## 📂 Project Structure

```text
WDS_Web_Project/
│
├── app.py                # Python Backend (Algorithm Logic & Routes)
├── README.md             # Documentation
│
├── static/
│   └── css/
│       └── style.css     # Custom Styling (Dark Mode)
│
└── templates/
    ├── base.html         # Master Layout (Navbar & Scripts)
    ├── index.html        # Home Page (Landing & Case Studies)
    ├── demo.html         # Demo Mode (Scenarios & Visuals)
    ├── custom.html       # User Input Mode
    └── real_world.html   # Case Study Detail Pages
