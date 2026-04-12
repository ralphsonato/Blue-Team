# SIEM - O Cérebro do SOC

---

## Antes de tudo: evento ≠ incidente
 
Parece básico, mas muita gente confunde.
 
- **Evento de segurança**: algo aconteceu no sistema que *pode* ser relevante. Uma falha de autenticação, por exemplo. Pode ser uma automação com token expirado - nada malicioso.
- **Incidente de segurança**: um ou mais eventos que indicam comprometimento real. Aquela mesma falha de autenticação, mas agora são 50 tentativas por segundo vindas do mesmo IP. Brute force.
 
**Todo incidente é um evento, mas nem todo evento é um incidente.** A diferença entre os dois? Contexto. E é exatamente isso que o SIEM faz, dá contexto.
 
---
 
## O que é SIEM?
 
SIEM = Security Information and Event Management.
 
Em termos simples: ele coleta logs de tudo (firewalls, endpoints, servidores, cloud, e-mail...) e joga tudo num mesmo lugar e cruza as informações para encontrar o que importa.
 
Três pilares:
 
1. **Gerenciamento de logs** - coleta centralizada de eventos de múltiplas fontes.
2. **Correlação e análise** - cruza dados para identificar padrões que isolados não significam nada, mas juntos acendem o alerta.
3. **Monitoramento e alertas** - classifica comportamentos anormais e notifica em tempo real.
 
Benefícios diretos: detecção de ameaças em tempo real, conformidade regulatória, automação com IA e suporte a investigações forenses.
 
---

Lembrando que o SIEM não substitui nenhum outra ferramenta de segurança, como EDR/XDR. Ele complementa, conectando pontos que nenhuma ferramenta isolada conseguiria.

---
