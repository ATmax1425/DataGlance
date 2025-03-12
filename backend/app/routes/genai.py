from fastapi import APIRouter, HTTPException
from sklearn import datasets

from visualization import get_dataset

router = APIRouter()

@router.get("/{dataset_name}/{chart_type}")
def generate_visualization(dataset_name: str, chart_type: str):
    df = get_dataset(dataset_name)

    if not df:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
