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
| :--- | :--- | :--- |
| **🤖 AI Clusters** | Long training epochs block checkpoint saves. | **Yield Points:** WDS pauses training to run quick saves. |
| **📡 5G Edge** | 4K video streams block health alert packets. | **Packet Yielding:** Emergency packets get priority override. |
| **🚗 Autonomous OS** | Map downloads block Lidar obstacle detection. | **Context Switch:** Lidar gets instant CPU access. |
| **☁️ Cloud Functions** | Cold starts delay user login requests. | **Aging Factor:** Login requests gain score while waiting. |


{% extends "base.html" %}

{% block content %}
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>
    body {
        font-family: 'Poppins', sans-serif;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
        padding: 50px 20px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 30px;
    }

    .doc-card {
        background: #212529;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 30px;
        margin-bottom: 25px;
        color: #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .doc-card h3 {
        color: #0dcaf0;
        font-weight: 700;
        margin-bottom: 20px;
        border-bottom: 2px solid #444;
        padding-bottom: 10px;
    }

    .doc-card p,
    .doc-card li {
        color: #adb5bd;
        line-height: 1.7;
        font-size: 1rem;
    }

    .doc-card strong {
        color: #fff;
    }

    .step-box {
        background: #2c3034;
        border-left: 4px solid #198754;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 4px;
    }

    .step-title {
        color: #198754;
        font-weight: bold;
        display: block;
        margin-bottom: 5px;
    }

    .formula-box {
        background: #1a1a1a;
        border-left: 5px solid #ffc107;
        padding: 20px;
        font-family: 'Courier New', monospace;
        color: #ffc107;
        font-size: 1.1rem;
        border-radius: 5px;
        text-align: center;
        margin: 20px 0;
    }

    .table-custom {
        width: 100%;
        color: #e0e0e0;
        margin-top: 15px;
    }

    .table-custom th {
        border-bottom: 2px solid #0d6efd;
        color: #0d6efd;
        padding: 10px;
    }

    .table-custom td {
        border-bottom: 1px solid #444;
        padding: 10px;
        vertical-align: top;
    }

    .test-case {
        background: #dc3545;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85em;
        font-weight: bold;
        margin-right: 10px;
        text-transform: uppercase;
    }

    /* ================================
       COMPLETE PROJECT WORKFLOW
       ================================ */

    .workflow-section {
        background: #212529;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 30px;
        margin-bottom: 25px;
        color: #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .workflow-section h3 {
        color: #0dcaf0;
        font-weight: 700;
        margin-bottom: 20px;
        border-bottom: 2px solid #444;
        padding-bottom: 10px;
    }

    .workflow-image-container {
        background: #111;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 15px;
        overflow-x: auto;
        text-align: center;
    }

    .workflow-image {
        width: 100%;
        max-width: 1400px;
        height: auto;
        display: block;
        margin: 0 auto;
        border-radius: 5px;
    }

    .workflow-description {
        color: #adb5bd;
        line-height: 1.7;
        font-size: 0.95rem;
    }
</style>


<!-- HERO SECTION -->

<div class="hero-section text-center text-white">
    <h1 class="display-5 fw-bold mb-2">Project Documentation</h1>

    <p class="lead mb-4" style="color: #adb5bd;">
        Technical Breakdown, User Guide & Testing Instructions
    </p>

    <a class="btn btn-outline-light fw-bold" href="/">
        Back to Dashboard
    </a>
</div>


<div class="container">

    <!-- HOW TO RUN -->

    <div class="doc-card">

        <h3>How to Run the Simulator</h3>

        <div class="row">

            <div class="col-md-6">

                <div class="step-box">

                    <span class="step-title">
                        OPTION 1: Demo Mode
                    </span>

                    <p class="mb-0">
                        Loads a pre-set "Starvation Scenario"
                        (1 Long Job vs. 5 Short Jobs).
                        Use this to instantly visualize how WDS
                        prevents the long job from being blocked forever.
                    </p>

                </div>

            </div>


            <div class="col-md-6">

                <div class="step-box"
                     style="border-left-color: #ffc107;">

                    <span class="step-title"
                          style="color: #ffc107;">

                        OPTION 2: Custom Input

                    </span>

                    <p class="mb-0">
                        Enter your own Arrival Times, Burst Times,
                        and Priorities. Use this mode to test specific
                        homework problems or stress-test the algorithm.
                    </p>

                </div>

            </div>

        </div>

    </div>


    <!-- PROJECT PURPOSE -->

    <div class="doc-card">

        <h3>Project Purpose</h3>

        <p>
            <strong>Why was this built?</strong>
            Standard operating system schedulers like FCFS and SJF
            are rigid. They optimize for <em>either</em> speed
            <em>or</em> fairness, but never both.
        </p>

        <p>
            The goal of this project is to demonstrate a
            <strong>Hybrid Heuristic Algorithm (WDS)</strong>
            that uses a weighted formula to dynamically adapt its behavior.
            It proves that we can achieve high throughput (Speed)
            without sacrificing user experience (Fairness)
            in Cloud and 5G environments.
        </p>

    </div>


    <!-- WDS FORMULA -->

    <div class="doc-card">

        <h3>The WDS Formula</h3>

        <p>
            Instead of a rigid rule, WDS calculates a real-time score
            for every waiting process. The highest score wins.
        </p>

        <div class="formula-box shadow-sm">

            Score =
            (W_wait × WaitTime) +
            (W_burst × 30/BurstTime) +
            (W_prio × Priority)

        </div>


        <table class="table-custom">

            <thead>

                <tr>

                    <th width="30%">
                        Component
                    </th>

                    <th>
                        Why we need it? (The Logic)
                    </th>

                </tr>

            </thead>


            <tbody>

                <tr>

                    <td>
                        <strong class="text-info">
                            W_wait (Aging)
                        </strong>
                    </td>

                    <td>
                        Ensures that if a task waits for a long time,
                        its score grows massive, forcing the CPU to pick it.
                        (Solves Starvation).
                    </td>

                </tr>


                <tr>

                    <td>
                        <strong class="text-warning">
                            W_burst (Efficiency)
                        </strong>
                    </td>

                    <td>
                        Gives a bonus to short jobs.
                        This clears the queue quickly and lowers
                        average system latency.
                    </td>

                </tr>


                <tr>

                    <td>
                        <strong class="text-danger">
                            W_prio (Urgency)
                        </strong>
                    </td>

                    <td>
                        Allows critical tasks
                        (e.g., "System Crash Alert")
                        to override the math and run immediately.
                    </td>

                </tr>

            </tbody>

        </table>

    </div>


    <!-- TESTING -->

    <div class="doc-card"
         style="border: 1px solid #fd7e14;">

        <h3 style="color: #fd7e14; border-color: #fd7e14;">
            For Developers: What to Test?
        </h3>

        <p>
            If you are looking to find flaws or verify stability,
            try these specific edge cases in <strong>Custom Mode</strong>:
        </p>


        <ul style="list-style: none; padding-left: 0;">

            <li class="mb-3">

                <span class="test-case">
                    TEST 1
                </span>

                <strong>The Starvation Trap</strong>

                <br>

                Add one massive job (Burst=100)
                followed by many tiny jobs (Burst=1).

                <br>

                <em class="text-secondary">
                    Expected Result:
                </em>

                The massive job should eventually run
                due to the "Aging Factor".

            </li>


            <li class="mb-3">

                <span class="test-case">
                    TEST 2
                </span>

                <strong>The Priority Override</strong>

                <br>

                Add a long job, then add a short job
                with Priority=10.

                <br>

                <em class="text-secondary">
                    Expected Result:
                </em>

                The Priority=10 job should cut the line immediately.

            </li>


            <li class="mb-3">

                <span class="test-case">
                    TEST 3
                </span>

                <strong>The Zero Burst Crash</strong>

                <br>

                Try entering a Burst Time of 0.

                <br>

                <em class="text-secondary">
                    Expected Result:
                </em>

                The system should handle it gracefully
                (internally converts to minimal burst)
                without crashing.

            </li>

        </ul>

    </div>


    <!-- PROBLEM VS WDS SOLUTION -->

    <div class="row">

        <div class="col-md-6">

            <div class="doc-card"
                 style="border-top: 4px solid #dc3545;">

                <h3 class="text-danger"
                    style="border-color: #dc3545;">

                    The Problem

                </h3>

                <p>
                    <strong>FCFS:</strong>
                    Causes "Convoy Effect"
                    (UI freezes behind background tasks).
                </p>

                <p>
                    <strong>SJF:</strong>
                    Causes "Starvation"
                    (Long videos never process if short texts keep coming).
                </p>

            </div>

        </div>


        <div class="col-md-6">

            <div class="doc-card"
                 style="border-top: 4px solid #198754;">

                <h3 class="text-success"
                    style="border-color: #198754;">

                    The WDS Solution

                </h3>

                <p>
                    <strong>Hybrid Approach:</strong>
                    Acts like SJF when the system is busy
                    to clear traffic, but switches to Fairness mode
                    for old tasks.
                </p>

                <p>
                    <strong>Cooperative:</strong>
                    Uses "Yield Points" to allow high-priority interruptions.
                </p>

            </div>

        </div>

    </div>


    <!-- =========================================
         COMPLETE PROJECT WORKFLOW
         ========================================= -->

    <div class="workflow-section">

        <h3>
            Complete Project Workflow
        </h3>


        <div class="workflow-image-container">

            <img
                src="{{ url_for('static', filename='images/wds-workflow.png') }}"
                alt="WDS Scheduler Complete Workflow Diagram"
                class="workflow-image"
            >

        </div>


        <p class="workflow-description text-center mt-3 mb-0">

            This diagram shows the complete WDS Scheduler flow,
            from the user's request and Flask routing to Jinja2 rendering,
            JavaScript interaction, backend scheduling algorithms,
            JSON responses, and final visualizations.

        </p>

    </div>


    <!-- TECH STACK -->

    <div class="doc-card">

        <h3>
            Tech Stack
        </h3>


        <div class="row">

            <div class="col-md-6">

                <ul>

                    <li>
                        <strong>Backend Logic:</strong>
                        Python (Flask)
                    </li>

                    <li>
                        <strong>Algorithm:</strong>
                        Custom Heuristic (O(N) Complexity)
                    </li>

                </ul>

            </div>


            <div class="col-md-6">

                <ul>

                    <li>
                        <strong>Frontend:</strong>
                        HTML5, Bootstrap 5, Jinja2
                    </li>

                    <li>
                        <strong>Deployment:</strong>
                        Vercel (Serverless)
                    </li>

                </ul>

            </div>

        </div>

    </div>

</div>


<!-- FOOTER -->

<footer class="text-center text-secondary small py-4 mt-5 border-top border-secondary">

    © 2025 WDS Scheduler Project |
    Designed for OS Efficiency Research

</footer>

{% endblock %}

---

## 🛠️ Tech Stack
* **Backend:** Python (Flask)
* **Algorithm:** Weighted Dynamic Scoring (Custom Heuristic)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Visualization:** Chart.js (for Latency Graphs)

---

## 🚀 How to Run Locally

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/wds-scheduler.git](https://github.com/your-username/wds-scheduler.git)
    cd wds-scheduler
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Server**
    ```bash
    python app.py
    ```

4.  **Open in Browser**
    Visit `http://127.0.0.1:5000`

---

## ☁️ Deployment
This project is deployed on **Vercel**.
1.  Push code to GitHub.
2.  Import repository into Vercel.
3.  Vercel automatically detects the Python runtime via `vercel.json`.

---

### 📄 License
This project is for educational research purposes.

## 🤝 Contributing & Issues
This project is open for viewing. **Direct changes are restricted.**

* **Found a bug?** Please [Open a New Issue](https://github.com/YOUR-USERNAME/os-el2025/issues/new) and describe the problem.
* **Want to fix it?** Please Fork the repo and submit a Pull Request (PR) for review.