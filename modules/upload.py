"""Module for handling dataset upload functionality"""
import pandas as pd
import streamlit as st


def upload_dataset():
    """
    Handle CSV file upload and preview.
    
    Returns:
        DataFrame or None: Uploaded dataset or None if no file is uploaded
    """
    uploaded_file = st.file_uploader("Upload a CSV file containing product reviews", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Dataset Size:** {df.shape[0]} rows × {df.shape[1]} columns")
            
            with col2:
                st.write(f"**Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            st.write("**Column Names:**")
            st.write(df.columns.tolist())
            
            st.write("**Dataset Preview (First 10 rows):**")
            st.dataframe(df.head(10), use_container_width=True)
            
            st.write("**Data Types:**")
            st.dataframe(df.dtypes.to_frame("Data Type"), use_container_width=True)
            
            # Validate dataset columns
            is_valid, missing_cols, required_cols = validate_dataset_columns(df)
            
            if not is_valid:
                st.error(f"❌ **Missing required columns:** {', '.join(missing_cols)}")
                st.warning(f"Your dataset must have: {', '.join(required_cols)}")
                return None
            else:
                st.success("✅ Dataset has all required columns for analysis!")
            
            return df
        
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            return None
    
    else:
        st.info("Please upload a CSV file to get started.")
        return None


def validate_dataset_columns(df):
    """
    Validate that uploaded dataset has required columns.
    
    Args:
        df: DataFrame to validate
    
    Returns:
        tuple: (is_valid, missing_columns, required_columns)
    """
    required_columns = ['review_text', 'label']
    optional_columns = ['rating', 'product_id', 'review_date']
    
    df_columns_lower = [col.lower() for col in df.columns]
    missing = []
    
    for req_col in required_columns:
        if req_col.lower() not in df_columns_lower:
            missing.append(req_col)
    
    is_valid = len(missing) == 0
    return is_valid, missing, required_columns
