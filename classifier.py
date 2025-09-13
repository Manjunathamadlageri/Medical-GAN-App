import random

def predict_disease(image_array):
    labels = ['Normal', 'Tumor', 'Pneumonia']
    regions = ['-', 'Left upper lobe', 'Lower right lobe']
    severities = ['-', 'Moderate', 'Severe']
    descriptions = {
        'Normal': 'No abnormal findings.',
        'Tumor': 'Tumors in the lung may indicate malignancy and require further clinical evaluation.',
        'Pneumonia': 'Pneumonia is an infection that inflames the air sacs in one or both lungs.'
    }
    idx = random.randint(0, 2)
    confidence = random.uniform(0.7, 0.99)
    return {
        'disease': labels[idx],
        'confidence': confidence,
        'region': regions[idx],
        'severity': severities[idx],
        'description': descriptions[labels[idx]]
    }
