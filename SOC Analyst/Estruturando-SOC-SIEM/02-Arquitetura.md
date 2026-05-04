# Definindo a Arquitetura

## Por que definir arquitetura antes de escolher fornecedor?

A arquitetura não é detalhe técnico, ela define custo, escalabilidade e o que é possível fazer. Ir para o mercado sem ter isso definido significa receber propostas incomparáveis entre si.

---

## Modelos de implantação

### On-Premise

O SIEM fica dentro da infraestrutura da empresa.

**Prós:**
- Controle total dos dados
- Sem custo variável por volume de log
- Melhor para ambientes com restrições regulatórias severas

**Contras:**
- Alto custo de hardware e manutenção
- Escalabilidade mais lenta
- Exige equipe interna qualificada para sustentar

**Quando faz sentido:** ambientes com dados altamente sensíveis, restrições legais que impedem dado em nuvem, ou organizações com infraestrutura robusta já instalada.

---

### Cloud (SaaS)

O SIEM é um serviço consumido na nuvem. Exemplos: Microsoft Sentinel, Google Chronicle, Splunk Cloud.

**Prós:**
- Deploy rápido
- Escalabilidade automática
- Atualizações e manutenção por conta do fornecedor

**Contras:**
- Custo atrelado ao volume de dados ingeridos
- Dependência do provedor
- Latência na ingestão de logs de ambientes on-premise

**Quando faz sentido:** organizações cloud-first, ambientes dinâmicos com volume variável de logs, ou quando não há equipe para sustentar infraestrutura interna.

---

### Híbrido

Parte on-premise, parte cloud. Comum em organizações que estão em processo de migração ou que têm dados sensíveis misturados com sistemas cloud.

**Desafio principal:** garantir a integração entre os dois ambientes sem criar pontos cegos na visibilidade.

---

## SIEM + SOAR - a combinação que faz diferença

SIEM detecta. SOAR responde. Trabalhar com os dois juntos é o padrão atual do mercado para SOCs maduros.

| | SIEM | SOAR |
|--|------|------|
| Função | Coleta, correlaciona e alerta | Orquestra e automatiza a resposta |
| Entrada | Logs e eventos | Alertas do SIEM e outras fontes |
| Saída | Alertas priorizados | Ações automáticas (bloquear IP, isolar endpoint, abrir ticket) |
| Exemplo | Splunk, Sentinel, QRadar | Palo Alto XSOAR, Splunk SOAR, IBM Resilient |

> Um SOC sem automação de resposta fica preso em triagem manual. O analista passa o dia fechando falsos positivos em vez de caçar ameaças reais.

---

## Arquitetura de coleta de logs

Como os logs chegam até o SIEM:

```
[Fontes de log]
    │
    ├── Agentes instalados nos endpoints (EDR, Sysmon)
    ├── Syslog (firewalls, switches, servidores Linux)
    ├── API (Office 365, AWS CloudTrail, Azure AD)
    ├── JDBC/ODBC (bancos de dados)
    └── Coletores intermediários (Logstash, Cribl, NXLog)
                │
         [Broker / Buffer]
         (Kafka, Redis — para ambientes de alto volume)
                │
            [SIEM]
```

---

## O que definir nessa etapa

- Modelo de implantação (on-premise / cloud / híbrido)
- Se haverá SOAR integrado
- Quais fontes de log serão conectadas (e como)
- Se haverá broker intermediário para normalização
- Política de retenção de dados (quente, morno, frio)
- Integração com Threat Intelligence (feeds externos)
- Integração com o framework MITRE ATT&CK para mapeamento das regras

---

## Alinhamento com MITRE ATT&CK

Cada regra de detecção do SIEM deveria mapear para uma ou mais técnicas do MITRE ATT&CK. Isso permite saber exatamente quais táticas adversariais o SOC consegue detectar e onde estão os pontos cegos.

```
Exemplo:
Regra: "Múltiplos logons falhos seguidos de logon bem-sucedido"
→ MITRE T1110.001 (Brute Force: Password Guessing)
→ MITRE T1078 (Valid Accounts)
```

Ter esse mapeamento desde o início facilita muito a evolução do SOC e a comunicação com gestores sobre cobertura de detecção.
