# ⚡ WDS Scheduling Engine (Weighted Dynamic Scoring)

> **A Next-Generation Non-Preemptive CPU Scheduler Comparison Tool.**
> 
> *Designed for the 2025 Era of High-Performance Computing.*

---

## ⚙️ System Workflow (Visual Logic)

```mermaid
graph TD;
    Start[New Process Arrives] --> Q{Add to Ready Queue};
    Q --> A[Calculate WDS Score];
    A -->|Factor 1| B(Aging: Time Waiting);
    A -->|Factor 2| C(Efficiency: 1 / Burst Time);
    A -->|Factor 3| D(Urgency: User Priority);
    B & C & D --> E[Final Score];
    E --> F{Highest Score?};
    F -->|Yes| G[Dispatch to CPU];
    F -->|No| H[Wait & Increase Aging];
    G --> I[Execute & Generate VS Log];
