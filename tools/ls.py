import os

def list_files_tool(input_data: dict) -> str:
    # print(f"Input data ls {input_data}")
    path = input_data.get("path", ".")
    # print(f"Path: {path}")

    try:
        files = os.listdir(path)
        return '\n'.join(files)
    except Exception as e:
        return f"Error listing files: {e}"