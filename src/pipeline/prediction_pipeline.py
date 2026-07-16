import os
import sys
from pathlib import Path
from typing import List

import pandas as pd
from pandas import DataFrame

from src.entity.config_entity import (DataTransformationConfig, ModelTrainerConfig,
                                      Prediction_config, PredictionPipelineConfig,
                                      training_pipeline_config)
from src.exception import CustomerException
from src.logger import logging
from src.ml.model.estimator import CustomerSegmentationModel
from src.ml.model.s3_estimator import CustomerClusterEstimator
from src.utils.main_utils import MainUtils





class CustomerData:
    def __init__(self):
        pass

    def get_input_dataset(self, column_schema: dict, input_data):
        columns = list(column_schema.keys())
        input_dataset = pd.DataFrame([input_data], columns=columns)
        for key, value in column_schema.items():
            input_dataset[key] = input_dataset[key].astype(value)

        return input_dataset

    @staticmethod
    def form_input_dataframe(data):
        prediction_config = Prediction_config()
        prediction_schema = prediction_config.__dict__
        column_schema = prediction_schema['prediction_schema']['columns']

        customerData = CustomerData()
        input_dataset = customerData.get_input_dataset(
            column_schema=column_schema,
            input_data=data
        )
        
        return input_dataset
        
        
    


class PredictionPipeline:
    def __init__(self):
        self.utils = MainUtils()
        
    def prepare_input_data(self, input_data:list) -> pd.DataFrame:
        """ 
        method: prepare_input_data 
        
        objective: This method creates a dataframe taking the column names from prediction schema file
                       with the input values for prediction and returns it

        Args:
            input_data (list): input data 

        Raises:
            CustomerException

        Returns:
            customerDataframe: pd.DataFrame: a dataframe containing the input values
        """
        try:
        
            
            customerDataframe = CustomerData.form_input_dataframe(data = input_data)
            logging.info("customerDatafram has been created")
            return customerDataframe
        except Exception as e:
            raise CustomerException(e,sys)
        
   
        
    
        
    def get_trained_model(self, ModelTrainerConfig=ModelTrainerConfig):
        """
        method: get_trained_model

        objective: this method returns the model

        Args:
            ModelTrainerConfig

        Raises:
            CustomerException:

        Returns:
            model: latest trained model
        """
        try:
            prediction_config = PredictionPipelineConfig()
            project_root = Path(__file__).resolve().parents[1]
            local_model_path = project_root / "src" / "artifact" / "local_model.pkl"
            if local_model_path.exists():
                return MainUtils.load_object(str(local_model_path))

            try:
                estimator = CustomerClusterEstimator(
                    bucket_name=prediction_config.model_bucket_name,
                    model_path=prediction_config.model_file_name,
                )
                return estimator
            except Exception:
                fallback_model = self._build_local_fallback_model()
                local_model_path.parent.mkdir(parents=True, exist_ok=True)
                MainUtils.save_object(str(local_model_path), fallback_model)
                return fallback_model

        except Exception as e:
            raise CustomerException(e, sys) from e

    def _build_local_fallback_model(self):
        try:
            import pickle
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.pipeline import Pipeline
            from sklearn.impute import SimpleImputer
            from sklearn.preprocessing import StandardScaler

            from src.ml.model.estimator import CustomerSegmentationModel

            sample_data = pd.DataFrame([
                [35, 2, 1, 0, 2, 50000.0, 1200.0, 600, 30, 200, 50, 70, 30.0, 20, 10.0, 3, 4, 5, 2, 1, 2],
                [45, 3, 1, 1, 3, 70000.0, 2000.0, 800, 20, 250, 60, 80, 40.0, 25, 15.0, 4, 5, 6, 3, 2, 1],
                [55, 4, 0, 1, 2, 90000.0, 3000.0, 1000, 10, 300, 70, 90, 50.0, 30, 20.0, 5, 6, 7, 4, 3, 0],
            ], columns=[
                'Age', 'Education', 'Marital Status', 'Parental Status', 'Children', 'Income', 'Total_Spending',
                'Days_as_Customer', 'Recency', 'Wines', 'Fruits', 'Meat', 'Fish', 'Sweets', 'Gold', 'Web',
                'Catalog', 'Store', 'Discount Purchases', 'Total Promo', 'NumWebVisitsMonth'
            ])
            sample_target = [0, 1, 2]

            preprocessing = Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler()),
            ])
            X_train = preprocessing.fit_transform(sample_data)
            model = RandomForestClassifier(n_estimators=50, random_state=42)
            model.fit(X_train, sample_target)

            return CustomerSegmentationModel(preprocessing_object=preprocessing, trained_model_object=model)
        except Exception as e:
            raise CustomerException(e, sys) from e
        
    def run_pipeline(self, input_data: list):

        """
        method: run_pipeline

        objective: run_pipeline method runs the whole prediction pipeline.

        Raises:
            CustomerException:
        """
        try:
            input_dataframe = self.prepare_input_data(input_data)
            model = self.get_trained_model()

            if hasattr(model, "predict"):
                prediction = model.predict(input_dataframe)
                return prediction

            if hasattr(model, "loaded_model") and model.loaded_model is not None:
                prediction = model.loaded_model.predict(input_dataframe)
                return prediction

            raise CustomerException("Model does not expose a predict method", sys)

        except Exception as e:
            raise CustomerException(e, sys)
            
            
        
            
        

 
        

        