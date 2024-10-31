import os
import sys
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('experiment.log')
    ]
)
logger = logging.getLogger(__name__)

# Constants matching frontend
SPECIALIZATIONS = [
    "Psychology",
    "Sociology", 
    "Natural Sciences", 
    "Mathematics",
    "Computer Science",
    "Humanities", 
    "Economics",
    "Medicine"
]

DIMENSION_WEIGHTS = {
    'Accuracy': 0.25,
    'Clarity': 0.20,
    'Depth': 0.20,
    'Ethics': 0.20,
    'Engagement': 0.15
}

SCORE_THRESHOLDS = {
    'excellent': 4.5,
    'good': 3.5,
    'acceptable': 2.5,
    'poor': 1.5
}

def setup_directories():
    """Create necessary directories if they don't exist."""
    dirs = ['data/outputs', 'data/visualizations', 'data/reports']
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def simulate_experiment(num_participants):
    """
    Simulate experiment data for given number of participants.
    Returns DataFrame with simulated results.
    """
    logger.info(f"Starting simulation with {num_participants} participants")
    
    results = []
    for participant_id in range(num_participants):
        # Simulate 5-12 interactions per participant
        num_interactions = np.random.randint(5, 13)
        
        for _ in range(num_interactions):
            # Generate random scores with realistic distributions
            scores = {
                dim: min(5.0, max(1.0, np.random.normal(3.8, 0.7)))
                for dim in DIMENSION_WEIGHTS.keys()
            }
            
            # Calculate weighted average
            weighted_score = sum(
                score * weight 
                for (dim, score), (_, weight) 
                in zip(scores.items(), DIMENSION_WEIGHTS.items())
            )
            
            results.append({
                'participant_id': participant_id,
                'specialization': np.random.choice(SPECIALIZATIONS),
                'timestamp': datetime.now(),
                **scores,
                'weighted_score': weighted_score
            })
            
        if participant_id % 10 == 0:
            logger.debug(f"Processed {participant_id} participants")
            
    return pd.DataFrame(results)

def plot_dimension_distributions(data, output_dir='data/visualizations'):
    """Generate dimension distribution plots."""
    logger.info("Generating dimension distribution plots")
    
    try:
        import seaborn as sns
        import matplotlib.pyplot as plt
        
        # Create dimension score distributions
        plt.figure(figsize=(12, 8))
        for dim in DIMENSION_WEIGHTS.keys():
            sns.kdeplot(data[dim], label=dim)
        
        plt.title('Distribution of Dimension Scores')
        plt.xlabel('Score')
        plt.ylabel('Density')
        plt.legend()
        plt.savefig(f'{output_dir}/dimension_distributions.png')
        plt.close()
        
    except Exception as e:
        logger.error(f"Error generating dimension plots: {str(e)}")
        raise

def plot_topic_performance(data, output_dir='data/visualizations'):
    """Generate topic performance visualizations."""
    logger.info("Generating topic performance plots")
    
    try:
        import seaborn as sns
        import matplotlib.pyplot as plt
        
        # Create topic performance boxplots
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='specialization', y='weighted_score', data=data)
        plt.xticks(rotation=45)
        plt.title('Score Distribution by Topic')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/topic_performance.png')
        plt.close()
        
    except Exception as e:
        logger.error(f"Error generating topic plots: {str(e)}")
        raise

def generate_summary_report(data, output_dir='data/reports'):
    """Generate and save summary report of results."""
    logger.info("Generating summary report")
    
    try:
        summary = {
            'total_participants': data['participant_id'].nunique(),
            'total_interactions': len(data),
            'avg_interactions_per_participant': len(data) / data['participant_id'].nunique(),
            'dimension_means': {
                dim: data[dim].mean() 
                for dim in DIMENSION_WEIGHTS.keys()
            },
            'topic_performance': data.groupby('specialization')['weighted_score'].agg([
                'mean', 'std', 'count'
            ]).to_dict(),
            'overall_mean_score': data['weighted_score'].mean(),
            'overall_std_score': data['weighted_score'].std()
        }
        
        # Save summary as JSON
        import json
        with open(f'{output_dir}/summary_report.json', 'w') as f:
            json.dump(summary, f, indent=4)
            
        return summary
        
    except Exception as e:
        logger.error(f"Error generating summary report: {str(e)}")
        raise

def main():
    """Main execution function."""
    try:
        # Setup directories
        setup_directories()
        
        # Simulate experiment with 100 participants
        logger.info("Starting experiment simulation")
        experiment_data = simulate_experiment(num_participants=100)
        
        # Save raw data
        logger.info("Saving experiment data")
        output_path = 'data/outputs/experiment_results.csv'
        experiment_data.to_csv(output_path, index=False)
        logger.info(f"Raw data saved to {output_path}")
        
        # Generate visualizations
        logger.info("Generating visualizations")
        plot_dimension_distributions(experiment_data)
        plot_topic_performance(experiment_data)
        
        # Generate summary report
        logger.info("Generating summary report")
        summary = generate_summary_report(experiment_data)
        
        logger.info("\nExperiment simulation complete!")
        logger.info("Results have been saved to the data/outputs directory")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
