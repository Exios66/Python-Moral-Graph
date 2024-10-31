import logging
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from moral_graph.simulator import simulate_experiment, SCORE_WEIGHTS
import pandas as pd
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

@app.route('/')
def index():
    """Serve the main page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index page: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    """Run psychology experiment simulation and return results"""
    try:
        # Validate request data
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({'error': 'Invalid JSON format'}), 400
            
        num_participants = data.get('participantCount', 100)
        if not isinstance(num_participants, int):
            return jsonify({'error': 'Participant count must be an integer'}), 400
        
        # Validate participant count against config
        if num_participants < Config.MIN_PARTICIPANTS or num_participants > Config.MAX_PARTICIPANTS:
            return jsonify({
                'error': f'Participant count must be between {Config.MIN_PARTICIPANTS} and {Config.MAX_PARTICIPANTS}'
            }), 400
        
        # Run the simulation
        logger.info(f"Starting simulation with {num_participants} participants")
        results_df = simulate_experiment(num_participants=num_participants)
        
        if results_df.empty:
            return jsonify({'error': 'Simulation produced no results'}), 500
            
        # Calculate summary statistics
        summary_stats = {
            'totalParticipants': num_participants,
            'averageScore': round(float(results_df['TotalWeightedScore'].mean()), 2),
            'completionRate': 100.0,
            'dimensionScores': {}
        }
        
        # Calculate average scores for each dimension
        for dimension in SCORE_WEIGHTS.keys():
            if dimension in results_df.columns:
                summary_stats['dimensionScores'][dimension] = round(float(results_df[dimension].mean()), 2)
        
        logger.info("Simulation completed successfully")
        return jsonify(summary_stats)
    
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logger.error(f"Unexpected error in simulation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Only run in debug mode during development
    is_debug = app.config.get('DEBUG', False)
    port = app.config.get('PORT', 5000)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=is_debug
    )