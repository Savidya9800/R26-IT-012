import torch
import torchvision.transforms as transforms
from PIL import Image
import torchvision.models as models
import io
import os
import cv2
import numpy as np
import base64
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
import timm

GASTRIC_CLASSES = ['Normal', 'Inflammation']

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../../model_training/trained_models/gastric/efficientnet_gastric_best.pt")

class GastricModel:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 1. Initialize Model - Use TIMM like training code
        self.model = timm.create_model('efficientnet_b4', pretrained=False, num_classes=len(GASTRIC_CLASSES))
        
        try:
            self.model.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            print("Gastric EfficientNet-B4 model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

        # 2. Setup Transform (keep same)
        self.transform = transforms.Compose([
            transforms.Resize((380, 380)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        # 3. Setup Grad-CAM (keep same)
        target_layers = [self.model.blocks[-1]]  # For EfficientNet in timm
        self.cam = GradCAM(model=self.model, target_layers=target_layers)

    def predict(self, image_bytes: bytes):
        # Open and preprocess image
        original_image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Resize original image for visualization purposes to match tensor size
        orig_resized = original_image.resize((380, 380))
        # Convert to numpy array in range [0, 1] for Grad-CAM utility
        rgb_img = np.float32(orig_resized) / 255.0

        tensor = self.transform(original_image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, predicted = torch.max(probabilities, 0)

        predicted_class = GASTRIC_CLASSES[predicted.item()]
        
        # Generate Grad-CAM Heatmap
        # We tell Grad-CAM to output the heatmap for the predicted class
        targets = [ClassifierOutputTarget(predicted.item())]
        
        # Generate the grayscale CAM mask map
        grayscale_cam = self.cam(input_tensor=tensor, targets=targets)[0, :]
        
        # Overlay the heatmap on the original image using the utility
        cam_image = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
        
        # Convert the generated CAM image (numpy array) to a base64 string
        cam_pil = Image.fromarray(cam_image)
        buffered = io.BytesIO()
        cam_pil.save(buffered, format="JPEG")
        cam_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # Determine Severity
        severity = "Low"
        if predicted_class != 'Normal':
             severity = "Medium" if confidence.item() < 0.85 else "Critical"

        return {
            "prediction": predicted_class,
            "confidence": round(confidence.item() * 100, 2),
            "severity": severity,
            "gradcam_base64": f"data:image/jpeg;base64,{cam_base64}"
        }

gastric_model_instance = GastricModel()