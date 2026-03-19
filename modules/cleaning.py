"""Module for data cleaning operations"""
import pandas as pd
import numpy as np
import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import re


# Download required NLTK data
@st.cache_resource
def download_nltk_data():
    """Download required NLTK datasets."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')


def check_missing_values(df):
    """Check and report missing values in dataset."""
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing Count': missing.values,
        'Percentage': missing_percent.values
    })
    
    missing_df = missing_df[missing_df['Missing Count'] > 0]
    
    if len(missing_df) == 0:
        st.success("✅ No missing values found!")
        return df
    else:
        st.warning(f"⚠️ Found {len(missing_df)} columns with missing values")
        st.dataframe(missing_df, use_container_width=True)
        return missing_df


def fill_missing_values(df, method='mean'):
    """Fill missing values using specified method."""
    df_copy = df.copy()
    
    for col in df_copy.columns:
        if df_copy[col].isnull().any():
            if df_copy[col].dtype in ['float64', 'int64']:
                if method == 'mean':
                    df_copy[col].fillna(df_copy[col].mean(), inplace=True)
                elif method == 'median':
                    df_copy[col].fillna(df_copy[col].median(), inplace=True)
                elif method == 'mode':
                    df_copy[col].fillna(df_copy[col].mode()[0], inplace=True)
            else:
                df_copy[col].fillna(df_copy[col].mode()[0] if len(df_copy[col].mode()) > 0 else 'Unknown', inplace=True)
    
    st.success("✅ Missing values filled successfully!")
    return df_copy


def remove_duplicates(df):
    """Remove duplicate rows from dataset."""
    initial_rows = len(df)
    df_cleaned = df.drop_duplicates()
    removed_rows = initial_rows - len(df_cleaned)
    
    st.info(f"Removed {removed_rows} duplicate rows. Remaining: {len(df_cleaned)} rows")
    return df_cleaned


def clean_text(text):
    """Clean text by converting to lowercase and removing special characters."""
    if pd.isna(text):
        return ""
    
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def remove_stopwords(text, language='english'):
    """Remove stopwords from text."""
    stop_words = set(stopwords.words(language))
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)


def lemmatize_text(text):
    """Lemmatize text using WordNetLemmatizer."""
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)


def apply_text_cleaning(df, text_column, remove_stopwords_flag=True, lemmatize=True):
    """Apply text cleaning pipeline to a column."""
    download_nltk_data()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    df_copy = df.copy()
    total_steps = 4 if remove_stopwords_flag and lemmatize else 2
    current_step = 0
    
    # Step 1: Basic text cleaning
    status_text.text("Step 1/3: Cleaning text...")
    df_copy[text_column] = df_copy[text_column].apply(clean_text)
    current_step += 1
    progress_bar.progress(current_step / total_steps)
    
    # Step 2: Remove stopwords
    if remove_stopwords_flag:
        status_text.text("Step 2/3: Removing stopwords...")
        df_copy[text_column] = df_copy[text_column].apply(remove_stopwords)
        current_step += 1
        progress_bar.progress(current_step / total_steps)
    
    # Step 3: Lemmatization
    if lemmatize:
        status_text.text("Step 3/3: Lemmatizing text...")
        df_copy[text_column] = df_copy[text_column].apply(lemmatize_text)
        current_step += 1
        progress_bar.progress(current_step / total_steps)
    
    status_text.text("✅ Text cleaning completed!")
    progress_bar.progress(1.0)
    
    return df_copy


def get_cleaning_summary(df_original, df_cleaned):
    """Generate a summary of cleaning operations."""
    summary = {
        'Original Rows': len(df_original),
        'Cleaned Rows': len(df_cleaned),
        'Rows Removed': len(df_original) - len(df_cleaned),
        'Original Columns': len(df_original.columns),
        'Cleaned Columns': len(df_cleaned.columns)
    }
    return summary
