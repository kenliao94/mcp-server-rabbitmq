from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)
import ssl
from .models import Enqueue, Fanout, ListQueues, ListExchanges
from .logger import Logger, LOG_LEVEL
from .connection import RabbitMQConnection, validate_rabbitmq_name
from .handlers import handle_enqueue, handle_fanout, handle_list_queues, handle_list_exchanges
from .admin import RabbitMQAdmin


async def serve(rabbitmq_host: str, port: int, username: str, password: str, use_tls: bool, log_level: str = LOG_LEVEL.DEBUG.name, api_port: int = 15671) -> None:
    # Setup server
    server = Server("mcp-rabbitmq")
    # Setup logger
    is_log_level_exception = False
    try:
        log_level = LOG_LEVEL[log_level]
    except Exception:
        is_log_level_exception = True
        log_level = LOG_LEVEL.WARNING
    logger = Logger("server.log", log_level)
    if is_log_level_exception:
        logger.warning("Wrong log_level received. Default to WARNING")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="enqueue",
                description="""Enqueue a message to a queue hosted on RabbitMQ""",
                inputSchema=Enqueue.model_json_schema(),
            ),
            Tool(
                name="fanout",
                description="""Publish a message to an exchange with fanout type""",
                inputSchema=Fanout.model_json_schema(),
            ),
            Tool(
                name="list_queues",
                description="""List all the queues in the broker""",
                inputSchema=ListQueues.model_json_schema(),
            ),
            Tool(
                name="list_exchanges",
                description="""List all the exchanges in the broker""",
                inputSchema=ListExchanges.model_json_schema(),
            )
        ]

    @server.call_tool()
    async def call_tool(
        name: str,
        arguments: dict
    ) -> list[TextContent]:
        if name == "enqueue":
            logger.debug("Executing enqueue tool")
            message = arguments["message"]
            queue = arguments["queue"]
            
            validate_rabbitmq_name(queue, "Queue name")

            try:
                # Setup RabbitMQ connection
                rabbitmq = RabbitMQConnection(rabbitmq_host, port, username, password, use_tls)
                handle_enqueue(rabbitmq, queue, message)
                return [TextContent(type="text", text=str("suceeded"))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]
        elif name == "fanout":
            logger.debug("Executing fanout tool")
            message = arguments["message"]
            exchange = arguments["exchange"]
            
            validate_rabbitmq_name(exchange, "Exchange name")

            try:
                # Setup RabbitMQ connection
                rabbitmq = RabbitMQConnection(rabbitmq_host, port, username, password, use_tls)
                handle_fanout(rabbitmq, exchange, message)
                return [TextContent(type="text", text=str("suceeded"))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]
        elif name == "list_queues":
            try:
                admin = RabbitMQAdmin(rabbitmq_host, api_port, username, password, use_tls)
                result = handle_list_queues(admin)
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]
            return [TextContent(type="text", text=str("succeeded"))]
        elif name == "list_exchanges":
            try:
                admin = RabbitMQAdmin(rabbitmq_host, api_port, username, password, use_tls)
                result = handle_list_exchanges(admin)
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"{e}")
                return [TextContent(type="text", text=str("failed"))]
        raise ValueError(f"Tool not found: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
