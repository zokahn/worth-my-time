from flask import Flask, render_template, jsonify, request
import os
import json
from datetime import datetime, timedelta
from src.rag_agent.config import config
from src.rag_agent.visualization import generate_activity_pie_chart, generate_activity_timeline
from src.rag_agent.ml.models import ActivityPredictor
from src.rag_agent.ml.training import load_activities

app = Flask(__name__)

DATA_DIR = config.get('DATA_DIR')
SUMMARIES_DIR = config.get('SUMMARIES_DIR')

# Initialize and train the activity predictor
activities = load_activities()
predictor = ActivityPredictor()
predictor.train(activities)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/activity_data')
def activity_data():
    today = datetime.now().strftime('%Y-%m-%d')
    activities_file = os.path.join(DATA_DIR, f'{today}.json')
    
    if os.path.exists(activities_file):
        with open(activities_file, 'r') as file:
            activities = json.load(file)
        return jsonify(activities)
    else:
        return jsonify([])

@app.route('/api/daily_summary')
def daily_summary():
    today = datetime.now().strftime('%Y-%m-%d')
    summary_file = os.path.join(SUMMARIES_DIR, f'{today}_summary.txt')
    
    if os.path.exists(summary_file):
        with open(summary_file, 'r') as file:
            summary = file.read()
        return jsonify({'summary': summary})
    else:
        return jsonify({'summary': 'No summary available for today.'})

@app.route('/api/visualizations')
def visualizations():
    today = datetime.now().strftime('%Y-%m-%d')
    activities_file = os.path.join(DATA_DIR, f'{today}.json')
    
    if os.path.exists(activities_file):
        with open(activities_file, 'r') as file:
            activities = json.load(file)
        
        visualization_dir = os.path.join(SUMMARIES_DIR, 'visualizations')
        os.makedirs(visualization_dir, exist_ok=True)
        
        generate_activity_pie_chart(activities, visualization_dir)
        generate_activity_timeline(activities, visualization_dir)
        
        return jsonify({
            'pie_chart': '/static/visualizations/activity_categories_pie.png',
            'timeline': '/static/visualizations/activity_timeline.png'
        })
    else:
        return jsonify({})

@app.route('/api/predict_activity', methods=['POST'])
def predict_activity():
    data = request.json
    timestamp = datetime.fromisoformat(data['timestamp'])
    window_title = data['window_title']
    predicted_category = predictor.predict(timestamp, window_title)
    return jsonify({'predicted_category': predicted_category})

if __name__ == '__main__':
    app.run(debug=True)
