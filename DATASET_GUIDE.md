# 📊 ReviewGuard - Dataset Upload Guide

## 🎯 Overview

ReviewGuard is built to work with **your own dataset**. This guide explains how to prepare and upload your data.

## ✅ Required Columns

Your CSV file must contain these columns:

### 1. **review_text** (Required)
- **Description**: The actual text content of the product review
- **Type**: Text/String
- **Example**: "This product is amazing! Great quality and fast delivery."
- **Notes**: Can be any length, will be processed automatically

### 2. **label** (Required)
- **Description**: Whether the review is fake or genuine
- **Type**: Numeric (0 or 1) OR Text ("genuine", "fake")
- **Mapping**: 
  - `0` = Genuine review
  - `1` = Fake review
- **Example**: 0 (for genuine) or 1 (for fake)
- **Notes**: Must be present for machine learning training

## 📋 Optional Columns

These columns are helpful but not required:

### 3. **rating** (Optional)
- **Description**: Product rating given by reviewer
- **Type**: Numeric (1-5 or 1-10)
- **Example**: 5, 4, 1
- **Notes**: Used for analysis and visualization

### 4. **product_id** (Optional)
- **Description**: Identifier for the product
- **Type**: Text or Numeric
- **Example**: "P001", "PROD_12345"
- **Notes**: Used for grouping analysis

### 5. **review_date** (Optional)
- **Description**: Date when review was posted
- **Type**: Date format (YYYY-MM-DD)
- **Example**: "2023-01-15"
- **Notes**: Used for temporal analysis

## 📝 CSV Format Example

### Minimum Format (Only Required Columns)
```csv
review_text,label
"Great product, highly recommend!",0
"Best item ever, amazing quality!",1
"Terrible, broke immediately",0
"Fantastic purchase, love it!",1
```

### Complete Format (All Columns)
```csv
review_text,rating,product_id,review_date,label
"This product is amazing! I love it.",5,P001,2023-01-15,0
"Best purchase ever made, highly recommended!",5,P002,2023-01-16,1
"Works as described, great value for money.",4,P003,2023-01-17,0
"Not worth the price, disappointed.",2,P004,2023-01-18,0
"Absolutely terrible, waste of money.",1,P005,2023-01-19,1
```

## 🔍 Data Quality Guidelines

### ✅ DO:
- Use UTF-8 encoding
- Keep review text meaningful (50+ characters ideally)
- Use consistent label values (all 0/1, not mixed with 0/1 and "true"/"false")
- Include balanced fake and genuine reviews if possible
- Ensure no duplicate rows (or mark as intentional)

### ❌ DON'T:
- Leave empty or null cells in review_text or label columns
- Mix label formats (don't use both 0 and "fake")
- Use special character encoding that causes display issues
- Include extremely long text (>5000 characters per review may slow processing)
- Have completely blank review text

## 📥 Uploading Your Dataset

### Step 1: Prepare Your CSV File
- Ensure all required columns are present
- Save as `.csv` format (not .xlsx or .json)
- Use UTF-8 encoding

### Step 2: Open ReviewGuard
```bash
streamlit run app.py
```

### Step 3: Go to Dataset Upload Tab
- Click on the **📁 Dataset Upload** tab
- You'll see the upload area

### Step 4: Upload Your File
- Click the upload button
- Select your CSV file
- Wait for validation

### Step 5: Verify Dataset
- Check the preview (first 10 rows)
- Verify column names and data types
- Confirm dataset size matches expectations

## 🎯 Sample Datasets

### Example 1: E-commerce Reviews
```csv
review_text,rating,product_id,review_date,label
"Amazing quality, delivered on time!",5,PHONE_001,2023-01-15,0
"Best phone ever, love it so much!!!",5,PHONE_001,2023-01-16,1
"Good phone, battery life could be better",3,PHONE_001,2023-01-17,0
"Terrible phone, don't buy this!",1,PHONE_001,2023-01-18,1
```

### Example 2: Restaurant Reviews
```csv
review_text,rating,product_id,review_date,label
"Food was delicious, service was great",5,REST_042,2023-02-10,0
"BEST RESTAURANT EVER!!!!! AMAZING!!!!",5,REST_042,2023-02-11,1
"Good food but a bit overpriced",3,REST_042,2023-02-12,0
"Worst experience ever, never going back",1,REST_042,2023-02-13,1
```

### Example 3: Movie Reviews
```csv
review_text,rating,label
"Great cinematography and compelling story",4,0
"This movie is SPECTACULAR!!!!! Must watch!!!!",5,1
"Average plot but good acting",3,0
"Waste of time, terrible movie",1,1
```

## 🚨 Common Issues & Solutions

### Issue 1: "Missing required columns"
**Solution**: Ensure your CSV has both `review_text` and `label` columns
- Check column names exactly (case-sensitive)
- Rename if needed: Right-click → Rename

### Issue 2: "Error reading file"
**Solution**:
- Verify CSV is properly formatted
- Try opening in a text editor to check format
- Ensure UTF-8 encoding (not Unicode or ASCII)
- Remove any special characters from column names

### Issue 3: "Labels not recognized"
**Solution**:
- Labels must be 0/1 or "genuine"/"fake"
- Not compatible with: True/False, yes/no, ✓/✗
- Clean label values if needed

### Issue 4: Dataset too slow
**Solution**:
- ReviewGuard works best with 500-10,000 reviews
- Reduce dataset size if it's very large (100k+ rows)
- Consider filtering to a subset

### Issue 5: Special characters causing issues
**Solution**:
- Save CSV with UTF-8 encoding
- Avoid emojis or unusual characters
- Test opening file in text editor first

## 📊 Dataset Size Recommendations

| Dataset Size | Recommended | Max | Speed |
|---|---|---|---|
| 100 reviews | Minimum | - | ~10 seconds |
| 500 reviews | Good | - | ~15-20 seconds |
| 1,000 reviews | Ideal | - | ~20-30 seconds |
| 5,000 reviews | Excellent | - | ~30-60 seconds |
| 10,000+ reviews | Large | 100,000 | ~1-2 minutes |

## 🔄 Data Preparation Checklist

Before uploading your dataset, verify:

- [ ] CSV file is saved with correct encoding (UTF-8)
- [ ] `review_text` column exists and has meaningful content
- [ ] `label` column exists with values 0 or 1
- [ ] No empty cells in required columns
- [ ] Column names are lowercase or properly formatted
- [ ] Dataset has 50+ reviews (more is better)
- [ ] Labels are balanced (roughly equal fake and genuine)
- [ ] No duplicate rows (unless intentional)
- [ ] File opens correctly in text editor
- [ ] CSV is less than 10 MB in size

## 💡 Tips for Better Results

### Dataset Quality
1. **Balance**: Try to have roughly equal fake and genuine reviews
2. **Variety**: Include reviews from different products and time periods
3. **Text Quality**: Real reviews have varied quality - include some short and some long
4. **Authenticity**: Mix natural writing styles

### Data Preparation
1. Remove spam/corrupted records
2. Handle special characters properly
3. Ensure consistent labeling
4. Remove exact duplicates if any

### For Better ML Models
1. **More data** = Better models (minimum 500, ideal 5,000+)
2. **Balanced labels** = Better accuracy
3. **Clean text** = Clear patterns for ML to learn
4. **Feature variety** = Different review lengths, ratings, products

## 📞 Need Help?

### Check These Resources:
1. Review README.md for complete documentation
2. Look at the SETUP_GUIDE.md for quick start
3. Check INSTALLATION.md for system requirements
4. Review this file for dataset guidelines

### Common Questions:

**Q: Can I use reviews in other languages?**
A: Currently optimized for English. Other languages may work but results vary.

**Q: What's the maximum file size?**
A: Recommended max 10 MB (~10,000 reviews). Larger files may be slow.

**Q: Can I have more than 5 columns?**
A: Yes! Extra columns are ignored but won't cause errors.

**Q: Do reviews need to be cleaned first?**
A: No! The app handles cleaning automatically.

**Q: What if I don't have labels?**
A: Labels are required for model training. You'll need to manually label some reviews.

---

## ✅ Ready to Upload?

1. Prepare your CSV file following this guide
2. Open ReviewGuard
3. Go to **📁 Dataset Upload** tab
4. Upload your file
5. Verify the preview
6. Proceed with analysis in other tabs!

**Good luck! 🛡️**
