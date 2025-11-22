"""
🌟 FESTIVAL TRANSMISSION - SIMPLE FLASK TEST
Basic version for testing without complex dependencies
"""

from flask import Flask, request, jsonify
import json
import uuid
import hashlib
from datetime import datetime, timezone

app = Flask(__name__)

def get_sacred_season():
    """Get current sacred season"""
    current_month = datetime.now(timezone.utc).month
    
    if current_month in [12, 1, 2]:
        return "❄️ Winter Solstice - Season of Reflection"
    elif current_month in [3, 4, 5]:
        return "🌸 Spring Equinox - Season of Renewal"
    elif current_month in [6, 7, 8]:
        return "☀️ Summer Solstice - Season of Radiance"
    elif current_month in [9, 10, 11]:
        return "🍂 Autumn Equinox - Season of Harvest"
    else:
        return "🌟 Eternal Season - Beyond Time"

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'service': 'Festival Transmission System',
        'status': 'ACTIVE',
        'flame_status': 'ETERNAL_BURNING',
        'current_season': get_sacred_season(),
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

@app.route('/test-ceremony', methods=['POST'])
def test_ceremony():
    """Test ceremony submission"""
    try:
        data = request.get_json() or {}
        
        # Generate response
        result = {
            'transmission_id': f"test_{uuid.uuid4().hex[:8]}",
            'status': 'TEST_SUCCESSFUL',
            'ceremony': {
                'rite': data.get('rite', 'Test Rite'),
                'sacred_season': get_sacred_season(),
            },
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🌟 Starting Festival Transmission Test Server...")
    app.run(host='127.0.0.1', port=8888, debug=True)