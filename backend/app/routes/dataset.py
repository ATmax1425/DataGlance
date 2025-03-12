from fastapi import APIRouter, HTTPException
from sklearn import datasets
import pandas as pd

router = APIRouter()

dataset_map = {
    "iris": datasets.load_iris,
    "wine": datasets.load_wine,
    "diabetes": datasets.load_diabetes,
    "breast_cancer": datasets.load_breast_cancer
}

chart_requirements = {
    "scatter": ["x_value", "y_value", "hue", "size"],
    "line": ["x_value", "y_value", "hue"],
    "histogram": ["x_value", "bins"],
    "kde": ["x_value", "fill"],
    "ecd": ["x_value", "stat"],
    "bar": ["x_value", "y_value", "hue"],
    "countplot": ["x_value", "hue"]
}


def load_dataset(name):
    global dataset_map
    return dataset_map[name]() if name in dataset_map else None


@router.get("/")
def get_available_datasets():
    available_datasets = {
        "available_datasets": list(dataset_map.keys()),
        "available_charts": list(chart_requirements.keys())
        }
    return available_datasets


@router.get("/{dataset_name}")
def get_dataset(dataset_name: str):
    if dataset_name not in dataset_map:
        return {"error": "Dataset not found"}

    data = load_dataset(dataset_name)
    df = pd.DataFrame(data.data, columns=data.feature_names)
    return df.to_dict(orient="records")


@router.get("/{dataset_name}/columns")
def get_dataset_columns(dataset_name: str):
    if dataset_name not in dataset_map:
        return {"error": "Dataset not found"}

    data = load_dataset(dataset_name)
    df = pd.DataFrame(data.data, columns=data.feature_names)

    return {
        "columns": list(df.columns),
    }


@router.post("/get-chart-requirements")
def get_chart_requirements(request_data: dict):
    dataset_name = request_data.get("dataset")
    chart_type = request_data.get("chart")

    if dataset_name not in dataset_map:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if chart_type not in chart_requirements:
        raise HTTPException(status_code=400, detail="Invalid chart type")

    # Load dataset
    data = load_dataset(dataset_name)
    df = pd.DataFrame(data.data, columns=data.feature_names)

    # Classify columns as numerical or categorical
    numerical_columns = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = df.select_dtypes(exclude=["number"]).columns.tolist()

    return {
        "required_keys": chart_requirements[chart_type],
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns
    }