import os
import requests

# IMPORTANT: Set your Gemini API key in your environment variables.
GEMINI_API_KEY = os.getenv('AIzaSyBDkxp4iGNtcZ8ri6Ezp34BxamvKjbCjbA')
GEMINI_ENDPOINT = 'https://api.generativeai.googleapis.com/v1/images:generate'  # Example endpoint

def generate_image(prompt: str, out_path: str) -> None:
    """
    Generates an image using the Gemini API and saves it to the specified path.

    Args:
        prompt: The text prompt for image generation.
        out_path: The path to save the generated image.
    """
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set.")
        # As a fallback for development, create a placeholder image.
        create_placeholder_image(prompt, out_path)
        return

    payload = {
        'prompt': prompt,
        'height': 1920,
        'width': 1080
    }
    headers = {'Authorization': f'Bearer {GEMINI_API_KEY}'}

    try:
        response = requests.post(GEMINI_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Process the response to get the image data (e.g., base64 or URL)
        image_data = response.json()  # This will vary based on the actual API response

        # For now, let's assume the API returns image bytes directly or a URL
        # This part needs to be adapted to the actual API response format
        # For example, if it's a URL:
        # image_url = image_data.get('url')
        # if image_url:
        #     image_response = requests.get(image_url)
        #     with open(out_path, 'wb') as f:
        #         f.write(image_response.content)

        print(f"Image generated and saved to {out_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        create_placeholder_image(prompt, out_path)

def create_placeholder_image(prompt: str, out_path: str):
    """
    Creates a placeholder image for development purposes when the API key is not available.
    """
    from PIL import Image, ImageDraw, ImageFont

    try:
        img = Image.new('RGB', (1080, 1920), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        # A basic font will be used. For better results, specify a path to a .ttf file.
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font = ImageFont.load_default()
        d.text((10,10), prompt, fill=(255,255,0), font=font)
        img.save(out_path)
        print(f"Created placeholder image at {out_path}")
    except Exception as e:
        print(f"Failed to create placeholder image: {e}")
