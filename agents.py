import os
import json
from typing import Dict, Any, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your_openai_api_key_here":
    print("Warning: OPENAI_API_KEY is not set properly in .env file.")


def get_client():
    """Helper to ensure client is initialized with the latest API key"""
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_cosmetic_product(product_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cosmetic Agent: Analyzes ingredients, safety, and skin compatibility.
    """
    openai_client = get_client()
    
    prompt = f"""
    Analyze the following cosmetic product data:
    {json.dumps(product_data, indent=2)}
    
    You are an advanced AI cosmetics and personal care analysis specialist.
    Provide a detailed, science-based assessment in strict JSON format.
    
    MANDATORY Output Format:
    You MUST return ONLY valid JSON in this exact structure:
    {{
      "product_type": "cosmetic",
      "health_score": {{
        "overall_score": 0.0,
        "safety_score": 0.0,
        "ingredient_score": 0.0,
        "category": "excellent/good/fair/poor/very poor",
        "summary": "string"
      }},
      "ingredient_analysis": [
        {{
          "name": "Ingredient Name",
          "safety_rating": 0.0,
          "concerns": ["string"],
          "benefits": ["string"],
          "function": "string",
          "alternatives": ["string"]
        }}
      ],
      "cosmetic_analysis": {{
        "skin_compatibility": "string",
        "irritation_potential": "string",
        "comedogenic_rating": 0,
        "environmental_impact": "string",
        "efficacy_rating": "string",
        "pregnancy_safe": true,
        "sensitive_skin_suitable": true
      }},
      "safety_assessment": {{
        "allergen_risk": "low/moderate/high",
        "endocrine_disruptor_risk": "none/low/moderate/high",
        "carcinogen_risk": "none/low/moderate/high",
        "overall_safety": "string",
        "regulatory_approval": "string"
      }},
      "skin_type_recommendations": {{
        "dry_skin": "string",
        "oily_skin": "string",
        "sensitive_skin": "string",
        "acne_prone": "string",
        "mature_skin": "string"
      }},
      "scoring_breakdown": {{
        "positive_aspects": [
          {{"name": "string", "points": 10, "reason": "string"}}
        ],
        "negative_aspects": [
          {{"name": "string", "points": -10, "reason": "string"}}
        ],
        "total_positive_points": 0,
        "total_negative_points": 0,
        "net_score": 0,
        "total_possible_points": 100,
        "percentage_calculation": "string",
        "final_score": 0.0
      }},
      "recommendations": {{
        "should_use": true,
        "warnings": ["string"],
        "tips": ["string"],
        "alternatives": ["string"],
        "target_audience": ["string"]
      }},
      "analysis_summary": "string",
      "processing_notes": ["string"]
    }}
    
    Do NOT include markdown formatting like ```json. Return ONLY the raw JSON string.
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional cosmetics scientist."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )
    
    return json.loads(response.choices[0].message.content)


def analyze_skin(image_base64: str, user_description: str) -> Dict[str, Any]:
    """
    Skin Analyzer Agent: Analyzes skin image and user description.
    """
    openai_client = get_client()
    
    prompt = f"""
    Analyze the provided skin image and compare it with the user's description.
    User's description: {user_description}
    
    CRITICAL: You MUST return ONLY valid JSON matching the provided schema.
    
    Analyze the image and return JSON with EXACT field names:
    - detected_skin_type: dry, oily, combination, normal, or sensitive
    - oily_percentage: percentage of oily skin (number)
    - allergic_percentage: percentage of allergic skin (number)
    - eczema_percentage: percentage of eczema skin (number)
    - detected_skin_tone: very light, light, medium, or deep
    - visible_concerns: list of issues like acne, wrinkles, dark spots, redness, texture
    - hydration_level: well-hydrated, normal, or dehydrated
    - validation_mismatch: boolean, true if user description doesn't match image
    - mismatch_explanation: string explaining any mismatch, or null
    - recommended_routine: dict with keys: cleansing, moisturizing, treatment, sunscreen
    - product_suggestions: list of product types to use
    - ingredients_to_look_for: list of beneficial ingredients
    - ingredients_to_avoid: list of ingredients to avoid
    - lifestyle_tips: list of lifestyle recommendations
    - health_warnings: list of concerns requiring dermatologist, or null
    
    If you cannot see the image clearly, return valid JSON with reasonable estimates.
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )
    
    return json.loads(response.choices[0].message.content)


def generate_workout_plan(user_profile: Dict[str, Any], preferences: Dict[str, Any]) -> Dict[str, Any]:
    """
    Workout Generation Agent: Generates a personalized 7-day workout plan.
    """
    openai_client = get_client()
    
    prompt = f"""
    Generate a personalized 7-day workout plan based on the user profile and preferences.
    
    USER PROFILE:
    {json.dumps(user_profile, indent=2)}
    
    PREFERENCES:
    {json.dumps(preferences, indent=2)}
    
    CRITICAL: You MUST respond with ONLY a valid JSON object in exactly this structure:
    {{
      "plan_id": "string",
      "generated_at": 0,
      "user_profile_summary": {{}},
      "difficulty_level": "beginner/intermediate/advanced",
      "primary_goals": ["string"],
      "equipment_required": ["string"],
      "weekly_plan": [
        {{
          "day": "Day 1: [Focus Area]",
          "warm_up": [
            {{
              "exercise": "string",
              "sets": 0,
              "reps": 0,
              "duration_seconds": 0,
              "weight_kg": 0,
              "instructions": "string",
              "safety_tips": "string"
            }}
          ],
          "main_workout": [
            {{
              "exercise": "string",
              "sets": 0,
              "reps": 0,
              "duration_seconds": 0,
              "weight_kg": 0,
              "instructions": "string",
              "safety_tips": "string"
            }}
          ],
          "cool_down": [
            {{
              "exercise": "string",
              "sets": 0,
              "reps": 0,
              "duration_seconds": 0,
              "weight_kg": 0,
              "instructions": "string",
              "safety_tips": "string"
            }}
          ],
          "notes": "string",
          "focus_areas": ["string"]
        }}
      ],
      "total_weekly_duration_minutes": 0,
      "nutrition_tips": ["string"],
      "recovery_tips": ["string"],
      "progression_notes": "string"
    }}
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional fitness trainer."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.5
    )
    
    return json.loads(response.choices[0].message.content)


def generate_meal_plan(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Meal Generation Agent: Generates a personalized 7-day meal plan.
    """
    openai_client = get_client()
    
    prompt = f"""
    Generate a personalized 7-day meal plan based on the following context:
    {json.dumps(context, indent=2)}
    
    Provide a complete 7-day meal plan with breakfast, lunch, and dinner for each day.
    
    Return ONLY a JSON object with this exact structure:
    {{
      "daily_calories": 2000,
      "Data": [
        {{
          "date": "Day 1, YYYY-MM-DD",
          "Breakfast": {{
            "Recipe": "string",
            "Ingredients": ["string"],
            "Instructions": "string",
            "Prep_Time": "string",
            "nutritional_info": {{
              "calories": 0,
              "protein": 0,
              "carbohydrates": 0,
              "fat": 0
            }}
          }},
          "Lunch": {{
            "Recipe": "string",
            "Ingredients": ["string"],
            "Instructions": "string",
            "Prep_Time": "string",
            "nutritional_info": {{
              "calories": 0,
              "protein": 0,
              "carbohydrates": 0,
              "fat": 0
            }}
          }},
          "Dinner": {{
            "Recipe": "string",
            "Ingredients": ["string"],
            "Instructions": "string",
            "Prep_Time": "string",
            "nutritional_info": {{
              "calories": 0,
              "protein": 0,
              "carbohydrates": 0,
              "fat": 0
            }}
          }}
        }}
      ]
    }}
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional nutritionist."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.5
    )
    
    return json.loads(response.choices[0].message.content)
