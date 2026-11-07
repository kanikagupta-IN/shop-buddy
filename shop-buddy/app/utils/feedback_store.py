# app/utils/feedback_store.py
import json
import os
from app.config import config

class LocalFeedbackStore:
    def __init__(self, file_path=config.FEEDBACK_STORE_PATH):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def save_review(self, rating: int, comments: str):
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
        except Exception:
            data = []
            
        data.append({"rating": rating, "comments": comments})
        
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def get_summary_metrics(self):
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
        except Exception:
            return {"avg_rating": 0.0, "total_count": 0}
            
        if not data:
            return {"avg_rating": 0.0, "total_count": 0}
            
        total_stars = sum(entry["rating"] for entry in data)
        return {
            "avg_rating": round(total_stars / len(data), 1),
            "total_count": len(data)
        }
