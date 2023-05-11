from typing import Callable

from fastapi import HTTPException, Request, Response
from fastapi.routing import APIRoute

from address_book.exceptions import MyCustomException


class RouteErrorHandler(APIRoute):
    """Custom APIRoute that handles application errors and exceptions"""
    # Source - https://stackoverflow.com/a/69720977/7032304

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except Exception as ex:
                if isinstance(ex, HTTPException):
                    raise ex
                # Demonstrating mapping a custom exception to a HTTPException
                elif isinstance(ex, MyCustomException):
                    raise HTTPException(status_code=444, detail=str(ex))
                print("uncaught error")
                # wrap error into pretty 500 exception
                raise HTTPException(status_code=500, detail=str(ex))

        return custom_route_handler