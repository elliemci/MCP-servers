from fastmcp import FastMCP

mcp = FastMCP(name="UtilityServer")


# define a too and register with the MCP server
@mcp.tool()
def convert_usd_to_eur(amount: float, rate: float = 0.85) -> float:
    """
    Converts a given amount in USD to EUR using the provided rate.

    Args:
        amount (float): The amount in USD.
        rate (float, optional): The conversion rate from USD to EUR. Defaults to 0.85.

    Returns:
        float: The converted amount in EUR, rounded to 2 decimal places.
    """
    return round(amount * rate, 2)


if __name__ == "__main__":
    print(" Starting Utility MCP Server .... ")
    mcp.run(transport="http")
