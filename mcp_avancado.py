import streamlit as st
import json
import subprocess
import time
import os
import shlex
import platform
from datetime import datetime

# Classes inspiradas no MCP Shell Server para validação e segurança
class CommandValidator:
    """Simula a validação de comandos do MCP Shell Server"""
    
    def __init__(self, allowed_commands=None):
        self.allowed_commands = allowed_commands or []
        
    def is_command_allowed(self, command):
        """Verifica se um comando está na lista de permitidos"""
        return command in self.allowed_commands
    
    def validate_no_shell_operators(self, command_str):
        """Detecta operadores shell perigosos"""
        shell_operators = [';', '&&', '||', '|', '>', '>>', '<', '<<']
        found_operators = []
        
        for op in shell_operators:
            if op in command_str:
                found_operators.append(op)
                
        return found_operators
    
    def validate_command(self, command_parts):
        """Valida um comando completo"""
        if not command_parts:
            return False, "Comando vazio"
            
        base_command = command_parts[0]
        if not self.is_command_allowed(base_command):
            return False, f"Comando não permitido: {base_command}"
            
        # Verificar operadores shell no comando completo
        command_str = ' '.join(command_parts)
        found_operators = self.validate_no_shell_operators(command_str)
        
        if found_operators:
            return False, f"Operadores shell não permitidos: {', '.join(found_operators)}"
            
        return True, ""

class DirectoryManager:
    """Gerencia e valida diretórios de trabalho"""
    
    def validate_directory(self, directory):
        """Valida se um diretório existe e tem permissões"""
        if not directory:
            return False, "Diretório não especificado"
            
        if not os.path.exists(directory):
            return False, f"Diretório não existe: {directory}"
            
        if not os.path.isdir(directory):
            return False, f"Não é um diretório: {directory}"
            
        if not os.access(directory, os.R_OK | os.W_OK | os.X_OK):
            return False, f"Permissões insuficientes para: {directory}"
            
        return True, ""

class ShellExecutor:
    """Simula o executor shell do MCP"""
    
    def __init__(self, validator, directory_manager):
        self.validator = validator
        self.directory_manager = directory_manager
        
    def execute(self, command_parts, directory, stdin=None, timeout=None):
        """Executa um comando shell de forma segura"""
        # Validar comando
        valid_cmd, cmd_error = self.validator.validate_command(command_parts)
        if not valid_cmd:
            return {
                "error": cmd_error,
                "status": 1,
                "stdout": "",
                "stderr": cmd_error,
                "execution_time": 0
            }
            
        # Validar diretório
        valid_dir, dir_error = self.directory_manager.validate_directory(directory)
        if not valid_dir:
            return {
                "error": dir_error,
                "status": 1,
                "stdout": "",
                "stderr": dir_error,
                "execution_time": 0
            }
            
        # Executar comando
        try:
            start_time = time.time()
            
            # Preparar processo para entrada stdin se necessário
            if stdin:
                proc = subprocess.run(
                    command_parts,
                    input=stdin,
                    text=True,
                    capture_output=True,
                    timeout=timeout,
                    cwd=directory
                )
            else:
                proc = subprocess.run(
                    command_parts,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=directory
                )
                
            execution_time = time.time() - start_time
            
            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "status": proc.returncode,
                "execution_time": execution_time
            }
            
        except subprocess.TimeoutExpired:
            return {
                "error": f"Comando excedeu o tempo limite de {timeout} segundos",
                "status": 1,
                "stdout": "",
                "stderr": f"Timeout após {timeout}s",
                "execution_time": timeout
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": 1,
                "stdout": "",
                "stderr": str(e),
                "execution_time": time.time() - start_time
            }

# Configuração da página
st.set_page_config(
    page_title="MCP Shell Server Avançado",
    page_icon="🔒",
    layout="wide"
)

# Título da aplicação
st.title("MCP Shell Server - Demonstração Avançada")
st.write("Uma implementação mais robusta inspirada no código real do MCP Shell Server")

# Sidebar com informações do sistema
st.sidebar.header("Informações do Sistema")
st.sidebar.write(f"**Sistema:** {platform.system()} {platform.release()}")
st.sidebar.write(f"**Python:** {platform.python_version()}")
st.sidebar.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Modo de depuração
debug_mode = st.sidebar.checkbox("Modo de depuração")

# Tabs principais
tabs = st.tabs([
    "O que é o MCP Shell?", 
    "Executor de Comandos", 
    "Validação de Comandos", 
    "Configuração"
])

# Tab 1: O que é o MCP Shell?
with tabs[0]:
    st.header("O que é o MCP Shell Server?")
    
    st.write("""
    O MCP Shell Server é um servidor seguro para execução de comandos shell que implementa 
    o Protocolo de Contexto de Modelo (MCP). Este servidor permite que assistentes de IA 
    como o Claude executem comandos shell no sistema de forma segura e controlada.
    
    O protocolo MCP (Model Context Protocol) foi desenvolvido pela Anthropic para permitir 
    que o Claude se comunique com serviços externos e execute ações no sistema operacional.
    """)
    
    st.subheader("Arquitetura do MCP Shell Server")
    
    st.write("""
    O MCP Shell Server é composto por vários componentes que garantem segurança e flexibilidade:
    
    1. **CommandValidator**: Valida comandos contra uma lista de permitidos e detecta operadores shell perigosos.
    2. **DirectoryManager**: Gerencia e valida diretórios de trabalho.
    3. **ShellExecutor**: Executa comandos shell de forma segura.
    4. **IORedirectionHandler**: Lida com redirecionamento de entrada/saída.
    5. **ProcessManager**: Gerencia processos e tempo de execução.
    """)
    
    st.subheader("Exemplo de Configuração")
    
    config_json = {
      "mcpServers": {
        "shell": {
          "command": "uvx",
          "args": ["mcp-shell-server"],
          "env": {
            "ALLOW_COMMANDS": "ls,cat,pwd,grep,wc,touch,find"
          }
        }
      }
    }
    
    st.code(json.dumps(config_json, indent=2), language="json")

# Tab 2: Executor de Comandos
with tabs[1]:
    st.header("Executor de Comandos Avançado")
    
    st.write("""
    Esta seção implementa um simulador mais fiel do MCP Shell Server, 
    com validações e execução de comandos mais robustas.
    """)
    
    # Definir comandos permitidos
    allowed_commands = st.multiselect(
        "Comandos permitidos para teste:",
        ["ls", "cat", "pwd", "grep", "wc", "touch", "find", "echo", "ps", "date"],
        default=["ls", "cat", "pwd", "echo"]
    )
    
    # Configurações avançadas
    with st.expander("Configurações avançadas"):
        col1, col2 = st.columns(2)
        
        with col1:
            directory = st.text_input(
                "Diretório de trabalho:", 
                value=os.getcwd(),
                help="Diretório onde o comando será executado"
            )
            
        with col2:
            timeout = st.slider(
                "Timeout (segundos):", 
                min_value=1, 
                max_value=30, 
                value=5,
                help="Tempo máximo de execução do comando"
            )
            
        stdin_input = st.text_area(
            "Entrada (stdin):",
            value="",
            help="Texto a ser passado como entrada para o comando"
        )
    
    # Input para comando
    st.subheader("Digite um comando para executar:")
    command_input = st.text_input("Comando:")
    
    # Parsing e validação do comando
    if command_input:
        # Inicializar validador e executor
        validator = CommandValidator(allowed_commands)
        dir_manager = DirectoryManager()
        executor = ShellExecutor(validator, dir_manager)
        
        # Processar comando
        try:
            # Parse do comando respeitando aspas
            command_parts = shlex.split(command_input)
            base_command = command_parts[0] if command_parts else ""
            
            # Blocos de validação e feedback
            st.subheader("Análise do Comando:")
            
            # Validação do comando base
            if validator.is_command_allowed(base_command):
                st.success(f"✅ Comando base permitido: '{base_command}'")
            else:
                st.error(f"❌ Comando base não permitido: '{base_command}'")
            
            # Validação de operadores shell
            operators = validator.validate_no_shell_operators(command_input)
            if operators:
                st.warning(f"⚠️ Operadores shell detectados: {', '.join(operators)}")
            else:
                st.success("✅ Nenhum operador shell detectado")
            
            # Validação do diretório
            valid_dir, dir_message = dir_manager.validate_directory(directory)
            if valid_dir:
                st.success(f"✅ Diretório válido: '{directory}'")
            else:
                st.error(f"❌ Problema com diretório: {dir_message}")
                
            # Estrutura da requisição
            st.subheader("Estrutura da requisição:")
            request = {
                "command": command_parts,
                "directory": directory,
                "timeout": timeout
            }
            if stdin_input:
                request["stdin"] = stdin_input
                
            st.json(request)
            
            # Verificar se pode executar
            valid_cmd, cmd_message = validator.validate_command(command_parts)
            can_execute = valid_cmd and valid_dir
            
            # Botão de execução
            if can_execute:
                if st.button("Executar Comando"):
                    with st.spinner(f"Executando '{command_input}' com timeout de {timeout}s..."):
                        # Executar comando
                        result = executor.execute(
                            command_parts,
                            directory,
                            stdin_input if stdin_input else None,
                            timeout
                        )
                        
                    # Mostrar resultado
                    st.subheader("Resultado da Execução:")
                    st.json(result)
                    
                    # Mostrar saída se houver
                    if result.get("stdout"):
                        st.subheader("Saída (stdout):")
                        st.code(result["stdout"])
                        
                    # Mostrar erro se houver
                    if result.get("stderr"):
                        st.subheader("Erro (stderr):")
                        st.code(result["stderr"])
                        
                    # Modo de depuração
                    if debug_mode:
                        st.subheader("Informações de Depuração:")
                        st.json({
                            "command_parts": command_parts,
                            "base_command": base_command,
                            "valid_dir": valid_dir,
                            "dir_message": dir_message,
                            "valid_cmd": valid_cmd,
                            "cmd_message": cmd_message,
                            "operators": operators,
                            "execution_time": result.get("execution_time")
                        })
            else:
                if st.button("Simular Resposta de Erro"):
                    error_msg = cmd_message if not valid_cmd else dir_message
                    error_response = {
                        "error": error_msg,
                        "status": 1,
                        "stdout": "",
                        "stderr": error_msg,
                        "execution_time": 0
                    }
                    st.subheader("Resposta de Erro Simulada:")
                    st.json(error_response)
        
        except Exception as e:
            st.error(f"Erro ao processar comando: {str(e)}")
            if debug_mode:
                st.exception(e)

# Tab 3: Validação de Comandos
with tabs[2]:
    st.header("Validação de Comandos")
    
    st.write("""
    Esta seção permite testar a validação de comandos sem executá-los.
    Você pode ver como o MCP Shell Server valida comandos para garantir a segurança.
    """)
    
    # Lista de comandos permitidos para teste
    test_allowed_commands = st.multiselect(
        "Comandos permitidos para validação:",
        ["ls", "cat", "pwd", "grep", "wc", "touch", "find", "echo", "ps", "rm", "chmod"],
        default=["ls", "cat", "pwd", "echo"]
    )
    
    # Campo para testar validação
    test_command = st.text_input("Digite um comando para validar:")
    
    if test_command:
        # Inicializar validador
        test_validator = CommandValidator(test_allowed_commands)
        
        st.subheader("Resultado da Validação:")
        
        try:
            # Parse do comando respeitando aspas
            test_parts = shlex.split(test_command)
            test_base = test_parts[0] if test_parts else ""
            
            # Feedback visual
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Validação do Comando Base:**")
                if test_validator.is_command_allowed(test_base):
                    st.success(f"✅ Comando base permitido: '{test_base}'")
                else:
                    st.error(f"❌ Comando base não permitido: '{test_base}'")
                
                st.write("**Verificação de Operadores Shell:**")
                operators = test_validator.validate_no_shell_operators(test_command)
                if operators:
                    st.warning(f"⚠️ Operadores shell detectados: {', '.join(operators)}")
                else:
                    st.success("✅ Nenhum operador shell detectado")
            
            with col2:
                st.write("**Validação Completa:**")
                valid, message = test_validator.validate_command(test_parts)
                if valid:
                    st.success("✅ Comando válido")
                else:
                    st.error(f"❌ Comando inválido: {message}")
                
                st.write("**Detalhes do Comando:**")
                st.json({
                    "comando_original": test_command,
                    "comando_parseado": test_parts,
                    "comando_base": test_base,
                    "operadores_detectados": operators,
                    "é_válido": valid,
                    "mensagem": message or "Comando válido"
                })
                
            # Exemplos de validação
            with st.expander("Exemplos de Validação"):
                st.write("""
                **Exemplos de como a validação funciona:**
                
                1. **Comando base não permitido**: `rm -rf /` - Falha porque 'rm' não está na lista de permitidos.
                2. **Operadores shell**: `ls && cat file.txt` - Falha devido ao operador '&&'.
                3. **Comando vazio**: `  ` - Falha porque o comando está vazio.
                4. **Comando válido**: `ls -la` - Passa se 'ls' estiver na lista de permitidos.
                """)
                
        except Exception as e:
            st.error(f"Erro ao validar comando: {str(e)}")
            if debug_mode:
                st.exception(e)

# Tab 4: Configuração
with tabs[3]:
    st.header("Configuração do MCP Shell Server")
    
    st.write("""
    Esta seção mostra como configurar o MCP Shell Server para uso com o Claude.
    Você pode personalizar a lista de comandos permitidos e outros parâmetros.
    """)
    
    # Lista de comandos permitidos
    config_allowed_commands = st.multiselect(
        "Selecione os comandos a serem permitidos:",
        ["ls", "cat", "pwd", "grep", "wc", "touch", "find", "echo", "ps", "date", 
         "mkdir", "rm", "cp", "mv", "chmod", "chown", "curl", "wget", "head", "tail"],
        default=["ls", "cat", "pwd", "grep", "wc", "touch", "find"]
    )
    
    # Aviso sobre comandos perigosos
    dangerous_commands = ["rm", "chmod", "chown"]
    selected_dangerous = [cmd for cmd in config_allowed_commands if cmd in dangerous_commands]
    
    if selected_dangerous:
        st.warning(f"""
        ⚠️ **Atenção:** Você selecionou os seguintes comandos potencialmente perigosos:
        **{', '.join(selected_dangerous)}**
        
        Estes comandos podem modificar ou remover arquivos e permissões. Use com cuidado!
        """)
    
    # Configuração do Claude Desktop
    st.subheader("Configuração para o Claude Desktop")
    
    config_json = {
      "mcpServers": {
        "shell": {
          "command": "uvx",
          "args": ["mcp-shell-server"],
          "env": {
            "ALLOW_COMMANDS": ",".join(config_allowed_commands)
          }
        }
      }
    }
    
    st.code(json.dumps(config_json, indent=2), language="json")
    
    st.info("""
    Para configurar o Claude Desktop:
    
    1. Edite o arquivo de configuração:
       - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
       - Windows: `%APPDATA%\\Claude\\claude_desktop_config.json`
       
    2. Cole o JSON acima no arquivo.
    
    3. Instale o MCP Shell Server via pip:
       ```
       pip install mcp-shell-server
       ```
       
    4. Reinicie o Claude Desktop.
    """)
    
    # Variáveis de ambiente
    st.subheader("Variáveis de Ambiente")
    
    env_vars = f"ALLOW_COMMANDS=\"{','.join(config_allowed_commands)}\""
    
    st.code(f"""
    # Para iniciar o servidor manualmente:
    {env_vars} uvx mcp-shell-server
    
    # Ou usando pip:
    {env_vars} python -m mcp_shell_server
    """, language="bash")
    
    # Dicas de segurança
    with st.expander("Dicas de Segurança"):
        st.write("""
        **Recomendações de segurança:**
        
        1. **Princípio do menor privilégio**: Permita apenas os comandos estritamente necessários.
        
        2. **Evite comandos destrutivos**: Comandos como `rm` podem excluir dados importantes.
        
        3. **Teste em ambiente controlado**: Antes de usar em produção, teste em um ambiente seguro.
        
        4. **Monitore a execução**: Mantenha um registro dos comandos executados.
        
        5. **Atualize regularmente**: Mantenha o MCP Shell Server atualizado para receber correções de segurança.
        """)

# Rodapé
st.markdown("---")
st.markdown("MCP Shell Server - Demonstração Avançada | Baseada no código real do MCP Shell Server") 