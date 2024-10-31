from moral_graph import (
    simulate_experiment,
    plot_dimension_distributions,
    plot_topic_performance,
    generate_summary_report
)

def main():
    # Simulate experiment with 100 participants
    print("Simulating experiment...")
    experiment_data = simulate_experiment(num_participants=100)
    
    # Save raw data
    print("Saving experiment data...")
    experiment_data.to_csv('data/outputs/experiment_results.csv', index=False)
    
    # Generate visualizations
    print("Generating visualizations...")
    plot_dimension_distributions(experiment_data)
    plot_topic_performance(experiment_data)
    
    # Generate summary report
    print("Generating summary report...")
    summary = generate_summary_report(experiment_data)
    
    print("\nExperiment simulation complete!")
    print("Results have been saved to the data/outputs directory.")

if __name__ == "__main__":
    main()
