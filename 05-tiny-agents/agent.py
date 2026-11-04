import os
import asyncio

from huggingface_hub import Agent

# Define the agent using the MCP server sentiment tool
agent = Agent(
    model="Qwen/Qwen2.5-72B-Instruct",
    provider="nebius",
    servers=[
        {
            "url": "https://elliemci-mcp-sentiment.hf.space/gradio_api/mcp/sse",
            "config": {"command": "npx", "args": ["mcp-remote"]},
        }
        # can add more servers with different tools
    ],
)


# Async generator loop for interactive CLI
async def run_agent():
    print("Agent is ready. Type your instruction (Ctrl+C to quit):\n")
    try:
        while True:
            prompt = input(">>> ").strip()
            if not prompt:
                continue
            # print only the assistant's text from each chunk which is streaming object like
            # ChatCompletionStreamOutput(
            # choices=[
            # ChatCompletionStreamOutputChoice(
            # delta=ChatCompletionStreamOutputDelta(content="some text")])

            print("Agent:", end=" ", flush=True)

            # since huggingface_hub.Agent generated asynchronous streaming which needs to be iterated over
            async for chunk in agent.run(prompt):
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
            print()
    except KeyboardInterrupt:
        print("\nSession ended.")


# Run the loop
if __name__ == "__main__":
    asyncio.run(run_agent())
