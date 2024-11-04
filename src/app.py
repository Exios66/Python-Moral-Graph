from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
import sys
import os
import logging
from psych_experiment_simulator import simulate_experiment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('experiment.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Get absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')
static_dir = os.path.join(current_dir, 'static')

# Initialize Flask app with explicit template and static paths
app = Flask(__name__,
           template_folder=template_dir,
           static_folder=static_dir)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    """Serve the main application page"""
    try:
        logger.info("Serving index page")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index page: {str(e)}")
        return str(e), 500

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    """Run the psychology experiment simulation"""
    try:
        logger.info("Starting simulation...")
        
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

        logger.info("Simulation completed successfully")
        return jsonify({
            'dimensionScores': dimension_scores,
            'metadata': metadata
        })

    except Exception as e:
        logger.error(f"Error in simulation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found_error(error):
    logger.error(f"404 error: {str(error)}")
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(403)
def forbidden_error(error):
    logger.error(f"403 error: {str(error)}")
    return jsonify({'error': 'Forbidden'}), 403

if __name__ == '__main__':
    # Log startup information
    logger.info(f"Template directory: {template_dir}")
    logger.info(f"Static directory: {static_dir}")
    logger.info("Starting Flask application...")
    
    # Run the app on port 5001 instead of 5000
    app.run(debug=True, port=5001, host='0.0.0.0')
