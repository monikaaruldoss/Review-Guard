"""Module for statistical analysis"""
import pandas as pd
import numpy as np
import streamlit as st
from collections import Counter
import re


def descriptive_statistics(df):
    """Calculate descriptive statistics for the dataset."""
    st.subheader("📊 Descriptive Statistics")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        st.warning("No numeric columns found in the dataset")
        return
    
    for col in numeric_cols:
        stats = {
            'Mean': df[col].mean(),
            'Median': df[col].median(),
            'Std Dev': df[col].std(),
            'Min': df[col].min(),
            'Max': df[col].max(),
            '25th Percentile': df[col].quantile(0.25),
            '75th Percentile': df[col].quantile(0.75)
        }
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"{col} - Mean", f"{stats['Mean']:.2f}")
        with col2:
            st.metric(f"{col} - Median", f"{stats['Median']:.2f}")
        with col3:
            st.metric(f"{col} - Std Dev", f"{stats['Std Dev']:.2f}")


def rating_distribution_analysis(df):
    """Analyze rating distribution."""
    st.subheader("⭐ Rating Distribution Analysis")
    
    if 'rating' in df.columns:
        rating_counts = df['rating'].value_counts().sort_index()
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Rating Counts:**")
            st.dataframe(rating_counts.to_frame("Count"), use_container_width=True)
        
        with col2:
            st.metric("Average Rating", f"{df['rating'].mean():.2f}")
            st.metric("Most Common Rating", f"{df['rating'].mode()[0]}")
    else:
        st.warning("No 'rating' column found in the dataset")


def review_length_analysis(df):
    """Analyze review length statistics."""
    st.subheader("📝 Review Length Analysis")
    
    review_cols = [col for col in df.columns if 'review' in col.lower()]
    
    if review_cols:
        review_col = review_cols[0]
        
        if 'review_length' not in df.columns:
            df['review_length'] = df[review_col].astype(str).apply(len)
        
        if 'word_count' not in df.columns:
            df['word_count'] = df[review_col].astype(str).apply(lambda x: len(x.split()))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Review Length", f"{df['review_length'].mean():.0f} chars")
        with col2:
            st.metric("Avg Word Count", f"{df['word_count'].mean():.0f} words")
        with col3:
            st.metric("Max Review Length", f"{df['review_length'].max():.0f} chars")
        
        st.write("**Review Length Statistics:**")
        length_stats = df['review_length'].describe().to_frame("Statistics")
        st.dataframe(length_stats, use_container_width=True)
    else:
        st.warning("No review text column found in the dataset")


def word_frequency_analysis(df, top_n=20):
    """Analyze word frequency in reviews."""
    st.subheader("🔤 Word Frequency Analysis")
    
    review_cols = [col for col in df.columns if 'review' in col.lower()]
    
    if review_cols:
        review_col = review_cols[0]
        
        # Combine all reviews and count words
        all_text = ' '.join(df[review_col].astype(str).str.lower())
        words = re.findall(r'\b[a-z]{3,}\b', all_text)  # Words of 3+ characters
        
        word_freq = Counter(words)
        top_words = word_freq.most_common(top_n)
        
        freq_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
        st.dataframe(freq_df, use_container_width=True)
    else:
        st.warning("No review text column found in the dataset")


def fake_vs_genuine_analysis(df):
    """Analyze differences between fake and genuine reviews."""
    st.subheader("🔍 Fake vs Genuine Review Analysis")
    
    if 'label' in df.columns or any('fake' in col.lower() or 'label' in col.lower() for col in df.columns):
        label_col = next((col for col in df.columns if 'label' in col.lower()), 'label')
        
        if label_col in df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Label Distribution:**")
                label_counts = df[label_col].value_counts()
                st.dataframe(label_counts.to_frame("Count"), use_container_width=True)
            
            with col2:
                st.metric("Total Reviews", len(df))
                if 'fake' in label_counts.index or 1 in label_counts.index:
                    fake_count = label_counts.get('fake', label_counts.get(1, 0))
                    st.metric("Fake Reviews", fake_count)
            
            # Analyze review characteristics by label
            review_cols = [col for col in df.columns if 'review' in col.lower()]
            if review_cols:
                review_col = review_cols[0]
                
                if 'review_length' not in df.columns:
                    df['review_length'] = df[review_col].astype(str).apply(len)
                
                if 'word_count' not in df.columns:
                    df['word_count'] = df[review_col].astype(str).apply(lambda x: len(x.split()))
                
                st.write("**Average Review Length by Label:**")
                length_by_label = df.groupby(label_col)['review_length'].mean()
                st.dataframe(length_by_label.to_frame("Avg Length"), use_container_width=True)
                
                st.write("**Average Word Count by Label:**")
                words_by_label = df.groupby(label_col)['word_count'].mean()
                st.dataframe(words_by_label.to_frame("Avg Words"), use_container_width=True)
        else:
            st.warning("Label column not found in the dataset")
    else:
        st.warning("No label/fake column found in the dataset")


def analysis_interface(df):
    """Main interface for data analysis."""
    analysis_type = st.selectbox(
        "Select analysis type:",
        ["Descriptive Statistics", "Rating Distribution", "Review Length", 
         "Word Frequency", "Fake vs Genuine Analysis"]
    )
    
    if analysis_type == "Descriptive Statistics":
        descriptive_statistics(df)
    elif analysis_type == "Rating Distribution":
        rating_distribution_analysis(df)
    elif analysis_type == "Review Length":
        review_length_analysis(df)
    elif analysis_type == "Word Frequency":
        word_frequency_analysis(df, top_n=st.slider("Top N words:", 5, 50, 20))
    elif analysis_type == "Fake vs Genuine Analysis":
        fake_vs_genuine_analysis(df)
