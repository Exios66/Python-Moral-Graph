import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from typing import Dict, Any
from .core import MORAL_GRAPH_RUBRIC_DIMENSIONS
import logging

# Configure logging
logger = logging.getLogger(__name__)

def plot_dimension_distributions(data: pd.DataFrame, output_dir: str = 'data/outputs') -> None:
    """
    Creates violin plots showing score distributions for each rubric dimension.
    Includes additional statistical overlays and styling.
    
    Args:
        data: DataFrame containing dimension scores
        output_dir: Directory to save output plot
    """
    try:
        plt.figure(figsize=(15, 8))
        dimension_scores = data[[dim.name for dim in MORAL_GRAPH_RUBRIC_DIMENSIONS]]
        
        # Enhanced violin plot with points and statistics
        sns.violinplot(data=dimension_scores, inner='box', color='lightblue')
        sns.swarmplot(data=dimension_scores, size=2, color='.3', alpha=0.3)
        
        # Add mean markers
        means = dimension_scores.mean()
        plt.plot(range(len(means)), means, 'ro', label='Mean')
        
        plt.xticks(rotation=45, ha='right')
        plt.title('Score Distributions Across Rubric Dimensions', pad=20)
        plt.ylabel('Score')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, 'dimension_distributions.png'), dpi=300)
        plt.close()
        
    except Exception as e:
        logger.error(f"Error plotting dimension distributions: {str(e)}")
        plt.close()
        raise

def plot_topic_performance(data: pd.DataFrame, output_dir: str = 'data/outputs') -> None:
    """
    Creates comprehensive visualizations of performance across different topics.
    Includes box plots, trend analysis, and statistical indicators.
    
    Args:
        data: DataFrame containing topic performance data
        output_dir: Directory to save output plots
    """
    try:
        # Create a figure with multiple subplots
        fig = plt.figure(figsize=(20, 15))
        
        # Box plot
        plt.subplot(2, 1, 1)
        sns.boxplot(x='Specialization', y='TotalWeightedScore', data=data, palette='viridis')
        plt.xticks(rotation=45, ha='right')
        plt.title('Performance Distribution by Topic')
        plt.grid(True, alpha=0.3)
        
        # Violin plot with individual points
        plt.subplot(2, 1, 2)
        sns.violinplot(x='Specialization', y='TotalWeightedScore', data=data, palette='viridis')
        sns.stripplot(x='Specialization', y='TotalWeightedScore', data=data, size=3, alpha=0.3, color='black')
        plt.xticks(rotation=45, ha='right')
        plt.title('Detailed Score Distribution by Topic')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, 'topic_performance.png'), dpi=300)
        plt.close()
        
    except Exception as e:
        logger.error(f"Error plotting topic performance: {str(e)}")
        plt.close()
        raise

def plot_correlation_matrix(data: pd.DataFrame, output_dir: str = 'data/outputs') -> None:
    """
    Creates a correlation matrix heatmap between dimensions.
    
    Args:
        data: DataFrame containing dimension scores
        output_dir: Directory to save output plot
    """
    try:
        dimension_scores = data[[dim.name for dim in MORAL_GRAPH_RUBRIC_DIMENSIONS]]
        corr_matrix = dimension_scores.corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
        plt.title('Correlation Matrix of Dimensions')
        plt.tight_layout()
        
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, 'correlation_matrix.png'), dpi=300)
        plt.close()
        
    except Exception as e:
        logger.error(f"Error plotting correlation matrix: {str(e)}")
        plt.close()
        raise

def plot_time_series(data: pd.DataFrame, output_dir: str = 'data/outputs') -> None:
    """
    Creates time series visualizations if temporal data is available.
    
    Args:
        data: DataFrame containing temporal score data
        output_dir: Directory to save output plot
    """
    try:
        if 'Timestamp' not in data.columns:
            logger.warning("No timestamp column found - skipping time series plot")
            return
            
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        plt.figure(figsize=(15, 8))
        
        # Rolling average of scores over time
        data.set_index('Timestamp').sort_index()['TotalWeightedScore'].rolling('1D').mean().plot()
        plt.title('Score Trends Over Time')
        plt.xlabel('Time')
        plt.ylabel('Average Score')
        plt.grid(True)
        plt.tight_layout()
        
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, 'time_series.png'), dpi=300)
        plt.close()
        
    except Exception as e:
        logger.error(f"Error plotting time series: {str(e)}")
        plt.close()
        raise

def generate_summary_report(data: pd.DataFrame, output_dir: str = 'data/outputs') -> Dict[str, Any]:
    """
    Generates a comprehensive summary report with enhanced statistics and visualizations.
    
    Args:
        data: DataFrame containing experiment data
        output_dir: Directory to save report
        
    Returns:
        Dictionary containing summary statistics
    """
    try:
        summary = {
            'Overall Statistics': data['TotalWeightedScore'].describe(),
            'Average Scores by Topic': data.groupby('Specialization')['TotalWeightedScore'].agg(['mean', 'std', 'count']),
            'Dimension Statistics': {
                dim.name: {
                    'mean': data[dim.name].mean(),
                    'std': data[dim.name].std(),
                    'median': data[dim.name].median(),
                    'skew': data[dim.name].skew(),
                    'kurtosis': data[dim.name].kurtosis()
                }
                for dim in MORAL_GRAPH_RUBRIC_DIMENSIONS
            },
            'Score Percentiles': np.percentile(data['TotalWeightedScore'], [10, 25, 50, 75, 90])
        }
        
        os.makedirs(output_dir, exist_ok=True)
        
        with open(os.path.join(output_dir, 'summary_report.txt'), 'w') as f:
            f.write("Experiment Summary Report\n")
            f.write("=======================\n\n")
            
            f.write("Overall Statistics:\n")
            f.write("-----------------\n")
            f.write(str(summary['Overall Statistics']))
            f.write("\n\n")
            
            f.write("Score Percentiles:\n")
            f.write("----------------\n")
            percentiles = [10, 25, 50, 75, 90]
            for p, score in zip(percentiles, summary['Score Percentiles']):
                f.write(f"{p}th percentile: {score:.2f}\n")
            f.write("\n")
            
            f.write("Performance by Topic:\n")
            f.write("-------------------\n")
            f.write(str(summary['Average Scores by Topic']))
            f.write("\n\n")
            
            f.write("Dimension Statistics:\n")
            f.write("-------------------\n")
            for dim, stats in summary['Dimension Statistics'].items():
                f.write(f"\n{dim}:\n")
                for stat, value in stats.items():
                    f.write(f"  {stat}: {value:.3f}\n")
        
        return summary
        
    except Exception as e:
        logger.error(f"Error generating summary report: {str(e)}")
        raise
