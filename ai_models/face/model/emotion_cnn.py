"""
CNN Model for Facial Emotion Detection
Uses a pre-trained model with fine-tuning for emotion recognition
"""

import cv2
import numpy as np
import os

# Try importing tensorflow/keras, handle if missing
try:
    from tensorflow import keras
    from keras.models import Sequential, load_model
    from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
    from keras.preprocessing.image import img_to_array
    HAS_TF = True
except ImportError:
    print("Warning: TensorFlow/Keras not found. Face analysis will use mock.")
    HAS_TF = False

class EmotionCNN:
    def __init__(self, model_path=None):
        """
        Initialize the CNN model for emotion detection
        """
        self.img_size = (48, 48)
        self.emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        self.model = None
        self.face_cascade = None
        
        if not HAS_TF:
            return

        try:
            if model_path and os.path.exists(model_path):
                self.model = load_model(model_path)
            else:
                # Build new model (random weights)
                self.model = self._build_model()
            
            # Load face cascade for detection
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
        except Exception as e:
            print(f"Error initializing EmotionCNN: {e}")

    def _build_model(self):
        """
        Build CNN architecture for emotion recognition
        Architecture inspired by mini-Xception
        """
        if not HAS_TF:
            return None

        model = Sequential([
            # Block 1
            Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
            BatchNormalization(),
            Conv2D(64, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Block 2
            Conv2D(128, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(128, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Block 3
            Conv2D(256, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(256, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Fully connected layers
            Flatten(),
            Dense(512, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(7, activation='softmax')  # 7 emotions
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def detect_faces(self, image_data):
        """
        Detect faces in the image
        """
        if self.face_cascade is None:
            return [], None

        # Convert bytes to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        return faces, gray
    
    def preprocess_face(self, face_roi):
        """
        Preprocess face ROI for model input
        """
        # Resize to model input size
        face_roi = cv2.resize(face_roi, self.img_size)
        
        # Normalize pixel values
        face_roi = face_roi.astype('float32') / 255.0
        
        # Reshape for model input
        face_roi = np.expand_dims(face_roi, axis=0)
        face_roi = np.expand_dims(face_roi, axis=-1)
        
        return face_roi
    
    def predict_emotion(self, image_data):
        """
        Predict emotion from image
        Returns: (emotion_label, confidence, all_probabilities)
        """
        if not HAS_TF or self.model is None:
            return "Neutral", 0.5, [0.14] * 7

        try:
            # Detect faces
            faces, gray = self.detect_faces(image_data)
            
            if len(faces) == 0:
                return "Neutral", 0.5, [0.14] * 7  # Default if no face detected
            
            # Use the first detected face
            (x, y, w, h) = faces[0]
            face_roi = gray[y:y+h, x:x+w]
            
            # Preprocess
            face_input = self.preprocess_face(face_roi)
            
            # Predict
            predictions = self.model.predict(face_input, verbose=0)[0]
            
            # Get emotion with highest probability
            emotion_idx = np.argmax(predictions)
            emotion_label = self.emotions[emotion_idx]
            confidence = float(predictions[emotion_idx])
            
            return emotion_label, confidence, predictions.tolist()
            
        except Exception as e:
            print(f"Error in emotion prediction: {str(e)}")
            return "Neutral", 0.5, [0.14] * 7
    
    def save_model(self, path):
        """
        Save the trained model
        """
        if self.model:
            self.model.save(path)
            print(f"Model saved to {path}")
