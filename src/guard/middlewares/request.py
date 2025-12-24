import time
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from guard.utils.logger import logger


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = start_time = time.perf_counter()

        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        request.state.request_id = request_id

        client = request.client
        client_ip = client.host if client else "unknown"
        client_port = client.port if client else "unknown"
        method = request.method
        path = request.url.path

        logger.info(f"[{request_id}] {method} {path} from {client_ip}:{client_port}")

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        process_time = time.perf_counter() - start_time
        logger.info(f"[{request_id}] Completed in {process_time:.3f}s")

        return response
