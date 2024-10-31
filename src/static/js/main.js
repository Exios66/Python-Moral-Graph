// Dimensions data from Python
const DIMENSIONS = [
    {
        name: "Accuracy",
        weight: 25,
        description: "Measures the factual correctness and reliability of responses"
    },
    {
        name: "Clarity", 
        weight: 20,
        description: "Evaluates how well ideas are communicated and explained"
    },
    {
        name: "Depth",
        weight: 20, 
        description: "Assesses the level of detail and thoroughness in responses"
    },
    {
        name: "Ethics",
        weight: 20,
        description: "Rates adherence to ethical principles and moral considerations"
    },
    {
        name: "Engagement",
        weight: 15,
        description: "Measures how well the interaction maintains participant interest"
    }
];

// Validate dimension weights sum to 100%
const totalWeight = DIMENSIONS.reduce((sum, dim) => sum + dim.weight, 0);
if (totalWeight !== 100) {
    throw new Error(`Dimension weights must sum to 100%. Current sum: ${totalWeight}`);
}

// Create lookup object for dimension weights
const DIMENSION_WEIGHTS = DIMENSIONS.reduce((obj, dim) => {
    obj[dim.name] = dim.weight / 100; // Convert to decimal
    return obj;
}, {});

// Score thresholds for evaluation
const SCORE_THRESHOLDS = {
    excellent: 4.5,
    good: 3.5,
    acceptable: 2.5,
    poor: 1.5
};