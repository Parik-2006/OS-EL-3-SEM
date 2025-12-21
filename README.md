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
The engine provides a visual "Head-to-Head" comparison for every CPU cycle:
* **Left Side:** What FCFS/SJF would have chosen (and why it failed).
* **Right Side:** What WDS chose (and why it won).

---

## ⚙️ System Workflow

```mermaid
graph TD;
    A[Input Process List] -->|Arrival Time, Burst, Prio| B(WDS Engine);
    B -->|Calculate Scores| C{Decision Logic};
    C -->|Old Job Waiting?| D[Aging Factor Boost];
    C -->|Short Job?| E[Efficiency Boost];
    C -->|Critical Priority?| F[Urgency Boost];
    D --> G[Final Score];
    E --> G;
    F --> G;
    G -->|Highest Score Wins| H[CPU Execution];
    H --> I[Visual Timeline & Logs];
