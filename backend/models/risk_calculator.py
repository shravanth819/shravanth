"""
Core risk scoring logic.
"""
from typing import Tuple

WEIGHTS = {
    'environmental_stress': 0.40,
    'crop_health_stress': 0.30,
    'socioeconomic_vulnerability': 0.30
}

THRESHOLDS = {
    'green': (0.0, 0.25),
    'yellow': (0.25, 0.50),
    'orange': (0.50, 0.75),
    'red': (0.75, 1.0)
}

def compute_risk(env_stress: float, crop_stress: float, socio_vuln: float) -> Tuple[float, str, str, float]:
    """
    Compute composite risk score and classification.
    Returns: (score, risk_level, color, confidence)
    """
    score = (
        (env_stress * WEIGHTS['environmental_stress']) +
        (crop_stress * WEIGHTS['crop_health_stress']) +
        (socio_vuln * WEIGHTS['socioeconomic_vulnerability'])
    )
    
    score = min(1.0, max(0.0, score))
    
    level = 'green'
    color = '#22c55e'
    if score >= THRESHOLDS['red'][0]:
        level = 'red'
        color = '#ef4444'
    elif score >= THRESHOLDS['orange'][0]:
        level = 'orange'
        color = '#f97316'
    elif score >= THRESHOLDS['yellow'][0]:
        level = 'yellow'
        color = '#eab308'
        
    confidence = 0.85 # static confidence for demo
    
    return score, level, color, confidence

def get_explanations_and_interventions(level: str) -> Tuple[list, list]:
    """Return reasons and suggested interventions for a given level."""
    explanations = []
    interventions = []
    
    if level == 'red':
        explanations.append("Critical risk factors detected across environmental and socio-economic indicators.")
        interventions.extend(["Declare agricultural emergency", "Deploy immediate food assistance", "Coordinate with international aid"])
    elif level == 'orange':
        explanations.append("High environmental stress detected with significant crop vulnerability.")
        interventions.extend(["Activate emergency irrigation schemes", "Deploy agricultural input support programs", "Prepare targeted food assistance programs"])
    elif level == 'yellow':
        explanations.append("Moderate stress detected. Early warning indicators triggered.")
        interventions.extend(["Monitor situation closely", "Increase frequency of data collection", "Review state reserves"])
    else:
        explanations.append("Normal conditions detected. No widespread stress observed.")
        interventions.extend(["Continue standard monitoring programs", "Support regular agricultural activities"])
        
    return explanations, interventions
