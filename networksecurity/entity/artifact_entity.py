from dataclasses import dataclass


# 1. Data Ingestion Artifacts:
@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str



# 2. Data Validation Artifacts:
@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
    

# 3. Data Transformation Artifacts:
@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str


# 4. Model Trainer Artifacts:
@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    test_metric_artifact: ClassificationMetricArtifact