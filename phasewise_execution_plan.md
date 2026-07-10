# Phase-wise execution plan for Customer Categorizer

## Phase 1: Confirm the MongoDB target
- The backend connects to MongoDB Atlas successfully.
- The app is configured to read from database `ineuron` and collection `customer_segmentation`.
- Current verification shows that database `ineuron` exists but has no collections yet.

## Phase 2: Load the dataset into MongoDB
- Import the customer dataset into the `customer_segmentation` collection inside database `ineuron`.
- Ensure each document contains the expected feature columns used by the project.
- If needed, create the collection first and insert documents.

## Phase 3: Run the ingestion pipeline
- Start the backend.
- Trigger the training route to run the data ingestion step.
- Confirm that the app reads documents from MongoDB and saves feature-store CSV files.

## Phase 4: Train and evaluate the model
- Run the training pipeline.
- Validate that the model training and evaluation complete without database-related errors.

## Phase 5: Test prediction
- Use the prediction endpoint or web UI.
- Confirm that the backend can read the trained model and generate a cluster prediction.
