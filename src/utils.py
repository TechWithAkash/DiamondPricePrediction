import os,sys,pickle
import numpy as np
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from sklearn.metrics import r2_score,mean_absolute_error
def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)
    except Exception as e:

        logging.info("Error occurred while saving object to file")
        raise CustomException(e, sys)
    
def evaluate_model(X_train, y_train,X_test, y_test,models):
    try:
        logging.info("Evaluating model Started")
        report={}
        for i in range(len(models)):
            model = list(models.values())[i]
            #Train Model
            model.fit(X_train, y_train)


            #Predict Testing Data
            y_test_pred = model.predict(X_test)

            #Get R2 Score for the Train and Test Data
            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score
    
    except Exception as e:
        logging.info("Error occurred while evaluating model Training")
        raise CustomException(e, sys)