from typing import Optional, Literal
from langchain.pydantic_v1 import BaseModel, Field

class RoomsListInput(BaseModel):
    room_name: Optional[str] = Field(
        description="Optional name of the rooms to filter by", default=""
    )

class DevicesListInput(BaseModel):
    room_name: Optional[str] = Field(
        description="Optional name of the rooms to filter by", default=""
    )

class DeviceToggleInput(BaseModel):
    device_name: str = Field(
        description="Name of the device to toggle", default=""
    )
    room_id: str = Field(
        description="Room ID of the device to toggle. Can be obtained using get-devices-list tool or get-rooms-list tool", default=""
    )
    action: Literal['on','off'] = Field(
        description="Toggle the device 'on' or 'off'", default="on"
    )