"""
Input validation utilities for the Food Security System.
"""
from typing import Dict, Any, List

def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate latitude and longitude."""
    try:
        lat = float(lat)
        lon = float(lon)
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return False
        return True
    except (ValueError, TypeError):
        return False

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize input payload."""
    sanitized = {}
    if 'latitude' in data:
        sanitized['latitude'] = float(data['latitude'])
    if 'longitude' in data:
        sanitized['longitude'] = float(data['longitude'])
    if 'district' in data:
        sanitized['district'] = str(data['district']).strip()
    if 'region_name' in data:
        sanitized['region_name'] = str(data['region_name']).strip()
    return sanitized

def validate_batch_request(regions: List[Dict[str, Any]], max_regions: int = 50) -> bool:
    """Validate batch requests."""
    if not isinstance(regions, list):
        return False
    if len(regions) > max_regions:
        return False
    for r in regions:
        if 'latitude' not in r or 'longitude' not in r:
            return False
        if not validate_coordinates(r['latitude'], r['longitude']):
            return False
    return True
