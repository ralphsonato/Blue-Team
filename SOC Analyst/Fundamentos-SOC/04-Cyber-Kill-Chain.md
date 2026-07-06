# Cyber Kill Chain

## O que é

Framework desenvolvido pela Lockheed Martin que descreve as fases que um atacante percorre, do reconhecimento inicial até o objetivo final. A lógica por trás dele é, quebrar a cadeia em qualquer fase impede o ataque de avançar, por isso o nome "kill chain".

```
Reconnaissance > Weaponization > Delivery > Exploitation > Installation > C&C > Actions on Objectives
```

---

## As 7 fases

**1. Reconnaissance (Reconhecimento)**
O atacante coleta informação sobre o alvo, de forma passiva ou ativa: pesquisas na internet, coleta de e-mails, varredura de rede.

**2. Weaponization (Armamento)**
O atacante monta o payload que vai entregar, pode ser uma RAT, backdoor, ferramenta de criptografia ou downloader de malware.

**3. Delivery (Entrega)**
O payload malicioso chega até a vítima: e-mail, watering hole (site comprometido), drive-by download, pendrive malicioso.

**4. Exploitation (Exploração)**
O payload é executado no sistema da vítima, usuário abre o anexo, visita o site malicioso. Pode ser um processo em múltiplas etapas, onde o payload inicial baixa outro malware.

**5. Installation (Instalação)**
Ferramentas adicionais são instaladas via a RAT/backdoor original: software de criptografia, malware mais complexo, C2, ferramentas de exfiltração, tudo que o atacante precisa para atingir o objetivo.

**6. Command & Control (C2)**
A máquina comprometida se conecta à infraestrutura do atacante, muitas vezes usando portas conhecidas para evadir firewall e criptografando o tráfego. É esse canal que permite ao atacante enviar novos comandos.

**7. Actions on Objectives (Ações sobre os objetivos)**
O atacante finalmente executa o que veio fazer: criptografia com pedido de resgate, roubo de dados, destruição de sistemas, disrupção de software, ou manter acesso persistente para objetivos futuros.

---

## Por que isso importa para o SOC

Cada fase da kill chain é uma oportunidade de detecção. Um SOC maduro não espera o atacante chegar em "Actions on Objectives" para agir, o objetivo é ter visibilidade e controles em cada fase anterior, porque quanto mais cedo a cadeia é quebrada, menor o dano.

Mapear as regras de detecção contra as fases da kill chain (junto com MITRE ATT&CK, que entra mais no detalhe de cada técnica) é o que dá ao SOC uma visão clara de onde estão os pontos cegos.

Fonte: [Lockheed Martin - Cyber Kill Chain](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html)
