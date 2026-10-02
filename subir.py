from huggingface_hub import HfApi
import os

# Si en algún momento quieres forzar el método HTTP legacy (sin Xet),
# descomenta la siguiente línea ANTES de importar HfApi:
# os.environ["HF_HUB_DISABLE_XET"] = "1"

api = HfApi()

api.upload_file(
    path_or_fileobj="preset-db/build/spooky.db",   # tu ruta local en Windows
    path_in_repo="preset-db/build/spooky.db",      # ruta dentro del repo
    repo_id="Milor123/spooky-preset-atlas-db",
    repo_type="dataset",
)