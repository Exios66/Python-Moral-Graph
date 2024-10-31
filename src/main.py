import os
import sys
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from config import Config

# Configure logging with both file and console handlers
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('experiment.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Import constants from config to ensure consistency
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

DIMENSION_WEIGHTS = Config.DIMENSION_WEIGHTS
SCORE_THRESHOLDS = Config.SCORE_THRESHOLDS

def setup_directories() -> None:
    """Create necessary directories if they don't exist."""
    dirs = ['data/outputs', 'data/visualizations', 'data/reports']
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created directory: {dir_path}")

def simulate_experiment(num_participants: int) -> pd.DataFrame:
    """
    Simulate experiment data for given number of participants.
    
    Args:
        num_participants: Number of participants to simulate
        
    Returns:
        DataFrame containing simulated results
        
    Raises:
        ValueError: If num_participants is not within configured limits
    """
    if not Config.MIN_PARTICIPANTS <= num_participants <= Config.MAX_PARTICIPANTS:
        raise ValueError(
            f"Number of participants must be between "
            f"{Config.MIN_PARTICIPANTS} and {Config.MAX_PARTICIPANTS}"
        )
    
    logger.info(f"Starting simulation with {num_participants} participants")
    
    results = []
    for participant_id in range(num_participants):
        # Simulate 5-12 interactions per participant
        num_interactions = np.random.randint(5, 13)
        
        for _ in range(num_interactions):
            # Generate random scores with realistic distributions
            scores = {
                dim: float(np.clip(np.random.normal(3.8, 0.7), 1.0, 5.0))
                for dim in DIMENSION_WEIGHTS.keys()
            }
            
            # Calculate weighted average using numpy for better performance
            weighted_score = np.sum([
                scores[dim] * weight 
                for dim, weight in DIMENSION_WEIGHTS.items()
            ])
            
            results.append({
                'participant_id': participant_id,
                'specialization': np.random.choice(SPECIALIZATIONS),
                'timestamp': datetime.now().isoformat(),
                **scores,
                'weighted_score': weighted_score
            })
            
        if participant_id > 0 and participant_id % 10 == 0:
            logger.debug(f"Processed {participant_id}/{num_participants} participants")
            
    return pd.DataFrame(results)

def plot_dimension_distributions(data: pd.DataFrame, output_dir: str = 'data/visualizations') -> None:
    """
    Generate dimension distribution plots.
    
    Args:
        data: DataFrame containing experiment results
        output_dir: Directory to save visualization files
        
    Raises:
        ImportError: If required plotting libraries are not available
        RuntimeError: If plotting fails
    """
    logger.info("Generating dimension distribution plots")
    
    try:
        import seaborn as sns
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(12, 8))
        for dim in DIMENSION_WEIGHTS.keys():
            sns.kdeplot(data=data, x=dim, label=dim)
        
        plt.title('Distribution of Dimension Scores')
        plt.xlabel('Score')
        plt.ylabel('Density')
        plt.legend()
        
        output_path = f'{output_dir}/dimension_distributions.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.debug(f"Saved dimension distribution plot to {output_path}")
        
    except ImportError as e:
        logger.error("Required plotting libraries not available")
        raise
    except Exception as e:
        logger.error(f"Error generating dimension plots: {str(e)}")
        raise RuntimeError(f"Failed to generate dimension plots: {str(e)}")

def plot_topic_performance(data: pd.DataFrame, output_dir: str = 'data/visualizations') -> None:
    """
    Generate topic performance visualizations.
    
    Args:
        data: DataFrame containing experiment results
        output_dir: Directory to save visualization files
        
    Raises:
        ImportError: If required plotting libraries are not available
        RuntimeError: If plotting fails
    """
    logger.info("Generating topic performance plots")
    
    try:
        import seaborn as sns
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(12, 8))
        sns.boxplot(data=data, x='specialization', y='weighted_score')
        plt.xticks(rotation=45, ha='right')
        plt.title('Score Distribution by Topic')
        
        output_path = f'{output_dir}/topic_performance.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.debug(f"Saved topic performance plot to {output_path}")
        
    except ImportError as e:
        logger.error("Required plotting libraries not available")
        raise
    except Exception as e:
        logger.error(f"Error generating topic plots: {str(e)}")
        raise RuntimeError(f"Failed to generate topic plots: {str(e)}")

def generate_summary_report(data: pd.DataFrame, output_dir: str = 'data/reports') -> Dict:
    """
    Generate and save summary report of results.
    
    Args:
        data: DataFrame containing experiment results
        output_dir: Directory to save report files
        
    Returns:
        Dictionary containing summary statistics
        
    Raises:
        RuntimeError: If report generation fails
    """
    logger.info("Generating summary report")
    
    try:
        summary = {
            'total_participants': int(data['participant_id'].nunique()),
            'total_interactions': len(data),
            'avg_interactions_per_participant': float(len(data) / data['participant_id'].nunique()),
            'dimension_means': {
                dim: float(data[dim].mean())
                for dim in DIMENSION_WEIGHTS.keys()
            },
            'topic_performance': data.groupby('specialization')['weighted_score'].agg([
                'mean', 'std', 'count'
            ]).round(3).to_dict('index'),
            'overall_mean_score': float(data['weighted_score'].mean()),
            'overall_std_score': float(data['weighted_score'].std())
        }
        
        # Save summary as JSON
        output_path = f'{output_dir}/summary_report.json'
        with open(output_path, 'w') as f:
            import json
            json.dump(summary, f, indent=4)
        logger.debug(f"Saved summary report to {output_path}")
            
        return summary
        
    except Exception as e:
        logger.error(f"Error generating summary report: {str(e)}")
        raise RuntimeError(f"Failed to generate summary report: {str(e)}")

def main() -> None:
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
        
        logger.info("Experiment simulation complete!")
        logger.info("Results have been saved to the data/outputs directory")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
