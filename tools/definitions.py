from typing import Callable, Dict, Any
from tools.read import read_file_tool
from tools.ls import list_files_tool
from tools.edit import edit_files_tool

class ToolDefinition:
    def __init__(
            self,
            name: str,
            description: str,
            parameters: Dict[str, Any],
            function: Callable[[Dict[str, Any]], str]
            ):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.function = function

# Read file tool 
read_file_schema = {
    "type":"object",
    "properties":{
        "path":{
            "type":"string",
            "description":"The relative path of a file in the working directory."
        }
    },
    "required": ["path"]
}

read_file_definition = ToolDefinition(
    name="read_file",
    description="Read the contents of a given relative file path. Use this when you want to see what's inside a file. Do not use this with directory names.",
    parameters=read_file_schema,
    function=read_file_tool
    )

# List files tool
list_files_schema = {
    "type":"object",
    "properties":{
        "path":{
            "type":"string",
            "description":"Optional relative path to list files from. Defaults to current directory if not provided."
        }
    },
    "required": []
}

list_files_definition = ToolDefinition(
    name="list_files",
    description="List files and directories at a given path. If no path is provided, lists files in the current directory.",
    parameters=list_files_schema,
    function=list_files_tool
)

# Edit files tool
edit_files_schema = {
    "type":"object",
    "properties":{
        "path":{
            "type":"string",
            "description":"The path to the file."
        },
        "old_str":{
            "type":"string",
            "description":"Text to search for - must match exactly and must only have one match exactly."
        },
        "new_str":{
            "type":"string",
            "description":"Text to replace old_str with."
        }
    },
    "required": ["path", "new_str"]
}

edit_files_definition = ToolDefinition(
    name="edit_files",
    description="""Make edits to a text file.

        Replaces 'old_str' with 'new_str' in the given file. 'old_str' and 'new_str' MUST be different from each other.

        If the file specified with path doesn't exist, it will be created.
    """,
    parameters=edit_files_schema,
    function=edit_files_tool
)