# MCP Shell Server

[![codecov](https://codecov.io/gh/tumf/mcp-shell-server/branch/main/graph/badge.svg)](https://codecov.io/gh/tumf/mcp-shell-server)

Um servidor seguro para execução de comandos shell que implementa o Protocolo de Contexto de Modelo (MCP). Este servidor permite a execução remota de comandos shell autorizados com suporte para entrada via stdin.

## Funcionalidades

* **Execução Segura de Comandos**: Apenas comandos autorizados podem ser executados
* **Suporte para Entrada Padrão**: Passa entrada para comandos via stdin
* **Saída Abrangente**: Retorna stdout, stderr, código de saída e tempo de execução
* **Segurança com Operadores Shell**: Valida comandos após operadores shell (;, &&, ||, |)
* **Controle de Timeout**: Define tempo máximo de execução para comandos

## Configuração do cliente MCP no seu Claude.app

### Versão publicada

```shell
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

```json
{
  "mcpServers": {
    "shell": {
      "command": "uvx",
      "args": [
        "mcp-shell-server"
      ],
      "env": {
        "ALLOW_COMMANDS": "ls,cat,pwd,grep,wc,touch,find"
      }
    },
  }
}
```

### Versão local

#### Configuração

```shell
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

```json
{
  "mcpServers": {
    "shell": {
      "command": "uv",
      "args": [
        "--directory",
        ".",
        "run",
        "mcp-shell-server"
      ],
      "env": {
        "ALLOW_COMMANDS": "ls,cat,pwd,grep,wc,touch,find"
      }
    },
  }
}
```

#### Instalação

```bash
pip install mcp-shell-server
```

## Uso

### Iniciando o Servidor

```bash
ALLOW_COMMANDS="ls,cat,echo" uvx mcp-shell-server
# Ou usando o alias
ALLOWED_COMMANDS="ls,cat,echo" uvx mcp-shell-server
```

A variável de ambiente `ALLOW_COMMANDS` (ou seu alias `ALLOWED_COMMANDS`) especifica quais comandos podem ser executados. Comandos podem ser separados por vírgulas com espaços opcionais ao redor deles.

Formatos válidos para ALLOW_COMMANDS ou ALLOWED_COMMANDS:

```bash
ALLOW_COMMANDS="ls,cat,echo"          # Formato básico
ALLOWED_COMMANDS="ls ,echo, cat"      # Com espaços (usando alias)
ALLOW_COMMANDS="ls,  cat  , echo"     # Múltiplos espaços
```

### Formato da Requisição

```python
# Execução básica de comando
{
    "command": ["ls", "-l", "/tmp"]
}

# Comando com entrada stdin
{
    "command": ["cat"],
    "stdin": "Hello, World!"
}

# Comando com timeout
{
    "command": ["long-running-process"],
    "timeout": 30  # Tempo máximo de execução em segundos
}

# Comando com diretório de trabalho e timeout
{
    "command": ["grep", "-r", "pattern"],
    "directory": "/path/to/search",
    "timeout": 60
}
```

### Formato da Resposta

Resposta de sucesso:

```json
{
    "stdout": "saída do comando",
    "stderr": "",
    "status": 0,
    "execution_time": 0.123
}
```

Resposta de erro:

```json
{
    "error": "Comando não permitido: rm",
    "status": 1,
    "stdout": "",
    "stderr": "Comando não permitido: rm",
    "execution_time": 0
}
```

## Segurança

O servidor implementa várias medidas de segurança:

1. **Lista Branca de Comandos**: Apenas comandos explicitamente permitidos podem ser executados
2. **Validação de Operadores Shell**: Comandos após operadores shell (;, &&, ||, |) também são validados contra a lista branca
3. **Sem Injeção de Shell**: Comandos são executados diretamente sem interpretação do shell

## Desenvolvimento

### Configurando o Ambiente de Desenvolvimento

1. Clone o repositório

```bash
git clone https://github.com/yourusername/mcp-shell-server.git
cd mcp-shell-server
```

2. Instale dependências incluindo requisitos de teste

```bash
pip install -e ".[test]"
```

### Executando Testes

```bash
pytest
```

## Referência da API

### Argumentos da Requisição

| Campo     | Tipo       | Obrigatório | Descrição                                    |
|-----------|------------|-------------|----------------------------------------------|
| command   | string[]   | Sim         | Comando e seus argumentos como elementos de array |
| stdin     | string     | Não         | Entrada a ser passada para o comando         |
| directory | string     | Não         | Diretório de trabalho para execução do comando |
| timeout   | integer    | Não         | Tempo máximo de execução em segundos         |

### Campos da Resposta

| Campo          | Tipo    | Descrição                                  |
|----------------|---------|---------------------------------------------|
| stdout         | string  | Saída padrão do comando                    |
| stderr         | string  | Saída de erro do comando                   |
| status         | integer | Código de status de saída                  |
| execution_time | float   | Tempo gasto para executar (em segundos)    |
| error          | string  | Mensagem de erro (presente apenas se falhou) |

## Requisitos

* Python 3.11 ou superior
* mcp>=1.1.0

## Licença

Licença MIT - Veja o arquivo LICENSE para detalhes
