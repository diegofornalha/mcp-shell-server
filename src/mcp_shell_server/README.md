```markdown
# mcp_shell_server ⚙️

Este projeto implementa um servidor MCP (Modelo de Código Pluggable) que permite a execução segura de comandos de shell em um diretório especificado.

📋 **Sumário**

- [Visão Geral 🔍](#visão-geral-)
- [Componentes 🧱](#componentes-)
    - [server.py 🖥️](#serverpy-)
    - [shell_executor.py 🛠️](#shell_executorpy-)
    - [version.py 🔢](#versionpy-)
- [Requisitos 📦](#requisitos-)
- [Instalação 🚀](#instalação-)
- [Uso 👨‍💻](#uso-)
    - [Executando comandos simples](#executando-comandos-simples)
    - [Executando pipelines](#executando-pipelines)
- [Exemplos 💡](#exemplos-)


## Visão Geral 🔍

O `mcp_shell_server` oferece uma interface para executar comandos de shell remotamente, com foco na segurança e controle.  Ele utiliza a classe `ShellExecutor` para validar os comandos contra uma lista pré-definida e gerenciar a execução, incluindo redirecionamento de E/S e timeouts. A versão atual do software é `0.0.0-dev`, indicando que ainda está em desenvolvimento ativo.


## Componentes 🧱

### server.py 🖥️

Este arquivo contém o código do servidor MCP. Ele escuta por comandos recebidos via stdin, os encaminha para o `ShellExecutor` e retorna a saída (stdout e stderr) para o cliente.

### shell_executor.py 🛠️

Define a classe `ShellExecutor`, responsável pela execução segura de comandos de shell.

- **Funcionalidade:** Valida comandos contra uma lista permitida, executa comandos e pipelines, gerencia timeouts e redireciona entrada/saída.
- **Segurança:** Previne a execução de comandos arbitrários, limitando as ações possíveis a um conjunto predefinido.
- **Tratamento de erros:** Captura e retorna erros de execução, fornecendo informações detalhadas sobre falhas.


### version.py 🔢

Define a versão atual do software: `0.0.0-dev`.


## Requisitos 📦

- Python 3.6+


## Instalação 🚀

1. Clone o repositório: `git clone <URL_DO_REPOSITORIO>`
2. Navegue até o diretório: `cd mcp_shell_server`


## Uso 👨‍💻

### Executando comandos simples

```python
from shell_executor import ShellExecutor

executor = ShellExecutor(allowed_commands=["ls", "pwd", "cat"])
result = executor.execute("ls -l")
print(result.stdout)
print(result.stderr)
```

### Executando pipelines

```python
from shell_executor import ShellExecutor

executor = ShellExecutor(allowed_commands=["ls", "grep", "wc"])
result = executor.execute("ls -l | grep txt | wc -l")
print(result.stdout)
print(result.stderr)
```


## Exemplos 💡

**Exemplo 1: Listando arquivos em um diretório:**

```python
from shell_executor import ShellExecutor

executor = ShellExecutor(allowed_commands=["ls"], working_directory="/tmp")
result = executor.execute("ls -a")
print(result) # Output: CompletedProcess(args='ls -a', returncode=0, stdout='.\n..\n...\n', stderr='')
```

**Exemplo 2: Comando inválido:**

```python
from shell_executor import ShellExecutor

executor = ShellExecutor(allowed_commands=["ls"])
result = executor.execute("rm -rf /") # Comando não permitido
print(result.stderr) # Output: Comando 'rm' não permitido.
```

**Exemplo 3: Timeout:**

```python
from shell_executor import ShellExecutor

executor = ShellExecutor(allowed_commands=["sleep"], timeout=1)
result = executor.execute("sleep 5")
print(result.stderr) # Output: Comando excedeu o tempo limite de 1 segundos.
```
```