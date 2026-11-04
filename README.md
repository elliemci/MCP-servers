# MCP-servers

Small Model Context Protocol (MCP) servers, clients and agents in Python, written while I learned how MCP works. The folders are numbered in the order I'd read them: from a first server with two tools, to servers that expose resources and prompts, to HTTP servers with their own clients, to agents that call an MCP server on their own.

> **Requirements:** Python 3.13 (what I used). Each folder has its own `requirements.txt`. Folders 04 and 05 also need API keys, described in their sections.

## Learning path

| #  | Folder                                        | What it shows                                                                             | Transport          | Needs                       |
|----|-----------------------------------------------|-------------------------------------------------------------------------------------------|--------------------|-----------------------------|
| 01 | [01-weather-server](01-weather-server/)       | The smallest useful server: two async tools that call the US National Weather Service API | stdio              | nothing                     |
| 02 | [02-server-primitives](02-server-primitives/) | The three things a server can expose: a tool, a resource and a prompt                     | SSE                | nothing                     |
| 03 | [03-utility-server](03-utility-server/)       | A server over HTTP plus a Python client that lists and calls its tool                     | HTTP               | nothing                     |
| 04 | [04-arxiv-server](04-arxiv-server/)           | A larger server: a resource, two tools and a prompt, with an interactive client           | HTTP               | Tavily API key              |
| 05 | [05-tiny-agents](05-tiny-agents/)             | An LLM agent that decides when to call an MCP server's tools                              | SSE via mcp-remote | Hugging Face token, Node.js |

## 01 · Weather server

`weather.py` is a [FastMCP](https://github.com/modelcontextprotocol/python-sdk) server with two tools:

- `get_alerts(state)`: active alerts for a US state, such as `CA`.
- `get_forecast(latitude, longitude)`: the next five forecast periods for a location.

It runs over stdio, so a client starts it as a subprocess instead of connecting to a port. To try it, use [mcp-chat-client](https://github.com/elliemci/mcp-chat-client):

```bash
cd 01-weather-server
pip install -r requirements.txt
# from the mcp-chat-client folder:
uv run client.py path/to/MCP-servers/01-weather-server/weather.py
```

## 02 · Server primitives

`server.py` has one tool (`get_weather`), one resource (`weather://{location}`) and one prompt (`weather_report`). The data is hard-coded, so this folder is about the shape of a server, not about real weather. Tools are actions the model can call, resources are data the client can read, and prompts are reusable templates.

```bash
cd 02-server-primitives
pip install -r requirements.txt
python server.py   # serves SSE on http://localhost:3001/sse
```

## 03 · Utility server and client

`util_server.py` has one tool, `convert_usd_to_eur(amount, rate=0.85)`. `client.py` lists the server's tools and calls the conversion with `amount=100`. The server uses HTTP transport, and the client expects `http://localhost:8000/mcp`.

```bash
cd 03-utility-server
pip install -r requirements.txt
python util_server.py      # terminal 1
python client.py           # terminal 2
```

TODO (Ellie): which course or tutorial did you follow for this?

## 04 · ArXiv explorer

A server named `ArxivExplorer` with one resource (`resource://ai/arxiv_topics`, a fixed list of four topics), two tools (`search_arxiv` finds ArXiv papers through Tavily search, `summarize_paper` asks Tavily's Q&A search for a summary) and one prompt (`explore_topic_prompt`) that tells an LLM to search, summarize each paper and combine the results. The client pings the server, lists tools, resources and prompts, reads the resource, then tries each tool and the prompt.

```bash
cd 04-arxiv-server
pip install -r requirements.txt
export TAVILY_API_KEY=...
python arxiv_server.py     # terminal 1
python arxiv_client.py     # terminal 2
```

## 05 · Tiny agents

Agents built with Hugging Face's tiny agents, following the [Hugging Face MCP course](https://huggingface.co/learn/mcp-course/en/unit0/introduction) (see the [tiny agents section](https://huggingface.co/learn/mcp-course/en/unit2/tiny-agents) of unit 2). The model decides when to call a tool, and the agent runs it through an MCP server.

`agent.py` connects to the Gradio MCP server that exposes a sentiment-analysis tool, the [mcp-sentiment](https://huggingface.co/spaces/elliemci/mcp-sentiment) Space, and then runs an interactive command-line loop where you give the agent instructions. The Space is reached over SSE through `npx mcp-remote`.

| File                     | Model                                  | MCP server                                            |
|--------------------------|----------------------------------------|-------------------------------------------------------|
| `agent.py`               | Qwen2.5-72B-Instruct (Nebius)          | The mcp-sentiment Space, run as a Python script       |
| `agent_mcpserver.json`   | Qwen2.5-72B-Instruct (Nebius)          | The same Space, as a config for the `tiny-agents` CLI |
| `agent_test.json`        | Qwen2.5-72B-Instruct (Nebius)          | Playwright (`@playwright/mcp`), for browser control   |
| `agent_local_model.json` | Qwen3-32B, served locally on port 1234 | A local MCP endpoint on the same port                 |

```bash
cd 05-tiny-agents
pip install -r requirements.txt      # huggingface_hub[mcp]>=0.32.0
npm i mcp-remote                      # bridge to the Gradio SSE server
export HF_TOKEN=...                   # Hugging Face token for inference

python agent.py                       # interactive loop
tiny-agents run agent_mcpserver.json  # or run a config with the CLI
```

Needs Node.js (for `npx`). I haven't re-run this folder since reorganizing the repo. `HF_TOKEN` is my assumption: the course's CLI section doesn't mention a token, but its JavaScript client reads one from that variable.

## Related projects

- [mcp-chat-client](https://github.com/elliemci/mcp-chat-client): a Claude-powered MCP client with a command-line and a Gradio interface. Works with the server in 01.
- [mcp-adk](https://github.com/elliemci/mcp-adk): Google ADK agents connected to a local SQLite MCP server and to Notion.
- [mcp-sentiment](https://huggingface.co/spaces/elliemci/mcp-sentiment): a sentiment-analysis MCP server on Hugging Face Spaces.
- [mcp-client](https://huggingface.co/spaces/elliemci/mcp-client): a Gradio agent that uses tools from a remote MCP server, on Hugging Face Spaces.

## Known gaps

- The HTTP servers (03 and 04) never set a port or path. They rely on FastMCP's defaults (port 8000, path `/mcp`, checked with FastMCP 4.1.6), which is what the clients expect. Pass `port=` to `mcp.run()` and update the clients if you change it.
- `summarize_paper` sends the URL to Tavily's Q&A search and does not fetch the paper itself, so the summary quality depends on Tavily.
- I checked that server 02 lists its tool, resource and prompt over SSE, and that the utility server and client (03) work end to end from their folders. For 01 I only confirmed that the server starts and lists both tools, without calling them. The ArXiv pair needs a Tavily key, and 05 needs a Hugging Face token and network access.
