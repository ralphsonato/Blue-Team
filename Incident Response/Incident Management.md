# Gerenciamento de Incidentes de Segurança

## O básico que não pode faltar
 
Segurança da informação se resume a três palavras: **confidencialidade, integridade e disponibilidade** a famosa tríade CIA. Quando qualquer uma delas é comprometida de forma inesperada e com impacto real no negócio, temos um incidente de segurança.
 
Gerenciamento de incidentes é o processo de identificar, conter, erradicar e aprender com esses incidentes. O objetivo é duplo: minimizar o impacto no negócio e evitar que a mesma coisa aconteça de novo.
 
---
## Frameworks de referência: NIST vs SANS
 
Os dois frameworks mais usados para incident response são muito parecidos. A diferença principal é que o SANS separa em fases distintas o que o NIST agrupa em uma só.
 
| NIST | SANS |
|---|---|
| 1. Preparação | 1. Preparação |
| 2. Detecção e análise | 2. Identificação |
| 3. Contenção, Erradicação e Recuperação | 3. Contenção |
| | 4. Erradicação |
| | 5. Recuperação |
| 4. Atividades pós-incidente | 6. Lições aprendidas |
 
Na essência, é a mesma coisa. Escolha o que fizer mais sentido pro seu contexto.
 
---
## As 4 fases (NIST)
 
### 1. Preparação
 
Tudo que a empresa faz **antes** do incidente acontecer. Políticas, planos, treinamentos, ferramentas, baselines de comportamento normal. Se você não se preparou, vai improvisar - e improvisar durante um incidente é receita pra desastre.
 
### 2. Detecção e análise
 
A fase mais desafiadora. O monitoramento do ambiente busca sinais de que algo está errado. Logs bem configurados e um SIEM fazendo correlação são fundamentais aqui.

Perguntas que precisam ser respondidas:
 
- Qual foi o vetor de ataque inicial?
- O atacante está explorando vulnerabilidades?
- Está havendo escalação de privilégios?
- Existe persistência no ambiente?
- Há movimentação lateral?
 
O **MITRE ATT&CK** é uma ferramenta essencial nessa fase pra mapear as TTPs (Táticas, Técnicas e Procedimentos) do atacante.
 
### 3. Contenção, Erradicação e Recuperação
 
**Contenção** - parar o sangramento. Impedir que o incidente se espalhe. A estratégia depende do cenário: pode ser isolar um host, bloquear um IP, desativar uma conta.
 
**Erradicação** - remover a ameaça do ambiente. Eliminar malware, fechar as portas de entrada, neutralizar vetores de ataque.
 
**Recuperação** - restaurar a capacidade operacional mínima para o negócio continuar. Importante: recuperação aqui não significa "voltou tudo ao normal". Significa que o essencial está funcionando.
 
### 4. Atividades pós-incidente / Lições aprendidas
 
Documentar tudo: cronologia dos fatos, ações tomadas, causa raiz. Sem essa fase, você vai cometer os mesmos erros. O relatório pós-incidente não é burocracia - é investimento.
 
---
