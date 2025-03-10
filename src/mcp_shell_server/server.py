import asyncio
import logging
import traceback
from collections.abc import Sequence
from typing import Any

from mcp.server import Server
from mcp.types import TextContent, Tool

from .shell_executor import ShellExecutor
from .version import __version__

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-shell-server")

app = Server("mcp-shell-server")


class ExecuteToolHandler:
    """Manipulador para execução de comandos shell"""

    name = "shell_execute"
    description = "Execute um comando shell"

    def __init__(self):
        self.executor = ShellExecutor()

    def get_allowed_commands(self) -> list[str]:
        """Obtém os comandos permitidos"""
        return self.executor.validator.get_allowed_commands()

    def get_tool_description(self) -> Tool:
        """Obtém a descrição da ferramenta para o comando execute"""
        return Tool(
            name=self.name,
            description=(
                f"{self.description}\n"
                f"Comandos permitidos: {', '.join(self.get_allowed_commands())}"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Comando e seus argumentos como array",
                    },
                    "stdin": {
                        "type": "string",
                        "description": "Entrada a ser passada para o comando via stdin",
                    },
                    "directory": {
                        "type": "string",
                        "description": "Diretório de trabalho onde o comando será executado",
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Tempo máximo de execução em segundos",
                        "minimum": 0,
                    },
                },
                "required": ["command", "directory"],
            },
        )

    async def run_tool(self, arguments: dict) -> Sequence[TextContent]:
        """Executa o comando shell com os argumentos fornecidos"""
        command = arguments.get("command", [])
        stdin = arguments.get("stdin")
        directory = arguments.get("directory", "/tmp")  # padrão para /tmp por segurança
        timeout = arguments.get("timeout")

        if not command:
            raise ValueError("Nenhum comando fornecido")

        if not isinstance(command, list):
            raise ValueError("'command' deve ser um array")

        # Certifica-se de que o diretório existe
        if not directory:
            raise ValueError("Diretório é obrigatório")

        content: list[TextContent] = []
        try:
            # Trata execução com timeout
            try:
                result = await asyncio.wait_for(
                    self.executor.execute(
                        command, directory, stdin, None
                    ),  # Passa None para timeout
                    timeout=timeout,
                )
            except asyncio.TimeoutError as e:
                raise ValueError("Tempo de execução do comando esgotado") from e

            if result.get("error"):
                raise ValueError(result["error"])

            # Adiciona stdout se presente
            if result.get("stdout"):
                content.append(TextContent(type="text", text=result["stdout"]))

            # Adiciona stderr se presente (filtra mensagens específicas)
            stderr = result.get("stderr")
            if stderr and "cannot set terminal process group" not in stderr:
                content.append(TextContent(type="text", text=stderr))

        except asyncio.TimeoutError as e:
            raise ValueError(
                f"Tempo de execução do comando esgotado após {timeout} segundos"
            ) from e

        return content


# Inicializa manipuladores de ferramentas
tool_handler = ExecuteToolHandler()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Lista ferramentas disponíveis."""
    return [tool_handler.get_tool_description()]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Manipula chamadas de ferramentas"""
    try:
        if name != tool_handler.name:
            raise ValueError(f"Ferramenta desconhecida: {name}")

        if not isinstance(arguments, dict):
            raise ValueError("Argumentos devem ser um dicionário")

        return await tool_handler.run_tool(arguments)

    except Exception as e:
        logger.error(traceback.format_exc())
        raise RuntimeError(f"Erro ao executar comando: {str(e)}") from e


async def main() -> None:
    """Ponto de entrada principal para o servidor MCP shell"""
    logger.info(f"Iniciando servidor MCP shell v{__version__}")
    try:
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream, write_stream, app.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"Erro no servidor: {str(e)}")
        raise
