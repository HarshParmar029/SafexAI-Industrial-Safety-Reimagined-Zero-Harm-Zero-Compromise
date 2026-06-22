from ultralytics import YOLO
from PIL import Image
import numpy as np
import io
import os

def get_ppe_model():
    model_path = "ppe_model.pt"
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
                    violations.append(f"❌ No Hardhat (conf: {round(conf*100,1)}%)")
                elif any(x in label_lower for x in ["no-vest", "no vest", "no_vest"]):
                    violations.append(f"❌ No Safety Vest (conf: {round(conf*100,1)}%)")

    annotated = results[0].plot()
    annotated_pil = Image.fromarray(annotated)
    buf = io.BytesIO()
    annotated_pil.save(buf, format="PNG")
    buf.seek(0)

    summary = {
        "total_detections": len(detections),
        "violations": violations,
        "violation_count": len(violations),
        "detections": detections,
        "risk_level": "CRITICAL" if len(violations) >= 3 else "HIGH" if len(violations) >= 1 else "SAFE"
    }
    
    return buf, summary
