# FurniMatch AI - Notebooks

This directory contains Jupyter notebooks for data analysis and model training.

## Notebooks Overview

### 1. Data Analytics Notebook (`1_data_analytics.ipynb`)

**Purpose:** Comprehensive exploratory data analysis of the furniture dataset.

**Contents:**
- Dataset loading and structure inspection
- Data quality assessment (missing values, duplicates)
- Price distribution analysis with visualizations
- Category and brand analysis
- Material and color distribution
- Price-by-category insights
- Data completeness summary
- Key insights and recommendations

**Key Findings:**
- Dataset size and quality metrics
- Price range and distribution patterns
- Most common categories and brands
- Material and color diversity
- Recommendations for model development

**Run Time:** ~2-3 minutes

---

### 2. Model Training Notebook (`2_model_training.ipynb`)

**Purpose:** Train and evaluate the semantic search recommendation model.

**Contents:**
- Data preprocessing and cleaning
- Weighted text representation strategy
- SentenceTransformers model loading
- Product embedding generation
- Keyword scoring implementation (category, material, color)
- Multi-factor recommendation algorithm
- Model evaluation with test queries
- Performance metrics and visualizations
- Model export for production

**Model Architecture:**
- **Base Model:** all-MiniLM-L6-v2 (SentenceTransformers)
- **Embedding Dimension:** 384
- **Scoring Weights:** 
  - Text similarity: 75%
  - Category matching: 15%
  - Material matching: 5%
  - Color matching: 5%

**Performance:**
- Average similarity score: >0.50
- Inference time: <1 second per query
- Memory efficient: ~few MB for embeddings
- High relevance for diverse queries

**Run Time:** ~10-15 minutes (first run includes model download)

---

## Setup Instructions

### Prerequisites

```bash
# Python 3.12+ required
python --version

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
# Install Jupyter and required libraries
pip install jupyter notebook
pip install pandas numpy matplotlib seaborn
pip install sentence-transformers scikit-learn
pip install tqdm
```

Or install from project requirements:

```bash
cd ../backend
pip install -r requirements.txt
pip install jupyter notebook
```

### Run Notebooks

```bash
# Start Jupyter
jupyter notebook

# Or use JupyterLab
pip install jupyterlab
jupyter lab
```

Then open the notebooks in order:
1. `1_data_analytics.ipynb`
2. `2_model_training.ipynb`

---

## Data Requirements

The notebooks expect the dataset at:
```
../backend/data/furniture_dataset.csv
```

**Required columns:**
- `uniq_id`: Unique product identifier
- `title`: Product name
- `brand`: Brand name
- `price`: Product price
- `categories`: Product categories
- `description`: Product description
- `material`: Primary material
- `color`: Primary color
- `images`: Image URLs

---

## Outputs

### Data Analytics Notebook
- Visualizations (histograms, bar charts, box plots)
- Statistical summaries
- Data quality reports
- Key insights document

### Model Training Notebook
- Trained embeddings (`../models/product_embeddings.npy`)
- Model metadata (`../models/model_metadata.pkl`)
- Performance metrics
- Evaluation visualizations

---

## Troubleshooting

**Issue:** Model download fails
```bash
# Solution: Check internet connection or use cache
export TRANSFORMERS_CACHE=/path/to/cache
```

**Issue:** Out of memory during embedding generation
```bash
# Solution: Reduce batch size in model training notebook
BATCH_SIZE = 16  # Default is 32
```

**Issue:** Jupyter kernel crashes
```bash
# Solution: Increase memory limit or process smaller batches
# Restart kernel and run cells one at a time
```

**Issue:** Missing dataset
```bash
# Solution: Ensure dataset is in correct location
ls ../backend/data/furniture_dataset.csv
```

---

## Notes

- Run notebooks in order (analytics before training)
- First run of training notebook downloads ~80MB model
- Embeddings are cached for reuse
- All visualizations are saved inline
- Model artifacts exported to `../models/` directory

---

## Contact

For issues or questions about the notebooks, refer to the main project README or contact the development team.
