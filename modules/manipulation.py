"""Module for interactive data manipulation"""
import pandas as pd
import streamlit as st


def filter_dataframe(df):
    """Allow users to filter rows based on conditions."""
    st.subheader("🔍 Filter Data")
    
    column = st.selectbox("Select column to filter:", df.columns)
    
    if df[column].dtype in ['float64', 'int64']:
        operator = st.selectbox("Select operator:", ['>', '<', '>=', '<=', '==', '!='])
        value = st.number_input("Enter value:")
        
        if operator == '>':
            filtered_df = df[df[column] > value]
        elif operator == '<':
            filtered_df = df[df[column] < value]
        elif operator == '>=':
            filtered_df = df[df[column] >= value]
        elif operator == '<=':
            filtered_df = df[df[column] <= value]
        elif operator == '==':
            filtered_df = df[df[column] == value]
        elif operator == '!=':
            filtered_df = df[df[column] != value]
    
    else:
        value = st.text_input("Enter value to filter:")
        filtered_df = df[df[column].astype(str).str.contains(value, case=False, na=False)]
    
    st.info(f"Showing {len(filtered_df)} rows out of {len(df)} total rows")
    st.dataframe(filtered_df, use_container_width=True)
    
    return filtered_df


def select_columns(df):
    """Allow users to select specific columns."""
    st.subheader("📋 Select Columns")
    
    selected_cols = st.multiselect("Select columns to keep:", df.columns, default=df.columns)
    
    if selected_cols:
        df_selected = df[selected_cols]
        st.dataframe(df_selected, use_container_width=True)
        st.info(f"Selected {len(selected_cols)} columns")
        return df_selected
    else:
        st.warning("Please select at least one column")
        return df


def drop_columns(df):
    """Allow users to drop specific columns."""
    st.subheader("🗑️ Drop Columns")
    
    cols_to_drop = st.multiselect("Select columns to drop:", df.columns)
    
    if cols_to_drop:
        df_dropped = df.drop(columns=cols_to_drop)
        st.dataframe(df_dropped, use_container_width=True)
        st.info(f"Dropped {len(cols_to_drop)} columns. Remaining: {len(df_dropped.columns)} columns")
        return df_dropped
    else:
        return df


def rename_columns(df):
    """Allow users to rename columns."""
    st.subheader("✏️ Rename Columns")
    
    rename_dict = {}
    for col in df.columns:
        new_name = st.text_input(f"Rename '{col}' to:", value=col, key=f"rename_{col}")
        if new_name != col:
            rename_dict[col] = new_name
    
    if rename_dict:
        df_renamed = df.rename(columns=rename_dict)
        st.dataframe(df_renamed, use_container_width=True)
        st.success(f"Renamed {len(rename_dict)} columns")
        return df_renamed
    else:
        return df


def sort_dataset(df):
    """Allow users to sort the dataset."""
    st.subheader("⬆️ Sort Data")
    
    sort_column = st.selectbox("Select column to sort by:", df.columns)
    ascending = st.checkbox("Sort in ascending order", value=True)
    
    df_sorted = df.sort_values(by=sort_column, ascending=ascending)
    st.dataframe(df_sorted, use_container_width=True)
    st.info(f"Dataset sorted by {sort_column} ({'ascending' if ascending else 'descending'})")
    
    return df_sorted


def create_new_features(df):
    """Create new derived features from existing columns."""
    st.subheader("➕ Create New Features")
    
    if 'review_text' in df.columns or any('review' in col.lower() for col in df.columns):
        review_col = next((col for col in df.columns if 'review' in col.lower()), None)
        
        if review_col and st.checkbox("Create 'review_length' feature"):
            df['review_length'] = df[review_col].astype(str).apply(len)
            st.success("✅ Created 'review_length' column")
        
        if review_col and st.checkbox("Create 'word_count' feature"):
            df['word_count'] = df[review_col].astype(str).apply(lambda x: len(x.split()))
            st.success("✅ Created 'word_count' column")
    
    if 'rating' in df.columns and st.checkbox("Create 'rating_category' feature"):
        df['rating_category'] = pd.cut(df['rating'], bins=[0, 2, 4, 5], labels=['Low', 'Medium', 'High'])
        st.success("✅ Created 'rating_category' column")
    
    st.dataframe(df, use_container_width=True)
    return df


def data_manipulation_interface(df):
    """Main interface for data manipulation."""
    option = st.selectbox(
        "Select manipulation operation:",
        ["Filter Data", "Select Columns", "Drop Columns", "Rename Columns", "Sort Data", "Create Features"]
    )
    
    if option == "Filter Data":
        return filter_dataframe(df)
    elif option == "Select Columns":
        return select_columns(df)
    elif option == "Drop Columns":
        return drop_columns(df)
    elif option == "Rename Columns":
        return rename_columns(df)
    elif option == "Sort Data":
        return sort_dataset(df)
    elif option == "Create Features":
        return create_new_features(df)
    
    return df
