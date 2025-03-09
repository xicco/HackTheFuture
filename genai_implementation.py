import google.generativeai as genai
from PIL import Image
import os


GOOGLE_API_KEY = "AIzaSyB5pbuKm2oi25OhzTDVAjN45EIfQeQ3aqc"
genai.configure(api_key=GOOGLE_API_KEY)


def classify_clothing(image_path):
    try:
        img = Image.open(image_path)

        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = """
        You are a clothing condition assessment expert. Analyze the clothing item in the image and evaluate the following factors:
        1. Stains: Are there any visible stains? If yes, describe them.
        2. Material Quality: Assess the fabric's condition (e.g., pilling, tears, or wear).
        3. Overall Quality: Provide an overall assessment of the item's condition.

        Based on your analysis, classify the item into one of these categories:
        - GOOD: Can be resold (minimal wear, good condition)
        - MEDIUM: Should be donated (wearable but shows signs of use)
        - BAD: Should be recycled (damaged, unwearable)

        Respond with:
        - Category (GOOD, MEDIUM, or BAD)
        - A detailed explanation covering stains, material quality, and overall quality.
        """

        response = model.generate_content([prompt, img])
        result = response.text

        result_upper = result.upper()
        if "GOOD" in result_upper:
            category = "GOOD"
        elif "MEDIUM" in result_upper:
            category = "MEDIUM"
        elif "BAD" in result_upper:
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


def get_recommendation(category):
    recommendations = {
        "GOOD": "This item can be resold in our second-hand marketplace.",
        "MEDIUM": "This item should be donated to local charities.",
        "BAD": "This item should be sent to textile recycling.",
        "UNKNOWN": "Further inspection required."
    }
    return recommendations.get(category, "Unable to process.")


def test_classification(image_path):
    print(f"Analyzing image: {image_path}")
    result = classify_clothing(image_path)

    print("\n=== CLASSIFICATION RESULTS ===")

    if 'explanation' in result:
        print(f"Explanation:\n{result['explanation']}")
    else:
        print(f"Response: {result}")

    if 'recommendation' in result:
        print(f"Recommendation: {result['recommendation']}")
    print("==============================\n")


if __name__ == "__main__":
    # Testing the classification with a sample image
    test_image = "mint_clothes.png"  # Replace with image path!
    test_classification(test_image)
