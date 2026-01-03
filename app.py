from flask import Flask, render_template, request, jsonify
import copy

app = Flask(__name__)

# --- CORE ALGORITHM (WDS) - FINAL TUNED WEIGHTS ---
def calculate_wds_score(process, current_time):  # Define the function that calculates a score for a single process
    # WEIGHTS (Tuned for Starvation Rescue & yielding)
    W_WAIT = 3.0    # Set importance of Waiting Time (High to prevent starvation)
    W_BURST = 1.0   # Set importance of Burst Time (Standard for efficiency)
    W_PRIO = 1.0    # Set importance of Priority (Standard for user rank)

    wait_time = current_time - process['at']  # Calculate how long the process has been waiting since arrival
    if wait_time < 0: wait_time = 0           # Ensure wait time isn't negative (if simulations start early)

    # Scaling 30: Short Job (2s) = 15 pts. Long Job (15s) = 2 pts. Gap = 13.
    burst_score = 30 / process['bt'] if process['bt'] > 0 else 0  # Calculate efficiency score (smaller burst = higher score)
    prio_score = process['prio'] * 10                             # Calculate urgency score (multiply by 10 to give it impact)

    score = (W_WAIT * wait_time) + (W_BURST * burst_score) + (W_PRIO * prio_score)  # Sum up the weighted scores to get the final value
    return round(score, 2)  # Return the result rounded to 2 decimal places for clean display

# --- ROUTE DEFINITIONS (The Traffic Controller) ---

@app.route('/')  # TRIGGER: Watch for users visiting the Home URL (e.g., website.com/)
def index():     # ACTION: Run this function when that URL is hit
    return render_template('index.html')  # RESULT: Find 'index.html' and show it to the user

@app.route('/demo')  # TRIGGER: Watch for users visiting the Demo URL (e.g., website.com/demo)
def demo():          # ACTION: Run this function for the demo page
    return render_template('demo.html')  # RESULT: Find 'demo.html' and show it to the user

@app.route('/custom')  # TRIGGER: Watch for users visiting the Custom Input URL (e.g., website.com/custom)
def custom():          # ACTION: Run this function for the custom input page
    return render_template('custom.html')  # RESULT: Find 'custom.html' and show it to the user

@app.route('/docs')  # TRIGGER: Watch for users visiting the Documentation URL (e.g., website.com/docs)
def docs():          # ACTION: Run this function for the docs page
    return render_template('readme.html')  # RESULT: Find 'readme.html' and show it to the user

# --- REAL-WORLD SCENARIOS DATABASE ---
# REMOVED: Icons and Emojis
scenarios_db = {
    'ai': {
        'title': 'AI Model Training Clusters',
        'problem': 'Deep Learning models train in massive "Epochs" (hours long). Standard schedulers (FCFS) lock the GPU for the entire epoch. If a short "Checkpoint Save" (10s) arrives, it gets blocked, risking data loss.',
        'solution': 'WDS uses Cooperative Multitasking. The training process yields control after every "Batch". WDS sees the "Checkpoint Save" has a high Efficiency Score and swaps it in immediately.',
        'stats': {'labels': ['Checkpoint Lag (FCFS)', 'Checkpoint Lag (WDS)'], 'data': [120, 5]}, 
        'refs': [{'title': 'Optimizing Checkpointing in Deep Learning (arXiv)', 'source': 'Cornell University (arXiv)', 'url': 'https://arxiv.org/abs/2011.01340'}]
    },
    '5g': {
        'title': '5G/6G Edge Gateways',
        'problem': 'Edge routers process mixed traffic. A 4K Netflix stream (High Bandwidth) blocks a tiny "Heart Attack Alert" packet (Low Latency) for 200ms—fatal in remote surgery.',
        'solution': 'WDS implements Packet-Level Yielding. The Health Alert (Priority 10) overrides the video stream immediately, ensuring < 10ms latency.',
        'stats': {'labels': ['Emergency Latency (FCFS)', 'Emergency Latency (WDS)'], 'data': [450, 12]},
        'refs': [{'title': 'Scheduling for 5G URLLC Traffic', 'source': 'IEEE Xplore', 'url': 'https://ieeexplore.ieee.org/document/8647610'}]
    },
    'auto': {
        'title': 'Autonomous Vehicle OS',
        'problem': 'A "Map Download" (Long Task) blocks "Lidar Obstacle Detection" (Critical Task). A 300ms delay at 60mph means the car travels 8 meters blind.',
        'solution': 'WDS uses Yield Points. It pauses the Map Download to ask: "Is anything urgent waiting?". WDS forces the Lidar task to run instantly.',
        'stats': {'labels': ['Braking Reaction (Standard)', 'Braking Reaction (WDS)'], 'data': [300, 45]},
        'refs': [{'title': 'Mixed Criticality Scheduling in Automotive', 'source': 'ResearchGate', 'url': 'https://www.researchgate.net/publication/322657731_Scheduling_of_Mixed-Criticality_Applications_in_Real-Time_Systems'}]
    },
    'cloud': {
        'title': 'Serverless Cloud Functions',
        'problem': 'In AWS Lambda, "Cold Starts" hang a user\'s "Login Request" if the server is busy compiling a background job. This kills user retention.',
        'solution': 'WDS utilizes the Aging Factor. As the Login Request waits, its score grows. WDS injects it next, preventing UI freeze.',
        'stats': {'labels': ['Cold Start Delay (FIFO)', 'Cold Start Delay (WDS)'], 'data': [2500, 300]}, 
        'refs': [{'title': 'Peeking Behind the Curtains of Serverless', 'source': 'USENIX ATC', 'url': 'https://www.usenix.org/conference/atc18/presentation/wang-liang'}]
    }
}

@app.route('/real-world/<scenario_id>')  # TRIGGER: Listen for ANY URL starting with /real-world/ (e.g., /real-world/ai) and capture the last part as 'scenario_id'
def real_world(scenario_id):             # ACTION: Run this function, passing the captured ID (e.g., "ai" or "auto") as a variable
    data = scenarios_db.get(scenario_id) # LOOKUP: Search the database dictionary for the key that matches the ID
    if not data: return "Scenario not found", 404  # SAFETY: If the ID doesn't exist (e.g., /real-world/pizza), show an error instead of crashing
    return render_template('real_world.html', data=data)  # RENDER: Load the generic template and fill it with the specific data found

# --- SIMULATION API (The Engine) ---
@app.route('/api/simulate', methods=['POST'])   # TRIGGER: Listen for POST requests sent to '/api/simulate'
def simulate():                                 # ACTION: Start the simulation function when triggered
    processes = request.json['processes']       # INPUT: specific list of processes sent by the user/browser

    # --- 1. DATA RESET (Cleaning the Slate) ---
    for p in processes:                         # LOOP: Go through every process in the list
        p['rem_bt'] = p['bt']                   # RESET: Set "Remaining Burst" equal to original "Burst" (Start fresh)
        p['wait'] = 0                           # RESET: Set Wait Time to 0
        p['tat'] = 0                            # RESET: Set Turnaround Time to 0
        p['start_time'] = -1                    # RESET: Mark as "Not Started" (-1)
        p['finish_time'] = -1                   # RESET: Mark as "Not Finished" (-1)

    # --- 2. SIMULATION VARIABLES (The State) ---
    current_time = 0                            # CLOCK: Initialize the System Clock to 0
    completed = 0                               # COUNTER: Track how many jobs have finished
    n = len(processes)                          # CONSTANT: Total number of processes to run
    timeline_wds = []                           # OUTPUT: Empty list to store Gantt Chart data
    decision_log = []                           # OUTPUT: Empty list to store the "Decision Log" history

    # --- 3. CLONING (Independent Universes) ---
    procs_fcfs = copy.deepcopy(processes)       # CLONE: Create a totally separate copy for the FCFS algorithm
    procs_sjf = copy.deepcopy(processes)        # CLONE: Create a totally separate copy for the SJF algorithm

    wds_processes = copy.deepcopy(processes)    # CLONE: Create the copy we will actually use for WDS
    wds_processes.sort(key=lambda x: x['at'])   # SORT: Organize them by Arrival Time first (good practice)
    active_procs = [p for p in wds_processes]   # WORK LIST: The working list of processes to modify
    
    last_process_id = None                      # MEMORY: Variable to remember who used the CPU last step

    # --- 4. THE MAIN CPU LOOP (Step-by-Step) ---
    while completed < n:                        # LOOP: Keep running as long as completed jobs < total jobs
        
        # FILTER: Find jobs that have Arrived (at <= now) AND are not finished (rem_bt > 0)
        available = [p for p in active_procs if p['at'] <= current_time and p['rem_bt'] > 0]
        
        if not available:                       # CHECK: Is the ready queue empty?
            current_time += 1                   # ACTION: If empty, idle the CPU (fast forward 1 sec)
            continue                            # SKIP: Restart the loop to check again

        # --- 5. SCORING (The WDS Algorithm) ---
        candidates = []                         # LIST: Temporary list to hold scores for this round
        for p in available:                     # LOOP: Check every available process
            score = calculate_wds_score(p, current_time)  # MATH: Run the WDS Formula to get the score
            candidates.append({                 # STORE: Save the details for the log
                'pid': p['pid'],                # ID: Process ID
                'final_score': score,           # SCORE: The calculated WDS Score
                'bt': p['bt'],                  # BURST: Burst Time (for comparison)
                'wait': current_time - p['at'], # WAIT: Current Wait Time (for comparison)
                'prio': p['prio']               # PRIORITY: User Priority (for comparison)
            })

        # --- 6. DECISION (The Election) ---
        winner_info = max(candidates, key=lambda x: x['final_score'])      # WINNER: Find the candidate with the highest score
        winner = next(p for p in available if p['pid'] == winner_info['pid']) # RETRIEVE: Get the actual process object of the winner

        # --- 7. LOGGING (Context Switching & History) ---
        system_msgs = []                        # LIST: Messages about context switching
        if winner['pid'] != last_process_id:    # CHECK: Is the new winner different from the last one?
            if last_process_id is not None:     # CHECK: Was there a previous process?
                system_msgs.append(f"SYSTEM: Saving State for Process {last_process_id}...") # LOG: Save old state
            
            system_msgs.append(f"SYSTEM: Loading State for Process {winner['pid']}...")      # LOG: Load new state
            last_process_id = winner['pid']     # UPDATE: Set the current winner as the "Last Process"

        decision_log.append({                   # RECORD: Save the entire decision event to the log
            'time': current_time,               # Timestamp
            'winner_pid': winner['pid'],        # Who won
            'candidates': candidates,           # The scores of everyone involved
            'system_msg': system_msgs           # Any context switch messages
        })

        # --- 8. EXECUTION (Running the Job) ---
        start = current_time                    # MARKER: Job starts now
        duration = winner['bt']                 # DURATION: Job runs for its full burst (Non-Preemptive)
        current_time += duration                # CLOCK: Fast forward time by the burst duration
        winner['rem_bt'] = 0                    # UPDATE: Job is now finished (0 remaining)
        
        # CALC: Finish Time = Current Clock
        winner['finish_time'] = current_time    
        # CALC: Turnaround = Finish - Arrival
        winner['tat'] = winner['finish_time'] - winner['at'] 
        # CALC: Wait = Turnaround - Burst
        winner['wait'] = winner['tat'] - winner['bt']        
        
        # SAVE: Add this block to the Gantt Chart timeline
        timeline_wds.append({'pid': winner['pid'], 'start': start, 'duration': duration})
        completed += 1                          # COUNT: Increment completed jobs by 1

    def calc_fcfs(procs):
        # --- 1. THE RULE (First Come First Served) ---
        procs.sort(key=lambda x: x['at'])   # SORT: Force the order to be strictly based on Arrival Time

        # --- 2. SETUP ---
        time = 0                            # CLOCK: Start simulation at Time = 0
        total_tat = 0                       # ACCUMULATOR: Variable to sum up all Turnaround Times

        # --- 3. THE LOOP ---
        for p in procs:                     # ITERATE: Go through the sorted line one by one
        
        # --- 4. GAP HANDLING ---
            if time < p['at']:              # CHECK: Is the CPU free before this job actually arrives?
                time = p['at']              # ACTION: Fast-forward (Idle) the clock to the job's arrival time

        # --- 5. EXECUTION ---
            time += p['bt']                 # RUN: Add Burst Time to clock. 'time' is now the FINISH TIME.
        
        # --- 6. METRIC CALCULATION ---
        # Formula: Turnaround Time = Finish Time - Arrival Time
            total_tat += (time - p['at'])   # SUM: Calculate this job's TAT and add to total

        # --- 7. RESULT ---
        return total_tat / len(procs)       # AVERAGE: Divide Total TAT by number of jobs to get the average

    def calc_sjf(procs):
        # --- 1. SETUP ---
        time = 0; completed = 0; total_tat = 0    # Init clock and counters
        local_procs = copy.deepcopy(procs)        # CLONE: Work on a copy so we don't break the original data

        # --- 2. MAIN LOOP ---
        while completed < len(local_procs):       # LOOP: Run until everyone is done
        
        # --- 3. FILTER ---
        # Find jobs that have Arrived (at <= time) AND are not done (bt > 0)
            avail = [p for p in local_procs if p['at'] <= time and p['bt'] > 0]
        
        # --- 4. IDLE CHECK ---
            if not avail:                         # CHECK: If nobody is here...
                time += 1; continue               # ACTION: Fast forward time by 1s and try again

        # --- 5. THE DECISION (SJF Logic) ---
        # Find the job with the MINIMUM Burst Time from the available list
            winner = min(avail, key=lambda x: x['bt'])

        # --- 6. EXECUTION ---
            time += winner['bt']                  # RUN: Add Burst Time to clock (Time is now Finish Time)
        
        # --- 7. MATH ---
        # TAT = Finish Time - Arrival Time
            total_tat += (time - winner['at'])    # SUM: Add to total

            winner['bt'] = 0                      # MARK: Set burst to 0 to indicate it is finished
            completed += 1                        # COUNT: Increment finished counter

    # --- 8. RESULT ---
        return total_tat / len(local_procs)       # AVERAGE: Return the average TAT

    # --- 9. FINAL STATISTICS (The Scoreboard) ---
    
    # CALCULATE WDS SCORE: Sum the 'tat' of all jobs we just ran and divide by N
    avg_tat_wds = sum(p['tat'] for p in wds_processes) / n
    
    # CALCULATE FCFS SCORE: Send a clean copy of data to the FCFS helper function
    avg_tat_fcfs = calc_fcfs(procs_fcfs)
    
    # CALCULATE SJF SCORE: Send a clean copy of data to the SJF helper function
    avg_tat_sjf = calc_sjf(procs_sjf)

    # --- 10. RESPONSE (Sending the Data Back) ---
    return jsonify({
        # GANTT DATA: List of blocks {pid, start, duration} for the timeline visual
        'timeline_wds': timeline_wds,
        
        # TABLE DATA: The full list of finished processes with all their stats
        'details': {'wds': wds_processes},
        
        # CHART DATA: The averages needed to draw the comparison bar chart
        'metrics': {
            'tat': {'wds': avg_tat_wds, 'fcfs': avg_tat_fcfs, 'sjf': avg_tat_sjf}
        },
        
        # LOG DATA: The history of every decision made (for the scrolling log)
        'decision_log': decision_log
    })

# --- EXECUTION START POINT ---
if __name__ == '__main__':    # CHECK: Is this script being run directly (not imported)?
    app.run(debug=True)       # ACTION: Start the Flask web server with Debug Mode ON (Auto-reload + Error logs)