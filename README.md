# ⚡ WDS Scheduling Engine (Weighted Dynamic Scoring)

> **A Next-Generation Non-Preemptive CPU Scheduler Comparison Tool.**
> 
> *Designed for the 2025 Era of High-Performance Computing.*

---

## ⚙️ System Workflow (Cooperative Architecture)

WDS operates in a **Cooperative Multitasking Environment**. Long tasks do not lock the CPU indefinitely; instead, they "yield" at specific checkpoints to allow the scheduler to re-evaluate urgency.

```mermaid
graph TD;
    A[Long Task Running] -->|Reach Yield Point| B{WDS Check: Any Higher Score?};
    B -->|No| C[Continue Long Task];
    B -->|Yes! Critical Job Waiting| D[Context Switch];
    D --> E[Run Critical Job];
    E -->|Job Done| A;