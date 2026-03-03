"""
Socioeconomic vulnerability analysis module.
"""
from typing import Dict

def analyze_vulnerability(socio_data: Dict[str, float]) -> float:
    """
    Calculate socioeconomic vulnerability index (0 to 1).
    Higher is worse.
    """
    # Normalize inputs
    pop_density = min(1.0, socio_data.get('population_density', 100.0) / 1000.0)
    poverty = min(1.0, socio_data.get('poverty_index', 0.2))
    price_pressure = min(1.0, socio_data.get('food_price_pressure', 5.0) / 20.0)
    import_dep = min(1.0, socio_data.get('import_dependency', 0.3))
    
    # Combine with weights
    weights = {
        'pop_density': 0.1,
        'poverty': 0.4,
        'price_pressure': 0.3,
        'import_dep': 0.2
    }
    
    total_vuln = (
        (pop_density * weights['pop_density']) +
        (poverty * weights['poverty']) +
        (price_pressure * weights['price_pressure']) +
        (import_dep * weights['import_dep'])
    )
    return min(1.0, max(0.0, total_vuln))
