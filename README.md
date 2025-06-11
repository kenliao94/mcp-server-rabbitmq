# RabbitMQ MCP Server
[![smithery badge](https://smithery.ai/badge/@kenliao94/mcp-server-rabbitmq)](https://smithery.ai/server/@kenliao94/mcp-server-rabbitmq)

A [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) server implementation for RabbitMQ. Enabling MCP client to interact with queues and topics hosted in a RabbitMQ instance.

## Features

### Manage your RabbitMQ message brokers using AI agent.
This MCP servers wraps admin APIs of a RabbitMQ broker as MCP tools. It also uses Pika to interact with RabbitMQ to operate at the message level. You can also specify a new RabbitMQ broker that you want to connect to, at runtime (default one is configured in the parameters passed to the MCP server).

### Supports streamable HTTP with FastMCP's `BearerAuthProvider`
You can start a remote RabbitMQ MCP server by configuring your own IdP and 3rd party authorization provider.

### Seamless integration with MCP client
The package is available on PyPI, you can use uvx without having to fork and build the MCP server locally first.


## Running locally with the Claude desktop app

### Installing via Smithery

To install RabbitMQ MCP Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@kenliao94/mcp-server-rabbitmq):

```bash
npx -y @smithery/cli install @kenliao94/mcp-server-rabbitmq --client claude
```

### Try it online
https://smithery.ai/server/@kenliao94/mcp-server-rabbitmq

### PyPI

https://pypi.org/project/mcp-server-rabbitmq/

```json
{
    "mcpServers": {
      "rabbitmq": {
        "command": "uvx",
        "args": [
            "mcp-server-rabbitmq@latest",
            "--rabbitmq-host",
            "<hostname ex. test.rabbit.com, localhost>",
            "--port",
            "<port number ex. 5672>",
            "--username",
            "<rabbitmq username>",
            "--password",
            "<rabbitmq password>",
            "--use-tls",
            "<true if uses amqps, false otherwise>"
        ]
      }
    }
}
```

### Manual Installation
1. Clone this repository.
2. Add the following to your `claude_desktop_config.json` file:
- On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
    "mcpServers": {
      "rabbitmq": {
        "command": "uv",
        "args": [
            "--directory",
            "/path/to/repo/mcp-server-rabbitmq",
            "run",
            "mcp-server-rabbitmq",
            "--rabbitmq-host",
            "<hostname ex. test.rabbit.com, localhost>",
            "--port",
            "<port number ex. 5672>",
            "--username",
            "<rabbitmq username>",
            "--password",
            "<rabbitmq password>",
            "--use-tls",
            "<true if uses amqps, false otherwise>"
        ]
      }
    }
}
```
4. Install and open the [Claude desktop app](https://claude.ai/download).
5. Try asking Claude to do a read/write operation of some sort to confirm the setup (e.g. ask it to publish a message to a queue). If there are issues, use the Debugging tools provided in the MCP documentation [here](https://modelcontextprotocol.io/docs/tools/debugging).

## Roadmap
1. Expose admin API tools and pika SDK tools
1. Support OAuth 2.1 and use it with RabbitMQ OAuth
1. Publish to PyPI

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/kenliao94/mcp-server-rabbitmq.git
cd mcp-server-rabbitmq

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
pytest
```

### Code Quality

This project uses ruff for linting and formatting:

```bash
# Run linter
ruff check .

# Run formatter
ruff format .
```

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
