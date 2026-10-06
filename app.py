from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json, os, re

app = Flask(__name__)
DATA_FILE = os.path.join('data','progress.json')

DEFAULT_PROGRESS = {
    'weight': 70, 'target_weight': 65, 'workouts': 0, 'water': 0,
    'streak': 0, 'weekly_goal': 5, 'completed_days': []
}

def load_progress():
    if not os.path.exists(DATA_FILE): return DEFAULT_PROGRESS.copy()
    try:
        with open(DATA_FILE,'r',encoding='utf-8') as f: return {**DEFAULT_PROGRESS, **json.load(f)}
    except Exception: return DEFAULT_PROGRESS.copy()

def save_progress(data):
    os.makedirs('data', exist_ok=True)
    with open(DATA_FILE,'w',encoding='utf-8') as f: json.dump(data,f,indent=2)

def bot_reply(msg):
    m = msg.lower().strip()
    if not m: return "Tell me your fitness goal and I’ll help you plan your next step."
    if any(x in m for x in ['hello','hi','hey']):
        return "Hey! I’m FitBuddy 💪 Tell me your goal—muscle gain, fat loss, strength, or general fitness—and I’ll help you get started."
    if 'muscle' in m or 'bulk' in m or 'gain' in m:
        return "For muscle gain, focus on progressive resistance training, enough protein, adequate calories, and 7–9 hours of sleep. A 4–5 day split can work well, depending on your experience and recovery."
    if 'fat' in m or 'weight loss' in m or 'lose weight' in m or 'cut' in m:
        return "For fat loss, combine resistance training with a sustainable calorie deficit, protein-rich foods, daily movement, and consistent sleep. Avoid crash diets."
    if 'protein' in m:
        return "Protein needs vary by body size and goal. For people doing regular resistance training, a common evidence-based range is roughly 1.6–2.2 g/kg/day. Spread intake across meals and choose foods you tolerate well."
    if 'water' in m or 'hydration' in m:
        return "Hydration needs vary with body size, climate, and training. Drink regularly through the day and increase fluids around sweaty workouts. In hot conditions, electrolytes may also matter."
    if 'chest' in m:
        return "A beginner-friendly chest session can include bench press or machine press, incline dumbbell press, and a cable or pec-deck movement. Start with controlled technique and leave a few reps in reserve."
    if 'leg' in m or 'legs' in m:
        return "A balanced leg session can include a squat or leg press, Romanian deadlift, leg curl, split squat, and calf raises. Warm up first and prioritize good technique."
    if 'back' in m:
        return "For back development, combine a vertical pull such as lat pulldown with a row, plus a hip-hinge movement when appropriate. Control the eccentric portion and avoid using momentum."
    if 'beginner' in m or 'start' in m:
        return "If you’re new, start with 3 full-body sessions per week. Use simple movements, moderate loads, and focus on learning technique before chasing heavy weights."
    if 'workout' in m or 'routine' in m or 'plan' in m:
        return "Try this 3-day starter plan: Day 1 full body, Day 2 rest/light cardio, Day 3 full body, Day 4 rest, Day 5 full body. Use 2–3 sets per exercise and gradually increase reps or load as your technique improves."
    if 'diet' in m or 'meal' in m or 'eat' in m:
        return "Build meals around a protein source, vegetables or fruit, a carbohydrate source, and healthy fats. Your total calories and protein should match your goal. I can help you create a simple meal structure."
    if 'sleep' in m or 'recovery' in m:
        return "Recovery matters as much as training. Aim for about 7–9 hours of sleep, include rest days, and reduce training volume if persistent soreness or fatigue is affecting performance."
    if 'pain' in m or 'injury' in m:
        return "Don’t train through sharp or worsening pain. Stop the movement and seek assessment from a qualified healthcare professional when needed. I can provide general fitness information, not a diagnosis."
    return "I can help with workouts, exercise selection, nutrition basics, recovery, hydration, and progress tracking. Try asking: ‘Give me a beginner workout’ or ‘How much protein should I eat?’"

@app.route('/')
def index(): return render_template('index.html', progress=load_progress())

@app.post('/api/chat')
def chat():
    data=request.get_json(silent=True) or {}
    return jsonify({'reply': bot_reply(str(data.get('message','')))})

@app.get('/api/progress')
def progress(): return jsonify(load_progress())

@app.post('/api/progress')
def update_progress():
    data=request.get_json(silent=True) or {}
    p=load_progress()
    for k in ['weight','target_weight','workouts','water','streak','weekly_goal']:
        if k in data:
            try: p[k]=max(0,float(data[k])) if k in ['weight','target_weight'] else max(0,int(data[k]))
            except (ValueError,TypeError): pass
    save_progress(p); return jsonify(p)

@app.post('/api/workout-complete')
def workout_complete():
    p=load_progress(); today=datetime.now().strftime('%Y-%m-%d')
    days=p.get('completed_days',[])
    if today not in days: days.append(today); p['workouts']=int(p.get('workouts',0))+1
    p['completed_days']=days[-30:]
    p['streak']=min(30, len(days))
    save_progress(p); return jsonify(p)

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000,debug=False)
