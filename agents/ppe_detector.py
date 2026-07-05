from ultralytics import YOLO
from PIL import Image
import numpy as np
import io
import os

def get_ppe_model():
    model_path = "models/best.pt"
    if not os.path.exists(model_path):
        from huggingface_hub import hf_hub_download
        model_path = hf_hub_download(
            repo_id="keremberke/yolov8n-hard-hat-detection",
            filename="best.pt"
        )
    return YOLO(model_path)

def detect_ppe(image_file):
    model = get_ppe_model()
    
    img = Image.open(image_file).convert("RGB")
    img_array = np.array(img)
    
    results = model(img_array, conf=0.25)
    
    violations = []
    detections = []
    
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names.get(cls_id, f"class_{cls_id}")
                
                detections.append({
                    "label": label,
                    "confidence": round(conf * 100, 1)
                })
                
                label_lower = label.lower()
                if any(x in label_lower for x in ["no-hardhat", "no hardhat", "no_hardhat", "without"]):
                    violations.append(f"Missing PPE detected: {label} ({round(conf*100,1)}% confidence)")
    
    result_img = Image.fromarray(results[0].plot()[..., ::-1])
    
    summary = {
        "total_detections": len(detections),
        "violations": violations,
        "violation_count": len(violations),
        "detections": detections
    }
    
    return result_img, summary