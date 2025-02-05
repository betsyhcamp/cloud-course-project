from fastapi import (
    Request,
    status,
)
from fastapi.responses import JSONResponse


# fastapi middleware URL docs:
async def handle_broad_exceptions(request: Request, call_next):
    """Handle any exception not raised by other specific error handlers"""

    try:
        return await call_next(request)
    except Exception:  # pylint: disable=broad-except
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
