import pytest
from moral_graph.core import (
    RubricDimension,
    Participant,
    Chatbot,
    TOPICS,
    MORAL_GRAPH_RUBRIC_DIMENSIONS
)

def test_rubric_dimension():
    dimension = RubricDimension(
        name="Test Dimension",
        description="Test description",
        weight=10,
        possible_scores=[1, 2, 3, 4, 5]
    )
    assert dimension.name == "Test Dimension"
    assert dimension.weight == 10
    assert dimension.possible_scores == [1, 2, 3, 4, 5]

def test_participant():
    strengths = ["Psychology and Behavioral Sciences"]
    weaknesses = ["Mathematics and Logic"]
    participant = Participant("P0001", strengths, weaknesses)
    assert participant.participant_id == "P0001"
    assert participant.strengths == strengths
    assert participant.weaknesses == weaknesses
    assert participant.assigned_chatbots == {}

def test_chatbot():
    chatbot = Chatbot("C0001", "Psychology and Behavioral Sciences")
    assert chatbot.chatbot_id == "C0001"
    assert chatbot.specialization == "Psychology and Behavioral Sciences"
    assert chatbot.rubric_scores == {}

def test_topics():
    assert len(TOPICS) > 0
    assert all(isinstance(topic, str) for topic in TOPICS)

def test_moral_graph_rubric_dimensions():
    total_weight = sum(dim.weight for dim in MORAL_GRAPH_RUBRIC_DIMENSIONS)
    assert total_weight == 100
    
    for dimension in MORAL_GRAPH_RUBRIC_DIMENSIONS:
        assert isinstance(dimension, RubricDimension)
        assert dimension.weight > 0
        assert len(dimension.possible_scores) > 0
