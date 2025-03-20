from pydantic import BaseModel


class CreateVNetRequest(BaseModel):
    chain_id: int


class VNetResponse(BaseModel):
    vnet_id: str
    rpc_url: str


class GetVNetRequest(BaseModel):
    chain_id: int


class GetVNetResponse(BaseModel):
    vnet_id: str
    rpc_url: str
