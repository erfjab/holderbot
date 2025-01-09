from datetime import datetime
from abc import ABC
from typing import Optional, Union, Dict, Any, Type, TypeVar
import httpx
from pydantic import BaseModel
from app.settings.log import logger

T = TypeVar("T", bound=BaseModel)


class ApiRequest(ABC):
    """
    Abstract base class for API interactions with robust session management
    """

    def __init__(
        self,
        host: str,
    ) -> None:
        """
        Initialize API client
        """
        self.host = host.rstrip("/")
        self._client = httpx.AsyncClient(timeout=5.0, verify=False)

    def _get_headers(self, access: Optional[str] = None) -> Dict[str, str]:
        """
        Generate authentication headers
        """
        if access:
            headers = {"Content-Type": "application/json"}
            headers["Authorization"] = f"Bearer {access}"
        else:
            headers = None
        return headers

    async def _request(
        self,
        method: str,
        endpoint: str,
        access: Optional[str] = None,
        data: Optional[Union[BaseModel, Dict[str, Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[T]] = None,
    ) -> Union[httpx.Response, T, bool]:
        """
        Generic request method with flexible parameters and empty response handling
        """
        try:
            headers = self._get_headers(access)
            clean_data = self._clean_payload(data)
            clean_params = self._clean_payload(params)
            full_url = f"{self.host}/{endpoint.lstrip('/')}"
            response = await self._client.request(
                method,
                full_url,
                headers=headers,
                data=clean_data if not access else None,
                json=clean_data if access else None,
                params=clean_params,
            )
            response.raise_for_status()

            if not response.content:
                if response.status_code in [200, 201, 204]:
                    return True
                return False

            if response_model:
                return response_model(**response.json())

            jsonres = response.json()
            return jsonres if jsonres != {} else True

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False

    def _clean_payload(
        self, payload: Optional[Union[BaseModel, Dict[str, Any]]]
    ) -> Optional[Dict[str, Any]]:
        if payload is None:
            return None

        if isinstance(payload, BaseModel):
            data = payload.model_dump()
        else:
            data = payload

        def clean_nones_and_convert_datetime(obj: Any) -> Any:
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {
                    key: clean_nones_and_convert_datetime(value)
                    for key, value in obj.items()
                    if value is not None
                }
            elif isinstance(obj, list):
                return [
                    clean_nones_and_convert_datetime(item)
                    for item in obj
                    if item is not None
                ]
            return obj

        return clean_nones_and_convert_datetime(data)

    async def close(self) -> None:
        """
        Close the HTTP client session
        """
        await self._client.aclose()

    async def get(
        self,
        endpoint: str,
        access: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[T]] = None,
    ) -> Union[httpx.Response, T]:
        """
        Perform a GET request
        """
        return await self._request(
            "GET", endpoint, params=params, response_model=response_model, access=access
        )

    async def post(
        self,
        endpoint: str,
        access: Optional[str] = None,
        data: Optional[Union[BaseModel, Dict[str, Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[T]] = None,
    ) -> Union[httpx.Response, T]:
        """
        Perform a POST request
        """
        return await self._request(
            "POST",
            endpoint,
            data=data,
            params=params,
            response_model=response_model,
            access=access,
        )

    async def put(
        self,
        endpoint: str,
        access: Optional[str] = None,
        data: Optional[Union[BaseModel, Dict[str, Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[T]] = None,
    ) -> Union[httpx.Response, T]:
        """
        Perform a PUT request
        """
        return await self._request(
            "PUT",
            endpoint,
            data=data,
            response_model=response_model,
            params=params,
            access=access,
        )

    async def delete(
        self,
        endpoint: str,
        access: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[T]] = None,
    ) -> Union[httpx.Response, T]:
        """
        Perform a DELETE request
        """
        return await self._request(
            "DELETE",
            endpoint,
            params=params,
            response_model=response_model,
            access=access,
        )
