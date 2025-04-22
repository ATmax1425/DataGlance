import seaborn as sns
import pandas as pd

databases = [
    {
        "index": 1,
        "name": "Tips",
        "database": sns.load_dataset("tips")
    },
    {
        "index": 2,
        "name": "Titanic",
        "database": sns.load_dataset("titanic")
    },
    {
        "index": 3,
        "name": "Flights",
        "database": sns.load_dataset("flights")
    },
    {
        "index": 4,
        "name": "Planets",
        "database": sns.load_dataset("planets")
    },
    {
        "index": 5,
        "name": "Diamonds",
        "database": sns.load_dataset("diamonds")
    },
    {
        "index": 6,
        "name": "Car_crashes",
        "database": sns.load_dataset("car_crashes")
    },
]

for i, database in enumerate(databases):
    dataset = database["database"]
    numeric_columns = dataset.select_dtypes(include=["number"]).columns.tolist()
    databases[i]["numerical_columns"] = numeric_columns
    dataset[numeric_columns] = dataset[numeric_columns].fillna(dataset[numeric_columns].median())
    
    categorical_columns = dataset.select_dtypes(include=["object", "category"]).columns.tolist()
    databases[i]["categorical_columns"] = categorical_columns
    for col in categorical_columns:
        mode_val = dataset[col].mode()
        if not mode_val.empty:
            dataset.loc[:, col] = dataset[col].fillna(mode_val[0])


def get_databases_name():
    return [{"index": i["index"], "name": i["name"]} for i in databases]


def get_database(database_index):
    for database_doc in databases:
        if database_doc["index"] == database_index:
            return database_doc["database"]
    return None

def get_database_cols(database_index):
    for database_doc in databases:
        if database_doc["index"] == database_index:
            return {
                "columns": database_doc["database"].columns.tolist(),
                "numerical_columns": numeric_columns,
                "categorical_columns": categorical_columns
            }
    return None

# print(get_database_cols(1))