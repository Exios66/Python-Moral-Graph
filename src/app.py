from flask import Flask, jsonify, render_template
from flask_cors import CORS
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from psych_experiment_simulator import simulate_experiment
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    try:
        # Run simulation with 100 participants
        df = simulate_experiment(num_participants=100)
        
        # Calculate average scores for each dimension
        dimension_scores = {}
        for col in df.columns:
            if col not in ['ParticipantID', 'ChatbotID', 'Specialization', 'AssignmentType', 'TotalWeightedScore', 'Timestamp']:
                dimension_scores[col] = float(df[col].mean())

        # Calculate metadata
        metadata = {
            'total_participants': len(df['ParticipantID'].unique()),
            'total_interactions': len(df),
            'avg_total_score': float(df['TotalWeightedScore'].mean()),
            'std_total_score': float(df['TotalWeightedScore'].std())
        }

        return jsonify({
            'dimensionScores': dimension_scores,
            'metadata': metadata
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
