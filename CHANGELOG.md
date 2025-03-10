# Registro de Alterações

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2024-12-23

### Adicionado
- Suporte a shell interativo para execução de comandos

### Alterado
- Mecanismo de detecção de shell de login aprimorado
- Limpeza de processos aprimorada em caso de erro

### Corrigido
- Melhorada a confiabilidade e cobertura de testes
- Corrigidos casos de teste de timeout de pipeline
- Melhorado o tratamento de redirecionamento e testes

## [1.0.2] - 2024-12-18

### Adicionado
- Suporte a redirecionamento de entrada/saída no ShellExecutor
- Capacidades de execução de pipeline
- Tratamento de timeout na comunicação de processos
- Validação de caminho de diretórios

### Alterado
- Mecanismos de limpeza de processos aprimorados
- Organização e configuração de testes aprimoradas
- Padronização do tratamento de erros em todo o código
- Atualizada a dependência do MCP para versão 1.1.2

### Corrigido
- Tratamento adequado de timeout na comunicação de processos
- Tratamento de casos extremos na execução de comandos shell
- Supressão de avisos para saída mais limpa
- Análise e execução de comandos de pipeline

### Segurança
- Validação aprimorada de permissões de diretórios
- Validação e sanitização de comandos aprimorada

## [1.0.1] - 2024-12-12

### Adicionado
- Exibição da versão do servidor nos logs de inicialização

### Alterado
- Sistema de gerenciamento de versão atualizado

## [1.0.0] - 2024-12-12

### Adicionado
- Lançamento inicial
- Execução básica de comandos shell via protocolo MCP
- Funcionalidade de lista branca de comandos
- Suporte a entrada padrão
- Controle de timeout de execução de comandos
- Especificação de diretório de trabalho
- Tratamento abrangente de saída (stdout, stderr, status)
- Validação de operadores shell
- Medidas básicas de segurança
- Fluxos de trabalho do GitHub Actions para testes e publicação
