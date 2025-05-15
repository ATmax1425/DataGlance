plot_types = {
    1: "Relational plots",
    2: "Distribution plots",
    3: "Categorical plots"
}

chart_requirements = [
    {
        "index": 1,
        "name": "Scatter Chart",
        "chartjs_type": "scatter",
        "plot_type": 1,
        "required": ["x_value", "y_value"],
        "optional": ["hue", "size"],
        "data_types": {
            "x_value": ["numerical", "categorical"],
            "y_value": ["numerical"],
            "hue": ["categorical"],
            "size": ["numerical"]
        }
    },{
        "index": 2,
        "name": "Line Chart",
        "chartjs_type": "line",
        "plot_type": 1,
        "required": ["x_value", "y_value"],
        "optional": ["hue"],
        "data_types": {
            "x_value": ["numerical", "categorical"],
            "y_value": ["numerical"],
            "hue": ["categorical"]
        }
    },{
        "index": 3,
        "name": "Histogram Chart",
        "chartjs_type": "bar",
        "plot_type": 2,
        "required": ["x_value"],
        "optional": ["bins", "hue"],
        "data_types": {
            "x_value": ["numerical"],
            "hue": ["categorical"],
            "bins": []
        }
    },{
        "index": 4,
        "name": "Bar Chart",
        "chartjs_type": "bar",
        "plot_type": 3,
        "required": ["x_value", "y_value"],
        "optional": ["hue"],
        "data_types": {
            "x_value": ["numerical"],
            "y_value": ["categorical"],
            "hue": ["categorical"]
        }
    },{
        "index": 5,
        "name": "count Chart",
        "chartjs_type": "bar",
        "plot_type": 3,
        "required": ["x_value"],
        "optional": ["hue"],
        "data_types": {
            "x_value": ["categorical"],
            "hue": ["categorical"]
        }
    },{
        "index": 6,
        "name": "Pie Chart",
        "chartjs_type": "pie",
        "plot_type": 3,
        "required": ["x_value", "y_value"],
        "data_types": {
            "x_value": ["categorical"],
            "y_value": ["numerical"]
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
    # "heatmap": {
    #     "required": ["x_value", "y_value"],
    #     "optional": ["agg_func", "hue"],
    #     "custom_options": {
    #         "agg_func": {
    #             "options": ["mean", "sum", "count", "min", "max", "median"],
    #         }
    #     },
    #     "data_types": {
    #         "x_value": ["categorical"],
    #         "y_value": ["categorical"],
    #         "hue": ["categorical"]
    #     }
    # },
    # "donut": {
    #     "required": ["x_value", "y_value"],
    #     "data_types": {
    #         "x_value": ["categorical"],
    #         "y_value": ["numerical"]
    #     }
    # },
    # "area": {
    #     "required": ["x_value", "y_value"],
    #     "optional": ["hue"],
    #     "data_types": {
    #         "x_value": ["numerical", "categorical"],
    #         "y_value": ["numerical"],
    #         "hue": ["categorical"]
    #     }
    # },
    # "bubble": {
    #     "required": ["x_value", "y_value", "size"],
    #     "optional": ["hue"],
    #     "data_types": {
    #         "x_value": ["numerical", "categorical"],
    #         "y_value": ["numerical"],
    #         "size": ["numerical"],
    #         "hue": ["categorical"]
    #     }
    # },
    # "regplot": {

    #     "required": ["x_value", "y_value"],
    #     "data_types": {
    #         "x_value": ["numerical"],
    #         "y_value": ["numerical"]
    #     }
    # }
]

def get_charts_name_type():
    charts_info = []
    for i in chart_requirements:
        charts_info.append({
            "index": i["index"],
            "name": i["name"], 
            "plot_type": plot_types[i["plot_type"]]
            })
    return charts_info


def get_chart_req(chart_index):
    for chart_doc in chart_requirements:
        if chart_doc["index"] == chart_index:
            return chart_doc
    return None
