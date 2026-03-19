"""Module for data visualization"""
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re


def histogram_review_length(df):
    """Display histogram of review length distribution."""
    st.subheader("📊 Review Length Distribution (Histogram)")
    
    review_cols = [col for col in df.columns if 'review' in col.lower()]
    
    if review_cols:
        review_col = review_cols[0]
        df['review_length'] = df[review_col].astype(str).apply(len)
        
        fig = px.histogram(df, x='review_length', nbins=30, title='Review Length Distribution',
                          labels={'review_length': 'Review Length (characters)'})
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No review text column found")


def bar_chart_rating_distribution(df):
    """Display bar chart of rating distribution."""
    st.subheader("⭐ Rating Distribution (Bar Chart)")
    
    if 'rating' in df.columns:
        rating_counts = df['rating'].value_counts().sort_index()
        
        fig = px.bar(x=rating_counts.index, y=rating_counts.values,
                    labels={'x': 'Rating', 'y': 'Count'},
                    title='Rating Distribution')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No 'rating' column found")


def pie_chart_fake_vs_genuine(df):
    """Display pie chart of fake vs genuine reviews."""
    st.subheader("🥧 Fake vs Genuine Reviews (Pie Chart)")
    
    label_cols = [col for col in df.columns if 'label' in col.lower() or 'fake' in col.lower()]
    
    if label_cols:
        label_col = label_cols[0]
        label_counts = df[label_col].value_counts()
        
        fig = px.pie(values=label_counts.values, names=label_counts.index,
                    title='Distribution of Fake vs Genuine Reviews')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No label/fake column found")


def word_frequency_plot(df, top_n=15):
    """Display word frequency plot."""
    st.subheader(f"🔤 Top {top_n} Most Frequent Words")
    
    review_cols = [col for col in df.columns if 'review' in col.lower()]
    
    if review_cols:
        review_col = review_cols[0]
        
        all_text = ' '.join(df[review_col].astype(str).str.lower())
        words = re.findall(r'\b[a-z]{3,}\b', all_text)
        
        word_freq = Counter(words)
        top_words = word_freq.most_common(top_n)
        
        words, frequencies = zip(*top_words)
        
        fig = px.bar(x=list(frequencies), y=list(words),
                    orientation='h', title=f'Top {top_n} Most Frequent Words',
                    labels={'x': 'Frequency', 'y': 'Word'})
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No review text column found")


def correlation_heatmap(df):
    """Display correlation heatmap for numeric columns."""
    st.subheader("🔥 Correlation Heatmap")
    
    numeric_df = df.select_dtypes(include=[np.number])
    
    if len(numeric_df.columns) > 1:
        correlation_matrix = numeric_df.corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, ax=ax, cbar_kws={'label': 'Correlation'})
        plt.title('Correlation Matrix of Numeric Features')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Not enough numeric columns for correlation analysis")


def box_plot_rating_by_label(df):
    """Display box plot of ratings by label."""
    st.subheader("📦 Rating Distribution by Label")
    
    if 'rating' in df.columns:
        label_cols = [col for col in df.columns if 'label' in col.lower()]
        
        if label_cols:
            label_col = label_cols[0]
            
            fig = px.box(df, x=label_col, y='rating', title='Rating Distribution by Label')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No label column found")
    else:
        st.warning("No 'rating' column found")


def scatter_plot_word_count_vs_rating(df):
    """Display scatter plot of word count vs rating."""
    st.subheader("📍 Word Count vs Rating (Scatter Plot)")
    
    review_cols = [col for col in df.columns if 'review' in col.lower()]
    
    if review_cols and 'rating' in df.columns:
        review_col = review_cols[0]
        
        if 'word_count' not in df.columns:
            df['word_count'] = df[review_col].astype(str).apply(lambda x: len(x.split()))
        
        label_cols = [col for col in df.columns if 'label' in col.lower()]
        color_col = label_cols[0] if label_cols else None
        
        fig = px.scatter(df, x='word_count', y='rating', color=color_col,
                        title='Word Count vs Rating',
                        labels={'word_count': 'Word Count', 'rating': 'Rating'})
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Required columns not found")


def line_chart_reviews_over_time(df):
    """Display line chart of review count over time."""
    st.subheader("📅 Reviews Over Time (Line Chart)")

    date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]

    if date_cols:
        date_col = date_cols[0]
        temp_df = df.copy()
        temp_df[date_col] = pd.to_datetime(temp_df[date_col], errors='coerce')
        temp_df = temp_df.dropna(subset=[date_col])

        if temp_df.empty:
            st.warning("Date column found, but values are not parseable as dates")
            return

        trend_df = temp_df.groupby(temp_df[date_col].dt.date).size().reset_index(name='review_count')
        trend_df.columns = ['date', 'review_count']

        fig = px.line(
            trend_df,
            x='date',
            y='review_count',
            markers=True,
            title='Number of Reviews Over Time',
            labels={'date': 'Date', 'review_count': 'Review Count'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No date/time column found")


def violin_plot_rating_by_label(df):
    """Display violin plot of rating distribution by label."""
    st.subheader("🎻 Rating by Label (Violin Plot)")

    label_cols = [col for col in df.columns if 'label' in col.lower() or 'fake' in col.lower()]

    if 'rating' in df.columns and label_cols:
        label_col = label_cols[0]
        fig = px.violin(
            df,
            x=label_col,
            y='rating',
            color=label_col,
            box=True,
            points='all',
            title='Rating Distribution by Label (Violin)'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Required columns 'rating' and label/fake not found")


def donut_chart_rating_share(df):
    """Display donut chart of rating share."""
    st.subheader("🍩 Rating Share (Donut Chart)")

    if 'rating' in df.columns:
        rating_counts = df['rating'].value_counts().sort_index()
        fig = go.Figure(
            data=[go.Pie(
                labels=rating_counts.index,
                values=rating_counts.values,
                hole=0.5,
                textinfo='label+percent'
            )]
        )
        fig.update_layout(title='Rating Share', height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No 'rating' column found")


def density_contour_wordcount_rating(df):
    """Display density contour for word count and rating."""
    st.subheader("🗺️ Word Count vs Rating (Density Contour)")

    review_cols = [col for col in df.columns if 'review' in col.lower()]

    if review_cols and 'rating' in df.columns:
        review_col = review_cols[0]
        temp_df = df.copy()
        if 'word_count' not in temp_df.columns:
            temp_df['word_count'] = temp_df[review_col].astype(str).apply(lambda x: len(x.split()))

        fig = px.density_contour(
            temp_df,
            x='word_count',
            y='rating',
            title='Density of Word Count vs Rating',
            labels={'word_count': 'Word Count', 'rating': 'Rating'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Required columns not found")


def cumulative_reviews_curve(df):
    """Display cumulative review curve."""
    st.subheader("📈 Cumulative Reviews Curve")

    date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]

    if date_cols:
        date_col = date_cols[0]
        temp_df = df.copy()
        temp_df[date_col] = pd.to_datetime(temp_df[date_col], errors='coerce')
        temp_df = temp_df.dropna(subset=[date_col]).sort_values(date_col)

        if temp_df.empty:
            st.warning("Date column found, but values are not parseable as dates")
            return

        daily = temp_df.groupby(temp_df[date_col].dt.date).size().reset_index(name='daily_reviews')
        daily.columns = ['date', 'daily_reviews']
        daily['cumulative_reviews'] = daily['daily_reviews'].cumsum()

        fig = px.area(
            daily,
            x='date',
            y='cumulative_reviews',
            title='Cumulative Reviews Over Time',
            labels={'date': 'Date', 'cumulative_reviews': 'Cumulative Reviews'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No date/time column found")


def visualization_interface(df):
    """Main interface for data visualization."""
    viz_type = st.selectbox(
        "Select visualization type:",
        ["Review Length Distribution", "Rating Distribution", "Fake vs Genuine",
         "Word Frequency", "Correlation Heatmap", "Rating by Label", "Word Count vs Rating",
         "Reviews Over Time", "Violin Rating by Label", "Donut Rating Share",
         "Density Contour: Word Count vs Rating", "Cumulative Reviews Curve"]
    )
    
    if viz_type == "Review Length Distribution":
        histogram_review_length(df)
    elif viz_type == "Rating Distribution":
        bar_chart_rating_distribution(df)
    elif viz_type == "Fake vs Genuine":
        pie_chart_fake_vs_genuine(df)
    elif viz_type == "Word Frequency":
        top_n = st.slider("Select top N words to display:", 5, 50, 15)
        word_frequency_plot(df, top_n=top_n)
    elif viz_type == "Correlation Heatmap":
        correlation_heatmap(df)
    elif viz_type == "Rating by Label":
        box_plot_rating_by_label(df)
    elif viz_type == "Word Count vs Rating":
        scatter_plot_word_count_vs_rating(df)
    elif viz_type == "Reviews Over Time":
        line_chart_reviews_over_time(df)
    elif viz_type == "Violin Rating by Label":
        violin_plot_rating_by_label(df)
    elif viz_type == "Donut Rating Share":
        donut_chart_rating_share(df)
    elif viz_type == "Density Contour: Word Count vs Rating":
        density_contour_wordcount_rating(df)
    elif viz_type == "Cumulative Reviews Curve":
        cumulative_reviews_curve(df)
