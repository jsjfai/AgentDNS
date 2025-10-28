from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def get_tools_number(baseurl):
    # Connect to a streamable HTTP server
    async with streamablehttp_client(baseurl) as (
        read_stream,
        write_stream,
        _,
    ):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tools = await session.list_tools()
            return len(tools.tools)
