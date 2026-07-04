# Papéis e Responsabilidades

## Os três tiers de analista

A estrutura clássica de SOC segue uma escalação por tier e cada nível resolve o que consegue e escala o que não consegue:

```
SOC Manager
             
Tier 3 - Threat Hunters / Forense
              
Tier 2 - Incident Responders
              
Tier 1 - Analistas
```

### Tier 1 - Primeira linha de defesa

- Monitora continuamente dashboards e alertas (ex: alertas do SIEM)
- Faz a triagem inicial: o alerta é legítimo ou falso positivo?
- Resolve o que é simples (falso alarme, evento benigno conhecido) e documenta
- Escala para o Tier 2 quando precisa de investigação mais profunda ou privilégios maiores

É o cargo de entrada mais comum em SOC, e onde a maioria dos analistas júnior começa.

### Tier 2 - respondedores de incidente

- Investiga os alertas escalados pelo Tier 1 e confirma se realmente é um incidente
- Faz análise mais aprofundada para entender escopo e impacto
- Toma as ações de resposta necessárias e inicia a remediação
- Coordena com a equipe de TI para resolver o incidente e coletar informação adicional

### Tier 3 - Threat Hunters e Especialistas Forenses

- Trata os incidentes mais complexos e avançados
- Caça ameaças proativamente (Threat Hunting), procura o que não gerou alerta nenhum
- Faz análise forense profunda para achar a causa raiz do ataque
- Melhora a capacidade de detecção do SOC: cria novos use cases, ajusta controles de segurança, mentora analistas júnior

> Esse último ponto é o que mais me chama atenção nessa trilha: T3 não é só "resolver o incidente mais difícil", é também quem retroalimenta o sistema, é a mesma lógica de ciclo de vida de use case que documentei em `SIEM/Use Cases.md`.

---

## Outros papéis dentro do SOC

| Papel | Função |
|-------|--------|
| Threat Intelligence Analyst | Foca em dados externos de ameaça (novas táticas, IOCs) para alimentar o time do SOC |
| SOC Engineer/Architect | Administra e ajusta as ferramentas (SIEM, IDS) e a infraestrutura que sustenta o SOC |
| Incident Coordinator | Em SOCs maiores, gerencia comunicação e fluxo de trabalho durante incidentes grandes |
| Malware Analyst / Compliance Specialist | Em organizações maiores, funções de suporte dedicadas dentro do próprio SOC |

---

## SOC Manager

Lidera o time, garante cobertura 24/7 e que os procedimentos sejam seguidos corretamente. Supervisiona o tratamento de incidentes e aprova ações de resposta significativas. Acompanha métricas de segurança e reporta a performance do SOC. É responsável por staffing, treinamento e melhoria contínua das operações e tecnologias do SOC.
