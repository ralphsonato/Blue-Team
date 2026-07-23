# MITRE ATT&CK

## O que é

ATT&CK = Adversarial Tactics, Techniques & Common Knowledge. É uma base de conhecimento de táticas e técnicas de adversários, construída a partir de observações reais de ataques e não é teórico, é catalogado com base no que já foi visto no mundo real.

Mantido pela MITRE e disponível publicamente em [attack.mitre.org](https://attack.mitre.org).

---

## Estrutura da matriz

A Matriz ATT&CK for Enterprise organiza o conhecimento em colunas (táticas) que contêm técnicas:

- As colunas representam as **táticas** - o "porquê" do atacante (ex: Persistência, Escalação de Privilégio, Exfiltração)
- Dentro de cada tática ficam as **técnicas** - o "como" (mais de 230 catalogadas)
- Cada técnica tem sub-técnicas, explicação, exemplos de procedimento real, mitigação sugerida e forma de detecção

Um exemplo de técnica é a T1566 (Phishing), que documenta as variações de phishing usadas como vetor de acesso inicial, junto com as sub-técnicas, plataformas afetadas e forma de mitigar/detectar.

---

## Por que isso importa pro analista de SOC

- Dá contexto pro "porquê" por trás de um alerta, não é só "evento estranho", é uma técnica catalogada com padrão conhecido
- Padroniza a comunicação: termos e IDs (como T1566) são universais entre SOCs, então um relatório de incidente citando MITRE ATT&CK é entendido por qualquer analista, em qualquer lugar
- Ajuda a conectar alertas isolados à cadeia de ataque completa, um alerta sozinho pode não dizer nada, mas mapeado numa sequência de táticas revela a intenção do atacante
- É conhecimento exigido pra evoluir de T1 para T2 ou para Threat Hunter

> Já uso esse framework nas minhas análises de laboratório (CyberDefenders) documentadas no repositório `Threat-Hunting`, lá o mapeamento MITRE já é parte padrão de cada write-up.
