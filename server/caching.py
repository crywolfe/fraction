from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from cachetools import TTLCache

class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.cache = TTLCache(maxsize=1000, ttl=300)

    async def dispatch(self, request: Request, call_next):
        if request.method == "GET" and "/players" in request.url.path:
            cache_key = request.url.path
            if cache_key in self.cache:
                cached_response_body = self.cache[cache_key]
                return Response(content=cached_response_body, media_type="application/json")
        
        response = await call_next(request)
        
        if request.method == "GET" and response.status_code == 200 and "/players" in request.url.path:
            if hasattr(response, "body"):
                response_body = await response.body()
                self.cache[cache_key] = response_body
                return Response(content=response_body, media_type="application/json", status_code=response.status_code, headers=response.headers)
            else:
                # Handle StreamingResponse
                response_body = response.body_iterator
                self.cache[cache_key] = response_body
                return response
        
        return response