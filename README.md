# 🌾 Food Security Intelligence System
## Early Famine Risk Detection Engine

An AI-powered regional food security monitoring and early warning platform that uses real-time environmental and socio-economic data to detect agricultural stress and famine risk before it becomes a crisis.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [API Documentation](#api-documentation)
7. [Usage Examples](#usage-examples)
8. [Data Sources](#data-sources)
9. [Monitoring & Deployment](#monitoring--deployment)
10. [Future Enhancements](#future-enhancements)

---

## 🎯 Overview

### The Problem
In many regions, crop failure and famine are detected too late. By the time governments react, crops are already damaged, food prices have spiked, farmers are in debt, and emergency aid is required.

### The Solution
This system detects agricultural stress early by:
- **Continuously monitoring** climate data (rainfall, temperature, humidity)
- **Observing crop health** using NDVI (vegetation indices)
- **Tracking vulnerability** indicators (population density, poverty)
- **Computing risk scores** in real-time
- **Providing actionable intelligence** for proactive decision-making

### Key Insight
Instead of a reactive crisis response, we enable proactive early-warning intelligence.

---

## ✨ Features

### Core Capabilities
- ✅ **Real-time Risk Assessment** - Get food security risk in seconds
- ✅ **Multi-factor Analysis** - Environmental + Socio-economic + Crop health
- ✅ **API-driven Architecture** - Easy integration with other systems
- ✅ **Batch Processing** - Assess up to 50 regions simultaneously
- ✅ **Confidence Scoring** - Know how reliable each assessment is
- ✅ **Actionable Recommendations** - Get suggested interventions

### Risk Levels
- 🟢 **Green** (0-25): Low risk, stable conditions
- 🟡 **Yellow** (25-50): Moderate risk, monitor closely
- 🟠 **Orange** (50-75): High risk, prepare interventions
- 🔴 **Red** (75-100): Critical risk, emergency action needed

---

## 🏗️ Architecture

```
food-security-system/
├── backend/
│   ├── app.py                              # Main Flask API
│   ├── models/
│   │   ├── risk_calculator.py             # Risk scoring logic
│   │   ├── environmental_stress.py        # Climate analysis
│   │   └── socioeconomic_analyzer.py      # Vulnerability analysis
│   ├── utils/
│   │   ├── data_fetcher.py                # API integrations
│   │   └── validators.py                  # Input validation
│   └── requirements.txt
├── frontend/
│   └── dashboard.html                      # Interactive web UI
├── README.md                               # This file
└── .env.example                            # Environment template
```

### Technology Stack
- **Backend**: Flask (Python web framework)
- **APIs**: Open-Meteo (climate data), NASA/USGS (satellite data)
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Database**: JSON (can extend to PostgreSQL/MongoDB)
- **Deployment**: Docker, Gunicorn, Nginx

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/famine-early-warning.git
cd famine-early-warning
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings (see Configuration section)
```

### Step 5: Run Backend API
```bash
python app.py
# Server starts at http://localhost:5000
```

### Step 6: Open Frontend Dashboard
- Open `frontend/dashboard.html` in your browser
- Or serve it with a local server:
```bash
cd frontend
python -m http.server 8000
# Open http://localhost:8000/dashboard.html
```

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
FLASK_ENV=development
FLASK_DEBUG=False
FLASK_PORT=5000

# API Keys (get from respective services)
OPEN_METEO_API_KEY=your_key_here
GOOGLE_EARTH_ENGINE_KEY=your_key_here
```

### Model Configuration
Edit `models/risk_calculator.py` to adjust:
- **Weights**: How much each factor contributes to risk
- **Thresholds**: Risk level cutoffs

Example:
```python
WEIGHTS = {
    'environmental_stress': 0.40,      # 40% weight
    'crop_health_stress': 0.30,        # 30% weight
    'socioeconomic_vulnerability': 0.30  # 30% weight
}
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```
GET /api/health
```

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00",
    "version": "1.0.0"
}
```

---

#### 2. Single Region Risk Assessment
```
POST /api/assess-risk
Content-Type: application/json
```

**Request Body:**
```json
{
    "latitude": 12.9716,
    "longitude": 77.5946,
    "district": "New Delhi",
    "region_name": "Delhi NCR Region"
}
```

**Response:**
```json
{
    "timestamp": "2024-01-15T10:30:00",
    "region": {
        "name": "Delhi NCR Region",
        "district": "New Delhi",
        "coordinates": {
            "latitude": 12.9716,
            "longitude": 77.5946
        }
    },
    "risk_assessment": {
        "risk_score": 0.52,
        "risk_level": "orange",
        "risk_color": "#f97316",
        "confidence": 0.87
    },
    "component_scores": {
        "environmental_stress_index": 0.65,
        "crop_health_stress_index": 0.48,
        "socioeconomic_vulnerability_index": 0.42
    },
    "environmental_data": {
        "current_rainfall_mm": 45.2,
        "temperature_celsius": 28.5,
        "humidity_percent": 62,
        "rainfall_deviation_percent": -25.3
    },
    "socioeconomic_factors": {
        "population_density": 425,
        "poverty_index": 0.35,
        "food_price_pressure": 6.2
    },
    "explanations": [
        "High environmental stress detected. Rainfall deviation is -25.3% from normal with temperature anomalies present.",
        "Vegetation stress indicators (NDVI) show crops are experiencing health challenges."
    ],
    "recommended_interventions": [
        "Activate emergency irrigation schemes",
        "Deploy agricultural input support programs",
        "Engage with food supply chain partners",
        "Prepare targeted food assistance programs"
    ],
    "monitoring_period": "14 days",
    "next_assessment_recommended": "In 7 days"
}
```

---

#### 3. Batch Risk Assessment
```
POST /api/batch-assess
Content-Type: application/json
```

**Request Body:**
```json
{
    "regions": [
        {"latitude": 12.9716, "longitude": 77.5946, "district": "New Delhi"},
        {"latitude": 19.0760, "longitude": 72.8777, "district": "Mumbai"},
        {"latitude": 28.7041, "longitude": 77.1025, "district": "Delhi"}
    ]
}
```

**Response:**
```json
{
    "timestamp": "2024-01-15T10:30:00",
    "total_regions": 3,
    "results": [
        { /* Full assessment for region 1 */ },
        { /* Full assessment for region 2 */ },
        { /* Full assessment for region 3 */ }
    ]
}
```

**Note:** Maximum 50 regions per request.

---

#### 4. Risk Level Explanation
```
GET /api/explain/{risk_level}
```

Where `{risk_level}` is one of: `green`, `yellow`, `orange`, `red`

**Response:**
```json
{
    "level": "High Risk",
    "description": "Significant agricultural stress. Food availability may be impacted.",
    "action": "Activate early warning protocols. Coordinate with supply chain partners.",
    "color": "#f97316"
}
```

---

## 💡 Usage Examples

### Python Client
```python
import requests
import json

API_BASE = "http://localhost:5000/api"

# Single assessment
payload = {
    "latitude": 12.9716,
    "longitude": 77.5946,
    "district": "New Delhi",
    "region_name": "Delhi NCR"
}

response = requests.post(
    f"{API_BASE}/assess-risk",
    json=payload,
    headers={"Content-Type": "application/json"}
)

result = response.json()
print(f"Risk Level: {result['risk_assessment']['risk_level']}")
print(f"Risk Score: {result['risk_assessment']['risk_score']}")
```

### cURL
```bash
# Single region assessment
curl -X POST http://localhost:5000/api/assess-risk \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 12.9716,
    "longitude": 77.5946,
    "district": "New Delhi"
  }'

# Health check
curl http://localhost:5000/api/health
```

### JavaScript (in browser)
```javascript
const payload = {
    latitude: 12.9716,
    longitude: 77.5946,
    district: "New Delhi"
};

fetch('http://localhost:5000/api/assess-risk', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
})
.then(res => res.json())
.then(data => {
    console.log('Risk Level:', data.risk_assessment.risk_level);
    console.log('Risk Score:', data.risk_assessment.risk_score);
})
.catch(err => console.error('Error:', err));
```

---

## 📊 Data Sources

### Climate Data (Free APIs)
- **Open-Meteo**: Rainfall, temperature, humidity (no API key required)
- **NASA POWER**: Historical climate data
- **NOAA**: Weather forecasts and historical data

### Satellite Data
- **Google Earth Engine**: NDVI, vegetation indices
- **USGS Landsat**: Land surface temperature, water indices
- **Sentinel-2**: High-resolution vegetation monitoring

### Socio-Economic Data
- **World Bank Open Data**: Poverty, population
- **National Census Data**: Regional demographics
- **FAO**: Food price indices, agricultural data
- **Local Government Resources**: District-level data

### Data Update Frequency
- Climate data: Daily
- Satellite data: Every 5-16 days (Sentinel-2)
- Socio-economic: Monthly/quarterly
- Risk assessment: Real-time (computed on demand)

---

## 🚀 Monitoring & Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Production Deployment
```bash
# Using Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app

# Using Docker Compose
docker-compose up -d
```

### Monitoring
- Track API response times
- Monitor data fetch success rates
- Alert on high-risk assessments
- Log all requests for audit trail

### Performance Metrics
- Single assessment: < 2 seconds
- Batch assessment (50 regions): < 30 seconds
- Uptime target: 99.5%

---

## 🔮 Future Enhancements

### Short-term (Next 3 months)
- [ ] Add Google Earth Engine integration for real NDVI data
- [ ] Implement historical risk tracking
- [ ] Add automated alerts for high-risk regions
- [ ] Database integration (PostgreSQL)

### Medium-term (6-12 months)
- [ ] Machine learning for risk forecasting
- [ ] Mobile app (iOS/Android)
- [ ] Real-time map visualization
- [ ] Multi-language support

### Long-term (1+ year)
- [ ] Integration with government early warning systems
- [ ] Supply chain risk modeling
- [ ] Humanitarian aid coordination
- [ ] Open-source community contributions

---

## 📝 License

[Specify your license - MIT, Apache 2.0, etc.]

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: [your-email@example.com]
- Discord: [Your Discord Server]

---

## 📚 References

- FAO Food Security Report: https://www.fao.org/
- NASA Earth Observatory: https://earthobservatory.nasa.gov/
- World Bank Open Data: https://data.worldbank.org/
- Google Earth Engine: https://earthengine.google.com/

---

**Last Updated:** January 2024  
**Version:** 1.0.0  
**Status:** Active Development
