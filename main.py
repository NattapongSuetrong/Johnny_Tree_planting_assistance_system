import os
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from PIL import Image
import google.generativeai as genai
from io import BytesIO
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Setup templates
templates = Jinja2Templates(directory="templates")

class NonCachingStaticFiles(StaticFiles):
    def is_not_modified(self, *args, **kwargs) -> bool:
        return False
    
app.mount("/static", NonCachingStaticFiles(directory=Path("static")), name="static")

# Configure Gemini API
def configure_genai():
    genai.configure(api_key=os.getenv('Your Gemini API Key')) 
    
# Initialize the model
def initialize_model():
    return genai.GenerativeModel('gemini-1.5-pro')

# Process the image and get response
async def process_image(model, image):
    prompt = """นี่คือต้นอะไร และช่วยแนะนำการปลูกต้นนี้ว่า ต้องใช้สัดส่วนปุ๋ยเท่าไหร่ น้ำ ความชื้น อุณหภูมิเป็นอย่างไร อธิบายเป็นภาษาไทย"""
    
    response = model.generate_content([prompt, image])
    return response.text

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process-receipt/")
async def process_receipt(file: UploadFile = File(...)):
    try:
        # Read and validate the image
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        
        # Configure and initialize Gemini
        configure_genai()
        model = initialize_model()
        
        # Process the image and get raw text response
        response_text = await process_image(model, image)
        
        return {
            "status": "success",
            "text": response_text
        }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)