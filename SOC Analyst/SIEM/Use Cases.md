## Use Cases - O coração da operação
 
Um SIEM sem use cases bem definidos é só um repositório caro de logs.
 
**Use case** = cenário específico que o SIEM deve detectar e alertar.
 
### Exemplos clássicos
 
- **Brute force**: X tentativas de login falhadas em Y segundos → alerta.
- **Impossible travel**: login via VPN de São Paulo e login presencial em Curitiba com 5 minutos de diferença → conta comprometida?
- **Atypical travel**: usuário que sempre acessa de Brasília de repente loga às 3h da manhã a partir da Rússia. Não é impossível fisicamente, mas foge completamente do padrão dele → investigar.
- **Alteração em grupos privilegiados do AD**: alguém foi adicionado ao Domain Admins sem autorização → notifica o owner do grupo.
 
### Componentes de um use case
 
- **Regras**: o que detectar.
- **Lógica**: como tratar o que foi detectado.
- **Ações**: o que fazer quando a condição bater (alerta, e-mail, ticket, bloqueio...).
 
---
 
## Construindo um use case - checklist rápido
 
1. Qual o objetivo de segurança? (detecção de ameaça, compliance, visibilidade?)
2. Quais fontes de dados são necessárias?
3. Qual o comportamento normal (baseline)?
4. Qual a lógica de detecção? (regra de correlação, threshold, regex, behavioral)
5. Quais os thresholds e triggers? (ex: 10 falhas em 60s)
6. Como o SOC será notificado? (dashboard, e-mail, ticket automático)
 
---
 
## Ciclo de vida dos use cases
 
Use case não é "cria e esquece". O fluxo é contínuo:
 
```
Threat Intel / Hunting → Modelagem → Desenvolvimento → Teste → Deploy → Monitoramento (L1/L2) → Ajuste de falsos positivos → volta pro início
```
 
Analistas L1/L2 reportam falsos positivos. Threat hunting identifica gaps. CTI traz novas ameaças. O engenheiro de use cases ajusta. Repete.
 
---

## Modelo formal de documentação (SOC Use Case Template)
 
Para quem quer documentar direito:
 
| Campo | Descrição |
|---|---|
| Nome | Nome do use case |
| Finalidade | O que ele faz e por que existe |
| Declaração do problema | Qual gap de segurança ele resolve |
| Requisitos | O que o sistema precisa fazer (alerta, relatório, etc.) |
| Fontes de dados | De onde vêm os logs |
| Campos necessários | Quais campos dos logs são usados |
| Kill Chain | Em qual fase da Cyber Kill Chain ele atua |
| Pressupostos e limitações | O que pode dar errado |
| Metadados | Autor, versão, política vinculada, data |
 
---
 
## Algumas ameaças que o SIEM ajuda a detectar
 
- **Insiders** - quem já tem acesso é o mais difícil de pegar
- **Phishing** - análise de tráfego de e-mail, links e anexos suspeitos
- **SQL Injection** - padrões nos logs de aplicação/WAF
- **DDoS** - volumetria anormal de tráfego
- **Exfiltração de dados** - conexões suspeitas para destinos incomuns (APT)
- **Violações de política** - BitTorrent na rede corporativa, dispositivos não autorizados
 
---
