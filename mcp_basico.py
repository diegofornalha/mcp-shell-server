import streamlit as st
import json
import subprocess
import time
import os
import platform
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="MCP Shell Demo", page_icon="🔒")

# Título da aplicação
st.title("MCP Shell Server - Demonstração Básica")
st.write("Uma demonstração simples do MCP Shell Server")

# Informações do sistema
st.sidebar.header("Informações do Sistema")
st.sidebar.write(f"**Sistema:** {platform.system()} {platform.release()}")
st.sidebar.write(f"**Python:** {platform.python_version()}")
st.sidebar.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Seções da aplicação
tab1, tab2 = st.tabs(["O que é o MCP Shell?", "Executor de Comandos"])

with tab1:
    st.header("O que é o MCP Shell Server?")
    
    st.write("""
    O MCP Shell Server é um servidor seguro para execução de comandos shell que implementa 
    o Protocolo de Contexto de Modelo (MCP). Este servidor permite que assistentes de IA 
    como o Claude executem comandos shell no sistema de forma segura e controlada.
    
    O protocolo MCP (Model Context Protocol) foi desenvolvido pela Anthropic para permitir 
    que o Claude se comunique com serviços externos e execute ações no sistema operacional.
    """)
    
    st.subheader("Principais Características:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        **Segurança:**
        - Lista branca de comandos
        - Validação de operadores shell
        - Execução sem interpretação shell
        """)
    
    with col2:
        st.write("""
        **Controle:**
        - Definição de comandos permitidos
        - Controle de timeout
        - Diretórios restritos
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

with tab2:
    st.header("Experimentando a Execução de Comandos")
    
    st.write("Esta seção simula o funcionamento do MCP Shell Server.")
    
    # Definir comandos permitidos para demonstração
    allowed_commands = st.multiselect(
        "Comandos permitidos para teste:",
        ["ls", "cat", "pwd", "grep", "wc", "touch", "find", "echo", "ps"],
        default=["ls", "cat", "pwd", "echo"]
    )
    
    # Input para comando
    command_input = st.text_input("Digite um comando para testar:")
    
    # Parsing do comando
    if command_input:
        command_parts = command_input.split()
        base_command = command_parts[0] if command_parts else ""
        
        # Validação do comando base
        if base_command in allowed_commands:
            st.success(f"✅ Comando permitido: '{base_command}'")
            
            # Executar o comando
            if st.button("Executar Comando"):
                try:
                    with st.spinner("Executando comando..."):
                        start_time = time.time()
                        result = subprocess.run(
                            command_parts, 
                            capture_output=True, 
                            text=True,
                            timeout=5
                        )
                        execution_time = time.time() - start_time
                    
                    # Mostrar resultado
                    output = {
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "status": result.returncode,
                        "execution_time": execution_time
                    }
                    
                    st.subheader("Resultado:")
                    st.json(output)
                    
                    if result.stdout:
                        st.subheader("Saída:")
                        st.code(result.stdout)
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        else:
            st.error(f"❌ Comando não permitido: '{base_command}'")
            
            # Simular erro
            if st.button("Simular Resposta de Erro"):
                error_response = {
                    "error": f"Comando não permitido: {base_command}",
                    "status": 1,
                    "stdout": "",
                    "stderr": f"Comando não permitido: {base_command}",
                    "execution_time": 0
                }
                st.json(error_response)

# Rodapé
st.markdown("---")
st.markdown("MCP Shell Server - Demonstração Básica") 