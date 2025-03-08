import google.generativeai as genai
from PIL import Image
import os, io

# Configure the API key
GOOGLE_API_KEY = "AIzaSyB5pbuKm2oi25OhzTDVAjN45EIfQeQ3aqc"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)


# Function to classify clothing
def classify_clothing(image_path):
    try:
        # Load the image
        img = Image.open(image_path)

        # Generate content using Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Create prompt for Gemini
        prompt = """
        Analyze this clothing item and determine its condition.
        Classify it into one of these categories:
        1. GOOD: Can be resold (minimal wear, good condition)
        2. MEDIUM: Should be donated (wearable but shows signs of use)
        3. BAD: Should be recycled (damaged, unwearable)

        Respond with ONLY the category (GOOD, MEDIUM, or BAD) followed by a brief explanation.
        """

        # Get response from Gemini
        response = model.generate_content([prompt, img])
        result = response.text

        # Extract the category
        if "GOOD" in result.upper().split():
            category = "GOOD"
        elif "MEDIUM" in result.upper().split():
            category = "MEDIUM"
        elif "BAD" in result.upper().split():
            category = "BAD"
        else:
            category = "UNKNOWN"

        return {
            "category": category,
            "explanation": result,
            "recommendation": get_recommendation(category)
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "category": "ERROR",
            "explanation": f"An error occurred: {str(e)}",
            "recommendation": "Please try again with a different image."
        }


# Get recommendation based on category
def get_recommendation(category):
    recommendations = {
        "GOOD": "This item can be resold in our second-hand marketplace.",
        "MEDIUM": "This item should be donated to local charities.",
        "BAD": "This item should be sent to textile recycling.",
        "UNKNOWN": "Further inspection required."
    }
    return recommendations.get(category, "Unable to process.")


# Test with a sample image
def test_classification(image_path):
    print(f"Analyzing image: {image_path}")
    result = classify_clothing(image_path)

    print("\n=== CLASSIFICATION RESULTS ===")
    print(f"Category: {result.get('category', 'UNKNOWN')}")

    # Safely access the explanation key
    if 'explanation' in result:
        print(f"Explanation: {result['explanation']}")
    else:
        print(f"Response: {result}")  # Print the raw result if no explanation key

    if 'recommendation' in result:
        print(f"Recommendation: {result['recommendation']}")
    print("==============================\n")


# Main execution
if __name__ == "__main__":
    # Test the classification with a sample image
    test_image = "image1.png"  # Replace with your image path
    test_classification(test_image)
