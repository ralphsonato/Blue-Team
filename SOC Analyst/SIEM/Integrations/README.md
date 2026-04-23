# Integração Cloudflare com Wazuh

## Introdução

A **Cloudflare** atua como camada de proteção na borda da rede, bloqueando ataques, mitigando DDoS e filtrando tráfego malicioso antes mesmo de chegar à infraestrutura. Porém, por padrão, esses eventos ficam isolados dentro do painel da própria Cloudflare.

O objetivo dessa integração é trazer esses eventos para dentro do **Wazuh SIEM**, centralizando a visibilidade no SOC. Com isso, qualquer bloqueio, ataque WAF, tentativa de DDoS ou alteração de configuração feita na Cloudflare vira um alerta rastreável com IP de origem, país, regra disparada e ação tomada no mesmo lugar onde estão todos os outros eventos de segurança do ambiente.

A solução funciona com um script Python que consulta a API da Cloudflare a cada 5 minutos, grava os eventos em um arquivo JSON no servidor Wazuh, e regras customizadas se encarregam de classificar e gerar os alertas por nível de severidade.
---

## O que é coletado

| Fonte | Tipo de Evento |
|-------|---------------|
| Firewall Events | Bloqueios, challenges, skips por regras de firewall |
| WAF / Security Events | Ataques detectados pelo Web Application Firewall |
| Audit Logs | Alterações de configuração na conta Cloudflare |
| DDoS Analytics | Ataques volumétricos mitigados |

---

## Pré-requisitos

- Servidor Wazuh 4.x instalado (testado no 4.14.2)
- Python 3 com `requests` instalado (`pip3 install requests`)
- Token de API da Cloudflare com as permissões:
  - `Zone.Firewall Services` - Read
  - `Zone.Analytics` - Read
  - `Account.Account Analytics` - Read
  - `Account.Audit Logs` - Read
- Zone ID e Account ID da zona Cloudflare

---

## Arquitetura

```
Cloudflare API (GraphQL + REST)
        ↓
  cloudflare.py  (roda via cron a cada 5 min)
        ↓
/var/ossec/logs/cloudflare_events.json  (uma linha JSON por evento)
        ↓
  Wazuh logcollector  (monitora o arquivo)
        ↓
  Decoder JSON  (extrai os campos)
        ↓
  Regras customizadas  (classifica e gera alertas)
        ↓
  Wazuh Dashboard  (alertas visíveis em tempo real)
```

---

## Passo a Passo

### 1. Script de Coleta

Faça o deploy do script `cloudflare.py` em `/opt/cloudflare.py` no servidor Wazuh.

Configure as variáveis de ambiente ou edite diretamente no script:

```python
CF_API_TOKEN  = os.environ.get("CF_API_TOKEN",  "SEU_TOKEN_AQUI")
CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID", "SEU_ACCOUNT_ID_AQUI")
CF_ZONE_ID    = os.environ.get("CF_ZONE_ID",    "SEU_ZONE_ID_AQUI")
```

Teste o script manualmente antes de continuar:

```bash
python3 /opt/cloudflare.py
cat /var/ossec/logs/cloudflare_events.json | head -5
```

Se aparecerem linhas JSON com os eventos, está funcionando.

---

### 2. Decoder Customizado

Crie o arquivo `/var/ossec/etc/decoders/cloudflare_decoder.xml`:

```xml
<decoder name="cloudflare_json">
  <prematch>"cf_source":</prematch>
</decoder>
```

> **Atenção:** O prematch `"cf_source":` (sem a chave de abertura `{`) é intencional.  
> Os eventos JSON começam com `{"action":` e o campo `cf_source` aparece no final.  
> Usar `{"cf_source":` faz o decoder nunca disparar.

Ajuste as permissões:

```bash
chown wazuh:wazuh /var/ossec/etc/decoders/cloudflare_decoder.xml
chmod 660 /var/ossec/etc/decoders/cloudflare_decoder.xml
```

---

### 3. Regras Customizadas

Crie o arquivo `/var/ossec/etc/rules/cloudflare_rules.xml`:

```xml
<group name="cloudflare,">

  <!-- Regra base: qualquer evento Cloudflare -->
  <rule id="910000" level="3">
    <decoded_as>json</decoded_as>
    <field name="cf_source">\.+</field>
    <description>Cloudflare: evento recebido - fonte: $(cf_source)</description>
    <group>cloudflare,</group>
  </rule>

  <!-- Firewall: qualquer ação -->
  <rule id="910001" level="5">
    <if_sid>910000</if_sid>
    <field name="cf_source">firewall</field>
    <description>Cloudflare Firewall: $(action) - IP $(clientIP) [$(clientCountryName)]</description>
    <group>cloudflare,firewall,</group>
  </rule>

  <!-- Firewall: bloqueio -->
  <rule id="910002" level="10">
    <if_sid>910001</if_sid>
    <action>block</action>
    <description>Cloudflare Firewall: BLOQUEIO - IP $(clientIP) [$(clientCountryName)] Regra: $(ruleId)</description>
    <group>cloudflare,firewall,block,</group>
  </rule>

  <!-- WAF: qualquer ação -->
  <rule id="910010" level="5">
    <if_sid>910000</if_sid>
    <field name="cf_source">waf</field>
    <description>Cloudflare WAF: $(action) - IP $(clientIP) [$(clientCountryName)]</description>
    <group>cloudflare,waf,</group>
  </rule>

  <!-- WAF: bloqueio -->
  <rule id="910011" level="12">
    <if_sid>910010</if_sid>
    <action>block</action>
    <description>Cloudflare WAF: BLOQUEIO - IP $(clientIP) [$(clientCountryName)] Regra: $(ruleId)</description>
    <group>cloudflare,waf,block,</group>
  </rule>

  <!-- Audit Logs: alteração de configuração -->
  <rule id="910020" level="8">
    <if_sid>910000</if_sid>
    <field name="cf_source">audit</field>
    <description>Cloudflare Audit: alteracao de configuracao detectada</description>
    <group>cloudflare,audit,</group>
  </rule>

  <!-- DDoS: ataque detectado -->
  <rule id="910030" level="12">
    <if_sid>910000</if_sid>
    <field name="cf_source">ddos</field>
    <description>Cloudflare DDoS: ataque detectado [$(clientCountryName)]</description>
    <group>cloudflare,ddos,</group>
  </rule>

</group>
```

> **Sobre os IDs:** Verifique quais IDs já estão em uso no seu Wazuh antes de aplicar.  
> Para checar o maior ID existente: `grep -r 'rule id' /var/ossec/etc/rules/ | grep -oP 'id="\K[0-9]+' | sort -n | tail -5`

---

### 4. Configurar o Wazuh para monitorar o arquivo

Edite `/var/ossec/etc/ossec.conf` e adicione o bloco abaixo **antes** do `</ossec_config>`:

```xml
<localfile>
  <log_format>json</log_format>
  <location>/var/ossec/logs/cloudflare_events.json</location>
</localfile>
```

---

### 5. Testar antes de reiniciar

Use o `wazuh-logtest` para validar decoder e regras sem precisar reiniciar o serviço:

```bash
/var/ossec/bin/wazuh-logtest
```

Cole um evento de exemplo (copie uma linha do arquivo JSON gerado pelo script) e verifique se:
- **Phase 2** mostra `decoder: json` com os campos extraídos
- **Phase 3** mostra a regra correta disparando com `Alert to be generated`

---

### 6. Reiniciar o Wazuh

```bash
systemctl restart wazuh-manager
```

---

### 7. Configurar o Cron

Instale o cron se necessário (Amazon Linux 2023):

```bash
yum install -y cronie
systemctl enable crond
systemctl start crond
```

Adicione a tarefa para rodar a cada 5 minutos:

```bash
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/bin/python3 /opt/cloudflare.py") | crontab -
crontab -l
```

---

### 8. Validar

Rode o script uma vez e verifique se os alertas aparecem:

```bash
python3 /opt/cloudflare.py
sleep 5
grep "cloudflare" /var/ossec/logs/alerts/alerts.log | tail -20
```

No **Wazuh Dashboard**, filtre por:
- `rule.groups: cloudflare`
- `location: /var/ossec/logs/cloudflare_events.json`

---

## Níveis de Severidade das Regras

| Regra | Nível | Descrição |
|-------|-------|-----------|
| 910000 | 3 | Qualquer evento Cloudflare |
| 910001 | 5 | Firewall - qualquer ação |
| 910002 | 10 | Firewall - bloqueio |
| 910010 | 5 | WAF - qualquer ação |
| 910011 | 12 | WAF - bloqueio |
| 910020 | 8 | Audit Log - alteração de configuração |
| 910030 | 12 | DDoS - ataque detectado |

---

## Troubleshooting

**Script roda mas não cria o arquivo JSON**
- Verifique se o token tem as permissões necessárias
- Teste manualmente e leia os logs: `tail -f /var/ossec/logs/cloudflare_integration.log`

**Arquivo criado mas sem alertas no Wazuh**
- Confirme que o bloco `<localfile>` está fora de qualquer comentário `<!-- -->` no `ossec.conf`
- Verifique se o logcollector reconhece o arquivo: `grep "cloudflare" /var/ossec/logs/ossec.log`

**Decoder não dispara**
- Confirme que o prematch é `"cf_source":` e não `{"cf_source":`
- Valide com `wazuh-logtest` colando uma linha real do arquivo

**Regras não disparam**
- Confirme que `<decoded_as>json</decoded_as>` está na regra base (910000)
- IDs de regra conflitantes causam erro silencioso - verifique com `grep -r "910000" /var/ossec/etc/rules/`

---

## Próximos passos sugeridos

- Tuning de regras: suprimir eventos de IPs conhecidos (ex: monitoramento Zabbix)
- Configurar `logrotate` para o arquivo `/var/ossec/logs/cloudflare_events.json`
- Criar alertas de e-mail ou integração com ticket para regras nível 10+
- Expandir para outros clientes replicando o mesmo padrão

## Sobre

Esse trabalho foi desenvolvido durante meu período na **Aquarela**, como parte das iniciativas de segurança e monitoramento do SOC.
