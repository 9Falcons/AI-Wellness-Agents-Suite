# AI Wellness Agents Suite

A 9Falcons AI project with standalone agents for cosmetic analysis, skin analysis, workout planning, and meal planning. Explore our AI agency services at [9Falcons](https://www.9falcons.com/).


This folder contains a standalone implementation of 4 specialized AI agents extracted from the Health Agents platform.

## Agents Included

1. **Cosmetic Agent**: Analyzes cosmetic and personal care products for safety, ingredients, and skin compatibility.
2. **Skin Analyzer**: Analyzes skin images and user descriptions to identify skin type, concerns, and routine recommendations.
3. **Workout Generation Agent**: Generates personalized 7-day workout plans.
4. **Meal Generation Agent**: Generates personalized 7-day meal plans.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn openai python-dotenv pydantic
   ```

2. Configure your OpenAI API Key in the `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## API Usage Guide

### 1. Cosmetic Agent
**Endpoint:** `POST /analyze-cosmetic`
**Request Body:**
```json
{
  "product_data": {
    "title": "Hydrating Face Cream",
    "brand": "SkinCare Co",
    "ingredients": "Aqua, Glycerin, Hyaluronic Acid, Phenoxyethanol"
  }
}
```

### 2. Skin Analyzer
**Endpoint:** `POST /analyze-skin`
**Request Body:**
```json
{
  "user_description": "I have dry skin with some redness around my nose.",
  "image_base64": "base64_encoded_image_string"
}
```
*Alternatively, use `POST /analyze-skin-upload` with multipart/form-data to upload an image file.*

### 3. Workout Generation Agent
**Endpoint:** `POST /generate-workout`
**Request Body:**
```json
{
  "user_profile": {
    "age": 25,
    "gender": "female",
    "workout_level": "beginner"
  },
  "preferences": {
    "workout_types": ["Yoga", "Pilates"],
    "workout_location": "home"
  }
}
```

### 4. Meal Generation Agent
**Endpoint:** `POST /generate-meal`
**Request Body:**
```json
{
  "context": {
    "goals": ["Weight Loss"],
    "dietary_restrictions": ["Vegetarian"],
    "time_constraints": "Quick meals",
    "activity_level": "Sedentary"
  }
}
```
