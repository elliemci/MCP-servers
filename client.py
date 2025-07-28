import asyncio
from fastmcp.client import Client


async def main():
    async with Client("http://localhost:8000/mcp") as client:
        # 1. List available tools
        tools = await client.list_tools()
        print(f"Available tools:, {[t.name for t in tools]}")

        # 2. Call the tool
        result = await client.call_tool("convert_usd_to_eur", arguments={"amount": 100})
        print(f"Result: {result.structured_content['result']}")


if __name__ == "__main__":
    asyncio.run(main())
