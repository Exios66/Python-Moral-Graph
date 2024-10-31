import pytest
from moral_graph.core import (
    RubricDimension,
    Participant,
    Chatbot,
    TOPICS,
    MORAL_GRAPH_RUBRIC_DIMENSIONS
)

def test_rubric_dimension_valid_input():
    """Test RubricDimension creation with valid inputs"""
    dimension = RubricDimension(
        name="Test Dimension",
        description="Test description",
        weight=10,
        possible_scores=[1, 2, 3, 4, 5]
    )
    assert dimension.name == "Test Dimension"
    assert dimension.description == "Test description"
    assert dimension.weight == 10
    assert dimension.possible_scores == [1, 2, 3, 4, 5]

def test_rubric_dimension_invalid_input():
    """Test RubricDimension validation with invalid inputs"""
    with pytest.raises(ValueError, match="Name must be a non-empty string"):
        RubricDimension("", "desc", 10, [1,2,3])
        
    with pytest.raises(ValueError, match="Weight must be between 1-100"):
        RubricDimension("Test", "desc", 0, [1,2,3])
        
    with pytest.raises(ValueError, match="All scores must be between 1-5"):
        RubricDimension("Test", "desc", 10, [0,6])

def test_participant_creation():
    """Test Participant object creation and validation"""
    strengths = ["Psychology and Behavioral Sciences"]
    weaknesses = ["Mathematics and Logic"] 
    participant = Participant("P0001", strengths, weaknesses)
    
    assert participant.participant_id == "P0001"
    assert participant.strengths == strengths
    assert participant.weaknesses == weaknesses
    assert participant.assigned_chatbots == {}
    
    # Test invalid inputs
    with pytest.raises(ValueError):
        Participant("", strengths, weaknesses)
    with pytest.raises(ValueError):
        Participant("P0001", [], weaknesses)

def test_chatbot_creation():
    """Test Chatbot object creation and validation"""
    chatbot = Chatbot("C0001", "Psychology and Behavioral Sciences")
    
    assert chatbot.chatbot_id == "C0001"
    assert chatbot.specialization == "Psychology and Behavioral Sciences"
    assert chatbot.rubric_scores == {}
    
    # Test invalid inputs
    with pytest.raises(ValueError):
        Chatbot("", "Psychology")
    with pytest.raises(ValueError):
        Chatbot("C0001", "Invalid Topic")

def test_topics_validation():
    """Test TOPICS constant validation"""
    assert len(TOPICS) > 0, "TOPICS list cannot be empty"
    assert all(isinstance(topic, str) for topic in TOPICS), "All topics must be strings"
    assert all(len(topic.strip()) > 0 for topic in TOPICS), "Topics cannot be empty strings"
    assert len(TOPICS) == len(set(TOPICS)), "Topics must be unique"

def test_moral_graph_rubric_dimensions():
    """Test rubric dimensions validation"""
    # Test total weight equals 100
    total_weight = sum(dim.weight for dim in MORAL_GRAPH_RUBRIC_DIMENSIONS)
    assert total_weight == 100, f"Total weight must be 100, got {total_weight}"
    
    # Test individual dimensions
    for dimension in MORAL_GRAPH_RUBRIC_DIMENSIONS:
        assert isinstance(dimension, RubricDimension), "Must be RubricDimension instance"
        assert 1 <= dimension.weight <= 100, f"Weight must be 1-100, got {dimension.weight}"
        assert len(dimension.possible_scores) > 0, "Must have possible scores"
        assert all(1 <= score <= 5 for score in dimension.possible_scores), "Scores must be 1-5"
        assert len(dimension.name.strip()) > 0, "Name cannot be empty"
        assert len(dimension.description.strip()) > 0, "Description cannot be empty"
