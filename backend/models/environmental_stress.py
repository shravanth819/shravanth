"""
Climate analysis and environmental stress calculations.
"""
from typing import Dict

def calculate_stress_index(climate_data: Dict[str, float], ndvi: float) -> float:
    """
    Calculate environmental stress index (0 to 1).
    Higher is worse.
    """
    # Base stress from NDVI (low NDVI = high stress)
    ndvi_stress = 1.0 - max(0.0, ndvi)
    
    # Rainfall deficit stress
    rain_dev = climate_data.get('rainfall_deviation_percent', 0.0)
    rain_stress = 0.0
    if rain_dev < 0:
        # e.g., -25% deviation -> 0.25 stress
        rain_stress = min(1.0, abs(rain_dev) / 100.0)
        
    # Temperature anomaly stress (rough proxy)
    temp = climate_data.get('temperature_celsius', 25.0)
    temp_stress = 0.0
    if temp > 35.0:
        temp_stress = min(1.0, (temp - 35.0) / 10.0)
        
    # Combine with weights
    weights = {'ndvi': 0.5, 'rain': 0.3, 'temp': 0.2}
    total_stress = (
        (ndvi_stress * weights['ndvi']) +
        (rain_stress * weights['rain']) +
        (temp_stress * weights['temp'])
    )
    return min(1.0, max(0.0, total_stress))
