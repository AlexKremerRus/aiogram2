from ollama_ocr import OCRProcessor

ocr = OCRProcessor(model_name="llama3.2-version:11b")

result = ocr.process_image(
    image_path='test.jpg',
    format_type='markdown'
)

print(result)