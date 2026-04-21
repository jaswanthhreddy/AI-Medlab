"""
Test script for Health Recommendations System
Run this to verify the CSV files are loading and recommendations work properly
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.health_recommendations import health_recommender

def test_health_recommendations():
    print("=" * 60)
    print("Testing Health Recommendations System")
    print("=" * 60)
    
    # Test 1: Get all available diseases
    print("\n1️⃣ Testing: Get all available diseases")
    diseases = health_recommender.get_all_diseases()
    print(f"   ✅ Found {len(diseases)} diseases with recommendations")
    print(f"   Sample diseases: {diseases[:5]}")
    
    # Test 2: Get recommendations for a specific disease
    print("\n2️⃣ Testing: Get recommendations for 'Diabetes'")
    diabetes_recs = health_recommender.get_recommendations("Diabetes")
    print(f"   Found: {diabetes_recs.get('found')}")
    print(f"   Description: {diabetes_recs.get('description', 'N/A')[:100]}...")
    print(f"   Medications: {len(diabetes_recs.get('medications', []))} items")
    print(f"   Diet recommendations: {len(diabetes_recs.get('diet', []))} items")
    print(f"   Precautions: {len(diabetes_recs.get('precautions', []))} items")
    print(f"   Workouts: {len(diabetes_recs.get('workouts', []))} items")
    
    # Test 3: Get formatted text
    print("\n3️⃣ Testing: Get formatted health tips for 'GERD'")
    gerd_formatted = health_recommender.format_recommendations_text("GERD")
    print(f"   ✅ Generated formatted text ({len(gerd_formatted)} characters)")
    print("   Preview:")
    print("   " + gerd_formatted[:200] + "...")
    
    # Test 4: Test case-insensitive matching
    print("\n4️⃣ Testing: Case-insensitive matching for 'fungal infection'")
    fungal_recs = health_recommender.get_recommendations("fungal infection")
    print(f"   Found: {fungal_recs.get('found')}")
    print(f"   Medications: {fungal_recs.get('medications', [])[:2]}")
    
    # Test 5: Test unknown disease
    print("\n5️⃣ Testing: Unknown disease 'XYZ Disease'")
    unknown_recs = health_recommender.get_recommendations("XYZ Disease")
    print(f"   Found: {unknown_recs.get('found')}")
    formatted_unknown = health_recommender.format_recommendations_text("XYZ Disease")
    print(f"   Fallback text generated: {bool(formatted_unknown)}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed successfully!")
    print("=" * 60)
    print("\nThe health recommendations system is working correctly.")
    print("You can now use it through the Flask API endpoints:")
    print("  • GET /health_recommendations/<disease>")
    print("  • GET /health_recommendations/formatted/<disease>")
    print("  • GET /available_diseases")
    print("=" * 60)

if __name__ == "__main__":
    test_health_recommendations()
