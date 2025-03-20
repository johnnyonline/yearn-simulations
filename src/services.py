import json
import uuid

import requests
from fastapi import HTTPException
from web3 import Web3

from src.config import ACCOUNT_SLUG, HEADERS, PROJECT_SLUG, VNET_FILE
from src.models import CreateVNetRequest, GetVNetResponse, VNetResponse


def load_vnet_mapping() -> dict:
    """
    Loads VNet mapping from a JSON file.

    Returns:
        dict: VNet mapping
    """
    try:
        with open(VNET_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_vnet_mapping(vnet_mapping: dict) -> None:
    """
    Saves VNet mapping to a JSON file.

    Args:
        vnet_mapping (dict): VNet mapping
    """
    with open(VNET_FILE, "w") as file:
        json.dump(vnet_mapping, file, indent=4)


def create_vnet(request: CreateVNetRequest) -> VNetResponse:
    """
    Creates a Virtual TestNet for the given chain_id

    Args:
        request (CreateVNetRequest): VNet creation request

    Returns:
        VNetResponse: VNet creation response
    """
    vnet_url = f"https://api.tenderly.co/api/v1/account/{ACCOUNT_SLUG}/project/{PROJECT_SLUG}/vnets"

    payload = {
        "slug": f"vnet-{request.chain_id}-msig-ci-{uuid.uuid4().hex[:12]}",
        "display_name": f"VNet for Chain {request.chain_id}",
        "fork_config": {"network_id": request.chain_id},
        "virtual_network_config": {"chain_config": {"chain_id": request.chain_id}},
        "sync_state_config": {
            "enabled": False,
            # "enabled": True, # this requires a higher plan
            "commitment_level": "latest",
        },
        "explorer_page_config": {"enabled": True, "verification_visibility": "src"},
    }

    response = requests.post(vnet_url, json=payload, headers=HEADERS)
    print(response.json())

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to create VNet"
        )

    response_data = response.json()
    vnet_id = response_data["id"]
    rpc_url = response_data["rpcs"][0]["url"]

    vnet_mapping = load_vnet_mapping()
    vnet_mapping[str(request.chain_id)] = vnet_id
    save_vnet_mapping(vnet_mapping)

    return VNetResponse(vnet_id=vnet_id, rpc_url=rpc_url)


def get_vnet(chain_id: int) -> GetVNetResponse:
    """
    Finds a VNet for the given chain_id and retrieves its RPC URL

    Args:
        chain_id (int): Chain ID

    Returns:
        GetVNetResponse: VNet data
    """

    vnet_mapping = load_vnet_mapping()
    vnet_id = vnet_mapping.get(str(chain_id))

    if not vnet_id:
        raise HTTPException(
            status_code=404, detail=f"No VNet found for chain_id {chain_id}"
        )

    vnet_url = f"https://api.tenderly.co/api/v1/account/{ACCOUNT_SLUG}/project/{PROJECT_SLUG}/vnets/{vnet_id}"
    response = requests.get(vnet_url, headers=HEADERS)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to fetch VNet"
        )

    vnet_data = response.json()
    vnet_rpc_url = vnet_data["rpcs"][0]["url"]

    web3 = Web3(Web3.HTTPProvider(vnet_rpc_url))
    if not web3.is_connected():
        raise HTTPException(
            status_code=500, detail="Failed to connect to the Virtual TestNet"
        )

    return GetVNetResponse(vnet_id=vnet_id, rpc_url=vnet_rpc_url)
