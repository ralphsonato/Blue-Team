# Investigação de Incidente: Comprometimento de Credencial VPN SSL e Movimento Lateral

## Ambiente

| Componente | Detalhe |
|------------|---------|
| SIEM | Wazuh (Indexer + Dashboard + Manager) |
| Firewall | FortiGate |
| VPN | SSL VPN FortiGate |
| Servidor alvo (movimento lateral) | `app1` - IP `10.10.10.11` |
| Servidor FTP (acesso anterior) | `ftp-server` - IP `172.16.8.21` |
| Período analisado | 01/08/2024 00:00 → 07/08/2024 00:00 |

---

## Resumo executivo

Um atacante realizou brute-force contra a interface SSL VPN do FortiGate, comprometeu a conta `adm_eric` e estabeleceu uma sessão VPN a partir de um IP no México. Divergência geográfica suspeita dado que o padrão legítimo do usuário é conexão a partir da Alemanha. Após obter acesso à rede interna via tunnel IP, o atacante realizou varredura de portas SSH e SMB, obteve acesso SSH ao servidor `app1` e executou comandos de reconhecimento de processos.

---

## Análise detalhada

### Q1 - Usuário com maior número de falhas de login SSL VPN

**Query:**
```dql
rule.groups: fortigate and full_log: *vpn*
```

<img width="2560" height="1331" alt="chrome_S6QXAR6ISk" src="https://github.com/user-attachments/assets/e995300e-3351-452e-8b14-0c2951b811fe" />


**Resposta:** `adm_eric`

**Observação técnica:** O campo `data.dstuser` apresentou inconsistência em parte dos eventos de falha os valores como `root` e `admin` aparecem no campo parseado, enquanto o `full_log` registra consistentemente `user="adm_eric"` em todos os eventos. A fonte de verdade é o `full_log`. Esse tipo de discrepância indica limitação no decoder FortiGate para logs SSL VPN, onde o campo `user` do log bruto e o campo parseado podem divergir dependendo da versão do firmware.

---

### Q2 - País com login bem-sucedido além da Alemanha

**Query:**
```dql
rule.groups: fortigate and data.subtype: vpn and data.action: tunnel-up and data.dstuser: adm_eric
```

<img width="2560" height="1331" alt="chrome_3YaMo9Hi19" src="https://github.com/user-attachments/assets/a75c3cda-efec-4c67-a531-2b527f60b37f" />


**Resposta:** `México`

**Observação técnica:** O usuário `adm_eric` conectou diariamente via VPN a partir da Alemanha (`176.88.151.196`) entre os dias 1 e 5 de agosto. No dia 6 de agosto, às `15:52:05`, houve uma conexão bem-sucedida originada do México (`189.221.34.106`), exatamente no mesmo período em que o brute-force SSL VPN estava ativo. Esse padrão configura um indicador clássico de **Impossible Travel** e/ou credencial comprometida.

---

### Q3 - Tunnel IP atribuído no login bem-sucedido (excluindo Alemanha)

**Query:**
```dql
rule.groups: fortigate and data.subtype: vpn and data.action: tunnel-up and data.dstuser: adm_eric
```

<img width="2560" height="1331" alt="chrome_ARPBEJARMi" src="https://github.com/user-attachments/assets/98603b25-af27-40b9-aebc-f90ff48e36a4" />


**Resposta:** `10.34.1.13`

**Observação técnica:** O tunnel IP é o endereço interno atribuído pelo FortiGate à sessão VPN. Todo tráfego subsequente originado pelo atacante dentro da rede interna parte desse IP é o que permite correlacionar os eventos de varredura e acesso com a sessão VPN comprometida.

---

### Q4 - Porta de destino mais acessada a partir do tunnel IP

**Query:**
```dql
rule.groups: fortigate and data.srcip: 10.34.1.13
```

<img width="2560" height="1331" alt="chrome_WI3k8oiynx" src="https://github.com/user-attachments/assets/0fae9d65-3b10-48e2-8629-2a023f89a04a" />


**Resposta:** `22` (SSH)

**Distribuição observada:**
- Porta `22` (SSH): 21 eventos
- Porta `445` (SMB): 9 eventos

**Observação técnica:** Imediatamente após a conexão VPN, o atacante iniciou varredura combinada SSH e SMB em toda a rede `10.10.10.0/24`. O scan SSH foi o principal vetor de reconhecimento, seguido do scan SMB, indicativo de intenção de movimento lateral tanto por autenticação remota quanto por exploração de compartilhamentos Windows.

---

### Q5 - Destinos únicos com SSH permitido via tunnel IP

**Query:**
```dql
rule.groups: fortigate and data.srcip: 10.34.1.13 and data.dstport: 22 and data.action: allow
```

<img width="2560" height="1331" alt="chrome_7uTWE8wORo" src="https://github.com/user-attachments/assets/5b0ea905-bf30-473f-9887-ef6eb615e770" />


**Resposta:** `3`

**IPs com porta 22 permitida pelo FortiGate:**
- `10.10.10.9`
- `10.10.10.10`
- `10.10.10.11`

---

### Q6 - IP com autenticação SSH bem-sucedida via tunnel IP

**Query:**
```dql
data.srcip: 10.34.1.13 and rule.groups: sshd and rule.groups: authentication_success
```

<img width="2560" height="1331" alt="chrome_jK2eYlS03m" src="https://github.com/user-attachments/assets/b1413d43-ee14-408b-b666-75f207001674" />


**Resposta:** `10.10.10.11` (`app1`)

**Observação técnica:** Dos 3 IPs com tráfego SSH permitido pelo firewall, apenas `10.10.10.11` (`app1`) registrou autenticação bem-sucedida como `root` às `16:02:00`, isso 10 minutos após o estabelecimento do tunnel VPN. O segundo hit retornado (`172.16.8.21` / `ftp-server`) é de `Aug 2`, anterior ao login mexicano, e representa uma sessão diferente não relacionada ao incidente de Aug 6.

---

### Q7 - Comando executado na atividade T1057 (Process Discovery)

**Query:**
```dql
agent.name: app1 and rule.mitre.id: T1057
```

<img width="2560" height="1331" alt="chrome_zUBpf8WolB" src="https://github.com/user-attachments/assets/17c1b011-92eb-407c-a6ce-9f9d014bfa7a" />


**Resposta:** `ps -aux | grep proftp`

---

### Q8 - Processo pesquisado na atividade T1057

**Query:**
```dql
agent.name: app1 and rule.mitre.id: T1057
```

<img width="2560" height="1331" alt="chrome_CYw8p6FTYl" src="https://github.com/user-attachments/assets/caaf528c-c1e4-4d9b-9492-3502fabd97f7" />


**Resposta:** `proftp`

**Observação técnica:** O ProFTPD é um daemon FTP amplamente utilizado em ambientes Linux. O atacante verificou se o processo estava ativo no `app1`, provavelmente para identificar a versão em execução e avaliar a possibilidade de exploração ou uso do serviço como vetor adicional de movimento lateral ou exfiltração de dados.

---

## Timeline do ataque

| Timestamp | Evento | MITRE |
|-----------|--------|-------|
| `01/08 → 05/08` | `adm_eric` conecta diariamente via VPN da Alemanha (`176.88.151.196`) |   |
| `03/08 01:34 → 01:45` | Brute-force SSL VPN contra `adm_eric` originado da Bulgária (`9.2.4.47`) | `T1110.001` |
| `06/08 15:52:05` | Login VPN bem-sucedido como `adm_eric` originado do México (`189.221.34.106`) | `T1078` |
| `06/08 15:52:05` | Tunnel IP `10.34.1.13` atribuído à sessão VPN |   |
| `06/08 16:00:00` | Varredura SSH (porta 22) e SMB (porta 445) em toda a rede `10.10.10.0/24` | `T1046` |
| `06/08 16:02:00` | Login SSH bem-sucedido como `root` no `app1` (`10.10.10.11`) | `T1021.004` |
| `06/08 16:03:00` | Execução de `ps -aux \| grep proftp` no `app1` | `T1057` |

---

## Respostas da investigação

| Q | Pergunta | Resposta |
|---|----------|----------|
| Q1 | Usuário com mais falhas de login SSL VPN | `adm_eric` |
| Q2 | País com login bem-sucedido além da Alemanha | `México` |
| Q3 | Tunnel IP atribuído no login suspeito | `10.34.1.13` |
| Q4 | Porta de destino mais acessada via tunnel IP | `22` |
| Q5 | Destinos únicos com SSH permitido via tunnel IP | `3` |
| Q6 | IP com autenticação SSH bem-sucedida via tunnel IP | `10.10.10.11` |
| Q7 | Comando executado na atividade T1057 | `ps -aux \| grep proftp` |
| Q8 | Processo pesquisado na atividade T1057 | `proftp` |

---

## Indicadores de comprometimento (IOCs)

| Tipo | Valor | Contexto |
|------|-------|----------|
| IP externo (brute-force) | `9.2.4.47` | Bulgária - origem do brute-force SSL VPN |
| IP externo (acesso) | `189.221.34.106` | México - origem do login VPN suspeito |
| Conta comprometida | `adm_eric` | Credencial VPN utilizada pelo atacante |
| Tunnel IP | `10.34.1.13` | IP interno atribuído à sessão VPN maliciosa |
| Host comprometido | `app1` (`10.10.10.11`) | Alvo de movimento lateral via SSH |
| Processo investigado | `proftp` | Alvo de reconhecimento pós-comprometimento |
