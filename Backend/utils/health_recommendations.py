"""
Health Recommendations Utility
Loads and provides health tips from CSV files in HealthPredict folder
"""

import pandas as pd
import os
import ast

class HealthRecommendations:
    def __init__(self):
        """Initialize and load all health recommendation CSV files"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        health_predict_dir = os.path.join(base_dir, "HealthPredict")
        
        # Load all CSV files
        self.descriptions = pd.read_csv(os.path.join(health_predict_dir, "description.csv"))
        self.diets = pd.read_csv(os.path.join(health_predict_dir, "diets.csv"))
        self.medications = pd.read_csv(os.path.join(health_predict_dir, "medications.csv"))
        self.precautions = pd.read_csv(os.path.join(health_predict_dir, "precautions_df.csv"))
        self.workouts = pd.read_csv(os.path.join(health_predict_dir, "workout_df.csv"))
        
    def get_recommendations(self, disease_name):
        """
        Get comprehensive health recommendations for a specific disease
        
        Args:
            disease_name (str): Name of the disease
            
        Returns:
            dict: Comprehensive health recommendations including description, diet, 
                  medications, precautions, and workouts
        """
        try:
            # Initialize result dictionary
            result = {
                "disease": disease_name,
                "description": "",
                "diet": [],
                "medications": [],
                "precautions": [],
                "workouts": [],
                "found": False,
                "suggested_diseases": []
            }
            
            # Try exact match first (case-insensitive)
            desc_row = self.descriptions[self.descriptions['Disease'].str.lower() == disease_name.lower()]
            
            # If no exact match, try partial match by checking keywords
            if desc_row.empty:
                # Try matching by individual words
                keywords = disease_name.lower().split()
                suggestions_set = set()
                
                for keyword in keywords:
                    if len(keyword) > 2:  # Only match words with more than 2 characters
                        matches = self.descriptions[
                            self.descriptions['Disease'].str.lower().str.contains(keyword, na=False, regex=False)
                        ]
                        suggestions_set.update(matches['Disease'].tolist())
                
                if suggestions_set:
                    result["suggested_diseases"] = list(suggestions_set)
                return result
            
            # Found exact match
            result["found"] = True
            result["description"] = desc_row.iloc[0]['Description']
            
            # Get diet recommendations
            diet_row = self.diets[self.diets['Disease'].str.lower() == disease_name.lower()]
            if not diet_row.empty:
                diet_str = diet_row.iloc[0]['Diet']
                try:
                    result["diet"] = ast.literal_eval(diet_str) if isinstance(diet_str, str) else []
                except:
                    result["diet"] = [diet_str]
            
            # Get medications
            med_row = self.medications[self.medications['Disease'].str.lower() == disease_name.lower()]
            if not med_row.empty:
                med_str = med_row.iloc[0]['Medication']
                try:
                    result["medications"] = ast.literal_eval(med_str) if isinstance(med_str, str) else []
                except:
                    result["medications"] = [med_str]
            
            # Get precautions
            prec_row = self.precautions[self.precautions['Disease'].str.lower() == disease_name.lower()]
            if not prec_row.empty:
                precautions_list = []
                for i in range(1, 5):
                    col_name = f'Precaution_{i}'
                    if col_name in prec_row.columns:
                        prec = prec_row.iloc[0][col_name]
                        if pd.notna(prec) and str(prec).strip():
                            precautions_list.append(str(prec).strip())
                result["precautions"] = precautions_list
            
            # Get workout/lifestyle recommendations
            workout_rows = self.workouts[self.workouts['disease'].str.lower() == disease_name.lower()]
            if not workout_rows.empty:
                result["workouts"] = workout_rows['workout'].tolist()
            
            return result
            
        except Exception as e:
            return {
                "disease": disease_name,
                "error": str(e),
                "found": False
            }
    
    def format_recommendations_text(self, disease_name):
        """
        Format recommendations as a comprehensive text suitable for health tips field
        
        Args:
            disease_name (str): Name of the disease
            
        Returns:
            str: Formatted health tips text
        """
        recs = self.get_recommendations(disease_name)
        
        if not recs.get("found"):
            # Check if there are suggested diseases
            if recs.get("suggested_diseases"):
                suggestions = "\n\nℹ️ Did you mean one of these?\n" + "\n".join([f"  • {d}" for d in recs["suggested_diseases"][:5]])
            else:
                suggestions = ""
            
            return f"⚠️ No specific recommendations found for '{disease_name}'{suggestions}\n\n📋 General health tips:\n\n• Follow prescribed medications as directed\n• Maintain a balanced and nutritious diet\n• Get adequate rest and sleep (7-8 hours)\n• Stay well hydrated (8-10 glasses of water daily)\n• Exercise regularly as advised by your doctor\n• Monitor your symptoms and keep a health diary\n• Attend all follow-up appointments\n• Avoid self-medication\n• Report any unusual symptoms immediately\n• Maintain good hygiene practices"
        
        text_parts = []
        
        # Description
        if recs.get("description"):
            text_parts.append(f"📋 About: {recs['description']}\n")
        
        # Medications
        if recs.get("medications"):
            text_parts.append("💊 Recommended Medications:")
            for med in recs["medications"][:5]:  # Limit to 5
                text_parts.append(f"  • {med}")
            text_parts.append("")
        
        # Diet
        if recs.get("diet"):
            text_parts.append("🥗 Dietary Recommendations:")
            for diet in recs["diet"][:5]:  # Limit to 5
                text_parts.append(f"  • {diet}")
            text_parts.append("")
        
        # Precautions
        if recs.get("precautions"):
            text_parts.append("⚠️ Precautions:")
            for prec in recs["precautions"]:
                text_parts.append(f"  • {prec.capitalize()}")
            text_parts.append("")
        
        # Workouts/Lifestyle
        if recs.get("workouts"):
            text_parts.append("🏃 Lifestyle & Exercise:")
            for workout in recs["workouts"][:5]:  # Limit to 5
                text_parts.append(f"  • {workout}")
        
        return "\n".join(text_parts)
    
    def get_all_diseases(self):
        """Get list of all diseases with recommendations available"""
        return self.descriptions['Disease'].tolist()


# Create global instance
health_recommender = HealthRecommendations()
