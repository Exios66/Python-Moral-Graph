from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from moral_graph.simulator import simulate_experiment
import pandas as pd
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    try:
        data = request.get_json()
        num_participants = data.get('participantCount', 100)
        
        if num_participants < Config.MIN_PARTICIPANTS or num_participants > Config.MAX_PARTICIPANTS:
            return jsonify({
                'error': f'Participant count must be between {Config.MIN_PARTICIPANTS} and {Config.MAX_PARTICIPANTS}'
            }), 400
        
        # Run the simulation
        results_df = simulate_experiment(num_participants=num_participants)
        
        # Calculate summary statistics
        summary_stats = {
            'totalParticipants': num_participants,
            'averageScore': float(results_df['TotalWeightedScore'].mean()),
            'completionRate': 100.0,
            'dimensionScores': {}
        }
        
        # Calculate average scores for each dimension
        for dimension in results_df.columns:
            if dimension not in ['ParticipantID', 'ChatbotID', 'Specialization', 'AssignmentType', 'TotalWeightedScore']:
                summary_stats['dimensionScores'][dimension] = float(results_df[dimension].mean())
        
        return jsonify(summary_stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)