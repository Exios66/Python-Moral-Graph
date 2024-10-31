from .core import (
    RubricDimension,
    Participant,
    Chatbot,
    TOPICS,
    MORAL_GRAPH_RUBRIC_DIMENSIONS
)

from .simulator import (
    simulate_experiment,
    assign_chatbots_to_participant,
    score_chatbot_interaction,
    calculate_total_weighted_score
)

from .visualization import (
    plot_dimension_distributions,
    plot_topic_performance,
    generate_summary_report
)

__version__ = '0.1.0'
