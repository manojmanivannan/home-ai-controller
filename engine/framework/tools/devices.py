from typing import Type
from langchain.pydantic_v1 import BaseModel
from ..models.room import DevicesListInput
from ...common.logger import log
from langchain.tools.base import ToolException
from .utils.tool_error_handler import ErrorHandleBaseTool
import requests
from ...configuration.config_loader import ConfigLoader
from langchain_core.runnables import RunnableConfig
import json

class DevicesListTool(ErrorHandleBaseTool):
    ACCEPT_VERSION = "1.0.0"

    name = "get-devices-list"
    description = (
        "Tool to retrieve the list of all available devices and room_id. useful if device's exact name or its room ID is not known."
    )
    args_schema: Type[BaseModel] = DevicesListInput
    return_direct: bool = False

    def _init_(self):
        super()._init_()
        self.handle_tool_error = self._handle_tool_error
        self.handle_validation_error = self._handle_validation_error

    def _run(
        self,
        config: RunnableConfig, #for langchain 0.2.41 RunnableConfig is only injected if defined as mandatory (https://www.reddit.com/r/LangChain/comments/1esdvq2/passing_config_to_langgraph_tool_discrepancies/)
        room_name: str = None,
        
    ) -> dict:
        #print("PAYLOAD AND CONFIG===================================+++++++++++++++++++++++++",config)

        
        try:
            log.debug("Calling get-devices-list tool")
            devices_list = self._get_devices_list(
                room_name=room_name if room_name != "" else None,
            )

        except Exception as ex:
            log.warning(
                f"Unexpected exception while fetching list of rooms, message: {ex}"
            )
            raise ToolException(
                "Unexpected exception while fetching list of rooms"
            ) from ex
            # raise Exception("Unexpected exception while fetching aggregator details, message: "+ str(ex))

        return devices_list

    def _arun(
            self,
            config: RunnableConfig,
            room_name: str = None,
    ) -> dict:
        return self._run(
            config=config,
            room_name=room_name
        )

    def _get_devices_list(self, room_name: str = "") -> list:
        url = ConfigLoader().home_automation_url+f"/devices/?room_name={room_name}" if room_name else ConfigLoader().home_automation_url+"/devices/"
        log.debug(f"Making API call to '{url}' get list of devices")
        devices_list = json.loads(requests.get(url=url).text)
        # in case of wrong metric or dimension, aggregators_list will be empty
        # so, invoke the API again without metric and dimension which will list all dimensions and metrics
        if not devices_list:
            return self._get_devices_list(
                room_name=""
            )
        return devices_list