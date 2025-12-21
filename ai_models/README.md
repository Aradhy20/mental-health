# AI Models Directory

This directory contains all the AI/ML models used in the Multimodal Mental Health Detection System.

## Overview

The system uses three primary modalities for mental health detection:
1. **Text Analysis** - Natural Language Processing for emotion detection
2. **Voice Analysis** - Audio processing for stress detection
3. **Face Analysis** - Computer vision for facial emotion recognition

## Model Architecture

### Text Analysis Model
- **Model**: DistilRoBERTa fine-tuned on emotion detection dataset
- **Framework**: Hugging Face Transformers
- **Input**: Text input from user
- **Output**: Emotion label and confidence score

### Voice Analysis Model
- **Model**: CNN trained on audio features (MFCC, pitch, intensity)
- **Framework**: Librosa + PyTorch
- **Input**: Audio recording from user
- **Output**: Stress level and confidence score

### Face Analysis Model
- **Model**: CNN trained on facial expression dataset
- **Framework**: OpenCV + PyTorch
- **Input**: Image from camera
- **Output**: Emotion label and confidence score

## Directory Structure

```
ai_models/
├── text/
│   ├── model/
│   │   ├── config.json
│   │   ├── pytorch_model.bin
│   │   └── tokenizer.json
│   ├── training/
│   │   ├── dataset/
│   │   ├── train.py
│   │   └── evaluate.py
│   └── inference/
│       └── text_analyzer.py
├── voice/
│   ├── model/
│   │   ├── voice_model.pth
│   │   └── feature_extractor.py
│   ├── training/
│   │   ├── dataset/
│   │   ├── train.py
│   │   └── evaluate.py
│   └── inference/
│       └── voice_analyzer.py
├── face/
│   ├── model/
│   │   ├── face_model.pth
│   │   └── face_detector.py
│   ├── training/
│   │   ├── dataset/
│   │   ├── train.py
│   │   └── evaluate.py
│   └── inference/
│       └── face_analyzer.py
└── fusion/
    ├── fusion_engine.py
    └── weights.json
```

## Model Training

### Text Model Training
1. Prepare dataset with labeled emotions
2. Fine-tune DistilRoBERTa using Hugging Face Trainer
3. Evaluate on validation set
4. Save model weights

### Voice Model Training
1. Extract audio features using Librosa
2. Train CNN on extracted features
3. Validate on test set
4. Save model weights

### Face Model Training
1. Detect and align faces in images
2. Extract facial features
3. Train CNN on facial expressions
4. Validate and save model

## Model Inference

Each model has an inference module that:
1. Loads the pre-trained model
2. Preprocesses input data
3. Runs inference
4. Post-processes results
5. Returns structured output

## Fusion Algorithm

The fusion service combines results from all three modalities using weighted averaging:
- Text: 30%
- Voice: 30%
- Face: 40%

Weights can be adjusted based on model performance and user requirements.

## Model Updates

To update models:
1. Retrain with new data
2. Evaluate performance
3. Update model files in respective directories
4. Update version numbers
5. Test integration with backend services

## Performance Metrics

Current model performance:
- Text Analysis: ~85% accuracy
- Voice Analysis: ~80% accuracy
- Face Analysis: ~82% accuracy
- Overall System: ~87% accuracy

## Requirements

- Python 3.8+
- PyTorch 1.10+
- Transformers 4.15+
- Librosa 0.9+
- OpenCV 4.5+
- NumPy 1.21+
- SciPy 1.7+

## Usage

Models are automatically loaded by the respective backend services:
- Text service loads text models
- Voice service loads voice models
- Face service loads face models
- Fusion service combines results

For manual testing, each inference module can be run independently.