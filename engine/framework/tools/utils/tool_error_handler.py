from langchain.tools import BaseTool

class ErrorHandleBaseTool(BaseTool):

    def _handle_validation_error(self,error)->str:
        return f"Error: {str(error.errors())}. Please fix your mistake."

    def _handle_tool_error(self,error) -> str:
        suggestion = ""
        error_str = repr(error)

        match error_str:
            case _ if "invalid metrics" in error_str.lower():
                suggestion = " Try get-aggregator-details to find the correct metric names."
                
            case _ if "invalid aggregator/dimension" in error_str.lower():
                suggestion = " Try get-aggregator-details to find the correct aggregator/dimension names."

        return f"Error: {error_str}.{suggestion} Please fix your mistake. "