# Multimodal Real Estate Price Prediction 🏠🛰️

This project predicts real estate prices using a **Multimodal Neural Network** that fuses traditional tabular data (square footage, bedrooms, year built) with satellite imagery (visual surroundings of the property).

The pipeline consists of three main stages: Data Acquisition, Preprocessing, and Model Training.

## 📂 Project Structure

* `data_fetcher.py`: Script to fetch satellite images for each property using an API.
* `preprocessing(1).ipynb`: Notebook to clean, engineer features, and normalize tabular data.
* `model-training(1).ipynb`: Notebook to train the XGBoost baseline and the Multimodal CNN (ResNet18 + MLP) model.

---

## 🚀 Usage Instructions

Follow these steps in order to reproduce the results.

### Step 1: Fetch Satellite Images
First, we need to download the visual data for every house in the dataset.

1.  Open `data_fetcher.py`.

2.  Ensure your API Key (e.g., Google Static Maps or other provider) is correctly set in the script variables.
4.  Run the script to download images into a local folder (e.g., `satellite_images/`).



### Step 2: Data Preprocessing

   Prepare the tabular data for the neural network. This step handles missing values, removes redundant features (like yr_built vs house_age), and performs Standard Scaling.

   Open preprocessing(1).ipynb (Jupyter Notebook or Google Colab).

   Update the file_path variable to point to your raw Excel/CSV dataset (e.g., train(1).xlsx).

   Run all cells.

What this script does:

  Generates house_age and years_since_reno features.

  Drops multicollinear features (sqft_above, yr_built).

  Scales numerical data (Mean=0, Std=1).

  Saves processed arrays to compressed files.

  Output:

  dataset.npz: Contains X_train, y_train, and X_test (scaled).

  test_ids.csv: Contains the IDs required for the final submission.

### Step 3: Model Training

Train the Multimodal Neural Network that combines the images from Step 1 and the data from Step 2.

  Open model-training(1).ipynb.

  Upload Data: Ensure the following are available in your environment (or Kaggle Input):

  The satellite_images/ folder.

  The dataset.npz and test_ids.csv files generated in Step 2.

  The original train.xlsx (required to align image IDs with training rows).

  Update Paths: Check the CONFIGURATION section at the top of the notebook to match your file paths:
  Python

  IMAGE_DIR = '/path/to/satellite_images'
  PROCESSED_DATA_PATH = '/path/to/dataset.npz'
  ORIGINAL_DATA_PATH = '/path/to/train(1).xlsx'

  Run all cells to train the model.

What this script does:

  XGBoost Baseline: Trains a gradient boosting model on tabular data only for performance benchmarking.

  Multimodal CNN:

  Loads images via a Custom PyTorch Dataset.

  Uses ResNet18 to extract visual features.

  Fuses visual embeddings with tabular data.

  Trains using Log-Transformed targets (to minimize RMSE on large prices).

  Inference: Generates predictions for the test set.

  Output:

  best_multimodal_model.pth: The saved PyTorch model weights.

  submission_multimodal.csv: The final submission file containing id and predicted price.

### 🛠️ Requirements

  Python 3.8+

  PyTorch & Torchvision

  pandas, numpy

  scikit-learn

  XGBoost

  Pillow (PIL)

  tqdm
