from fastapi import APIRouter, HTTPException
import pandas as pd
from io import BytesIO
import base64
from sklearn import datasets

router = APIRouter()

def get_dataset(dataset_name):
    dataset_map = {
        "iris": datasets.load_iris(),
        "wine": datasets.load_wine(),
        "diabetes": datasets.load_diabetes(),
        "breast_cancer": datasets.load_breast_cancer()
    }

    if dataset_name not in dataset_map:
        return False

    data = dataset_map[dataset_name]
    df = pd.DataFrame(data.data, columns=data.feature_names)
    return df

# @router.get("/{dataset_name}/{chart_type}")
# def generate_visualization(dataset_name: str, chart_type: str):

#     if chart_type == "hist":
#         df.hist()
#     elif chart_type == "correlation":
#         sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
#     else:
#         raise HTTPException(status_code=400, detail="Invalid chart type")

#     # Convert plot to base64
#     img = BytesIO()
#     plt.savefig(img, format="png")
#     img.seek(0)
#     encoded_img = base64.b64encode(img.getvalue()).decode()

#     return {"image": encoded_img}
