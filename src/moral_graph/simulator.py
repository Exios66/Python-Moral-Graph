import random
import pandas as pd
import uuid
from .core import TOPICS, MORAL_GRAPH_RUBRIC_DIMENSIONS, Participant, Chatbot

def assign_chatbots_to_participant(participant, chatbots_pool):
    """
    Assigns two chatbots to the participant:
    1. One that aligns with their most knowledgeable area (strength)
    2. One that aligns with their weakest area (weakness)
    """
    strength_topic = random.choice(participant.strengths) if participant.strengths else random.choice(TOPICS)
    weakness_topic = random.choice(participant.weaknesses) if participant.weaknesses else random.choice(TOPICS)

    strength_chatbot = next((cb for cb in chatbots_pool if cb.specialization == strength_topic), None)
    if not strength_chatbot:
        strength_chatbot = Chatbot(chatbot_id=str(uuid.uuid4()), specialization=strength_topic)
        chatbots_pool.append(strength_chatbot)

    weakness_chatbot = next((cb for cb in chatbots_pool if cb.specialization == weakness_topic), None)
    if not weakness_chatbot:
        weakness_chatbot = Chatbot(chatbot_id=str(uuid.uuid4()), specialization=weakness_topic)
        chatbots_pool.append(weakness_chatbot)

    participant.assigned_chatbots['strength'] = strength_chatbot
    participant.assigned_chatbots['weakness'] = weakness_chatbot

def score_chatbot_interaction(chatbot, rubric_dimensions):
    """Simulates scoring of a chatbot interaction based on rubric dimensions."""
    scores = {}
    for dimension in rubric_dimensions:
        score = random.choice(dimension.possible_scores)
        scores[dimension.name] = score
    chatbot.rubric_scores = scores
    return scores

def calculate_total_weighted_score(chatbot, rubric_dimensions):
    """Calculates the total weighted score for a chatbot based on rubric scores."""
    total = 0
    for dimension in rubric_dimensions:
        score = chatbot.rubric_scores.get(dimension.name, 0)
        weighted_score = score * (dimension.weight / 100)
        total += weighted_score
    return total

def simulate_experiment(num_participants=100):
    """
    Simulates the experiment by creating participants, assigning chatbots,
    scoring interactions, and aggregating the results.
    """
    participants = []
    chatbots_pool = []
    data_records = []

    for i in range(1, num_participants + 1):
        participant_id = f"P{i:04d}"
        
        num_strengths = random.randint(1, 3)
        num_weaknesses = random.randint(1, 3)
        strengths = random.sample(TOPICS, num_strengths)
        weaknesses = random.sample(TOPICS, num_weaknesses)
        
        participant = Participant(participant_id, strengths, weaknesses)
        assign_chatbots_to_participant(participant, chatbots_pool)
        
        for key, chatbot in participant.assigned_chatbots.items():
            scores = score_chatbot_interaction(chatbot, MORAL_GRAPH_RUBRIC_DIMENSIONS)
            total_weighted_score = calculate_total_weighted_score(chatbot, MORAL_GRAPH_RUBRIC_DIMENSIONS)
            
            record = {
                'ParticipantID': participant.participant_id,
                'ChatbotID': chatbot.chatbot_id,
                'Specialization': chatbot.specialization,
                'AssignmentType': key,
                'TotalWeightedScore': total_weighted_score
            }
            
            for dimension in MORAL_GRAPH_RUBRIC_DIMENSIONS:
                record[dimension.name] = scores.get(dimension.name, None)
            
            data_records.append(record)
        
        participants.append(participant)
    
    return pd.DataFrame(data_records)
