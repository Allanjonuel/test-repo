from fastapi.responses import JSONResponse
from fastapi import HTTPException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_error(e: Exception) -> JSONResponse:
    """
    Handle exceptions and return a JSON response with appropriate error details.

    :param e: Exception to handle
    :return: JSONResponse with error details
    """
    if isinstance(e, HTTPException):
        logger.error(f"HTTPException: {e.detail}")
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    else:
        logger.error(f"Unhandled Exception: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

def format_response(data: dict, message: str = "Success") -> JSONResponse:
    """
    Format a successful response with a given message and data.

    :param data: Data to include in the response
    :param message: Message to include in the response
    :return: JSONResponse with formatted data
    """
    logger.info(f"Response: {message}")
    return JSONResponse(status_code=200, content={"message": message, "data": data})
