import asyncio
from fastmcp import Client

async def main():
    client = Client("http://localhost:8000/sse")

    async with client:
        print("Connected to FastMCP server.")

        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")

        # Call the 'get_cluster_nodes' tool
        print("Calling 'get_cluster_nodes' tool...")
        result = await client.call_tool("get_cluster_nodes")
        print(f"Tool response: {result}")

        # Call the 'get_pods_in_namespace' tool
        print("Calling 'get_pods_in_namespace' tool for 'default' namespace...")
        result = await client.call_tool("get_pods_in_namespace", {"namespace": "default"})
        print(f"Tool response: {result}")
        
        # Call the 'get_pods_in_namespace' tool for 'genai' namespace
        print("Calling 'get_pods_in_namespace' tool for 'genai' namespace...")
        result = await client.call_tool("get_pods_in_namespace", {"namespace": "genai"})
        print(f"Tool response: {result}")

if __name__ == "__main__":
    asyncio.run(main())
