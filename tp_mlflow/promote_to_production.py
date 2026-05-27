from mlflow.tracking import MlflowClient

MODEL_NAME = 'prix-immobilier-predictor'
client = MlflowClient()

# Trouver version en Staging
staging_versions = client.get_latest_versions(MODEL_NAME, stages=['Staging'])

if not staging_versions:
    print('Aucun modèle en Staging.')

else:
    version = staging_versions[0].version

    # Archiver ancienne prod
    prod_versions = client.get_latest_versions(MODEL_NAME, stages=['Production'])

    if prod_versions:
        old_version = prod_versions[0].version

        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=old_version,
            stage='Archived'
        )

        print(f'Ancienne version v{old_version} → Archived')

    # Promotion
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=version,
        stage='Production'
    )

    print(f'Version v{version} → Production')