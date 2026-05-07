import os

def edit_files_tool(input_data: dict) -> str:
    print(f"Input data edit {input_data}")
    path = input_data.get("path")
    old_str = input_data.get("old_str","")
    new_str = input_data.get("new_str","")

    # Invalid inputs
    if not path: 
        return "Error: path is required"
    if old_str == new_str:
        return "Error: old_str and new_str cannot be the same"
    
    # File doesnt exist -> create_file
    if not os.path.exists(path):
        if old_str == "":
            try:
                with open(path, "w") as f:
                    f.write(new_str)
                return f"OK (created file: {path})"
            except Exception as e:
                return f"Error creating file: {path} - {e}"
    try:
        with open(path, "r") as f:
            old_content = f.read()
    except Exception as e:
        return f"Error reading file {e}"

    new_content = old_content.replace(old_str, new_str)

    # if old_content == new_content and old_str != "":
    #     return ""

    #Write file
    try:
        with open(path, "w") as f:
            f.write(new_content)
    except Exception as e:
        return f"Error writing file: {e}"
    
    return "OK"