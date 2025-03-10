# 📋 Sumário

* [🔍 Visão Geral](#-visão-geral)
* [🧪 Testes](#-testes)
    * [conftest.py](#conftestpy)
    * [test_command_validator.py](#test_command_validatorpy)
    * [test_directory_manager.py](#test_directory_managerpy)
    * [test_process_manager.py](#test_process_managerpy)
    * [test_server.py](#test_serverpy)
    * [test_shell_executor_error_cases.py](#test_shell_executor_error_casespy)
    * [test_shell_executor_new_tests.py](#test_shell_executor_new_testspy)
    * [test_shell_executor_pipe.py](#test_shell_executor_pipepy)
    * [test_shell_executor_pipeline.py](#test_shell_executor_pipelinepy)
    * [test_shell_executor_redirections.py](#test_shell_executor_redirectionspy)
    * [test_shell_executor_redirections.py.bak (backup)](#test_shell_executor_redirectionspybak-backup)
* [⚙️ Instalação e Uso](#️-instalação-e-uso)


## 🔍 Visão Geral

Este diretório contém uma suíte de testes abrangente para garantir a funcionalidade e robustez de um sistema de execução de comandos shell, incluindo validação, gerenciamento de diretórios, processos e tratamento de erros. Os testes utilizam o framework `pytest` e incluem fixtures para facilitar a configuração e simulação de diferentes cenários.

## 🧪 Testes

### conftest.py

Este arquivo define fixtures reutilizáveis para os testes, incluindo mocks para arquivos, gerenciador de processos, executor de shell, diretório temporário e um loop de eventos assíncrono. Essas fixtures simplificam a configuração dos testes e promovem o isolamento.

### test_command_validator.py

Valida a classe `CommandValidator`, que verifica comandos em relação a uma lista de comandos permitidos (definidos por variáveis de ambiente) e a presença de operadores de shell potencialmente perigosos.

```python
# Exemplo: teste para verificar se um comando é permitido
def test_allowed_command(valid_command):
    validator = CommandValidator()
    assert validator.validate(valid_command) is True
```

### test_directory_manager.py

Testa a classe `DirectoryManager`, responsável por validar e resolver caminhos de diretório.

```python
# Exemplo: teste para verificar a resolução de um caminho relativo
def test_relative_path_resolution(temp_dir):
    manager = DirectoryManager()
    resolved_path = manager.resolve_path("subfolder")
    assert resolved_path == os.path.join(temp_dir, "subfolder")
```

### test_process_manager.py

Testa a classe `ProcessManager`, que gerencia a execução de processos e pipelines, incluindo tratamento de timeouts e erros.

```python
# Exemplo: teste para verificar o timeout na execução de um processo
def test_process_timeout(process_manager):
    with pytest.raises(TimeoutExpired):
        process_manager.run_command("sleep 10", timeout=1)
```

### test_server.py

Testa um servidor que executa comandos shell, simulando diferentes cenários com mocks.

### test_shell_executor_error_cases.py

Concentra-se nos cenários de erro da classe `ShellExecutor`, como comandos inválidos, timeouts e falhas na execução.

### test_shell_executor_new_tests.py

Inclui testes adicionais para o `ShellExecutor`, focando em redirecionamentos de entrada/saída, validação de diretórios e timeouts.

### test_shell_executor_pipe.py

Testa a execução de comandos com pipes (|) usando o `ShellExecutor`.

### test_shell_executor_pipeline.py

Testa a execução de pipelines de comandos shell, verificando a divisão correta dos comandos e o tratamento de sucessos, erros e timeouts.

### test_shell_executor_redirections.py

Testa o redirecionamento de entrada e saída (stdin, stdout) no `ShellExecutor`, simulando operações com arquivos.

### test_shell_executor_redirections.py.bak (backup)

Um arquivo de backup contendo testes semelhantes aos de `test_shell_executor_redirections.py`.


## ⚙️ Instalação e Uso

1. **Clone o repositório:**

```bash
git clone <URL_DO_REPOSITORIO>
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt  # Certifique-se de ter um arquivo requirements.txt com as dependências, como pytest
```

3. **Execute os testes:**

```bash
pytest tests/
```


Este README fornece uma visão geral dos testes presentes neste diretório.  Cada arquivo de teste cobre aspectos específicos do sistema de execução de comandos, garantindo sua qualidade e confiabilidade.  A utilização de fixtures e mocks facilita a manutenção e execução dos testes, permitindo simular diferentes cenários e isolar o código testado.