import pytest
import pandas as pd
import numpy as np
from moral_graph.simulator import (
    simulate_experiment,
    assign_chatbots_to_participant,
    score_chatbot_interaction,
    calculate_total_weighted_score
)
from moral_graph.core import Participant, Chatbot, MORAL_GRAPH_RUBRIC_DIMENSIONS, TOPICS

def test_simulate_experiment():
    """Test the full experiment simulation with various participant counts"""
    # Test with different participant counts
    participant_counts = [5, 10, 100]
    
    for num_participants in participant_counts:
        df = simulate_experiment(num_participants=num_participants)
        
        # Validate DataFrame structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) == num_participants * 2  # Each participant gets 2 chatbots
        
        # Validate required columns exist
        required_columns = ['ParticipantID', 'ChatbotID', 'TotalWeightedScore', 
                          'Topic', 'InteractionCount']
        for col in required_columns:
            assert col in df.columns
            
        # Validate data types
        assert df['ParticipantID'].dtype == object
        assert df['ChatbotID'].dtype == object
        assert pd.api.types.is_numeric_dtype(df['TotalWeightedScore'])
        
        # Validate score ranges
        assert df['TotalWeightedScore'].min() >= 1.0
        assert df['TotalWeightedScore'].max() <= 5.0
        
        # Check for duplicates
        assert not df.duplicated(['ParticipantID', 'ChatbotID']).any()
        
        # Validate topics
        assert all(topic in TOPICS for topic in df['Topic'].unique())

def test_assign_chatbots_to_participant():
    """Test chatbot assignment logic"""
    # Create test participant
    participant = Participant(
        participant_id="test_p1",
        strengths=["Psychology and Behavioral Sciences"],
        weaknesses=["Mathematics and Logic"]
    )
    
    # Test assignment
    assigned_chatbots = assign_chatbots_to_participant(participant)
    
    assert len(assigned_chatbots) == 2
    assert all(isinstance(bot, Chatbot) for bot in assigned_chatbots)
    assert len(set(bot.chatbot_id for bot in assigned_chatbots)) == 2  # Unique bots
    
    # Test topic alignment
    topics = [bot.primary_topic for bot in assigned_chatbots]
    assert any(topic in participant.strengths for topic in topics)
    assert any(topic in participant.weaknesses for topic in topics)

def test_score_chatbot_interaction():
    """Test scoring logic for individual chatbot interactions"""
    chatbot = Chatbot("test_bot", "Psychology and Behavioral Sciences")
    
    # Test multiple scoring iterations
    for _ in range(10):
        scores = score_chatbot_interaction(chatbot, MORAL_GRAPH_RUBRIC_DIMENSIONS)
        
        # Validate structure
        assert isinstance(scores, dict)
        assert len(scores) == len(MORAL_GRAPH_RUBRIC_DIMENSIONS)
        
        # Validate each dimension score
        for dimension in MORAL_GRAPH_RUBRIC_DIMENSIONS:
            assert dimension.name in scores
            score = scores[dimension.name]
            assert isinstance(score, (int, float))
            assert 1 <= score <= 5
            assert score in dimension.possible_scores

def test_calculate_total_weighted_score():
    """Test weighted score calculation"""
    chatbot = Chatbot("test_bot", "Psychology and Behavioral Sciences")
    
    # Test multiple calculations
    for _ in range(10):
        scores = score_chatbot_interaction(chatbot, MORAL_GRAPH_RUBRIC_DIMENSIONS)
        total_score = calculate_total_weighted_score(scores, MORAL_GRAPH_RUBRIC_DIMENSIONS)
        
        # Validate score
        assert isinstance(total_score, float)
        assert 1.0 <= total_score <= 5.0
        
        # Validate weighted calculation
        expected_score = sum(
            scores[dim.name] * (dim.weight / 100)
            for dim in MORAL_GRAPH_RUBRIC_DIMENSIONS
        )
        assert abs(total_score - expected_score) < 0.0001  # Account for float precision

def test_edge_cases():
    """Test edge cases and error handling"""
    # Test with minimum participants
    df_min = simulate_experiment(num_participants=1)
    assert len(df_min) == 2
    
    # Test with large number of participants
    df_large = simulate_experiment(num_participants=1000)
    assert len(df_large) == 2000
    
    # Test invalid inputs
    with pytest.raises(ValueError):
        simulate_experiment(num_participants=0)
    
    with pytest.raises(ValueError):
        simulate_experiment(num_participants=-1)
