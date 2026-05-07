

def read_file_tool(input_data: dict) -> str:
    path = input_data["path"]
    # print("Inside read file")

    with open(path, "r") as f:
        return f.read()
    
