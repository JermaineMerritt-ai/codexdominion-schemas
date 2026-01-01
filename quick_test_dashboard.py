import requests
import sys

try:
    response = requests.get('http://localhost:5000/creative/')
    print(f'✅ Status: {response.status_code}')
    if 'Creative Intelligence Engine' in response.text:
        print('✅ Dashboard HTML contains correct title')
        print(f'✅ Response length: {len(response.text)} characters')
        sys.exit(0)
    else:
        print('❌ Dashboard title not found')
        sys.exit(1)
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
