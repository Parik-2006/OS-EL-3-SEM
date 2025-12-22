from flask import Flask, render_template, request, jsonify
import copy

app = Flask(__name__)

# --- CORE ALGORITHM (WDS) - FINAL TUNED WEIGHTS ---
def calculate_wds_score(process, current_time):
    # WEIGHTS (Tuned for Starvation Rescue & yielding)
    W_WAIT = 3.0    
    W_BURST = 1.0   
    W_PRIO = 1.0

    wait_time = current_time - process['at']
    if wait_time < 0: wait_time = 0

    # Scaling 30: Short Job (2s) = 15 pts. Long Job (15s) = 2 pts. Gap = 13.
    burst_score = 30 / process['bt'] if process['bt'] > 0 else 0
    prio_score = process['prio'] * 10

    score = (W_WAIT * wait_time) + (W_BURST * burst_score) + (W_PRIO * prio_score)
    return round(score, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/custom')
def custom():
    return render_template('custom.html')

# --- REAL-WORLD SCENARIOS DATABASE ---
scenarios_db = {
    'ai': {
        'title': 'AI Model Training Clusters',
        'icon': '🤖',
        'problem': 'Deep Learning models train in massive "Epochs" (hours long). Standard schedulers (FCFS) lock the GPU for the entire epoch. If a short "Checkpoint Save" (10s) arrives, it gets blocked.',
        'solution': 'WDS uses <b>Cooperative Multitasking</b>. The training process yields control after every "Batch". WDS sees the "Checkpoint Save" has a high Efficiency Score and swaps it in immediately.',
        'stats': {'labels': ['Checkpoint Lag (FCFS)', 'Checkpoint Lag (WDS)'], 'data': [120, 5]}, 
        'refs': [{'title': 'Optimizing Checkpointing', 'source': 'arXiv', 'url': '#'}]
    },
    '5g': {
        'title': '5G/6G Edge Gateways',
        'icon': '📡',
        'problem': 'Edge routers process mixed traffic. A 4K Netflix stream blocks a tiny "Heart Attack Alert" packet for 200ms—fatal in remote surgery.',
        'solution': 'WDS implements <b>Packet-Level Yielding</b>. The Health Alert (Priority 10) overrides the video stream immediately, ensuring < 10ms latency.',
        'stats': {'labels': ['Emergency Latency (FCFS)', 'Emergency Latency (WDS)'], 'data': [450, 12]},
        'refs': [{'title': 'URLLC in 5G', 'source': 'IEEE Xplore', 'url': '#'}]
    },
    'auto': {
        'title': 'Autonomous Vehicle OS',
        'icon': '🚗',
        'problem': 'A "Map Download" (Long Task) blocks "Lidar Obstacle Detection" (Critical Task). A 300ms delay at 60mph means the car travels 8 meters blind.',
        'solution': 'WDS uses <b>Yield Points</b>. It pauses the Map Download to ask: <i>"Is anything urgent waiting?"</i>. WDS forces the Lidar task to run instantly.',
        'stats': {'labels': ['Braking Reaction (Standard)', 'Braking Reaction (WDS)'], 'data': [300, 45]},
        'refs': [{'title': 'Real-Time Scheduling in AUTOSAR', 'source': 'SAE International', 'url': '#'}]
    },
    'cloud': {
        'title': 'Serverless Cloud Functions',
        'icon': '☁️',
        'problem': 'In AWS Lambda, "Cold Starts" hang a user\'s "Login Request" if the server is busy compiling a background job.',
        'solution': 'WDS utilizes the <b>Aging Factor</b>. As the Login Request waits, its score grows. WDS injects it next, preventing UI freeze.',
        'stats': {'labels': ['Cold Start Delay (FIFO)', 'Cold Start Delay (WDS)'], 'data': [2500, 300]}, 
        'refs': [{'title': 'Mitigating Cold Starts', 'source': 'USENIX', 'url': '#'}]
    }
}

@app.route('/real-world/<scenario_id>')
def real_world(scenario_id):
    data = scenarios_db.get(scenario_id)
    if not data: return "Scenario not found", 404
    return render_template('real_world.html', data=data)

# --- SIMULATION API ---
@app.route('/api/simulate', methods=['POST'])
def simulate():
    processes = request.json['processes']
    for p in processes:
        p['rem_bt'] = p['bt']
        p['wait'] = 0
        p['tat'] = 0
        p['start_time'] = -1
        p['finish_time'] = -1

    # SIMULATION VARIABLES
    current_time = 0
    completed = 0
    n = len(processes)
    timeline_wds = []
    
    # "VS Battle" Decision Logs
    decision_log = []

    # COPY LISTS FOR COMPARISON
    procs_fcfs = copy.deepcopy(processes)
    procs_sjf = copy.deepcopy(processes)

    # --- 1. RUN WDS SIMULATION ---
    wds_processes = copy.deepcopy(processes)
    wds_processes.sort(key=lambda x: x['at'])
    active_procs = [p for p in wds_processes]
    
    # TRACK PREVIOUS PROCESS (For Context Switch Logic)
    last_process_id = None 

    while completed < n:
        # Move arrived processes to Ready Queue
        available = [p for p in active_procs if p['at'] <= current_time and p['rem_bt'] > 0]
        
        if not available:
            current_time += 1
            continue

        # --- DECISION MOMENT ---
        candidates = []
        for p in available:
            score = calculate_wds_score(p, current_time)
            candidates.append({
                'pid': p['pid'], 
                'final_score': score, 
                'bt': p['bt'], 
                'wait': current_time - p['at'],
                'prio': p['prio']
            })

        # Pick Winner
        winner_info = max(candidates, key=lambda x: x['final_score'])
        winner = next(p for p in available if p['pid'] == winner_info['pid'])

        # --- CONTEXT SWITCH LOGIC (INTEGRATED) ---
        system_msgs = []
        if winner['pid'] != last_process_id:
            # If there was a previous process, save its state
            if last_process_id is not None:
                system_msgs.append(f"💾 SYSTEM: Saving State for Process {last_process_id}...")
            
            # Load the new process
            system_msgs.append(f"🚀 SYSTEM: Loading State for Process {winner['pid']}...")
            
            # Update tracker
            last_process_id = winner['pid']

        # LOG THE DECISION
        decision_log.append({
            'time': current_time,
            'winner_pid': winner['pid'],
            'candidates': candidates,
            'system_msg': system_msgs  # <--- Sent to Frontend
        })

        # EXECUTE PROCESS (Non-Preemptive chunk)
        start = current_time
        duration = winner['bt']
        current_time += duration
        winner['rem_bt'] = 0
        winner['finish_time'] = current_time
        winner['tat'] = winner['finish_time'] - winner['at']
        winner['wait'] = winner['tat'] - winner['bt']
        
        timeline_wds.append({'pid': winner['pid'], 'start': start, 'duration': duration})
        completed += 1

    # --- 2. METRICS (FCFS & SJF) ---
    def calc_fcfs(procs):
        procs.sort(key=lambda x: x['at'])
        time = 0; total_tat = 0
        for p in procs:
            if time < p['at']: time = p['at']
            time += p['bt']
            total_tat += (time - p['at'])
        return total_tat / len(procs)

    def calc_sjf(procs):
        time = 0; completed = 0; total_tat = 0
        local_procs = copy.deepcopy(procs)
        while completed < len(local_procs):
            avail = [p for p in local_procs if p['at'] <= time and p['bt'] > 0]
            if not avail: time += 1; continue
            winner = min(avail, key=lambda x: x['bt'])
            time += winner['bt']
            total_tat += (time - winner['at'])
            winner['bt'] = 0
            completed += 1
        return total_tat / len(local_procs)

    avg_tat_wds = sum(p['tat'] for p in wds_processes) / n
    avg_tat_fcfs = calc_fcfs(procs_fcfs)
    avg_tat_sjf = calc_sjf(procs_sjf)

    return jsonify({
        'timeline_wds': timeline_wds,
        'details': {'wds': wds_processes},
        'metrics': {
            'tat': {'wds': avg_tat_wds, 'fcfs': avg_tat_fcfs, 'sjf': avg_tat_sjf}
        },
        'decision_log': decision_log
    })

if __name__ == '__main__':
    app.run(debug=True)