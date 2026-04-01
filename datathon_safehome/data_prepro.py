import kagglehub

# Download latest version
path = kagglehub.dataset_download("hungkhoi/skeleton-data-of-ntu-rgbd-60-dataset")

print(f"Path to dataset files:", path)