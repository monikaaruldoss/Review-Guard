"""Module for model training"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import streamlit as st


def train_logistic_regression(X_train, y_train, max_iter=1000):
    """Train Logistic Regression model."""
    model = LogisticRegression(max_iter=max_iter, random_state=42)
    model.fit(X_train, y_train)
    return model


def train_naive_bayes(X_train, y_train):
    """Train Naive Bayes model."""
    model = MultinomialNB()
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train, y_train, n_estimators=100, random_state=42):
    """Train Random Forest model."""
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state, n_jobs=-1)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
    
    Returns:
        dict: Evaluation metrics
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0),
        'f1': f1_score(y_test, y_pred, zero_division=0),
        'confusion_matrix': confusion_matrix(y_test, y_pred)
    }
    
    return metrics, y_pred


def display_metrics(metrics):
    """Display evaluation metrics in Streamlit."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Accuracy", f"{metrics['accuracy']:.4f}")
    with col2:
        st.metric("Precision", f"{metrics['precision']:.4f}")
    with col3:
        st.metric("Recall", f"{metrics['recall']:.4f}")
    with col4:
        st.metric("F1-Score", f"{metrics['f1']:.4f}")
    
    st.write("**Confusion Matrix:**")
    cm_df = pd.DataFrame(
        metrics['confusion_matrix'],
        columns=['Predicted Negative', 'Predicted Positive'],
        index=['Actual Negative', 'Actual Positive']
    )
    st.dataframe(cm_df, use_container_width=True)


def save_model(model, filepath):
    """Save trained model to file."""
    joblib.dump(model, filepath)
    return True


def load_model(filepath):
    """Load trained model from file."""
    return joblib.load(filepath)


def train_and_evaluate(X_train, X_test, y_train, y_test, algorithm='logistic_regression'):
    """
    Train model and evaluate its performance.
    
    Args:
        X_train: Training features
        X_test: Test features
        y_train: Training labels
        y_test: Test labels
        algorithm: Algorithm to use
    
    Returns:
        tuple: (trained model, metrics, predictions)
    """
    if algorithm == 'logistic_regression':
        model = train_logistic_regression(X_train, y_train)
    elif algorithm == 'naive_bayes':
        model = train_naive_bayes(X_train, y_train)
    elif algorithm == 'random_forest':
        model = train_random_forest(X_train, y_train)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    metrics, predictions = evaluate_model(model, X_test, y_test)
    
    return model, metrics, predictions


def cross_validate_model(X, y, model, cv=5):
    """
    Perform cross-validation on model.
    
    Args:
        X: Features
        y: Labels
        model: Model to validate
        cv: Number of folds
    
    Returns:
        array: Cross-validation scores
    """
    from sklearn.model_selection import cross_val_score
    
    scores = cross_val_score(model, X, y, cv=cv, scoring='f1')
    return scores
