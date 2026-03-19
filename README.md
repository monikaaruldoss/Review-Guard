# ReviewGuard - Fake Product Review Detection System

Fake Product Review Detector uses AI to analyze e-commerce reviews and identify suspicious, fake, or manipulated opinions.


## 🛡️ Overview

**ReviewGuard** is a comprehensive Python application that uses machine learning and natural language processing (NLP) to automatically detect fake product reviews. This tab-based Streamlit application provides tools for data upload, cleaning, analysis, visualization, and fake review detection.

Fake reviews are a major challenge in e-commerce, misleading consumers and damaging trust. ReviewGuard helps overcome this by providing:

- **Automatic Detection**: Machine learning models to identify fake reviews
- **Data Analysis Tools**: Comprehensive statistical analysis and exploration
- **Visualization Suite**: Interactive charts and visualizations
- **ML Models**: Multiple algorithms (Logistic Regression, Naive Bayes, Random Forest)

## 📋 Project Structure

```
reviewguard/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── modules/                        # Core functionality modules
│   ├── __init__.py
│   ├── upload.py                   # Dataset upload functionality
│   ├── cleaning.py                 # Data cleaning operations
│   ├── manipulation.py             # Interactive data manipulation
│   ├── analysis.py                 # Statistical analysis
│   ├── visualization.py            # Data visualization
│   ├── preprocessing.py            # Text preprocessing
│   ├── feature_extraction.py       # Feature engineering
│   ├── model_training.py           # Model training and evaluation
│   └── prediction.py               # Prediction functionality
│
├── data/                           # Data folder
│   └── reviews_dataset.csv         # Sample dataset (optional)
│
└── models/                         # Trained models storage
    └── fake_review_model.pkl       # Saved model file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd reviewguard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - The application will automatically open at `http://localhost:8501`

## 📊 Application Features

### 🏠 Tab 1: Home
- Project introduction and overview
- Application objectives and features
- Technology stack information
- Quick start guide

### 📁 Tab 2: Dataset Upload
- Upload CSV files containing product reviews
- Preview dataset information
- Display dataset size and columns
- Load sample datasets

**Expected CSV columns:**
- `review_text`: The content of the review
- `rating`: Product rating (1-5)
- `product_id`: Product identifier
- `review_date`: Date of review
- `label`: 0 (genuine) or 1 (fake)

### 🧹 Tab 3: Data Cleaning
- **Missing Value Handling**
  - Detect missing values
  - Fill using mean, median, or mode
  
- **Data Quality**
  - Remove duplicate rows
  - Text normalization (lowercase)
  
- **Text Preprocessing**
  - Remove URLs and emails
  - Remove special characters
  - Remove stopwords
  - Lemmatization

### 🛠️ Tab 4: Data Manipulation
- **Filter Data**: Filter rows by conditions
- **Select Columns**: Choose specific columns
- **Drop Columns**: Remove unwanted columns
- **Rename Columns**: Rename column headers
- **Sort Data**: Sort by any column
- **Create Features**: Generate new features
  - `review_length`: Length of review text
  - `word_count`: Number of words
  - `rating_category`: Categorical rating

### 📊 Tab 5: Data Analysis
- **Descriptive Statistics**: Mean, median, std, min, max
- **Rating Distribution**: Analyze rating patterns
- **Review Length Analysis**: Text length statistics
- **Word Frequency Analysis**: Most common words
- **Fake vs Genuine Analysis**: Compare characteristics

### 📈 Tab 6: Data Visualization
- **Histogram**: Review length distribution
- **Bar Chart**: Rating distribution
- **Pie Chart**: Fake vs genuine proportion
- **Word Frequency Plot**: Top words visualization
- **Correlation Heatmap**: Feature correlations
- **Box Plot**: Ratings by label
- **Scatter Plot**: Word count vs rating

### 🤖 Tab 7: Fake Review Detection
Complete ML workflow with:

1. **Preprocessing**
   - Text cleaning and normalization
   - Tokenization
   - Lemmatization

2. **Feature Extraction**
   - TF-IDF vectorization
   - Word count features
   - Review length features
   - Statistical features

3. **Model Training**
   - **Logistic Regression**: Fast, interpretable
   - **Naive Bayes**: Good for text classification
   - **Random Forest**: Ensemble method with high accuracy

4. **Evaluation**
   - Accuracy, Precision, Recall, F1-Score
   - Confusion Matrix visualization
   - Feature importance analysis

5. **Prediction**
   - Batch predictions on full dataset
   - Single review prediction
   - Confidence scores
   - Export results to CSV

## 🔧 Technology Stack

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### Machine Learning
- **Scikit-learn**: ML algorithms and evaluation
- **Joblib**: Model serialization

### Natural Language Processing
- **NLTK**: Text processing and tokenization
  - Stopword removal
  - Lemmatization
  - Tokenization

### Visualization
- **Matplotlib**: Static plotting
- **Seaborn**: Statistical visualizations
- **Plotly**: Interactive visualizations

### User Interface
- **Streamlit**: Web application framework

## 📊 Model Performance Metrics

### Accuracy
Percentage of correct predictions (true positives + true negatives) / total

### Precision
True positives / (true positives + false positives)
- Measures how many predicted fakes are actually fake

### Recall
True positives / (true positives + false negatives)
- Measures how many actual fakes are correctly identified

### F1-Score
Harmonic mean of precision and recall
- Balanced metric for imbalanced datasets

### Confusion Matrix
- True Positives (TP): Correctly identified fake reviews
- True Negatives (TN): Correctly identified genuine reviews
- False Positives (FP): Genuine reviews marked as fake
- False Negatives (FN): Fake reviews marked as genuine

## 📥 Import/Export Features

### Import
- Upload CSV files with any structure
- Supports large datasets
- Automatic column detection

### Export
- **Cleaned Dataset**: Download cleaned data as CSV
- **Prediction Results**: Export predictions with confidence scores
- **Trained Model**: Save model as pkl file for future use

## 💡 Usage Tips

1. **Data Quality**: Larger, cleaner datasets lead to better models
2. **Preprocessing Important**: Text cleaning significantly improves results
3. **Feature Engineering**: Create relevant features for better predictions
4. **Model Selection**: Try different algorithms for optimal performance
5. **Validation**: Always validate on test data before production use
6. **Confidence Scores**: Pay attention to prediction confidence levels

## 🎯 Workflow Example

1. **Upload Data**
   - Go to "Dataset Upload" tab
   - Upload your CSV file
   - Review the dataset structure

2. **Clean Data**
   - Go to "Data Cleaning" tab
   - Handle missing values
   - Remove duplicates
   - Process text (remove stopwords, lemmatize)

3. **Analyze**
   - Go to "Data Analysis" tab
   - Explore word frequencies
   - Analyze rating distribution
   - Compare fake vs genuine patterns

4. **Visualize**
   - Go to "Data Visualization" tab
   - Create charts to understand patterns
   - Review correlation heatmap

5. **Train & Predict**
   - Go to "Fake Review Detection" tab
   - Configure model parameters
   - Train the model
   - Make predictions
   - Export results

## 📝 Sample Dataset Format

| review_text | rating | product_id | review_date | label |
|-------------|--------|-----------|------------|-------|
| Great product, highly recommend! | 5 | P001 | 2023-01-15 | 0 |
| Best purchase ever | 5 | P001 | 2023-01-16 | 1 |
| Works as described, good quality | 4 | P002 | 2023-01-17 | 0 |
| Not worth the price | 2 | P003 | 2023-01-18 | 0 |

## 🔐 Model Storage

Trained models are saved in the `models/` directory as `.pkl` files using joblib serialization. This allows you to:
- Reuse models without retraining
- Share models with others
- Deploy models in production

## 🛠️ Customization

### Adding Custom Features
Edit `modules/feature_extraction.py` to add new features

### Changing Algorithms
Modify `modules/model_training.py` to add new ML algorithms

### Adjusting Preprocessing
Edit `modules/preprocessing.py` to customize text cleaning

## 📚 Dependencies Details

- **streamlit** (5.32.2+): Web framework
- **pandas** (1.3.0+): Data manipulation
- **numpy** (1.21.0+): Numerical computing
- **scikit-learn** (1.0.0+): ML algorithms
- **nltk** (3.6.0+): NLP toolkit
- **matplotlib** (3.4.0+): Plotting
- **seaborn** (0.11.0+): Statistical visualization
- **plotly** (5.0.0+): Interactive plots
- **joblib** (1.0.0+): Model serialization

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### NLTK data not downloading
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

### Out of memory on large datasets
- Process data in chunks
- Reduce max_features for TF-IDF
- Use smaller test set size

## 📈 Performance Tips

- **Optimal batch size**: 1000-5000 reviews
- **Best preprocessing**: Lemmatization + stopword removal
- **Fastest algorithm**: Logistic Regression
- **Most accurate**: Random Forest (with more time)

## 🎓 Learning Resources

- [Scikit-learn Docs](https://scikit-learn.org)
- [NLTK Docs](https://www.nltk.org)
- [Streamlit Docs](https://docs.streamlit.io)
- [Pandas Docs](https://pandas.pydata.org)

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

The MIT License is a permissive open-source license that allows you to:
- ✅ Use for commercial and private purposes
- ✅ Modify and distribute the code
- ✅ Include it in proprietary applications

**The only requirement is** to include the original license and copyright notice in any copies or substantial portions of the software.

For more information about MIT License, visit [opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 👥 Author

ReviewGuard Development Team

---

**Built with ❤️ for data science and machine learning enthusiasts**

For questions or support, please create an issue on the project repository.
