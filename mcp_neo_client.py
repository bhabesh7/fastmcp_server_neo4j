# client.py
import asyncio
from fastmcp import client
from fastmcp.client.transports import StreamableHttpTransport
import httpx
import pprint
# import json


async def getdatafrom_kg():
    '''Function to get data from the knowledge graph using the MCP client.
    This function initializes the MCP client, connects to the server, and retrieves data from the Neo4j database.'''
    # Example usage of the MCP client
    transport = StreamableHttpTransport("http://localhost:8000/mcp")
    async with client.Client(transport) as mcp_client:
        await mcp_client.ping()
        print("Ping successful")

        tools = await mcp_client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")

        data_file_results = await mcp_client.call_tool("get_all_datasets_and_files", {})
        
        print("Neo4j results:")
        print(30*"-")
        print(pprint.pformat(data_file_results))
       
        feature_results = await mcp_client.call_tool("get_features_for_file", {"file_name": "train_FD001"})
        
        print("feature_results:")
        print(30*"-")
        print(pprint.pformat(feature_results))

        files_by_type_results = await mcp_client.call_tool("get_files_by_type", {"file_type": "test"})
        
        print("Files by type results:")
        print(30*"-")
        print(pprint.pformat(files_by_type_results))

        units_results = await mcp_client.call_tool("get_all_units", {})
        
        print("Units results:")
        print(30*"-")
        print(pprint.pformat(units_results))

        

if __name__ == "__main__":
    # Run the example
    asyncio.run(getdatafrom_kg())

    
