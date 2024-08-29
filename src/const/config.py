from enum import StrEnum


class SecretsPath(StrEnum):
    LOCAL: str = "./secrets"
    DOCKER: str = "/run/secrets"
