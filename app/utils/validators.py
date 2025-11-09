from uuid import UUID
from fastapi import HTTPException, status


def validate_uuid(value: str, field_name: str = "ID") -> UUID:
    """Validate and convert string to UUID."""
    try:
        return UUID(value)
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {field_name} format"
        )

