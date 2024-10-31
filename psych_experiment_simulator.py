import itertools
import pandas as pd
import random
import uuid
from typing import List, Dict, Generator, Optional
import logging
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np
from datetime import datetime

# Configure logging with both file and console handlers
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('experiment.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# -------------------------------
# 1. Define Topics and Disciplines  
# -------------------------------

TOPICS = [
    "Psychology and Behavioral Sciences",
    "Sociology and Anthropology", 
    "Natural Sciences (Physics, Chemistry, Biology)",
    "Mathematics and Logic",
    "Technology and Computer Science", 
    "Humanities (History, Philosophy, Literature)",
    "Economics and Business",
    "Health and Medicine"
]

# -------------------------------
# 2. Define the Moral Graph Rubric
# -------------------------------

@dataclass
class RubricDimension:
    """Represents a dimension in the evaluation rubric"""
    name: str
    description: str 
    weight: int
    possible_scores: List[int]

    def __post_init__(self):
        """Validate dimension attributes"""
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Name must be a non-empty string")
            
        if not isinstance(self.description, str) or not self.description.strip():
            raise ValueError("Description must be a non-empty string")
            
        if not isinstance(self.weight, int):
            raise ValueError("Weight must be an integer")
            
        if not (1 <= self.weight <= 100):
            raise ValueError(f"Weight must be between 1-100, got {self.weight}")
            
        if not isinstance(self.possible_scores, list):
            raise ValueError("Possible scores must be a list")
            
        if not self.possible_scores:
            raise ValueError("Possible scores cannot be empty")
            
        if not all(isinstance(score, int) for score in self.possible_scores):
            raise ValueError("All scores must be integers")
            
        if not all(1 <= score <= 5 for score in self.possible_scores):
            raise ValueError("All scores must be between 1-5")

# Define rubric dimensions
MORAL_GRAPH_RUBRIC_DIMENSIONS = [
    RubricDimension(
        name="Ethical Alignment",
        description="Alignment with ethical guidelines.",
        weight=20,
        possible_scores=[1, 2, 3, 4, 5]
    ),
    RubricDimension(
        name="Empathy and Emotional Intelligence", 
        description="Ability to understand and respond to emotions.",
        weight=15,
        possible_scores=[1, 2, 3, 4, 5]
    ),
    RubricDimension(
        name="Accuracy and Reliability",
        description="Correctness and dependability of information.",
        weight=20,
        possible_scores=[1, 2, 3, 4, 5]
    ),
    RubricDimension(
        name="Engagement and Responsiveness",
        description="Maintaining participant interest and timely responses.",
        weight=10,
        possible_scores=[1, 2, 3, 4, 5]
    ),
    RubricDimension(
        name="Cultural Sensitivity",
        description="Respect for diverse cultural backgrounds.",
        weight=10,
        possible_scores=[1, 2, 3, 4, 5]
    ),
    RubricDimension(
        name="Conflict Resolution and Problem-Solving",
        description="Effectiveness in addressing disagreements or complex issues.",
        weight=10,
        possible_scores=[1, 2, 3, 4, 5]
    ),
    RubricDimension(
        name="Privacy and Confidentiality",
        description="Handling of sensitive participant information.",
        weight=10,
        possible_scores=[1, 2, 3, 4, 5]
    ),
    RubricDimension(
        name="Adaptability and Learning",
        description="Capability to learn from interactions and improve.",
        weight=5,
        possible_scores=[1, 2, 3, 4, 5]
    )
]

# Validate total weight
TOTAL_WEIGHT = sum(dimension.weight for dimension in MORAL_GRAPH_RUBRIC_DIMENSIONS)
if TOTAL_WEIGHT != 100:
    raise ValueError(f"Total weight must be 100%, got {TOTAL_WEIGHT}%")

# -------------------------------
# 3. Generate Score Combinations
# -------------------------------

def generate_all_score_combinations(
    rubric_dimensions: List[RubricDimension]
) -> Generator[Dict[str, int], None, None]:
    """
    Generates all possible score combinations for the given rubric dimensions.
    
    Args:
        rubric_dimensions: List of RubricDimension objects
        
    Yields:
        Dictionary mapping dimension names to scores
        
    Raises:
        ValueError: If rubric_dimensions is empty
    """
    if not rubric_dimensions:
        raise ValueError("Rubric dimensions list cannot be empty")
        
    try:
        dimension_names = [dim.name for dim in rubric_dimensions]
        dimension_scores = [dim.possible_scores for dim in rubric_dimensions]
        
        for combination in itertools.product(*dimension_scores):
            yield dict(zip(dimension_names, combination))
            
    except Exception as e:
        logger.error(f"Error generating score combinations: {str(e)}")
        raise

# -------------------------------
# 4. Participant Simulation
# -------------------------------

@dataclass 
class Chatbot:
    """Represents an AI chatbot in the experiment"""
    chatbot_id: str
    specialization: str
    rubric_scores: Dict[str, int] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate chatbot attributes"""
        if not isinstance(self.chatbot_id, str) or not self.chatbot_id.strip():
            raise ValueError("Chatbot ID must be a non-empty string")
            
        if self.specialization not in TOPICS:
            raise ValueError(f"Invalid specialization: {self.specialization}")

@dataclass
class Participant:
    """Represents a participant in the experiment"""
    participant_id: str
    strengths: List[str]
    weaknesses: List[str]
    assigned_chatbots: Dict[str, Chatbot] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate participant attributes"""
        if not isinstance(self.participant_id, str) or not self.participant_id.strip():
            raise ValueError("Participant ID must be a non-empty string")
            
        if not all(topic in TOPICS for topic in self.strengths):
            raise ValueError("Invalid strength topic")
            
        if not all(topic in TOPICS for topic in self.weaknesses):
            raise ValueError("Invalid weakness topic")
            
        if any(topic in self.weaknesses for topic in self.strengths):
            raise ValueError("A topic cannot be both a strength and weakness")

def assign_chatbots_to_participant(
    participant: Participant,
    chatbots_pool: List[Chatbot]
) -> None:
    """
    Assigns chatbots to a participant based on their strengths and weaknesses.
    
    Args:
        participant: Participant object to assign chatbots to
        chatbots_pool: List of available Chatbot objects
        
    Raises:
        ValueError: If participant or chatbots_pool is invalid
    """
    if not isinstance(participant, Participant):
        raise ValueError("Invalid participant object")
        
    if not isinstance(chatbots_pool, list):
        raise ValueError("Chatbots pool must be a list")
    
    try:
        # Select topics
        strength_topic = random.choice(participant.strengths) if participant.strengths else random.choice(TOPICS)
        weakness_topic = random.choice(participant.weaknesses) if participant.weaknesses else random.choice(TOPICS)

        # Find or create chatbots
        for assignment_type, topic in [("strength", strength_topic), ("weakness", weakness_topic)]:
            chatbot = next((cb for cb in chatbots_pool if cb.specialization == topic), None)
            if not chatbot:
                chatbot = Chatbot(chatbot_id=str(uuid.uuid4()), specialization=topic)
                chatbots_pool.append(chatbot)
            participant.assigned_chatbots[assignment_type] = chatbot

    except Exception as e:
        logger.error(f"Error assigning chatbots to participant {participant.participant_id}: {str(e)}")
        raise

# -------------------------------
# 5. Scoring Mechanism
# -------------------------------

def score_chatbot_interaction(
    chatbot: Chatbot,
    rubric_dimensions: List[RubricDimension]
) -> Dict[str, int]:
    """
    Scores a chatbot interaction across all rubric dimensions.
    
    Args:
        chatbot: Chatbot object to score
        rubric_dimensions: List of RubricDimension objects
        
    Returns:
        Dictionary of dimension scores
        
    Raises:
        ValueError: If chatbot or rubric_dimensions is invalid
    """
    if not isinstance(chatbot, Chatbot):
        raise ValueError("Invalid chatbot object")
        
    if not rubric_dimensions:
        raise ValueError("Rubric dimensions list cannot be empty")
    
    try:
        scores = {}
        for dimension in rubric_dimensions:
            # Use weighted random choice to favor middle scores
            weights = [0.1, 0.2, 0.4, 0.2, 0.1]  # Favors score of 3
            scores[dimension.name] = random.choices(
                dimension.possible_scores,
                weights=weights,
                k=1
            )[0]
        chatbot.rubric_scores = scores
        return scores
        
    except Exception as e:
        logger.error(f"Error scoring chatbot {chatbot.chatbot_id}: {str(e)}")
        raise

def calculate_total_weighted_score(
    chatbot: Chatbot,
    rubric_dimensions: List[RubricDimension]
) -> float:
    """
    Calculates total weighted score for a chatbot.
    
    Args:
        chatbot: Chatbot object with scores
        rubric_dimensions: List of RubricDimension objects
        
    Returns:
        Float representing total weighted score
        
    Raises:
        ValueError: If chatbot or rubric_dimensions is invalid
    """
    if not isinstance(chatbot, Chatbot):
        raise ValueError("Invalid chatbot object")
        
    if not rubric_dimensions:
        raise ValueError("Rubric dimensions list cannot be empty")
        
    if not chatbot.rubric_scores:
        raise ValueError("Chatbot has no scores")
    
    try:
        total = 0.0
        for dimension in rubric_dimensions:
            score = chatbot.rubric_scores.get(dimension.name)
            if score is None:
                raise ValueError(f"Missing score for dimension: {dimension.name}")
            total += score * (dimension.weight / 100)
        return round(total, 2)
        
    except Exception as e:
        logger.error(f"Error calculating score for chatbot {chatbot.chatbot_id}: {str(e)}")
        raise

# -------------------------------
# 6. Data Storage and Export
# -------------------------------

def simulate_experiment(num_participants: int = 100) -> pd.DataFrame:
    """
    Runs a complete experiment simulation.
    
    Args:
        num_participants: Number of participants to simulate
        
    Returns:
        DataFrame containing experiment results
        
    Raises:
        ValueError: If num_participants is invalid
    """
    if not isinstance(num_participants, int) or num_participants < 1:
        raise ValueError("Number of participants must be a positive integer")
    
    try:
        participants = []
        chatbots_pool = []
        data_records = []

        for i in range(1, num_participants + 1):
            # Create participant
            participant_id = f"P{i:04d}"
            num_strengths = random.randint(1, 3)
            num_weaknesses = random.randint(1, 3)
            
            # Ensure no overlap between strengths and weaknesses
            all_topics = TOPICS.copy()
            strengths = random.sample(all_topics, num_strengths)
            remaining_topics = [t for t in all_topics if t not in strengths]
            weaknesses = random.sample(remaining_topics, num_weaknesses)
            
            participant = Participant(participant_id, strengths, weaknesses)
            assign_chatbots_to_participant(participant, chatbots_pool)
            
            # Score interactions
            for key, chatbot in participant.assigned_chatbots.items():
                scores = score_chatbot_interaction(chatbot, MORAL_GRAPH_RUBRIC_DIMENSIONS)
                total_score = calculate_total_weighted_score(chatbot, MORAL_GRAPH_RUBRIC_DIMENSIONS)
                
                record = {
                    'ParticipantID': participant_id,
                    'ChatbotID': chatbot.chatbot_id,
                    'Specialization': chatbot.specialization,
                    'AssignmentType': key,
                    'TotalWeightedScore': total_score,
                    'Timestamp': datetime.now().isoformat(),
                    **scores
                }
                data_records.append(record)
            
            participants.append(participant)

        return pd.DataFrame(data_records)

    except Exception as e:
        logger.error(f"Error in experiment simulation: {str(e)}")
        raise

def export_data(df: pd.DataFrame, filename: str = "experiment_results.csv") -> None:
    """
    Exports experiment data to CSV.
    
    Args:
        df: DataFrame containing results
        filename: Output filename
        
    Raises:
        ValueError: If df is empty or filename is invalid
    """
    if df.empty:
        raise ValueError("DataFrame is empty")
        
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("Invalid filename")
    
    try:
        # Create output directory if it doesn't exist
        output_dir = Path("data/outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / filename
        df.to_csv(output_path, index=False)
        logger.info(f"Data exported to {output_path.absolute()}")
        
    except Exception as e:
        logger.error(f"Error exporting data: {str(e)}")
        raise

# -------------------------------
# 7. Main Execution
# -------------------------------

if __name__ == "__main__":
    try:
        # Run simulation
        start_time = datetime.now()
        logger.info("Starting experiment simulation")
        
        num_participants = 100
        experiment_data = simulate_experiment(num_participants=num_participants)
        
        # Calculate and display summary statistics
        logger.info("\nExperiment Summary:")
        logger.info(f"Total participants: {num_participants}")
        logger.info(f"Total interactions: {len(experiment_data)}")
        logger.info(f"Simulation duration: {datetime.now() - start_time}")
        
        logger.info("\nAverage scores per dimension:")
        for dim in MORAL_GRAPH_RUBRIC_DIMENSIONS:
            avg = experiment_data[dim.name].mean()
            std = experiment_data[dim.name].std()
            logger.info(f"{dim.name}:")
            logger.info(f"  Mean: {avg:.2f}")
            logger.info(f"  Std Dev: {std:.2f}")
            
        # Export results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_data(experiment_data, f"experiment_results_{timestamp}.csv")
        
    except Exception as e:
        logger.error(f"Fatal error in experiment: {str(e)}")
        raise
