import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(env_variable: str) -> str:
    """Obtaion variable value in cur venv by its name."""
    try:
        return os.environ[env_variable]
    except KeyError:
        raise ImproperlyConfigured(
            f'Set {env_variable} environment variable'
        )
