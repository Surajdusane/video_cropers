from google.cloud import vision
import io

def detect_text_in_image(image_path):
    """
    Detects text in the given image using Google Cloud Vision API and returns the extracted text.

    :param image_path: Path to the image file.
    :return: Extracted text from the image.
    """
    try:
        # Initialize a client
        client = vision.ImageAnnotatorClient()

        # Read the image file
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        # Construct an image instance
        image = vision.Image(content=content)

        # Perform text detection on the image file
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if response.error.message:
            raise Exception(response.error.message)

        # Extract detected text
        detected_text = texts[0].description if texts else 'No text detected'

        return detected_text
    except Exception as e:
        return str(e)

# Example usage:
# Ensure that the path to your JSON key file is set in the environment variable
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'assets\metal-sky-427303-k8-d50bf27a72c3.json'

# image_path = 'temp\snapshot.png'
# detected_text = detect_text_in_image(image_path)
# print(detected_text)
