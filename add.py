import cv2
import pytesseract
from pdf2image import convert_from_path
import os
import csv

def preprocess_image(image):
    """Preprocess the image to enhance OCR accuracy."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    processed_image = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return processed_image

def extract_text_from_image(image):
    """Extract text from the image using OCR."""
    text = pytesseract.image_to_string(image)
    return text

def pdf_to_images(pdf_path, output_folder):
    """Convert PDF pages to images."""
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i+1}.jpg')
        image.save(image_path, 'JPEG')
        image_paths.append(image_path)
    return image_paths

def extract_text_from_pdf(pdf_path, output_folder):
    """Extract text from all pages of a PDF."""
    image_paths = pdf_to_images(pdf_path, output_folder)
    extracted_text = ""
    for image_path in image_paths:
        image = cv2.imread(image_path)
        processed_image = preprocess_image(image)
        text = extract_text_from_image(processed_image)
        extracted_text += text + "\n"
    return extracted_text

def update_csv(file_path, data):
    """Update a CSV file with the extracted data."""
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = ['Extracted Text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'Extracted Text': data})


pdf_path = r'C:\Users\ASUS\Desktop\pdf_to_text\test.pdf'

output_folder = r'C:\Users\ASUS\Desktop\pdf_to_text\temp_images'

csv_file_path = r'C:\Users\ASUS\Desktop\pdf_to_text\extracted_data.csv'


os.makedirs(output_folder, exist_ok=True)


try:
    extracted_text = extract_text_from_pdf(pdf_path, output_folder)
 
    update_csv(csv_file_path, extracted_text)
    print("Data successfully written to CSV.")
except Exception as e:
    print(f"An error occurred: {e}")
