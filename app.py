from flask import Flask, request, jsonify, render_template
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image , ImageOps
import io
from model import EnhancedCNN
app = Flask(__name__)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = EnhancedCNN().to(device)

model.load_state_dict(torch.load('best_model.pth', map_location=device))
model.eval() 

transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1), 
    transforms.Resize((28, 28)),                 
    transforms.ToTensor(),
    transforms.Normalize((0.13,), (0.31,))
])

def transform_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('L')
    
    bbox = image.getbbox()
    if bbox:
        image = image.crop(bbox)
        

    width, height = image.size
    max_dim = max(width, height)
    new_image = Image.new('L', (max_dim, max_dim), color=0)
    
    offset_x = (max_dim - width) // 2
    offset_y = (max_dim - height) // 2
    new_image.paste(image, (offset_x, offset_y))
    

    new_image = ImageOps.expand(new_image, border=int(max_dim * 0.25), fill=0)
    

    new_image = new_image.resize((28, 28), Image.Resampling.LANCZOS)
    

    return transform(new_image).unsqueeze(0).to(device)

@app.route('/')
def home():

    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:

        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
            

        img_bytes = file.read()
        tensor = transform_image(img_bytes)
        
        
        with torch.no_grad():
            outputs = model(tensor)
            _, predicted = torch.max(outputs.data, 1)
            prediction = predicted.item()
            
        return jsonify({'prediction': prediction})
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18099)