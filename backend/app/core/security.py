# Minimal security functions
def verify_api_key(api_key: str) -> bool:
    # Add real verification logic here
    return len(api_key) > 5