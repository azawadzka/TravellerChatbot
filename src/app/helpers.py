import os
from pathlib import Path

from src.const import SecretsPath


def get_secret(secret_name: str) -> str:
    if os.path.exists(SecretsPath.LOCAL):
        secrets_path = SecretsPath.LOCAL
    elif os.path.exists(SecretsPath.DOCKER):
        secrets_path = SecretsPath.DOCKER
    else:
        raise FileNotFoundError("Secrets directory not found")
    secret_path = Path(secrets_path) / secret_name
    if not os.path.exists(secret_path):
        raise FileNotFoundError(f"Secret {secret_name} not found")
    with open(secret_path) as fh:
        return fh.read().strip()
