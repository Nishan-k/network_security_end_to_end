from networksecurity.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
import os
import mlflow
import joblib
import sys
import dagshub
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier)
from networksecurity.utils.main_utils.utils import (load_object, evaluate_models, 
                                                    save_obj_to_pkl, load_numpy_arr_data, read_yaml_file)
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel



load_dotenv()

dagshub_token = os.getenv("DAGSHUB_TOKEN")

# MLflow Setup:
if dagshub_token:
    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token
    mlflow.set_tracking_uri(f"https://{dagshub_token}@dagshub.com/Nishan-k/network_security_end_to_end.mlflow")


# Initializing DagsHub:
try:
    dagshub.init(repo_owner="Nishan-k", repo_name="network_security_end_to_end", mlflow=True)
except Exception as e:
    print(f"Warning !!! couldn't initialize Dagshub:{e}")




class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    def track_mlflow(self, best_model, classification_metric):
        try:
            with mlflow.start_run():
                f1_score = classification_metric.f1_score
                precision_score = classification_metric.precision_score
                recall_score = classification_metric.recall_score


                mlflow.log_metrics({
                    "f1_score": f1_score,
                    "precision_score": precision_score,
                    "recall_score": recall_score
                })
                model_path = "model.pkl"
                joblib.dump(best_model, model_path)
                mlflow.log_artifact(model_path)
        except Exception as e:
            print(f"Warning !!, could not log to MLFlow: {e}")
            raise NetworkSecurityException(e, sys)
    
    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "Decision_Tree": DecisionTreeClassifier(),
            "Random_Forest": RandomForestClassifier(verbose=1),
            "Gradient_Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic_Regression": LogisticRegression(verbose=1),
            "Ada_Boost": AdaBoostClassifier()
        }

        params = read_yaml_file("parameters/params.yaml")
        model_report: dict = evaluate_models(X_train=X_train, y_train=y_train, 
                                             X_test=X_test, y_test=y_test, models=models, params=params['model_params'])
        


        # Get the best model out of all:
        best_model_score = max(sorted(model_report.values()))
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model = models[best_model_name]

        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        network_model = NetworkModel(preprocessor=preprocessor, model=best_model)

        y_pred = network_model.predict(X_test)
        classification_report_test = get_classification_score(y_true=y_test, y_pred=y_pred)
        self.track_mlflow(best_model, classification_report_test)

        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

       
        save_obj_to_pkl(self.model_trainer_config.trained_model_file_path, obj=network_model)
        save_obj_to_pkl("final_model/model.pkl", network_model)


         # Model Trainer Artifact:
        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             test_metric_artifact=classification_report_test
                             )

        return model_trainer_artifact
    

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # Load the data as array:
            train_array = load_numpy_arr_data(train_file_path)
            test_array = load_numpy_arr_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            model_trainer_artifact = self.train_model(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
            print(model_trainer_artifact)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


                               
