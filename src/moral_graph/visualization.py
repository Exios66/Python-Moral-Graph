import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from .core import MORAL_GRAPH_RUBRIC_DIMENSIONS

def plot_dimension_distributions(data, output_dir='data/outputs'):
    """
    Creates violin plots showing score distributions for each rubric dimension.
    """
    plt.figure(figsize=(15, 8))
    dimension_scores = data[[dim.name for dim in MORAL_GRAPH_RUBRIC_DIMENSIONS]]
    
    sns.violinplot(data=dimension_scores)
    plt.xticks(rotation=45, ha='right')
    plt.title('Score Distributions Across Rubric Dimensions')
    plt.tight_layout()
    
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'dimension_distributions.png'))
    plt.close()

def plot_topic_performance(data, output_dir='data/outputs'):
    """
    Creates a box plot showing performance across different topics.
    """
    plt.figure(figsize=(15, 8))
    
    sns.boxplot(x='Specialization', y='TotalWeightedScore', data=data)
    plt.xticks(rotation=45, ha='right')
    plt.title('Performance Distribution by Topic')
    plt.tight_layout()
    
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'topic_performance.png'))
    plt.close()

def generate_summary_report(data, output_dir='data/outputs'):
    """
    Generates a summary report of the experiment results.
    """
    summary = {
        'Overall Statistics': data['TotalWeightedScore'].describe(),
        'Average Scores by Topic': data.groupby('Specialization')['TotalWeightedScore'].mean(),
        'Average Dimension Scores': {
            dim.name: data[dim.name].mean() 
            for dim in MORAL_GRAPH_RUBRIC_DIMENSIONS
        }
    }
    
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'summary_report.txt'), 'w') as f:
        f.write("Experiment Summary Report\n")
        f.write("=======================\n\n")
        
        f.write("Overall Statistics:\n")
        f.write("-----------------\n")
        f.write(str(summary['Overall Statistics']))
        f.write("\n\n")
        
        f.write("Average Scores by Topic:\n")
        f.write("----------------------\n")
        f.write(str(summary['Average Scores by Topic']))
        f.write("\n\n")
        
        f.write("Average Dimension Scores:\n")
        f.write("-----------------------\n")
        for dim, score in summary['Average Dimension Scores'].items():
            f.write(f"{dim}: {score:.2f}\n")
    
    return summary
