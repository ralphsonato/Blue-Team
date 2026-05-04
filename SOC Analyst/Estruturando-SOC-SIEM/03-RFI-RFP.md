# RFI - Request for Information

## O que é e quando usar?

RFI é a "sondagem de mercado". Antes de pedir proposta, eu preciso saber quem existe, o que cada um oferece e se faz sentido chamá-los para uma disputa formal.

O documento de RFI vai ao mercado com o objetivo de explorar fornecedores e coletar informações sobre produtos e serviços, sem compromisso de compra ainda.

---

## O que compartilhar com os fornecedores (informações da empresa)

Não faz sentido pedir informações sem dar contexto. O fornecedor precisa saber o suficiente para responder adequadamente:

- A necessidade em alto nível: "precisamos de um SOC 24/7 com SIEM incluso, processo certificado ISO 27001, 100% terceirizado por no mínimo 12 meses"
- Apresentação geral da empresa (porte, setor, criticidade do ambiente)

> Atenção: não compartilhe detalhes sensíveis da infraestrutura nessa fase. O RFI é exploratório.

---

## O que solicitar dos fornecedores

| O que pedir | Por quê |
|-------------|---------|
| Histórico da empresa | Quantos anos no mercado, solidez financeira |
| Referências de clientes | Contato direto com quem já implementou - não aceitar nomes sem contato |
| Portfólio completo de serviços | O que oferecem além do básico (threat hunting, threat intel, forense) |
| Certificação ISO 27001 para o processo de SOC | Processo auditável e controlado |
| Comprovação de experiência em SOC | Cases documentados, não só apresentações bonitas |
| Capacidade de SOAR | Automação de resposta inclusa ou integrada? |
| Suporte a regulamentações | LGPD, PCI-DSS, outros relevantes para o seu negócio |

---

## O que fazer com as respostas do RFI?

Com as respostas em mãos, eu filtro quem segue para a próxima etapa. Critérios de corte típicos:
- Tem ISO 27001 para o processo de SOC?
- Tem referência verificável de projeto similar ao meu?
- Atende aos requisitos mínimos de escopo?

Quem passar nessa triagem recebe o RFP.

---
---

# RFP - Request for Proposal

## O que é?

RFP é a solicitação formal de proposta. Aqui o nível de detalhe aumenta muito - peço que o fornecedor apresente uma solução completa para o meu problema, com escopo, premissas, restrições, custo e governança.

Diferente do RFI (que é exploratório), o RFP é o documento que orienta a competição entre fornecedores.

> O RFP pode ser usado sem o RFI antes, mas a qualidade das propostas tende a ser menor quando os fornecedores não tiveram contato prévio com o ambiente.

---

## Estrutura de uma RFP para SOC/SIEM

### 1. Introdução
Contexto da empresa e do projeto. Quem somos, qual o ambiente, por que estamos buscando essa solução agora.

### 2. Objetivo
O que esperamos contratar. Exemplo: "SOC 24/7, cobrindo X ativos, com SIEM provisionado e gerenciado pelo fornecedor, SLA de 15 minutos para alertas críticos."

### 3. Prazo para resposta
Data limite para entrega da proposta. Seja realista - propostas feitas às pressas têm mais surpresas depois.

### 4. Cronograma macro
Linha do tempo do processo de seleção:
- Data de envio do RFP
- Prazo para dúvidas dos fornecedores
- Data de resposta das dúvidas
- Prazo final de entrega da proposta
- Período de análise
- Data de início da PoC

### 5. Escopo
O que está incluído: fontes de log, ativos monitorados, horário de operação, idioma de atendimento, localização dos analistas.

### 6. Fora do escopo
Tão importante quanto o escopo. O que não será responsabilidade do fornecedor - evita conflito depois.

### 7. Requisitos do SIEM
Funcionalidades mínimas esperadas: correlação de eventos, dashboards, relatórios de compliance, integração com as fontes de log do ambiente, retenção mínima de logs.

### 8. Processo de Resposta a Incidentes
Como o fornecedor vai atuar quando um incidente for identificado? Quais os passos, quem notifica, como é feita a contenção, quais as evidências geradas.

### 9. Critérios de avaliação (quantitativos)
Como as propostas serão pontuadas. Deixar claro para não ter questionamentos depois.

### 10. Premissas e restrições
O que eu assumo que é verdade (premissas) e o que limita o projeto (restrições). Exemplos de restrição: "os logs não podem sair do Brasil" ou "o SIEM deve ser on-premise".

### 11. Proposta comercial
Formato esperado para a proposta de preço. Peça para separar por componente: licença, implantação, sustentação mensal.

### 12. Procedimentos e contato
Canal oficial para dúvidas durante o processo. Importante centralizar as perguntas para garantir que todos os fornecedores recebam as mesmas respostas.
