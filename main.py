# from fastapi import FastAPI, Response, Request
# import pandas as pd
# import seaborn as sns
# import joblib
# import io
# from matplotlib import pyplot as plt


# app = FastAPI()

# pipe = joblib.load("pipeline.joblib")

# class Model:
#     def __init__(self, df):
#         self.df = df

#     def apply_pipeline(self):
#         transformed_data = pipe[:-1].transform(self.df)
#         columns = pipe[:-1].get_feature_names_out()
#         return pd.DataFrame(transformed_data, columns=columns)

#     def generate_kde_plot(self, df):
#         kde = sns.kdeplot(df)
#         fig = kde.get_figure()
#         return fig


# @app.get("/before-pipeline")
# async def iris_before(request : Request):
#     body = await request.json()
#     data_set = body["dataset_name"]
#     df = sns.load_dataset(data_set)
#     obj = Model(df)
#     fig = obj.generate_kde_plot(df)
#     img_buf = io.BytesIO()
#     fig.savefig(img_buf, format="png")
#     plt.close(fig)

#     return Response(img_buf.getvalue(), media_type="image/png")


# @app.get("/after-pipeline")
# async def iris_after(request: Request):
#     body = await request.json()
#     datset = body["dataset_name"]
#     df = sns.load_dataset(datset)
#     obj = Model(df)
#     transformed_df = obj.apply_pipeline()
#     fig = obj.generate_kde_plot(transformed_df)
#     img_buf = io.BytesIO()
#     fig.savefig(img_buf, format="png")
#     plt.close(fig)

#     return Response(img_buf.getvalue(), media_type="image/png")



from fastapi import FastAPI, Response, Request, HTTPException
import pandas as pd
import seaborn as sns
import joblib
import io
from matplotlib import pyplot as plt

app = FastAPI()

# Load the pipeline
pipe = joblib.load("pipeline.joblib")

class Model:
    def __init__(self, df):
        self.df = df

    def apply_pipeline(self):
        """Apply the pipeline transformation (excluding the final estimator)."""
        transformed_data = pipe[:-1].transform(self.df)
        columns = pipe[:-1].get_feature_names_out()
        return pd.DataFrame(transformed_data, columns=columns)

    def generate_kde_plot(self, df):
        """Generate a KDE plot for the given DataFrame."""
        kde = sns.kdeplot(df)
        fig = kde.get_figure()
        return fig


@app.get("/before-pipeline")
async def iris_before(request: Request):
    """Get the KDE plot before applying the pipeline."""
    try:
        body = await request.json()
        print(request)
        dataset_name = body["dataset_name"]
        df = sns.load_dataset(dataset_name)
        obj = Model(df)
        fig = obj.generate_kde_plot(df)
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format="png")
        plt.close(fig)
        
        return Response(img_buf.getvalue(), media_type="image/png")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/after-pipeline")
async def iris_after(request: Request):
    try:
        body = await request.json()
        dataset_name = body["dataset_name"]
        df = sns.load_dataset(dataset_name)
        obj = Model(df)
        transformed_df = obj.apply_pipeline()
        
        fig = obj.generate_kde_plot(transformed_df)
        
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format="png")
        plt.close(fig)
        
        return Response(img_buf.getvalue(), media_type="image/png")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

