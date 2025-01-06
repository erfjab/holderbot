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
    ) -> Union[httpx.Response, T]:
        """
        Generic request method with flexible parameters
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
        except Exception as e:
            logger.error(str(e))
            return False

        if response_model:
            return response_model(**response.json())

        return response.json()

    def _clean_payload(
        self, payload: Optional[Union[BaseModel, Dict[str, Any]]]
    ) -> Optional[Dict[str, Any]]:
        if payload is None:
            return None

        if isinstance(payload, BaseModel):
            data = payload.model_dump()
        else:
            data = payload

        def convert_datetime(obj: Any) -> Any:
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {key: convert_datetime(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_datetime(item) for item in obj]
            return obj

        return convert_datetime(data)

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
        response_model: Optional[Type[T]] = None,
    ) -> Union[httpx.Response, T]:
        """
        Perform a PUT request
        """
        return await self._request(
            "PUT", endpoint, data=data, response_model=response_model, access=access
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
