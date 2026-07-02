# O que é um SOC

## Definição

SOC (Security Operations Center) é a unidade dedicada a monitorar e defender a infraestrutura de TI de uma organização. Na prática, é o posto de comando da segurança: uma equipe de analistas que fica de olho em rede, sistemas e aplicações procurando sinais de ameaça, o tempo todo.

Não é só monitoramento passivo, é a combinação de pessoas, processos e tecnologia trabalhando juntos para detectar e responder a ataques. Tirar qualquer uma dessas três pernas (gente treinada, processo definido, ferramenta adequada) e o SOC não funciona direito.

---

## O SOC como hub central

O SOC é o ponto onde os dados de segurança de toda a organização convergem:

- É o local onde dados de várias ferramentas e fontes são coletados e analisados
- Trabalha lado a lado com outras áreas de TI e segurança, virando o centro nervoso durante um incidente
- Coordena todo o esforço de monitoramento e resposta da organização

Isso é o que diferencia um SOC de "alguém olhando logs de vez em quando", é a centralização que permite correlacionar sinais que, isolados, não diriam nada.

---

## Como o SOC detecta ameaças

O ciclo de detecção segue uma lógica bem direta:

```
Monitoramento contínuo de logs e eventos
              
Ferramentas (IDS, SIEM) geram alertas
              
Analista investiga o alerta
              
Confirma se é incidente real ou falso positivo
```

Quanto mais cedo uma ameaça é detectada, mais rápido ela pode ser contida e é essa velocidade que justifica ter uma estrutura dedicada rodando 24/7 em vez de depender de alguém notar algo errado por acaso.

---

## Por que uma organização precisa de um SOC

- **Incidentes não respeitam horário comercial** - por isso o SOC opera 24/7
- **Reduz o tempo de detecção** - quanto mais rápido detecta, mais rápido remedia
- **Traz estrutura para a resposta a incidentes** - em vez de cada um improvisar
- **Atende exigências regulatórias** - vários frameworks e normas exigem monitoramento contínuo, e o SOC ajuda na auditoria e conformidade
- **Dá confiança para a organização** - saber que tem alguém vigiando o ambiente 24/7 é um diferencial, inclusive comercial

> Isso conversa direto com o que documentei em `Estruturando-SOC-SIEM/01-Levantamento-Requisitos.md`, a etapa de levantamento de requisitos já parte do princípio de que o SOC existe para resolver esses pontos. Aqui é o "porquê" por trás daquele processo.
