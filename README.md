# 🚀 WDS: Weighted Dynamic Scheduler

> **A Next-Generation Non-Preemptive Scheduler for High-Performance Computing.**

![Status](https://img.shields.io/badge/Status-Research%20Prototype-blue)
![Python](https://img.shields.io/badge/Python-3.x-yellow)
![Flask](https://img.shields.io/badge/Backend-Flask-black)
![Algorithm](https://img.shields.io/badge/Algorithm-Weighted%20Dynamic%20Scoring-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 Project Objective

**WDS (Weighted Dynamic Scheduler)** is a hybrid, non-preemptive CPU scheduling algorithm designed to solve the fundamental trade-off between **speed** and **fairness** found in traditional scheduling algorithms.

Unlike standard algorithms such as **FCFS** and **SJF**, WDS dynamically evaluates every waiting process using a weighted score.

### 🎯 Core Goals

- Prevent **Starvation**
- Reduce **Average Waiting Time**
- Improve **System Throughput**
- Support **Priority-based execution**
- Dynamically balance **fairness and efficiency**
- Demonstrate practical applications in **AI, 5G, Autonomous Vehicles, and Cloud Computing**

---

# 🧠 The WDS Algorithm

At every scheduling decision point, WDS calculates a score for every process currently waiting in the ready queue.

The process with the **highest score** is selected for execution.

### 📐 WDS Formula

```text
Score =
(W_wait × WaitTime)
+
(W_burst × 30/BurstTime)
+
(W_prio × Priority)
