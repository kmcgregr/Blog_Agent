from ollama_ocr import OCRProcessor

ocr = OCRProcessor(model_name='gwen2.5vl:7b')

result = ocr.process_image(
    image_path="./images/july_7_2025.jpg",
    format_type="text"
)
print(result)