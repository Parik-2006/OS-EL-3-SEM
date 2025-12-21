# ⚡ WDS Scheduling Engine (Weighted Dynamic Scoring)

> **A Next-Generation Non-Preemptive CPU Scheduler Comparison Tool.**
> 
> *Designed for the 2025 Era of High-Performance Computing.*

![Home Page Dashboard](image_b141eb.jpg)

---

## 🎨 Visual Overview

### 1. The Core Dashboard
A modern, dark-mode interface that allows users to seamlessly switch between **Demo Scenarios** and **Custom Workloads**.

### 2. Real-World Application Analysis
Unlike standard simulators, WDS includes deep-dive case studies showing how the algorithm impacts modern tech like **5G, AI, and Autonomous Vehicles**.

![Real World Case Studies](image_b14cd1.jpg)

### 3. The "VS Battle" Decision Engine
*(Add a screenshot of your Demo Page 'VS Battle' Card here)*
> The engine provides a visual "Head-to-Head" comparison for every CPU cycle:
> * **Left Side:** What FCFS/SJF would have chosen (and why it failed).
> * **Right Side:** What WDS chose (and why it won).

---

## 📖 What is WDS?
The **Weighted Dynamic Scoring** Engine is a hybrid CPU scheduler designed to solve the "Trilemma" of non-preemptive scheduling:

1.  **Speed (Efficiency):** We want to finish short jobs fast (like SJF).
2.  **Fairness (Anti-Starvation):** We want to ensure old jobs eventually run (like FCFS).
3.  **Urgency (Priority):** We want VIP tasks to cut the line instantly.

### 🧮 The Logic
At every time step, the system calculates a **Score** for every waiting process. The highest score wins.

> **Score = (Aging × WaitTime) + (Efficiency × 1/Burst) + (Urgency × Priority)**

---

## 🚀 Key Features

### 🚦 Visual Ready Queue
A real-time timeline at the bottom of the screen shows exactly:
* **🟩 Green Box:** Process currently inside the CPU.
* **⬜ Grey Boxes:** Processes waiting in the Ready Queue.

### 🧪 Interactive Scenarios
We pre-loaded 4 "Killer Scenarios" where standard algorithms fail:
* **Scenario 1:** The Convoy Effect (One huge job blocking tiny ones).
* **Scenario 2:** The VIP Emergency (Critical task stuck behind a long task).
* **Scenario 3:** Starvation Rescue (Old job being ignored).
* **Scenario 4:** The Smart Trade-off (Balancing all factors).

---

## 🛠️ How to Run Locally

**1. Install Dependencies**
You only need Python and Flask.
```bash
pip install flask
