"""Module for feature extraction"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import joblib


def extract_tfidf_features(text_data, max_features=100, ngram_range=(1, 2)):
    """
    Extract TF-IDF features from text data.
    
    Args:
        text_data: List of text documents
        max_features: Maximum number of features
        ngram_range: Range of n-grams to extract
    
    Returns:
        tuple: (TF-IDF matrix, TfidfVectorizer object)
    """
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        min_df=2,
        max_df=0.9
    )
    
    tfidf_matrix = vectorizer.fit_transform(text_data)
    
    return tfidf_matrix, vectorizer


def extract_count_features(text_data, max_features=100):
    """
    Extract count-based features from text data.
    
    Args:
        text_data: List of text documents
        max_features: Maximum number of features
    
    Returns:
        tuple: (Count matrix, CountVectorizer object)
    """
    vectorizer = CountVectorizer(max_features=max_features, min_df=2, max_df=0.9)
    count_matrix = vectorizer.fit_transform(text_data)
    
    return count_matrix, vectorizer


def create_statistical_features(df):
    """
    Create statistical features from review data.
    
    Args:
        df: DataFrame with review data
    
    Returns:
        DataFrame: Original dataframe with new features
    """
    df_copy = df.copy()
    
    review_cols = [col for col in df.columns if 'review' in col.lower()]
    
    if review_cols:
        review_col = review_cols[0]
        
        # Review length feature
        if 'review_length' not in df_copy.columns:
            df_copy['review_length'] = df_copy[review_col].astype(str).apply(len)
        
        # Word count feature
        if 'word_count' not in df_copy.columns:
            df_copy['word_count'] = df_copy[review_col].astype(str).apply(lambda x: len(x.split()))
        
        # Unique word count
        if 'unique_word_count' not in df_copy.columns:
            df_copy['unique_word_count'] = df_copy[review_col].astype(str).apply(lambda x: len(set(x.split())))
        
        # Average word length
        if 'avg_word_length' not in df_copy.columns:
            df_copy['avg_word_length'] = df_copy[review_col].astype(str).apply(
                lambda x: np.mean([len(word) for word in x.split()]) if len(x.split()) > 0 else 0
            )
    
    return df_copy


def prepare_features_for_model(df, text_column, max_features=100):
    """
    Prepare complete feature set for model training.
    
    Args:
        df: DataFrame with review data
        text_column: Name of text column
        max_features: Max TF-IDF features
    
    Returns:
        DataFrame: Features ready for model training
    """
    df_copy = df.copy()
    
    # Create statistical features
    df_copy = create_statistical_features(df_copy)
    
    # Extract TF-IDF features
    if text_column in df_copy.columns:
        text_data = df_copy[text_column].astype(str).fillna('')
        tfidf_matrix, _ = extract_tfidf_features(text_data, max_features=max_features)
        
        # Convert sparse matrix to dense and create DataFrame
        tfidf_df = pd.DataFrame(
            tfidf_matrix.toarray(),
            columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
        )
        
        # Combine with other features
        numeric_features = df_copy.select_dtypes(include=[np.number]).columns
        feature_df = pd.concat([
            df_copy[numeric_features],
            tfidf_df
        ], axis=1)
        
        return feature_df, tfidf_matrix, df_copy[numeric_features].columns.tolist()
    
    return df_copy, None, []


def save_vectorizer(vectorizer, filepath):
    """Save vectorizer to file."""
    joblib.dump(vectorizer, filepath)


def load_vectorizer(filepath):
    """Load vectorizer from file."""
    return joblib.load(filepath)


def get_feature_importance(model, feature_names, top_n=10):
    """
    Extract feature importance from trained model.
    
    Args:
        model: Trained model
        feature_names: List of feature names
        top_n: Number of top features to return
    
    Returns:
        DataFrame: Top N features and their importance scores
    """
    if hasattr(model, 'coef_'):
        # For linear models
        importance = np.abs(model.coef_[0])
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return feature_importance.head(top_n)
    
    elif hasattr(model, 'feature_importances_'):
        # For tree-based models
        importance = model.feature_importances_
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return feature_importance.head(top_n)
    
    return pd.DataFrame()
