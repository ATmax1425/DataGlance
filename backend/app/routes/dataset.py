from fastapi import APIRouter, HTTPException
from scipy.stats import linregress
import pandas as pd
import numpy as np
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

dataset_map = {
    "tips": sns.load_dataset("tips"),
    "titanic": sns.load_dataset("titanic"),
    "flights": sns.load_dataset("flights"),
    "planets": sns.load_dataset("planets"),
    "diamonds": sns.load_dataset("diamonds"),
    "car_crashes": sns.load_dataset("car_crashes"),
}

# Filling NaN values
for dataset_name, dataset in dataset_map.items():
    numeric_columns = dataset.select_dtypes(include=["number"]).columns
    dataset[numeric_columns] = dataset[numeric_columns].fillna(dataset[numeric_columns].median())
    
    categorical_columns = dataset.select_dtypes(include=["object", "category"]).columns
    for col in categorical_columns:
        dataset[col].fillna(dataset[col].mode()[0], inplace=True)
    
    dataset_map[dataset_name] = dataset

chart_requirements = {
    "scatter": {
        "required": ["x_value", "y_value"],
        "optional": ["hue", "size"],
        "data_types": {
            "x_value": ["numerical", "categorical"],
            "y_value": ["numerical"],
            "hue": ["categorical"],
            "size": ["numerical"]
        }
    },
    "line": {
        "required": ["x_value", "y_value"],
        "optional": ["hue"],
        "data_types": {
            "x_value": ["numerical", "categorical"],
            "y_value": ["numerical"],
            "hue": ["categorical"]
        }
    },
    "histogram": {
        "required": ["x_value"],
        "optional": ["bins", "hue"],
        "data_types": {
            "x_value": ["numerical"],
            "hue": ["categorical"],
            "bins": []
        }
    },
    "bar": {
        "required": ["x_value", "y_value"],
        "optional": ["hue"],
        "data_types": {
            "x_value": ["numerical"],
            "y_value": ["categorical"],
            "hue": ["categorical"]
        }
    },
    "countplot": {
        "required": ["x_value"],
        "optional": ["hue"],
        "data_types": {
            "x_value": ["categorical"],
            "hue": ["categorical"]
        }
    },
    # "boxplot": {
    #     "required": ["x_value", "y_value"],
    #     "optional": ["hue"],
    #     "data_types": {
    #         "x_value": ["categorical"],
    #         "y_value": ["numerical"],
    #         "hue": ["categorical"]
    #     }
    # },p
    "heatmap": {
        "required": ["x_value", "y_value"],
        "optional": ["agg_func", "hue"],
        "custom_options": {
            "agg_func": {
                "options": ["mean", "sum", "count", "min", "max", "median"],
            }
        },
        "data_types": {
            "x_value": ["categorical"],
            "y_value": ["categorical"],
            "hue": ["categorical"]
        }
    },
    "pie": {
        "required": ["x_value", "y_value"],
        "data_types": {
            "x_value": ["categorical"],
            "y_value": ["numerical"]
        }
    },
    "donut": {
        "required": ["x_value", "y_value"],
        "data_types": {
            "x_value": ["categorical"],
            "y_value": ["numerical"]
        }
    },
    "area": {
        "required": ["x_value", "y_value"],
        "optional": ["hue"],
        "data_types": {
            "x_value": ["numerical", "categorical"],
            "y_value": ["numerical"],
            "hue": ["categorical"]
        }
    },
    "bubble": {
        "required": ["x_value", "y_value", "size"],
        "optional": ["hue"],
        "data_types": {
            "x_value": ["numerical", "categorical"],
            "y_value": ["numerical"],
            "size": ["numerical"],
            "hue": ["categorical"]
        }
    },
    "regplot": {
        "required": ["x_value", "y_value"],
        "data_types": {
            "x_value": ["numerical"],
            "y_value": ["numerical"]
        }
    }
}

chart_conversion_map = {
    "histogram": "bar",
    "countplot": "bar",
    "boxplot": "scatter",
    "heatmap": "bar",
    "regplot": "scatter",
    "area": "line",
    "violin": "scatter",
}

# def load_dataset(name):
#     global dataset_map
#     return dataset_map[name]() if name in dataset_map else None


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

    df = dataset_map[dataset_name]
    return df.to_dict(orient="records")


@router.get("/{dataset_name}/columns")
def get_dataset_columns(dataset_name: str):
    if dataset_name not in dataset_map:
        return {"error": "Dataset not found"}
    df = dataset_map[dataset_name]
    numerical_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    categorical_columns = [col for col in df.columns if pd.api.types.is_categorical_dtype(df[col]) or pd.api.types.is_object_dtype(df[col])]
    return {
        "columns": list(df.columns),
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns
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
    df = dataset_map[dataset_name]

    # Classify columns as numerical or categorical
    columns = df.columns.tolist()
    numerical_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    categorical_columns = [col for col in df.columns if pd.api.types.is_categorical_dtype(df[col]) or pd.api.types.is_object_dtype(df[col])]

    logger.info({
        "required_keys": chart_requirements[chart_type],
        "columns": columns,
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns
    })
    return {
        "required_keys": chart_requirements[chart_type],
        "columns": columns,
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns
    }


@router.post("/generate-chart-data")
def generate_chart_data(request_data: dict):
    logger.info(f"request_data: {request_data}")
    dataset_name = request_data.get("dataset")
    chart_type = request_data.get("chart")

    if dataset_name not in dataset_map:
        error_mes = "Dataset not found"
        logger.error(error_mes)
        raise HTTPException(status_code=404, detail=error_mes)

    if chart_type not in chart_requirements:
        error_mes = "Chart type not supported"
        logger.error(error_mes)
        raise HTTPException(status_code=400, detail=error_mes)
    
    if not request_data.get("fields"):
        error_mes = "fields not found"
        logger.error(error_mes)
        raise HTTPException(status_code=400, detail=error_mes)

    required_params = chart_requirements[chart_type]["required"]
    for param in required_params:
        if param not in request_data.get("fields"):
            error_mes = f"Missing required parameter: {param}"
            logger.error(error_mes)
            raise HTTPException(status_code=400, detail=error_mes)

    x_value = request_data["fields"].get("x_value")
    y_value = request_data["fields"].get("y_value", None)
    hue = request_data["fields"].get("hue", None)
    size = request_data["fields"].get("size", None)
    bins = request_data["fields"].get("bins", 10)
    agg_func = request_data["fields"].get("agg_func", "mean")

    df = dataset_map[dataset_name]

    for col in [x_value, y_value, hue, size]:
        if col and col not in df.columns:
            error_mes = f"Invalid column selected: {col}"
            logger.error(error_mes)
            raise HTTPException(status_code=400, detail=error_mes)

    chartjs_data = {"labels": df[x_value].astype(str).tolist()}

    if chart_type == "scatter":
        chartjs_data = {
            "labels": df[x_value].tolist(),
            "datasets": [{
                "label": y_value,
                "data": [{"x": x, "y": y} for x, y in zip(df[x_value], df[y_value])],
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)"
            }]
        }

    elif chart_type == "line":
        df.sort_values(x_value, inplace=True)
        # df["x_value_round"] = (df[x_value] * 2).round() / 2
        # filtered_df = df.groupby("x_value_round")[x_value].agg([list, "mean"]).reset_index()
        chartjs_data = {
            "labels": df[x_value].tolist(),
            "datasets": [{
                "label": y_value,
                "data": df[y_value].tolist(),
                "borderColor": "rgba(75, 192, 192, 1)",
                "fill": False
            }]
        }

    elif chart_type == "histogram":
        counts, bin_edges = np.histogram(df[x_value], bins=bins)
        bin_labels = [f"{bin_edges[i]}-{bin_edges[i+1]}" for i in range(len(bin_edges) - 1)]
        chartjs_data = {
            "labels": bin_labels,
            "datasets": [{
                "label": x_value,
                "data": counts.tolist(),
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)"
            }]
        }

    elif chart_type == "bar":
        chartjs_data = {
            "labels": df[x_value].tolist(),
            "datasets": [{
                "label": y_value,
                "data": df[y_value].tolist(),
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)"
            }]
        }

    elif chart_type == "countplot":
        counts = df[x_value].value_counts().sort_index()
        chartjs_data = {
            "labels": counts.index.tolist(),
            "datasets": [{
                "label": x_value,
                "data": counts.tolist(),
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)"
            }]
        }

    elif chart_type == "boxplot":
        def calculate_boxplot_stats(data):
            q1 = np.percentile(data, 25)
            median = np.percentile(data, 50)
            q3 = np.percentile(data, 75)
            iqr = q3 - q1
            lower_whisker = max(min(data), q1 - 1.5 * iqr)
            upper_whisker = min(max(data), q3 + 1.5 * iqr)
            return {
                "min": lower_whisker,
                "q1": q1,
                "median": median,
                "q3": q3,
                "max": upper_whisker
            }

        boxplot_stats = calculate_boxplot_stats(df[y_value])
        chartjs_data = {
            "labels": [x_value],
            "datasets": [{
                "label": y_value,
                "data": [boxplot_stats],
                "borderColor": "rgba(75, 192, 192, 1)",
                "backgroundColor": "rgba(75, 192, 192, 0.5)"
            }]
        }

    elif chart_type == "heatmap":
        heatmap_data = df.pivot_table(index=x_value, columns=y_value, aggfunc=agg_func, fill_value=0)
        chartjs_data = {
            "labels": heatmap_data.columns.tolist(),
            "datasets": [{
                "label": f"{x_value} vs {y_value}",
                "data": heatmap_data.values.tolist(),
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)"
            }]
        }

    elif chart_type == "pie":
        chartjs_data = {
            "labels": df[x_value].tolist(),
            "datasets": [{
                "label": y_value,
                "data": df[y_value].tolist(),
                "backgroundColor": [
                    "rgba(75, 192, 192, 0.5)",
                    "rgba(255, 99, 132, 0.5)",
                    "rgba(54, 162, 235, 0.5)"
                ]
            }]
        }

    elif chart_type == "donut":
        chartjs_data = {
            "labels": df[x_value].tolist(),
            "datasets": [{
                "label": y_value,
                "data": df[y_value].tolist(),
                "backgroundColor": [
                    "rgba(75, 192, 192, 0.5)",
                    "rgba(255, 99, 132, 0.5)",
                    "rgba(54, 162, 235, 0.5)"
                ]
            }]
        }

    elif chart_type == "area":
        area_data = df.groupby(x_value)[y_value].sum().reset_index()
        chartjs_data = {
            "labels": area_data[x_value].tolist(),
            "datasets": [{
                "label": y_value,
                "data": area_data[y_value].tolist(),
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "fill": True
            }]
        }

    elif chart_type == "bubble":
        chartjs_data = {
            "labels": df[x_value].tolist(),
            "datasets": [{
                "label": y_value,
                "data": [{"x": x, "y": y, "r": s} for x, y, s in zip(df[x_value], df[y_value], df[size])],
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)"
            }]
        }

    elif chart_type == "regplot":
        slope, intercept, r_value, p_value, std_err = linregress(df[x_value], df[y_value])
        regression_line = slope * df[x_value] + intercept
        chartjs_data = {
            "labels": df[x_value].tolist(),
            "datasets": [
                {
                    "label": "Data",
                    "data": df[y_value].tolist(),
                    "type": "scatter",
                    "backgroundColor": "rgba(75, 192, 192, 0.5)",
                    "borderColor": "rgba(75, 192, 192, 1)"
                },
                {
                    "label": "Regression Line",
                    "data": regression_line.tolist(),
                    "type": "line",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "fill": False
                }
            ]
        }

    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    chart_type = chart_conversion_map.get(chart_type, chart_type)

    response_data = {
        "chartType": chart_type,
        "chartData": chartjs_data,
    }

    return response_data
