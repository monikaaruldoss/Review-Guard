"""Module for text preprocessing"""
import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
import nltk


# Download required NLTK data
def download_nltk_resources():
    """Download required NLTK datasets."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)


def remove_urls(text):
    """Remove URLs from text."""
    return re.sub(r'http\S+|www\S+|https\S+', '', text)


def remove_emails(text):
    """Remove email addresses from text."""
    return re.sub(r'\S+@\S+', '', text)


def remove_special_characters(text):
    """Remove special characters and digits."""
    return re.sub(r'[^a-zA-Z\s]', '', text)


def remove_extra_whitespace(text):
    """Remove extra whitespace."""
    return re.sub(r'\s+', ' ', text).strip()


def convert_to_lowercase(text):
    """Convert text to lowercase."""
    return str(text).lower()


def tokenize_text(text):
    """Tokenize text into words."""
    download_nltk_resources()
    return word_tokenize(text)


def remove_stopwords_func(text, language='english'):
    """Remove stopwords from text."""
    download_nltk_resources()
    stop_words = set(stopwords.words(language))
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)


def lemmatize(text):
    """Lemmatize text."""
    download_nltk_resources()
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    lemmatized = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized)


def stem_text(text):
    """Stem text using Porter Stemmer."""
    stemmer = PorterStemmer()
    words = text.split()
    stemmed = [stemmer.stem(word) for word in words]
    return ' '.join(stemmed)


def preprocess_text(text, remove_urls_flag=True, remove_emails_flag=True,
                   remove_special_flag=True, lowercase_flag=True,
                   remove_stopwords_flag=True, lemmatize_flag=True, stem_flag=False):
    """Full text preprocessing pipeline."""
    
    if pd.isna(text):
        return ""
    
    text = str(text)
    
    if remove_urls_flag:
        text = remove_urls(text)
    
    if remove_emails_flag:
        text = remove_emails(text)
    
    if lowercase_flag:
        text = convert_to_lowercase(text)
    
    if remove_special_flag:
        text = remove_special_characters(text)
    
    text = remove_extra_whitespace(text)
    
    if remove_stopwords_flag:
        text = remove_stopwords_func(text)
    
    if lemmatize_flag:
        text = lemmatize(text)
    
    if stem_flag:
        text = stem_text(text)
    
    return text.strip()
