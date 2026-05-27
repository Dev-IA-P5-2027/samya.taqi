import mlflow
import mlflow.sklearn
import pandas as pd 

RUN_ID='000e0e3a42bd43659464b8df1d0989cb'

model= mlflow.sklearn.load_model(f'runs:/{RUN_ID}/model')

appartement = pd.DataFrame([{ 
    'surface': 75, 
    'chambres': 3, 
    'distance_centre': 5.2, 
    'annee_construction': 2005 
}])

prix_predict=model.predict(appartement)[0]
print(f'Prix predit: {prix_predict:,.0f}$')