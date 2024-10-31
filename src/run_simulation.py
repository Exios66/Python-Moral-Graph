from moral_graph import simulate_experiment
from moral_graph.core import MORAL_GRAPH_RUBRIC_DIMENSIONS
import os
from tabulate import tabulate
import pandas as pd
pd.set_option('display.precision', 2)

def format_statistics(stats_series):
    """Format statistics into a pretty markdown table"""
    stats_dict = stats_series.to_dict()
    rows = [
        ['Count', f"{stats_dict['count']:.0f}"],
        ['Mean', f"{stats_dict['mean']:.2f}"],
        ['Std Dev', f"{stats_dict['std']:.2f}"],
        ['Min', f"{stats_dict['min']:.2f}"],
        ['25%', f"{stats_dict['25%']:.2f}"],
        ['Median', f"{stats_dict['50%']:.2f}"],
        ['75%', f"{stats_dict['75%']:.2f}"],
        ['Max', f"{stats_dict['max']:.2f}"]
    ]
    return tabulate(rows, headers=['Metric', 'Value'], tablefmt='pipe')

def main():
    # Create output directory if it doesn't exist
    os.makedirs('data/outputs', exist_ok=True)
    
    print("# Moral Graph Experiment Simulation")
    print("\n## Running Simulation")
    print("Simulating experiment with 100 participants...")
    
    # Run simulation
    experiment_data = simulate_experiment(num_participants=100)
    
    # Save data
    output_path = 'data/outputs/experiment_results.csv'
    experiment_data.to_csv(output_path, index=False)
    
    # Print formatted results
    print("\n## Experiment Results")
    print("\n### Overview")
    print(f"- Total Participants: {len(experiment_data['ParticipantID'].unique())}")
    print(f"- Total Interactions: {len(experiment_data)}")
    print(f"- Output File: `{output_path}`")
    
    print("\n### Score Statistics")
    print("\nDistribution of Total Weighted Scores:\n")
    print(format_statistics(experiment_data['TotalWeightedScore'].describe()))
    
    print("\n### Topic Distribution")
    topic_counts = experiment_data['Specialization'].value_counts()
    print("\nNumber of interactions per topic:\n")
    topic_table = [[topic, count] for topic, count in topic_counts.items()]
    print(tabulate(topic_table, headers=['Topic', 'Count'], tablefmt='pipe'))
    
    print("\n### Dimension Scores")
    dimension_scores = {dim.name: experiment_data[dim.name].mean() for dim in MORAL_GRAPH_RUBRIC_DIMENSIONS}
    dimension_table = [[dim, f"{score:.2f}"] for dim, score in dimension_scores.items()]
    print("\nAverage scores per dimension:\n")
    print(tabulate(dimension_table, headers=['Dimension', 'Average Score'], tablefmt='pipe'))

if __name__ == "__main__":
    main()
