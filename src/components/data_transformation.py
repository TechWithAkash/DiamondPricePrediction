from sklearn.impute import SimpleImputer  # Handling Missing values
from sklearn.preprocessing import StandardScaler  # Handling Feature Scaling
from sklearn.preprocessing import OrdinalEncoder  # Ordinal Encoding

##Pipelines
from sklearn.pipeline import Pipeline  # helps to Create a Pipeline
from sklearn.compose import ColumnTransformer  # Helps to combine the multiple pipeline
import numpy as np
import pandas as pd
import sys, os
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

# Data Transformation Configuration


@dataclass
class DataTransformationconfig:
    preprocessor_ob_file_path = os.path.join("artifacts", "preprocessor.pkl")


# Data IngestionConfig Class


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformation()

    def get_data_transformation_object(self):
        try:
            logging.info(" Data transformation Initiated.....")
            # Defining which columns should be ordinal-encoded and which should be scaled
            categorical_cols = ["cut", "color", "clarity"]
            numeric_cols = ["carat", "depth", "table", "x", "y", "z"]

            # Defining the custom Ranking of each Ordinal-encoded Variable
            cut_categories = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
            color_categories = ["D", "E", "F", "G", "H", "I", "J"]
            clarity_categories = [
                "I1",
                "SI2",
                "SI1",
                "VS2",
                "VS1",
                "VVS2",
                "VVS1",
                "IF",
            ]

            logging.info("Pipeline Initiated.....")

            # Numerical Pipeline
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            # Categorical Pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    (
                        "ordinal_encoder",
                        OrdinalEncoder(
                            categories=[
                                cut_categories,
                                color_categories,
                                clarity_categories,
                            ]
                        ),
                    ),
                ]
            )

            # Column Transformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numeric_cols),
                    ("cat_pipeline", cat_pipeline, categorical_cols),
                ]
            )

            return preprocessor
            logging.info("Pipeline Completed........")

        except Exception as e:
            logging.error("Data Transformation Initiation Failed.....")
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:

            # Reading Train and Test Data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading of training and test data Completed")
            logging.info(f"Train DataFrame Head : \n{train_df.head().to_string}")
            logging.info(f"Test DataFrame Head : \n{test_df.head().to_string}")
            logging.info("Obtaining the Preprocessing Object of Feature Scaling")

            preprocessing_obj = self.get_data_transformation_object()

            # Seggregating the Independent and Dependent Features

            target_column_name = "price"
            drop_columns = [target_column_name, "id"]

            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=drop_columns, axis=1)
            target_feature_test_df = test_df[target_column_name]

            # Applying the Transformmation

            input_feature_train_arr = preprocessing_obj.fit_transform(
                input_feature_train_df
            )
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info(
                " Applying Preprocessing object to training and testing datasets"
            )

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj,
            )

            logging.info(
                "Preprocessor Pickle is Created and Saved to the artifacts directory successfully...."
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            logging.error("Data Transformation Failed.....")
            raise CustomException(e, sys)
