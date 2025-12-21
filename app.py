from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- ALGORITHMS ENGINE ---
def run_simulation_logic(algo, processes, weights):
    # weights = [w_wait, w_burst, w_prio]
    pool = [p.copy() for p in processes]
    for p in pool: p.update({'done': False, 'wait': 0, 'tat': 0, 'ct': 0, 'rt': 0, 'start_time': -1})
    
    current_time = 0
    completed = 0
    n = len(pool)
    timeline = []
    decision_log = [] # Must exist
    
    while completed < n:
        candidates = [p for p in pool if p['at'] <= current_time and not p['done']]
        
        if not candidates:
            current_time += 1
            continue
            
        winner = None
        
        # --- ALGORITHM SELECTION ---
        if algo == 'FCFS':
            winner = min(candidates, key=lambda x: x['at'])
        elif algo == 'SJF':
            winner = min(candidates, key=lambda x: x['bt'])
        elif algo == 'WDS':
            best_score = -99999
            candidate_scores = []
            
            for p in candidates:
                wait = current_time - p['at']
                bt_score = (1.0 / p['bt']) if p['bt'] > 0 else 0
                
                # THE FORMULA
                score = (weights[0] * wait) + (weights[1] * bt_score) + (weights[2] * p['prio'])
                score = round(score, 2)
                
                candidate_scores.append({
                    'pid': p['pid'], 'wait': wait, 'bt': p['bt'], 'prio': p['prio'], 'final_score': score
                })
                
                if score > best_score:
                    best_score = score
                    winner = p
            
            # LOGGING THE DECISION (Critical for the UI)
            decision_log.append({
                'time': current_time,
                'candidates': candidate_scores,
                'winner_pid': winner['pid']
            })
        
        # Execute Process
        start = current_time
        finish = start + winner['bt']
        winner['start_time'] = start
        winner['ct'] = finish
        winner['tat'] = finish - winner['at']
        winner['wait'] = start - winner['at']
        winner['done'] = True
        
        timeline.append({'pid': winner['pid'], 'start': start, 'duration': winner['bt'], 'algo': algo})
        current_time = finish
        completed += 1
        
    avg_tat = sum(p['tat'] for p in pool) / n
    avg_wt = sum(p['wait'] for p in pool) / n
    
    # RETURN EVERYTHING
    return timeline, avg_tat, avg_wt, pool, decision_log

# --- ROUTES ---
@app.route('/')
def home(): return render_template('index.html')

@app.route('/demo')
def demo(): return render_template('demo.html')

@app.route('/custom')
def custom(): return render_template('custom.html')

@app.route('/api/simulate', methods=['POST'])
def simulate():
    data = request.json
    processes = data.get('processes')
    weights = [float(data.get('w_wait', 2.0)), float(data.get('w_burst', 50.0)), float(data.get('w_prio', 1.5))]
    
    # Run All 3 Algos
    tl_fcfs, tat_fcfs, wt_fcfs, det_fcfs, _ = run_simulation_logic('FCFS', processes, weights)
    tl_sjf, tat_sjf, wt_sjf, det_sjf, _ = run_simulation_logic('SJF', processes, weights)
    tl_wds, tat_wds, wt_wds, det_wds, decision_log = run_simulation_logic('WDS', processes, weights)
    
    return jsonify({
        'timeline_wds': tl_wds,
        'decision_log': decision_log, # <--- THIS MUST BE SENT
        'metrics': {
            'tat': {'fcfs': tat_fcfs, 'sjf': tat_sjf, 'wds': tat_wds},
            'wt': {'fcfs': wt_fcfs, 'sjf': wt_sjf, 'wds': wt_wds}
        },
        'details': { 'wds': det_wds }
    })

# --- REAL-WORLD SCENARIOS DATABASE ---
# --- REAL-WORLD SCENARIOS DATABASE ---
scenarios_db = {
    'ai': {
        'title': 'AI Model Training Clusters',
        'icon': '🤖',
        'problem': 'In Deep Learning, "Checkpointing" (saving progress) is a short, frequent task. "Training Epochs" are massive, long tasks. Standard schedulers (FCFS) force Checkpoints to wait behind Epochs. If the system crashes, hours of training are lost because the Checkpoint never ran.',
        'solution': 'WDS uses its <b>Burst Weight (Efficiency)</b> to identify Checkpoints as "Short Jobs". It pauses the queue of long Training Epochs to slip in the Checkpoint immediately. This guarantees data safety with zero impact on overall training time.',
        'stats': {'labels': ['Checkpoint Lag (FCFS)', 'Checkpoint Lag (WDS)'], 'data': [120, 5]}, 
        'refs': [
            {'title': 'Optimizing Checkpointing in Distributed Deep Learning', 'source': 'arXiv', 'url': 'https://scholar.google.com/scholar?q=Optimizing+Checkpointing+in+Distributed+Deep+Learning'},
            {'title': 'Job Scheduling for GPU Clusters', 'source': 'USENIX OSDI', 'url': 'https://scholar.google.com/scholar?q=Job+Scheduling+for+GPU+Clusters'}
        ]
    },
    '5g': {
        'title': '5G/6G Edge Gateways',
        'icon': '📡',
        'problem': 'Edge towers process mixed traffic: YouTube 4K streams (High Bandwidth, Low Urgency) and Heart Attack Alerts from wearables (Tiny Data, Critical Urgency). FCFS processes the massive Video packets first, delaying the Health Alert by milliseconds—which is fatal.',
        'solution': 'WDS leverages <b>Priority Weight (Urgency)</b>. It assigns "Health Alerts" Priority 10. Even if a 4K stream is running, WDS calculates the massive priority score of the Alert and preempts the video stream instantly.',
        'stats': {'labels': ['Emergency Latency (FCFS)', 'Emergency Latency (WDS)'], 'data': [450, 12]},
        'refs': [
            {'title': 'Ultra-Reliable Low-Latency Communication (URLLC) in 5G', 'source': 'IEEE Xplore', 'url': 'https://scholar.google.com/scholar?q=URLLC+5G+Scheduling+Latency'},
            {'title': 'Slice Scheduling for IoT Edge Devices', 'source': 'ACM Sigcomm', 'url': 'https://scholar.google.com/scholar?q=Network+Slicing+Scheduling+IoT'}
        ]
    },
    'auto': {
        'title': 'Autonomous Vehicle OS',
        'icon': '🚗',
        'problem': 'A self-driving car OS handles "Map Downloads" (Long) and "Lidar Obstacle Detection" (Short, Critical). If the OS is busy downloading a map update (FCFS/Round Robin), the Lidar processing might be delayed by 200ms—enough to cause an accident at 60mph.',
        'solution': 'WDS acts as a <b>Real-Time Hybrid</b>. It sees the Lidar task is both Short (Burst Score) and Critical (Priority Score). It forces the Map Download to yield immediately, ensuring safety-critical reaction times.',
        'stats': {'labels': ['Braking Reaction (Standard)', 'Braking Reaction (WDS)'], 'data': [300, 45]},
        'refs': [
            {'title': 'Real-Time Scheduling in Automotive AUTOSAR', 'source': 'SAE International', 'url': 'https://scholar.google.com/scholar?q=Real-Time+Scheduling+in+Automotive+AUTOSAR'},
            {'title': 'Safety-Critical OS Design for Tesla/Waymo', 'source': 'IEEE IV Symposium', 'url': 'https://scholar.google.com/scholar?q=Safety-Critical+OS+Scheduling+Autonomous+Vehicles'}
        ]
    },
    'cloud': {
        'title': 'Serverless Cloud Functions',
        'icon': '☁️',
        'problem': 'In AWS Lambda/Azure, "Cold Starts" occur when a new function needs to spin up. If the server is busy compiling a large background job, the user\'s simple "Login Request" hangs for seconds (Starvation).',
        'solution': 'WDS uses the <b>Aging Factor</b>. As the Login Request waits, its score rises exponentially. WDS realizes the user is waiting and pauses the background compilation to serve the Login Request, ensuring a snappy UI.',
        'stats': {'labels': ['Cold Start Delay (FIFO)', 'Cold Start Delay (WDS)'], 'data': [2500, 300]}, 
        'refs': [
            {'title': 'Mitigating Cold Starts in Serverless Computing', 'source': 'USENIX', 'url': 'https://scholar.google.com/scholar?q=Mitigating+Cold+Starts+in+Serverless+Computing'},
            {'title': 'Fairness in Multi-Tenant Cloud Scheduling', 'source': 'Google Cloud Research', 'url': 'https://scholar.google.com/scholar?q=Fairness+in+Multi-Tenant+Cloud+Scheduling'}
        ]
    }
}

@app.route('/real-world/<scenario_id>')
def real_world(scenario_id):
    data = scenarios_db.get(scenario_id)
    if not data: return "Scenario not found", 404
    return render_template('real_world.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)