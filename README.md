# ⚡ WDS Scheduling Engine (Weighted Dynamic Scoring)

> **A Next-Generation Non-Preemptive CPU Scheduler.**
> *Designed for High-Performance Computing, Cloud Clusters, and Autonomous Systems.*

---

## 📖 Project Objective

Modern computing environments (like 5G Edge Gateways and AI Training Clusters) suffer from inefficiencies when using standard CPU schedulers:

* **FCFS (First-Come-First-Serve):** causes the "Convoy Effect" (UI freezes behind background tasks).
* **SJF (Shortest Job First):** causes "Starvation" (Long tasks never run).

**The Solution:**
The **Weighted Dynamic Score (WDS)** algorithm. It utilizes a **Cooperative Multitasking Architecture** where tasks yield control at specific checkpoints. The scheduler calculates a dynamic score based on **Efficiency**, **Fairness**, and **Priority** to decide the next task.

---

## ⚙️ The WDS Formula

The engine calculates a score ($S$) for every waiting process in real-time:

$$S = (W_{wait} \times T_{waiting}) + (W_{burst} \times \frac{30}{T_{burst}}) + (W_{prio} \times P_{level})$$

* **$W_{wait}$ (Aging Factor):** Prevents starvation by boosting the score of waiting tasks.
* **$W_{burst}$ (Efficiency):** Favors short jobs to reduce system latency.
* **$W_{prio}$ (Urgency):** Allows critical operations (e.g., "Emergency Braking") to override standard logic.

---

## 🌍 Real-World Scenarios

This project simulates WDS performance in four specific industries:

| Industry | The Problem | The WDS Solution |
| --- | --- | --- |
| **🤖 AI Clusters** | Long training epochs block checkpoint saves. | **Yield Points:** WDS pauses training to run quick saves. |
| **📡 5G Edge** | 4K video streams block health alert packets. | **Packet Yielding:** Emergency packets get priority override. |
| **🚗 Autonomous OS** | Map downloads block Lidar obstacle detection. | **Context Switch:** Lidar gets instant CPU access. |
| **☁️ Cloud Functions** | Cold starts delay user login requests. | **Aging Factor:** Login requests gain score while waiting. |

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Algorithm:** Weighted Dynamic Scoring (Custom Heuristic)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Visualization:** Chart.js (for Latency Graphs)

---

## 🚀 How to Run Locally

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/wds-scheduler.git
cd wds-scheduler

```


2. **Install Dependencies**
```bash
pip install -r requirements.txt

```


3. **Run the Server**
```bash
python app.py

```


4. **Open in Browser**
Visit `http://127.0.0.1:5000`

---

## ☁️ Deployment

This project is live and deployed on **Vercel**.

1. Push code to GitHub.
2. Import repository into Vercel.
3. Vercel automatically detects the Python runtime via `vercel.json`.

* **Live Link:** [https://osel2025.vercel.app/](https://osel2025.vercel.app/)

---

### 👨‍🏫 Acknowledgments

This project was developed as part of the **Operating Systems (OS-EL)** curriculum at **R V College of Engineering**. Special thanks to:

* **Prof. Savitri Kulkarni**, Assistant Professor, Dept. of CSE, RVCE.
* **Dr. Prapulla S B**, Associate Professor, Dept. of CSE, RVCE.

---

### 📄 License

This project is for educational research purposes.

## 🤝 Contributing & Issues

This project is open for viewing. **Direct changes are restricted.**

* **Found a bug?** Please [Open a New Issue](https://github.com/YOUR-USERNAME/os-el2025/issues/new) and describe the problem.
* **Want to fix it?** Please Fork the repo and submit a Pull Request (PR) for review.
