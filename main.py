import os
from openai import OpenAI
import json
from typing import Callable, Optional, Dict, List, Any
from tools.definitions import ToolDefinition, read_file_definition, list_files_definition, edit_files_definition

class Agent:
    def __init__(
            self,
            client: OpenAI,
            tools: List[ToolDefinition]
    ):
        self.client = client
        self.tools = tools

    def run(self):

        read_user_input = True
        previous_response = None
        conversation = []
        
        print("\033[94m" + r"""
        ███╗   ██╗██╗ ██████╗ ██████╗ ██████╗ ███████╗
        ████╗  ██║██║██╔════╝██╔═══██╗██╔══██╗██╔════╝
        ██╔██╗ ██║██║██║     ██║   ██║██║  ██║█████╗  
        ██║╚██╗██║██║██║     ██║   ██║██║  ██║██╔══╝  
        ██║ ╚████║██║╚██████╗╚██████╔╝██████╔╝███████╗
        ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
        """+ "\033[0m")
        print("\033[92m         Chat with your own agent ^^ (ctrl + D to exit) \033[0m")

        while(True):
            # print(conversation)
            if read_user_input:
                message = self.get_user_message()
                if not message:
                    break

                # Add user message to conversation
                conversation.append({
                    "role":"user",
                    "content":message
                })

            
            # Call OpenAI model
            response = self.client.responses.create(
                model="gpt-5.4-mini",
                input=conversation,
                max_output_tokens = 1024,
                tools=[self.to_openai_tool(t) for t in self.tools],
                previous_response_id= previous_response.id if previous_response else None
            )

            previous_response = response
            tool_results = []
            has_tool_call = False

            # print(response)
            # Type of response actions
            assistant_message = ""
            for item in response.output:
                if item.type == 'message':
                    for content in item.content:
                        if content.type == "output_text":
                            assistant_message += content.text
                elif item.type == 'function_call':
                    conversation.append({
                        "type":item.type, "name":item.name, 
                        "arguments":item.arguments, "call_id": item.call_id
                        })
                    has_tool_call = True
                    tool_result = self.execute_tool(item.call_id ,item.name, item.arguments)
                    tool_results.append(tool_result)

            if not has_tool_call:
                read_user_input = True
                print(f"\033[32mAssistant\033[0m: {assistant_message}")
                # Add assistant message to conversation
                conversation.append({
                    "role":"assistant",
                    "content":assistant_message
                })
                continue

            read_user_input = False
            # Add tool results to conversation
            for result in tool_results:
                conversation.append(result)


            

            
            
    def get_user_message(self):
        try:
            return input('\u001b[94mYou\u001b[0m: ')
        except EOFError:
            return None
    
    def to_openai_tool(self, tool: ToolDefinition):
        return {
            "type":"function",
            "name":tool.name,
            "description":tool.description,
            "parameters":tool.parameters
        }
    
    def execute_tool(self, call_id, name, arguments):
        found = False

        for t in self.tools:
            if t.name == name:
                found = True
                input_data = json.loads(arguments)
                result = t.function(input_data)
                print(f"\033[92mtool\033[0m: {name}({input_data["path"]})")
                print(f"\033[90mResult: {result}\033[0m")
                break

        if not found:
            return "tool not found"
        
        return {
            "type":"function_call_output",
            "call_id": call_id,
            "output": result
        }                        

def new_agent(client: OpenAI, tools):
    return Agent(client, tools)

def main():
    client = OpenAI()
    tools = [
        read_file_definition, 
        list_files_definition, 
        edit_files_definition
        ]
    agent = new_agent(client, tools)

    try:
        agent.run()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()