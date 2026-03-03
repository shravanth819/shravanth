"""
Main Flask Application for Food Security Intelligence System
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

from models.risk_calculator import compute_risk, get_explanations_and_interventions
from models.environmental_stress import calculate_stress_index
from models.socioeconomic_analyzer import analyze_vulnerability
from utils.data_fetcher import fetch_climate_data, fetch_ndvi_data, get_demo_socioeconomic_data
from utils.validators import validate_coordinates, sanitize_input, validate_batch_request

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    })

def process_single_region(data: dict) -> dict:
    """Helper to process a single region assessment."""
    lat = data['latitude']
    lon = data['longitude']
    
    # 1. Fetch external data
    climate_data = fetch_climate_data(lat, lon)
    ndvi = fetch_ndvi_data(lat, lon)
    socio_data = get_demo_socioeconomic_data(lat, lon)
    
    # 2. Compute components
    env_stress = calculate_stress_index(climate_data, ndvi)
    crop_stress = 1.0 - max(0.0, ndvi)  # Simplified ndvi mapping
    socio_vuln = analyze_vulnerability(socio_data)
    
    # 3. Overall risk
    score, level, color, confidence = compute_risk(env_stress, crop_stress, socio_vuln)
    
    # 4. Exps & Interventions
    exps, inters = get_explanations_and_interventions(level)
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "region": {
            "name": data.get('region_name', f"Region at {lat},{lon}"),
            "district": data.get('district', "Unknown"),
            "coordinates": {"latitude": lat, "longitude": lon}
        },
        "risk_assessment": {
            "risk_score": round(score, 2),
            "risk_level": level,
            "risk_color": color,
            "confidence": confidence
        },
        "component_scores": {
            "environmental_stress_index": round(env_stress, 2),
            "crop_health_stress_index": round(crop_stress, 2),
            "socioeconomic_vulnerability_index": round(socio_vuln, 2)
        },
        "environmental_data": climate_data,
        "socioeconomic_factors": socio_data,
        "explanations": exps,
        "recommended_interventions": inters,
        "monitoring_period": "14 days",
        "next_assessment_recommended": "In 7 days"
    }


@app.route('/api/assess-risk', methods=['POST'])
def assess_risk():
    data = request.get_json()
    if not data or 'latitude' not in data or 'longitude' not in data:
        return jsonify({"error": "Missing latitude or longitude in payload"}), 400
        
    sanitized = sanitize_input(data)
    if 'latitude' not in sanitized or not validate_coordinates(sanitized['latitude'], sanitized['longitude']):
        return jsonify({"error": "Invalid coordinates"}), 400
        
    result = process_single_region(sanitized)
    return jsonify(result)

@app.route('/api/batch-assess', methods=['POST'])
def batch_assess():
    data = request.get_json()
    if not data or 'regions' not in data:
        return jsonify({"error": "Missing regions array"}), 400
        
    regions = data['regions']
    if not validate_batch_request(regions):
        return jsonify({"error": "Invalid batch request format or too many regions (max 50)"}), 400
        
    results = []
    for r in regions:
        sanitized = sanitize_input(r)
        results.append(process_single_region(sanitized))
        
    return jsonify({
        "timestamp": datetime.utcnow().isoformat(),
        "total_regions": len(results),
        "results": results
    })

@app.route('/api/explain/<level>', methods=['GET'])
def explain_level(level):
    level = level.lower()
    if level not in ['green', 'yellow', 'orange', 'red']:
        return jsonify({"error": "Invalid risk level"}), 400
        
    exps, inters = get_explanations_and_interventions(level)
    return jsonify({
        "level": level.capitalize() + " Risk",
        "description": exps[0] if exps else "No description available",
        "action": inters[0] if inters else "No action specified"
    })

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')
