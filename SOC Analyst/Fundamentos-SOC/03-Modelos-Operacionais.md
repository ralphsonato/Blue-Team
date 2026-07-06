# Modelos Operacionais

## SOC On-site vs. Outsourced

**On-site (in-house):** o SOC roda dentro da própria organização, com funcionários próprios.

- Dados sensíveis e detalhes de incidentes ficam sob controle total da organização
- A equipe conhece intimamente os sistemas do ambiente
- Linha direta de comunicação com TI, jurídico e gestão

**Outsourced (MSSP):** um provedor terceirizado oferece o serviço de SOC remotamente.

**Híbrido:** boa parte das organizações usa uma combinação dos dois. Organizações com dados altamente sensíveis ou classificados tendem a preferir manter o SOC in-house.

> Esse é exatamente o tipo de decisão que documentei em `Estruturando-SOC-SIEM/02-Arquitetura.md` na hora de escolher entre on-premise, cloud e híbrido para o SIEM, a decisão de "quem opera" segue lógica parecida com "onde a infraestrutura mora".

---

## Operação 24/7

Ameaça não segue horário comercial, então o SOC precisa ter cobertura contínua:

- Analistas se revezam em turnos (shifts)
- A passagem de plantão entre turnos precisa ser estruturada - o que ficou em aberto, o que precisa de acompanhamento
- Monitoramento 24/7 é o que garante detectar ataques nos estágios iniciais, antes que o atacante avance na kill chain

---

## SOC Global

Organizações com presença mundial geralmente não sustentam a operação com um único SOC centralizado:

- Multinacionais costumam operar vários SOCs em regiões diferentes para dar cobertura global
- Modelo **"follow-the-sun"**: a responsabilidade pelo monitoramento passa de SOC em SOC conforme o horário comercial de cada região
- Um SOC central pode coordenar os SOCs regionais, compartilhando informação entre eles
