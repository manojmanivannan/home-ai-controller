from typing import Type, Literal, Union
from pydantic import BaseModel
from ..models.room import DeviceToggleInput
from ...common.logger import log
from langchain.tools.base import ToolException
from .utils.tool_error_handler import ErrorHandleBaseTool
import requests
from ...configuration.config_loader import ConfigLoader
from langchain_core.runnables import RunnableConfig
import json

class ToggleDeviceTool(ErrorHandleBaseTool):
    ACCEPT_VERSION: str = "1.0.0"

    name: str = "toogle-devices-on-or-off"
    description: str = (
        "Tool to toggle a single device ON or OFF. Exact device name and room_id is required. Use it multiple times to toggle multiple devices."
    )
    args_schema: Type[BaseModel] = DeviceToggleInput
    return_direct: bool = False

    def _init_(self):
        super()._init_()
        self.handle_tool_error = self._handle_tool_error
        self.handle_validation_error = self._handle_validation_error

    def _run(
        self,
        config: RunnableConfig, #for langchain 0.2.41 RunnableConfig is only injected if defined as mandatory (https://www.reddit.com/r/LangChain/comments/1esdvq2/passing_config_to_langgraph_tool_discrepancies/)
        device_name: str = None,
        room_name: str = None,
        action: Literal['on','off'] = 'on'
        
    ) -> list:
        #print("PAYLOAD AND CONFIG===================================+++++++++++++++++++++++++",config)

        
        try:
            log.debug("Calling toogle-devices-on-or-off tool")
            devices_list = self._toggle_device(
                    device_name=device_name,
                    room_name=room_name,
                    action=action
                )


        except Exception as ex:
            log.warning(
                f"Unexpected exception while toggling the device, message: {ex}"
            )
            raise ToolException(
                "Unexpected exception while toggling the device"
            ) from ex
            # raise Exception("Unexpected exception while fetching aggregator details, message: "+ str(ex))

        return devices_list

    def _arun(
            self,
            config: RunnableConfig,
            room_name: str = None,
    ) -> list:
        return self._run(
            config=config,
            room_name=room_name
        )

    def _toggle_device(self, device_name: str = "", room_name: str = None, action: str="on") -> list:
        if action == 'on':
            url = ConfigLoader().home_automation_url+f"/turnon/"
        else:
            url = ConfigLoader().home_automation_url+f"/turnoff/"

        # room_id = int(room_id) if room_id.isnumeric() else room_id
        log.debug(f"Making API call to '{url}' togggle the device {device_name}")
        devices_list = json.loads(requests.post(url=url, data=json.dumps({"name":device_name,"room_name":room_name})).text)
        # in case of wrong metric or dimension, aggregators_list will be empty
        # so, invoke the API again without metric and dimension which will list all dimensions and metrics
        return devices_list
    