from fastapi import APIRouter, Depends, Header, HTTPException

from src.config import CREATE_VNET_PASSWORD
from src.models import CreateVNetRequest, GetVNetResponse, VNetResponse
from src.services import create_vnet, get_vnet

router = APIRouter()


def verify_password(x_password: str = Header(None)) -> None:
    """
    Simple password protection using FastAPI headers.

    Args:
        x_password (str): Password from the header
    """
    if x_password != CREATE_VNET_PASSWORD:
        raise HTTPException(status_code=403, detail="Unauthorized")


# @router.post(
#     "/create", response_model=VNetResponse, dependencies=[Depends(verify_password)]
# )
@router.post("/create", response_model=VNetResponse)
def create_vnet_endpoint(request: CreateVNetRequest) -> VNetResponse:
    """
    Creates a Virtual TestNet for a given chain_id - Requires Password

    Usage:
        curl -X POST "http://0.0.0.0:8000/create" -H "Content-Type: application/json" -d '{"chain_id": 1}'

    Args:
        request (CreateVNetRequest): VNet creation request

    Returns:
        VNetResponse: VNet creation
    """
    return create_vnet(request)


@router.get("/get/{chain_id}", response_model=GetVNetResponse)
def get_vnet_endpoint(chain_id: int) -> GetVNetResponse:
    """
    Retrieves an existing Virtual TestNet by chain_id - Requires Password

    Usage:
        curl -v https://0.0.0.0:8000/get/1 --insecure

    Args:
        chain_id (int): Chain ID

    Returns:
        GetVNetResponse: VNet data
    """
    return get_vnet(chain_id)
