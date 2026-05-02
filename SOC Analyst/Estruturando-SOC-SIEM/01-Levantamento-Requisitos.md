# Levantamento de Requisitos

## Por que essa etapa é a mais importante?

Antes de falar em ferramenta, fornecedor ou preço, eu preciso entender o ambiente que vou monitorar. Sem isso, qualquer SIEM vai ser mal dimensionado - caro demais, com alertas errados e cobrindo o que não precisa ser coberto.

O objetivo aqui é entender o ambiente atual, identificar as necessidades reais de segurança, as restrições técnicas e operacionais, e definir os critérios que vão guiar todo o projeto.

---

## As perguntas que não podem ficar sem resposta

- Quais eventos precisam ser monitorados?
- Quais sistemas críticos precisam estar no radar do SOC?
- Quais métricas e SLAs o SOC deverá cumprir?
- Como será a escalação funcional de atendimento?
- O SOC será interno, terceirizado ou híbrido?
- Qual o volume de logs esperado? (EPS — Events Per Second)
- Qual o período de retenção de logs necessário?
- Existem requisitos de compliance que precisam ser atendidos?

---

## Inventário do ambiente

Antes de qualquer coisa, preciso saber o que existe:

| Categoria | O que mapear |
|-----------|-------------|
| Ativos críticos | Servidores, bancos de dados, aplicações core |
| Fontes de log | Firewalls, EDR, AD, proxies, cloud, aplicações |
| Volume de dados | Estimativa de EPS (Events Per Second) por fonte |
| Rede | Segmentação, zonas DMZ, ambientes cloud |
| Usuários | Quantidade, perfis, usuários privilegiados |
| Endpoints | SO, versão, cobertura de agentes |

> 💡 O EPS é fundamental para dimensionar o licenciamento do SIEM. Subestimar esse número é um erro clássico que gera custos inesperados no meio do contrato.

---

## Requisitos de compliance

Compliance não é opcional - ele frequentemente define o que precisa ser monitorado, por quanto tempo os logs precisam ser retidos e quais relatórios precisam estar disponíveis.

| Framework | Exigência relevante para o SOC |
|-----------|-------------------------------|
| **LGPD** | Monitorar acessos a dados pessoais, registrar incidentes |
| **PCI-DSS** | Logs de acesso ao ambiente de cartões, retenção de 1 ano |
| **ISO 27001** | Gestão de incidentes, evidências para auditoria |
| **SOX** | Trilha de auditoria para sistemas financeiros |
| **NIST CSF** | Identificar, proteger, detectar, responder, recuperar |

---

## Definição dos SLAs

Sem SLA definido, não tem como cobrar do fornecedor nem da equipe interna. Exemplos de SLA por criticidade:

| Criticidade | Tempo para triagem | Tempo para resposta |
|-------------|-------------------|-------------------|
| Crítico | 15 minutos | 1 hora |
| Alto | 30 minutos | 4 horas |
| Médio | 2 horas | 24 horas |
| Baixo | 8 horas | 72 horas |

---

## Estrutura do SOC - tiers de atendimento

A escalação funcional precisa estar clara antes de contratar qualquer coisa:

```
[N1 — Analista de Monitoramento / Analista de SOC]
  → Triagem de alertas, classificação inicial, abertura de tickets
  → Escalona para N2 se não conseguir resolver

[N2 — Analista de Segurança]
  → Investigação aprofundada, correlação de eventos, contenção inicial
  → Escalona para N3 em incidentes críticos ou complexos

[N3 — Especialista / Threat Hunter / Incident Response]
  → Resposta a incidentes críticos, análise forense, caça a ameaças avançadas
  → Também responsável pelo tuning das regras de detecção
```

---

## Resultado esperado dessa etapa

Ao final do levantamento, eu devo ter em mãos:

- Inventário de ativos e fontes de log priorizados
- Estimativa de EPS por ambiente
- Requisitos de compliance documentados
- SLAs definidos por criticidade
- Modelo de escalação aprovado pelas partes interessadas
- Lista de use cases prioritários para o SOC monitorar

Só com isso em mãos faz sentido avançar para a definição de arquitetura.
