# MCP-servers

This is a small Model Context Protocol (MCP) servers and clients project, written in Python with FastMCP while I learned how MCP works. There are two independent examples: a currency-conversion utility server and an ArXiv research explorer.

> **Requirements:** Python with the `fastmcp` package. The ArXiv server also needs the `tavily` package (`tavily-python`) and a Tavily API key in the `TAVILY_API_KEY` environment variable.

## Sub-projects

| # | Sub-project                                    | What it does                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Where                                | How to run                                                                                                                                                          | Builds on                                                                                              |
|---|------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| A | **Utility server + test client**               | An MCP server with one tool, `convert_usd_to_eur(amount, rate=0.85)`. The client lists the tools and calls the conversion with `amount=100`.                                                                                                                                                                                                                                                                                                                                              | `util_server.py`, `client.py`        | Terminal 1: `python util_server.py`. Terminal 2: `python client.py`. Both use HTTP transport, and the client expects `http://localhost:8000/mcp`.                   | FastMCP basics. TODO (Ellie): which course or tutorial did you follow for this?                        |
| B | **ArXiv Explorer server + interactive client** | A server named `ArxivExplorer` with one resource (`resource://ai/arxiv_topics`, a fixed list of four topics), two tools (`search_arxiv` finds ArXiv papers through Tavily search, `summarize_paper` asks Tavily's Q&A search for a summary), and one prompt (`explore_topic_prompt`) that tells an LLM to search, summarize each paper and combine the results. The client pings the server, lists tools, resources and prompts, reads the resource, then tries each tool and the prompt. | `arxiv_server.py`, `arxiv_client.py` | `export TAVILY_API_KEY=...`, then `python arxiv_server.py` in one terminal and `python arxiv_client.py` in another. The client expects `http://localhost:8000/mcp`. | FastMCP and the Tavily Python client. TODO (Ellie): course or tutorial this was based on, with a link? |

Note: To recreate the environments

```bash
python3.13 -m venv venv
venv/bin/pip install --only-binary=cryptography -r requirements.txt
```

## What I did

- I wrote the utility server and client first, then the ArXiv server, then the interactive client for it.
- The ArXiv client has a helper, `unwrap_tool_result`, that turns a tool response into a Python object, whether it comes back as JSON or as text.

## Known gaps

- The servers use HTTP transport but the code never sets a port or path. They rely on FastMCP's defaults (port 8000, path `/mcp`, checked with FastMCP 4.1.6), which is what the clients expect. Pass `port=` to `mcp.run()` and update the clients if you change it.
- `summarize_paper` sends the URL to Tavily's Q&A search and does not fetch the paper itself, so the summary quality depends on Tavily.
- I only ran the utility server and client end to end. The ArXiv pair needs a Tavily API key.
