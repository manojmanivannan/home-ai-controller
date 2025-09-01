from typing import Type
from pydantic import BaseModel
from ..models.room import RoomsListInput
from ...common.logger import log
from langchain.tools.base import ToolException
from .utils.tool_error_handler import ErrorHandleBaseTool
import requests
from ...configuration.config_loader import ConfigLoader
from langchain_core.runnables import RunnableConfig
import json

class RoomsListTool(ErrorHandleBaseTool):
    ACCEPT_VERSION: str = "1.0.0"

    name: str = "get-rooms-list"
    description: str = (
        "Tool to retrieve the list of all available rooms and room_id. useful if room's exact name or ID is not known."
    )
    args_schema: Type[BaseModel] = RoomsListInput
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
       
        try:
            log.debug("Calling get-rooms-list tool")
            rooms_list = self._get_rooms_list(
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

        return rooms_list

    def _arun(
            self,
            config: RunnableConfig,
            room_name: str = None,
    ) -> dict:
        return self._run(
            config=config,
            room_name=room_name
        )

    def _get_rooms_list(self, room_name: str = None) -> list:
        url = ConfigLoader().home_automation_url+"/rooms/"
        log.debug(f"Making API call to '{url}'get list of rooms")
        rooms_list = json.loads(requests.get(url=url).text)
        # in case of wrong metric or dimension, aggregators_list will be empty
        # so, invoke the API again without metric and dimension which will list all dimensions and metrics
        if not rooms_list:
            return self._get_rooms_list(
                room_name=room_name
            )
        return rooms_list