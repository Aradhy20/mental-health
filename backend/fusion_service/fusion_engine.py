from typing import Tuple
import numpy as np

class FusionEngine:
    def __init__(self):
        # Fusion weights for different modalities
        self.weights = {
            "text": 0.3,
            "voice": 0.3,
            "face": 0.4
        }
        
        # Risk level thresholds
        self.risk_thresholds = {
            "low": (0.0, 0.3),
            "medium": (0.3, 0.6),
            "high": (0.6, 1.0)
        }
    
    def determine_risk_level(self, score: float) -> str:
        """Determine risk level based on final score"""
        if score <= 0.3:
            return "low"
        elif score <= 0.6:
            return "medium"
        else:
            return "high"
    
    def fuse_results(self, text_score: float, voice_score: float, face_score: float) -> Tuple[float, str]:
        """
        Fuse results from different modalities using weighted average
        Returns: (final_score, risk_level)
        """
        # Apply weights to each modality score
        weighted_text = text_score * self.weights["text"]
        weighted_voice = voice_score * self.weights["voice"]
        weighted_face = face_score * self.weights["face"]
        
        # Calculate final fusion score
        final_score = weighted_text + weighted_voice + weighted_face
        
        # Ensure score is within valid range
        final_score = max(0.0, min(1.0, final_score))
        
        # Determine risk level
        risk_level = self.determine_risk_level(final_score)
        
        return final_score, risk_level
    
    def calculate_confidence(self, text_conf: float, voice_conf: float, face_conf: float) -> float:
        """
        Calculate overall confidence based on individual confidences
        """
        # Weighted average of confidences
        weighted_conf = (
            text_conf * self.weights["text"] +
            voice_conf * self.weights["voice"] +
            face_conf * self.weights["face"]
        )
        
        return min(weighted_conf, 1.0)

    def detect_discrepancy(self, text_score: float, voice_score: float, face_score: float) -> bool:
        """
        Detect if there is a significant discrepancy between modalities
        """
        scores = [text_score, voice_score, face_score]
        max_diff = max(scores) - min(scores)
        
        # If difference is greater than 0.4, flag as discrepancy
        return max_diff > 0.4

# Global instance
engine = FusionEngine()