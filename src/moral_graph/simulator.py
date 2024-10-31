import itertools
import logging
import numpy as np
import pandas as pd
import random
import uuid
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Core simulation constants
SPECIALIZATIONS = [
    "Psychology", "Sociology", "Natural Sciences", "Mathematics",
    "Computer Science", "Humanities", "Economics", "Medicine"
]

INTERACTION_TYPES = [
    "Question-Answer", "Discussion", "Problem-Solving", 
    "Analysis", "Explanation", "Debate"
]

SCORE_WEIGHTS = {
    "Accuracy": 0.25,
    "Clarity": 0.20, 
    "Depth": 0.20,
    "Ethics": 0.15,
    "Engagement": 0.20
}

# Validate score weights sum to 1.0
if not np.isclose(sum(SCORE_WEIGHTS.values()), 1.0):
    raise ValueError("Score weights must sum to 1.0")

# Simulation parameters
MIN_INTERACTIONS = 5  # Minimum interactions per participant
MAX_INTERACTIONS = 12 # Maximum interactions per participant
POSSIBLE_SCORES = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]  # Granular scoring scale

# Score thresholds for evaluation
THRESHOLD_EXCELLENT = 4.5
THRESHOLD_GOOD = 3.5
THRESHOLD_ACCEPTABLE = 2.5
THRESHOLD_POOR = 1.5

@dataclass
class RubricDimension:
    """A dimension in the evaluation rubric with scoring criteria."""
    name: str
    description: str
    weight: float
    possible_scores: List[float]

    def __post_init__(self):
        """Validate the dimension parameters."""
        if not (0 <= self.weight <= 1):
            raise ValueError("Weight must be between 0 and 1")
        if not self.possible_scores:
            raise ValueError("Must provide possible scores")
        if not all(isinstance(s, (int, float)) for s in self.possible_scores):
            raise ValueError("All scores must be numeric")
        self.possible_scores = sorted(self.possible_scores)

    def validate_score(self, score: float) -> bool:
        """Check if a score is valid for this dimension."""
        return score in self.possible_scores

def generate_participant_interactions(participant_id: str) -> List[Dict]:
    """
    Generate a realistic set of interactions for a participant.
    
    Args:
        participant_id: Unique identifier for the participant
        
    Returns:
        List of dictionaries containing interaction data
        
    Raises:
        ValueError: If participant_id is empty
    """
    if not participant_id:
        raise ValueError("Participant ID cannot be empty")
        
    try:
        num_interactions = random.randint(MIN_INTERACTIONS, MAX_INTERACTIONS)
        interactions = []
        
        # Track specialization distribution to ensure realistic variety
        specialization_counts = {spec: 0 for spec in SPECIALIZATIONS}
        
        for _ in range(num_interactions):
            # Favor previously used specializations but allow for variety
            if random.random() < 0.7 and any(count > 0 for count in specialization_counts.values()):
                weights = [1 / (count + 1) for count in specialization_counts.values()]
                specialization = random.choices(SPECIALIZATIONS, weights=weights)[0]
            else:
                specialization = random.choice(SPECIALIZATIONS)
            
            specialization_counts[specialization] += 1
            
            # Generate correlated scores (good performance tends to be consistent)
            base_score = random.gauss(3.5, 0.7)  # Center around 3.5 with some variance
            base_score = max(1.0, min(5.0, base_score))  # Clamp between 1.0 and 5.0
            
            # Generate individual dimension scores with correlation to base score
            scores = {}
            for dimension in SCORE_WEIGHTS.keys():
                score = base_score + random.gauss(0, 0.5)  # Add some noise
                score = min(5.0, max(1.0, score))  # Clamp between 1.0 and 5.0
                # Round to nearest valid score
                scores[dimension] = min(POSSIBLE_SCORES, key=lambda x: abs(x - score))
            
            interaction = {
                'ParticipantID': participant_id,
                'InteractionID': str(uuid.uuid4()),
                'Specialization': specialization,
                'InteractionType': random.choice(INTERACTION_TYPES),
                **scores
            }
            
            # Calculate weighted score
            total_score = sum(scores[dim] * SCORE_WEIGHTS[dim] 
                            for dim in SCORE_WEIGHTS.keys())
            interaction['TotalWeightedScore'] = round(total_score, 2)
            
            interactions.append(interaction)
        
        return interactions
        
    except Exception as e:
        logger.error(f"Error generating interactions for participant {participant_id}: {str(e)}")
        raise

def simulate_experiment(num_participants: int = 100) -> pd.DataFrame:
    """
    Simulate a complete experiment with multiple participants.
    
    Args:
        num_participants: Number of participants to simulate (default: 100)
        
    Returns:
        DataFrame containing all simulated interactions and scores
        
    Raises:
        ValueError: If num_participants is less than 1
        RuntimeError: If no valid interactions were generated
    """
    if num_participants < 1:
        raise ValueError("Number of participants must be at least 1")
        
    try:
        all_interactions = []
        
        # Generate unique participant IDs
        participant_ids = [str(uuid.uuid4()) for _ in range(num_participants)]
        
        # Generate interactions for each participant
        for participant_id in participant_ids:
            try:
                participant_interactions = generate_participant_interactions(participant_id)
                all_interactions.extend(participant_interactions)
            except Exception as e:
                logger.warning(f"Failed to generate interactions for participant {participant_id}: {str(e)}")
                continue
        
        # Convert to DataFrame
        results_df = pd.DataFrame(all_interactions)
        
        if results_df.empty:
            raise RuntimeError("No valid interactions were generated")
        
        # Add metadata
        results_df['Timestamp'] = pd.Timestamp.now()
        results_df['SimulationVersion'] = '1.0.0'
        
        # Sort by ParticipantID and Timestamp for consistency
        results_df = results_df.sort_values(['ParticipantID', 'Timestamp'])
        
        return results_df
        
    except Exception as e:
        logger.error(f"Error in experiment simulation: {str(e)}")
        raise
