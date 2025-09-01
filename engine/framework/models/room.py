from typing import Optional, Literal
from pydantic import BaseModel, Field

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
    room_name: str = Field(
        description="Name of the room which contains the device to toggle. Can be obtained using get-devices-list tool or get-rooms-list tool", default=""
    )
    action: Literal['on','off'] = Field(
        description="Toggle the device 'on' or 'off'", default="on"
    )