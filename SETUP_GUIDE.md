# ReviewGuard - Quick Setup Guide

## 🚀 Installation & Running Instructions

### Step 1: Navigate to the Project Directory
```bash
cd "/Users/monika_aruldoss/Downloads/Detection of fake Review/reviewguard"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

### Step 4: Access the Application
- The application will automatically open in your default browser
- URL: `http://localhost:8501`
- If not opened automatically, manually visit the URL above

## 📊 Using the Application

### Tab 1: Home 🏠
- Read the project description and objectives
- Understand the features and technology stack
- View quick start instructions

### Tab 2: Dataset Upload 📁
- Upload your CSV file (or use the sample dataset)
- Preview the data structure
- Check dataset dimensions and columns

### Tab 3: Data Cleaning 🧹
- Handle missing values (fill or delete)
- Remove duplicate rows
- Clean and preprocess text
  - Remove URLs, emails, special characters
  - Remove stopwords
  - Lemmatize text

### Tab 4: Data Manipulation 🛠️
- Filter rows by conditions
- Select specific columns
- Drop unwanted columns
- Rename columns
- Sort data
- Create new features (review_length, word_count, etc.)

### Tab 5: Data Analysis 📊
- View descriptive statistics
- Analyze rating distribution
- Review length analysis
- Word frequency analysis
- Compare fake vs genuine reviews

### Tab 6: Data Visualization 📈
- Interactive charts
- Review length histogram
- Rating distribution bar chart
- Fake vs genuine pie chart
- Word frequency plots
- Correlation heatmap
- Box plots and scatter plots

### Tab 7: Fake Review Detection 🤖
1. **Preprocess Data**
   - Click "Start Preprocessing" to prepare text data
   - Extract TF-IDF features

2. **Train Model**
   - Choose algorithm (Logistic Regression, Naive Bayes, or Random Forest)
   - Click "Train Model"
   - View evaluation metrics

3. **Make Predictions**
   - Generate predictions on entire dataset
   - Predict single reviews
   - View confidence scores
   - Export results

## 📥 Sidebar Features

### Dataset Management
- View current dataset status
- See if data is cleaned or model is trained

### Export Options
- Download results as CSV
- Save trained model as PKL file
- Use downloaded model for future predictions

## 💾 Sample Dataset

A sample dataset is included at `data/reviews_dataset.csv` with:
- 50 product reviews
- Mix of fake (label=1) and genuine (label=0) reviews
- Ratings from 1-5
- Various review lengths and sentiments

## 🔧 System Requirements

- Python 3.7+
- 2GB RAM minimum
- 500MB disk space for dependencies
- macOS, Windows, or Linux

## 📝 Common Issues & Solutions

### Issue: "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: NLTK data download fails
**Solution:**
```python
python -m nltk.downloader punkt stopwords wordnet
```

### Issue: Port 8501 already in use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Issue: Out of memory
**Solution:**
- Use smaller dataset
- Reduce TF-IDF max_features slider
- Close other applications

## 🎯 Recommended Workflow

1. **Start with Sample Data** (Tab 2)
   - Use included sample dataset to understand the flow
   
2. **Clean the Data** (Tab 3)
   - Remove duplicates
   - Handle missing values
   - Process text

3. **Explore the Data** (Tabs 5-6)
   - Run analysis
   - View visualizations
   - Understand patterns

4. **Train a Model** (Tab 7)
   - Configure model parameters
   - Train on preprocessed data
   - Evaluate performance

5. **Make Predictions** (Tab 7)
   - Generate predictions
   - Test with single reviews
   - Export results

## 📚 Expected CSV Format

Your dataset should have these columns:
- `review_text` - The review content (required)
- `rating` - Product rating (recommended)
- `product_id` - Product ID (recommended)
- `review_date` - Review date (optional)
- `label` - 0 for genuine, 1 for fake (required for training)

## 🛑 Stopping the Application

Press `Ctrl + C` in your terminal to stop the Streamlit server.

## 🎓 Tips for Best Results

1. **Use Clean Data**
   - More data = better models
   - Balanced dataset improves accuracy
   
2. **Preprocess Text**
   - Remove stopwords improves feature quality
   - Lemmatization recommended
   
3. **Feature Engineering**
   - Create relevant features
   - Review length helps distinguish fake reviews
   
4. **Model Selection**
   - Logistic Regression: Fast, interpretable
   - Naive Bayes: Good baseline
   - Random Forest: Best accuracy (slower)

5. **Validate Results**
   - Check model metrics
   - Review confidence scores
   - Analyze misclassifications

## 📊 File Descriptions

### Main Files
- **app.py** - Main Streamlit application (800+ lines)
- **requirements.txt** - Python package dependencies
- **README.md** - Complete documentation

### Modules (in modules/ folder)
- **upload.py** - CSV upload and dataset preview
- **cleaning.py** - Data cleaning and text preprocessing
- **manipulation.py** - Data filtering and transformation
- **analysis.py** - Statistical analysis functions
- **visualization.py** - Interactive charts and plots
- **preprocessing.py** - Text preprocessing pipeline
- **feature_extraction.py** - TF-IDF and feature creation
- **model_training.py** - ML model training and evaluation
- **prediction.py** - Batch and single predictions

### Data
- **data/reviews_dataset.csv** - Sample dataset with 50 reviews

## 🔐 Model Export & Reuse

Trained models are automatically saved and downloadable:
1. After training, download the model from sidebar
2. Load in another Python script:
   ```python
   import pickle
   with open('fake_review_model.pkl', 'rb') as f:
       data = pickle.load(f)
       model = data['model']
       vectorizer = data['vectorizer']
   ```

## 🎯 Project Goals Achieved

✅ Tab-based interface with 7 tabs
✅ CSV dataset upload and preview
✅ Data cleaning (missing values, duplicates, text preprocessing)
✅ Data manipulation (filter, select, drop, rename, sort, features)
✅ Statistical analysis and descriptive statistics
✅ Multiple visualization types
✅ Complete ML workflow with 3 algorithms
✅ Model evaluation with multiple metrics
✅ Single review prediction
✅ Export predictions and models
✅ Beginner-friendly interface
✅ Comprehensive documentation

---

## Need Help?

1. Check README.md for detailed documentation
2. Review the docstrings in module files
3. Look at sample dataset format
4. Test with sample data first

Happy detecting fake reviews! 🛡️
