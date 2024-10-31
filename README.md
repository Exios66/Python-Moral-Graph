# Python-Moral-Graph

A Python package for simulating and analyzing moral decision-making experiments using a sophisticated rubric-based evaluation system.

## Features

- Simulates psychological experiments with multiple participants and chatbots
- Implements a comprehensive moral evaluation rubric with 8 dimensions
- Generates detailed analytics and visualizations
- Supports customizable experiment parameters
- Provides data export capabilities for further analysis

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Python-Moral-Graph.git
cd Python-Moral-Graph
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from moral_graph import simulate_experiment

# Run simulation with 100 participants
experiment_data = simulate_experiment(num_participants=100)

# Save results to CSV
experiment_data.to_csv('experiment_results.csv', index=False)
```

### Running the Full Pipeline

```bash
python src/main.py
```

This will:

1. Run the experiment simulation
2. Generate visualizations
3. Create a summary report
4. Save all outputs to the `data/outputs` directory

## Project Structure

```plaintext

Python-Moral-Graph/
├── data/
│   └── outputs/          # Generated data and visualizations
├── src/
│   ├── moral_graph/     # Main package
│   │   ├── __init__.py
│   │   ├── core.py      # Core classes and constants
│   │   ├── simulator.py # Simulation logic
│   │   └── visualization.py # Data visualization
│   └── main.py          # Example usage script
├── tests/               # Test files
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Moral Graph Rubric Dimensions

The evaluation system uses 8 key dimensions:

1. Ethical Alignment (20%)
2. Empathy and Emotional Intelligence (15%)
3. Accuracy and Reliability (20%)
4. Engagement and Responsiveness (10%)
5. Cultural Sensitivity (10%)
6. Conflict Resolution and Problem-Solving (10%)
7. Privacy and Confidentiality (10%)
8. Adaptability and Learning (5%)

## Testing

Run tests using pytest:

```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
