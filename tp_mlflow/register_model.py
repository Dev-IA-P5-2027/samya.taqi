import mlflow 
import mlflow.sklearn 
from mlflow.tracking import MlflowClient 
# Le nom sous lequel le modèle sera connu dans le Registry 
MODEL_NAME = 'prix-immobilier-predictor' 
# Remplacer par le Run ID du meilleur run (visible dans l'UI) 
RUN_ID = '213a37f365c043d2a72fed956755b452' 
# Enregistrer le modèle du run dans le Registry 
# MLflow crée automatiquement la version 1, 2, 3... à chaque enregistrement 

result = mlflow.register_model( 
    model_uri=f'runs:/{RUN_ID}/model', 
    name=MODEL_NAME 
) 
print(f'Modèle enregistré : {MODEL_NAME} version {result.version}')
# ── Ajouter une description ───────────────────────────────────── 

client = MlflowClient() 
client.update_model_version( 
    name=MODEL_NAME, 
    version=result.version, 
    description='Random Forest 200 arbres. MAE ~18000 €. R² = 0.92.' 
) 

# ── Passer le modèle en Staging ────────────────────────────────── 
# Staging = modèle validé techniquement, en attente de validation métier 
client.transition_model_version_stage( 
    name=MODEL_NAME, 
    version=result.version, 
    stage='Staging' 
) 
print(f'Modèle v{result.version} → Staging') 