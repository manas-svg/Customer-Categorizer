
# Customer Personality Segmentation

## Overview

This repository implements a customer segmentation and prediction solution using unsupervised clustering and supervised classification. The project ingests customer records from MongoDB, performs exploratory data analysis and feature engineering, creates cluster labels using K-Means / Agglomerative clustering, and then trains a classification model to predict the segment for new customers.

## What this project does

- Loads the marketing campaign dataset into MongoDB
- Exports feature-store data from MongoDB into the training pipeline
- Runs EDA including missing value handling, correlation and VIF analysis
- Builds clusters using PCA-assisted clustering and silhouette analysis
- Converts cluster assignments into classification targets
- Evaluates multiple classifiers and selects the best performing model
- Stores trained model artifacts in AWS S3
- Serves predictions through a FastAPI backend with a simple web UI

## Key skills used

- Exploratory Data Analysis (EDA)
- Data cleaning and missing value handling
- Correlation analysis, VIF, and feature engineering
- Dimensionality reduction with PCA
- Clustering with K-Means and Agglomerative Clustering
- Model selection and hyperparameter tuning with `GridSearchCV`
- Classification using Logistic Regression, Random Forest, AdaBoost, and Gradient Boosting
- Performance reporting with accuracy, classification report, and confusion matrix
- Backend development using FastAPI and Jinja2 templates
- MongoDB data ingestion and feature store export
- AWS S3 for model storage and deployment artifacts
- Modular ML pipeline design with ingestion, validation, transformation, training, evaluation, and pushing

## What you will find in notebooks

- `notebooks/EDA.ipynb`
  - Exploratory Data Analysis
  - Missing value detection (Income column)
  - Correlation and VIF analysis
  - Target-free dataset analysis and clustering preparation

- `notebooks/Feature_engineering_and_clustering.ipynb`
  - Data preprocessing and scaling
  - PCA and silhouette score analysis
  - Comparison of K-Means and Agglomerative clustering
  - Conclusion that K-Means is a strong candidate for cluster generation

- `notebooks/Feature_Selection_and_classification.ipynb`
  - Classification after clustering
  - Train/test split and model comparison
  - `GridSearchCV` hyperparameter tuning
  - Best model selection via classification report and confusion matrix
  - Logistic Regression identified as the best-performing model

## Backend architecture

The backend is built with `FastAPI` and exposes:

- `GET /` — renders the customer prediction form
- `POST /` — accepts form input, runs prediction pipeline, and renders output
- `GET /train` — triggers the training pipeline end-to-end

Key backend files:

- `app.py` — FastAPI application and routing
- `src/pipeline/train_pipeline.py` — orchestrates data ingestion, validation, transformation, training, evaluation, and S3 pushing
- `src/pipeline/prediction_pipeline.py` — prepares input data and loads the model from S3 for prediction

## Data and infrastructure flow

1. `scripts/load_mongodb_data.py` loads `notebooks/marketing_campaign.csv` into MongoDB
2. `src/components/data_ingestion.py` reads MongoDB collection, drops schema-specified columns, and saves train/test CSVs
3. `src/components/data_validation.py` validates data and optionally checks drift via Evidently
4. `src/components/data_transformation.py` prepares transformed training data
5. `src/components/model_trainer.py` trains the classifier
6. `src/components/model_evaluation.py` validates model acceptance
7. `src/components/model_pusher.py` uploads the trained model artifact to AWS S3
8. `src/pipeline/prediction_pipeline.py` loads the S3 model and predicts new customer cluster labels

## AWS and MongoDB usage

- MongoDB is used as the source of truth for raw customer data
- Environment variable names:
  - `MONGO_DB_URL` (preferred)
  - `MONGODB_URL` or `MONGODB_URI`
- AWS S3 is used for model artifact storage via `boto3`
- S3 bucket names defined in code:
  - Training bucket: `customer-segmentation-bucket`
  - Prediction data bucket: `sensor-datasource`

## Installation and local run

1. Clone the repository:

```bash
git clone https://github.com/Machine-Learning-01/Customer_segmentation.git
cd Customer-Categorizer
```

2. Create and activate your Python environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables using your AWS and MongoDB credentials:

```powershell
setx AWS_ACCESS_KEY_ID "<AWS_ACCESS_KEY_ID>"
setx AWS_SECRET_ACCESS_KEY "<AWS_SECRET_ACCESS_KEY>"
setx AWS_DEFAULT_REGION "<AWS_DEFAULT_REGION>"
setx MONGO_DB_URL "<your_mongo_db_connection_string>"
```

5. Load data into MongoDB:

```bash
python scripts/load_mongodb_data.py
```

6. Run the FastAPI app:

```bash
python app.py
```

7. Access the app:

- Training endpoint: `http://localhost:5000/train`
- Frontend: `http://localhost:5000/`

## Docker (optional)

Build and run the container locally:

```bash
docker build --build-arg AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> --build-arg AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> --build-arg AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION> --build-arg MONGODB_URL=<MONGODB_URL> .

docker run -d -p 5000:5000 <IMAGE_NAME>
```

## Alternative AWS scope

A production-ready AWS alternative architecture could include:

- **API Gateway + AWS Lambda** for serverless prediction endpoints
- **Amazon SageMaker** for training and model hosting
- **Amazon DynamoDB** for metadata and feature-store indexing
- **Amazon S3** for dataset, artifacts, and model versions
- **AWS Step Functions** for orchestrating training, evaluation, and deployment workflows
- **CodePipeline / CodeBuild** for CI/CD

This alternative would shift the app from a single `FastAPI` service to a managed serverless / MLOps workflow while preserving the same data and model logic.

## Future scope

- Add end-to-end CI/CD with tests, linting, and deployment automation
- Implement model monitoring and drift detection
- Add more classification algorithms and ensemble stacking
- Build a REST API contract with OpenAPI and versioned model endpoints
- Support batch scoring and real-time scoring separately
- Add user authentication and access control for predictions
- Expand the feature store and include more customer behavior signals
- Move from CSV artifact storage to a managed feature store service

## Folder structure summary

- `app.py` — FastAPI entry point
- `scripts/` — utility scripts for data loading and setup
- `src/components/` — pipeline components for ingestion, transformation, training, evaluation, pushing
- `src/configuration/` — AWS and MongoDB connection configuration
- `src/cloud_storage/` — S3 storage helper classes
- `src/pipeline/` — pipeline orchestration for training and prediction
- `src/entity/` — configuration and artifact schema classes
- `src/constant/` — constants for app, AWS, MongoDB, training, and prediction
- `notebooks/` — EDA, clustering, and classification exploration notebooks

## Notes

- The model pipeline is designed to use MongoDB as the raw data backend and AWS S3 as the model artifact store.
- The FastAPI backend accepts form-based customer input and returns predicted customer cluster labels.
- The repository supports both local experimentation and a scalable AWS-backed artifact workflow.


