"""Module for making predictions on new reviews"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import streamlit as st


def predict_batch(model, X_features):
    """
    Make predictions on a batch of samples.
    
    Args:
        model: Trained model
        X_features: Feature matrix
    
    Returns:
        array: Predictions
    """
    predictions = model.predict(X_features)
    
    # Get prediction probabilities if available
    try:
        probabilities = model.predict_proba(X_features)
        return predictions, probabilities
    except:
        return predictions, None


def add_predictions_to_dataframe(df, model, X_features):
    """
    Add predictions to DataFrame.
    
    Args:
        df: Original DataFrame
        model: Trained model
        X_features: Feature matrix
    
    Returns:
        DataFrame: DataFrame with predictions
    """
    predictions, probabilities = predict_batch(model, X_features)
    
    df_copy = df.copy()
    df_copy['prediction'] = predictions
    
    if probabilities is not None:
        if len(probabilities[0]) == 2:
            df_copy['prediction_confidence'] = np.max(probabilities, axis=1)
            df_copy['prob_genuine'] = probabilities[:, 0]
            df_copy['prob_fake'] = probabilities[:, 1]
    
    return df_copy


def predict_single_review(review_text, model, vectorizer, preprocessing_func=None):
    """
    Predict if a single review is fake or genuine.
    
    Args:
        review_text: Text of the review
        model: Trained model
        vectorizer: Fitted vectorizer
        preprocessing_func: Function to preprocess text
    
    Returns:
        dict: Prediction result with confidence
    """
    # Preprocess if function provided
    if preprocessing_func:
        review_text = preprocessing_func(review_text)
    
    # Vectorize
    text_features = vectorizer.transform([review_text])
    
    # Predict
    prediction = model.predict(text_features)[0]
    
    try:
        probabilities = model.predict_proba(text_features)[0]
        confidence = np.max(probabilities)
    except:
        confidence = None
    
    result = {
        'prediction': 'Fake Review' if prediction == 1 else 'Genuine Review',
        'confidence': confidence,
        'prediction_value': prediction
    }
    
    return result


def export_predictions(df, filepath):
    """
    Export predictions to CSV file.
    
    Args:
        df: DataFrame with predictions
        filepath: Path to save file
    """
    df.to_csv(filepath, index=False)
    return True


def generate_prediction_report(df_predictions):
    """
    Generate summary report of predictions.
    
    Args:
        df_predictions: DataFrame with predictions
    
    Returns:
        dict: Summary statistics
    """
    if 'prediction' not in df_predictions.columns:
        return None
    
    total_reviews = len(df_predictions)
    fake_count = (df_predictions['prediction'] == 1).sum()
    genuine_count = (df_predictions['prediction'] == 0).sum()
    
    report = {
        'total_reviews': total_reviews,
        'fake_reviews': fake_count,
        'genuine_reviews': genuine_count,
        'fake_percentage': (fake_count / total_reviews) * 100 if total_reviews > 0 else 0,
        'genuine_percentage': (genuine_count / total_reviews) * 100 if total_reviews > 0 else 0
    }
    
    return report


def get_high_confidence_predictions(df_predictions, threshold=0.8):
    """
    Get predictions with high confidence.
    
    Args:
        df_predictions: DataFrame with predictions and confidence
        threshold: Confidence threshold
    
    Returns:
        DataFrame: High confidence predictions
    """
    if 'prediction_confidence' in df_predictions.columns:
        return df_predictions[df_predictions['prediction_confidence'] >= threshold]
    else:
        return df_predictions


def get_uncertain_predictions(df_predictions, threshold=0.6):
    """
    Get uncertain predictions (confidence near 0.5).
    
    Args:
        df_predictions: DataFrame with predictions and confidence
        threshold: Uncertainty threshold
    
    Returns:
        DataFrame: Uncertain predictions
    """
    if 'prediction_confidence' in df_predictions.columns:
        return df_predictions[df_predictions['prediction_confidence'] < threshold]
    else:
        return df_predictions
