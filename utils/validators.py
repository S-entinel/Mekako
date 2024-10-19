# utils/validators.py

def validate_positive(value: float, name: str):
    if value <= 0:
        raise ValueError(f"{name} must be positive.")