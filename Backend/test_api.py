import requests
import json

print("=" * 60)
print("TESTING PREDICTION API")
print("=" * 60)

base_url = "http://127.0.0.1:5000"

# Test 1: Fever and cough
test_cases = [
    {
        "name": "Test 1: Fever + Cough",
        "data": {
            "age": 30,
            "gender": "Male",
            "symptoms": ["fever", "cough"]
        }
    },
    {
        "name": "Test 2: Headache + Dizziness",
        "data": {
            "age": 45,
            "gender": "Female",
            "symptoms": ["headache", "dizziness"]
        }
    },
    {
        "name": "Test 3: Chest pain + Shortness of breath",
        "data": {
            "age": 60,
            "gender": "Male",
            "symptoms": ["chest pain", "shortness of breath"]
        }
    },
    {
        "name": "Test 4: Nausea + Vomiting + Diarrhea",
        "data": {
            "age": 25,
            "gender": "Other",
            "symptoms": ["nausea", "vomiting", "diarrhea"]
        }
    },
    {
        "name": "Test 5: Loss of taste + Loss of smell",
        "data": {
            "age": 35,
            "gender": "Female",
            "symptoms": ["loss of taste", "loss of smell"]
        }
    }
]

print("\nRunning test cases...")
print()

for test in test_cases:
    print(f"\n{test['name']}")
    print(f"  Input: {test['data']}")
    
    try:
        response = requests.post(f"{base_url}/predict", json=test['data'])
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ Prediction: {result['predicted_disease']}")
        else:
            print(f"  ❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"  ❌ Connection error: {e}")
        print("  (Make sure Flask app is running: python app.py)")
        break

print("\n" + "=" * 60)
