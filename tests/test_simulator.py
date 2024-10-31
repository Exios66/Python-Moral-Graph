import pytest
from moral_graph.simulator import (
    simulate_experiment,
    assign_chatbots_to_participant,
    score_chatbot_interaction,
    calculate_total_weighted_score
)
from moral_graph.core import Participant, MORAL_GRAPH_RUBRIC_DIMENSIONS

def test_simulate_experiment():
    # Test with a small number of participants
    df = simulate_experiment(num_participants=5)
    
    # Check basic properties of the output
    assert len(df) == 10  # 5 participants * 2 chatbots each
    assert 'ParticipantID' in df.columns
    assert 'ChatbotID' in df.columns
    assert 'TotalWeightedScore' in df.columns
    
    # Check score ranges
    assert df['TotalWeightedScore'].min() >= 1
    assert df['TotalWeightedScore'].max() <= 5

def test_score_chatbot_interaction():
    from moral_graph.core import Chatbot
    
    chatbot = Chatbot("test_id", "Psychology and Behavioral Sciences")
    scores = score_chatbot_interaction(chatbot, MORAL_GRAPH_RUBRIC_DIMENSIONS)
    
    # Check that all dimensions are scored
    for dimension in MORAL_GRAPH_RUBRIC_DIMENSIONS:
        assert dimension.name in scores
        assert 1 <= scores[dimension.name] <= 5

def test_calculate_total_weighted_score():
    from moral_graph.core import Chatbot
    
    chatbot = Chatbot("test_id", "Psychology and Behavioral Sciences")
    scores = score_chatbot_interaction(chatbot, MORAL_GRAPH_RUBRIC_DIMENSIONS)
    total_score = calculate_total_weighted_score(chatbot, MORAL_GRAPH_RUBRIC_DIMENSIONS)
    
    # Check score range
    assert 1 <= total_score <= 5
