# 🚀 Quick Start Guide

Get the Food Security Intelligence System running in 5 minutes!

## Option 1: Local Installation (Recommended for Development)

### Step 1: Install Python
Make sure you have Python 3.8+ installed:
```bash
python --version
```

### Step 2: Clone & Setup
```bash
# Navigate to project directory
cd famine-early-warning

# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Run Backend
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * WARNING in app.run_simple and running via pytest, use 'python -m pytest' instead.
 * Restarting with reloader
```

### Step 5: Open Frontend
In another terminal (keep backend running):

**Option A: Simple file open**
- Navigate to `frontend/dashboard.html`
- Double-click to open in browser
- Or right-click → "Open with Browser"

**Option B: Local web server**
```bash
cd frontend
python -m http.server 8000
# Open http://localhost:8000/dashboard.html
```

### Step 6: Test It!
1. Enter coordinates: `12.9716, 77.5946` (Delhi)
2. Enter district: `New Delhi`
3. Click "Analyze Risk"
4. See the results!

---

## Option 2: Docker (Recommended for Production)

### Prerequisites
- Docker installed: https://www.docker.com/

### Step 1: Build Docker Image
```bash
docker build -t famine-system:latest .
```

### Step 2: Run Container
```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  famine-system:latest
```

### Step 3: Access
- Backend API: `http://localhost:5000/api`
- Dashboard: `http://localhost:8000/dashboard.html`

---

## Option 3: Docker Compose (Easiest)

### Step 1: Create docker-compose.yml
See the docker-compose.yml file in the project root

### Step 2: Start Services
```bash
docker-compose up -d
```

### Step 3: Access
- API: `http://localhost:5000/api`
- Dashboard: `http://localhost:3000`

### Stop Services
```bash
docker-compose down
```

---

## 📝 Testing the API

### Method 1: Browser Dashboard
1. Open `frontend/dashboard.html`
2. Enter coordinates and click "Analyze Risk"

### Method 2: cURL
```bash
curl -X POST http://localhost:5000/api/assess-risk \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 12.9716,
    "longitude": 77.5946,
    "district": "New Delhi"
  }'
```

### Method 3: Python Script
```python
import requests

response = requests.post(
    'http://localhost:5000/api/assess-risk',
    json={
        'latitude': 12.9716,
        'longitude': 77.5946,
        'district': 'New Delhi'
    }
)

print(response.json())
```

---

## 🧪 Test Data & Example Locations

Try these coordinates:

### India
```
New Delhi:     12.9716, 77.5946
Mumbai:        19.0760, 72.8777
Bangalore:     12.9716, 77.5946
Chennai:       13.0827, 80.2707
Kolkata:       22.5726, 88.3639
```

### Global Examples
```
Cairo, Egypt:          30.0444, 31.2357
Lagos, Nigeria:        6.5244, 3.3792
Beijing, China:        39.9042, 116.4074
São Paulo, Brazil:     -23.5505, -46.6333
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
export FLASK_PORT=8888
python app.py
```

### CORS Errors
The backend includes CORS configuration. If you get CORS errors:
- Make sure both frontend and backend are on localhost
- Check that `flask_cors` is installed

### API Not Responding
1. Check backend is running: `http://localhost:5000/api/health`
2. Check the terminal for error messages
3. Verify all dependencies are installed

### Data Issues
- The system uses demo data if APIs are unavailable
- For real data, configure API keys in `.env`
- Check internet connection for API calls

---

## 📚 Next Steps

1. **Customize Risk Model**
   - Edit `models/risk_calculator.py`
   - Adjust weights and thresholds for your region

2. **Add Real Data Sources**
   - Integrate Google Earth Engine for NDVI
   - Connect to local government databases
   - Add NASA climate data

3. **Deploy to Production**
   - Use Docker container
   - Set up CI/CD with GitHub Actions
   - Deploy to AWS/GCP/Azure

4. **Enable Notifications**
   - Add email alerts
   - Integrate with WhatsApp/SMS
   - Send alerts to stakeholders

---

## 📖 Documentation

- Full API docs: See `README.md`
- Architecture: See `ARCHITECTURE.md`
- Data sources: See `DATA_SOURCES.md`
- Deployment: See `DEPLOYMENT.md`

---

## 💡 Tips

- **Development**: Use `FLASK_DEBUG=True` for auto-reload
- **Testing**: Use Postman or Insomnia for API testing
- **Logging**: Check logs in `logs/` directory
- **Performance**: Use batch assessment for multiple regions

---

## ✅ Success Checklist

- [ ] Python installed
- [ ] Dependencies installed
- [ ] Backend running on port 5000
- [ ] Frontend accessible in browser
- [ ] Can enter coordinates and get results
- [ ] API returns JSON responses
- [ ] Risk levels display correctly

---

## 🎓 Learning Resources

- Flask: https://flask.palletsprojects.com/
- NDVI/Satellite: https://earthengine.google.com/
- Food Security: https://www.fao.org/
- Climate Data: https://www.open-meteo.com/

---

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs**: `tail -f logs/famine_system.log`
2. **Test the API**: `curl http://localhost:5000/api/health`
3. **Review error messages** in browser console (F12)
4. **Check documentation** in README.md
5. **Open an issue** on GitHub

---
