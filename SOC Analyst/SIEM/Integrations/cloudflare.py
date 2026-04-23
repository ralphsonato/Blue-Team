#!/usr/bin/env python3
"""
Cloudflare -> Wazuh Integration
Coleta: Firewall Events, Audit Logs, Security Events, DDoS Events
"""

import json
import logging
import os
import requests
from datetime import datetime, timedelta, timezone

# ──────────────────────────────────────────────
# CONFIGURAÇÃO
# ──────────────────────────────────────────────
CF_API_TOKEN  = os.environ.get("CF_API_TOKEN", "SEU_TOKEN_AQUI")
CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID", "SEU_ACCOUNT_ID_AQUI")
CF_ZONE_ID    = os.environ.get("CF_ZONE_ID",    "SEU_ZONE_ID_AQUI")

WAZUH_EVENTS  = "/var/ossec/logs/cloudflare_events.json"
CURSOR_FILE   = "/var/ossec/logs/cloudflare_cursor.json"
LOG_FILE      = "/var/ossec/logs/cloudflare_integration.log"
LOOKBACK_MIN  = 5

# ──────────────────────────────────────────────
# LOGGER
# ──────────────────────────────────────────────
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
log = logging.getLogger("cloudflare")

HEADERS = {
    "Authorization": f"Bearer {CF_API_TOKEN}",
    "Content-Type": "application/json"
}

# ──────────────────────────────────────────────
# CURSOR (evita eventos duplicados)
# ──────────────────────────────────────────────
def load_cursor():
    try:
        with open(CURSOR_FILE) as f:
            return json.load(f)
    except Exception:
        return {}

def save_cursor(cursor: dict):
    with open(CURSOR_FILE, "w") as f:
        json.dump(cursor, f)

# ──────────────────────────────────────────────
# ENVIO AO WAZUH
# ──────────────────────────────────────────────
def send_to_wazuh(source: str, event: dict):
    try:
        event["cf_source"] = source
        with open(WAZUH_EVENTS, "a") as f:
            f.write(json.dumps(event, default=str) + "\n")
    except Exception as e:
        log.error(f"Erro ao gravar evento [{source}]: {e}")

# ──────────────────────────────────────────────
# 1. FIREWALL EVENTS (GraphQL)
# ──────────────────────────────────────────────
def fetch_firewall_events(since: str, until: str):
    query = """
    query FirewallEvents($zoneTag: String!, $since: Time!, $until: Time!) {
      viewer {
        zones(filter: { zoneTag: $zoneTag }) {
          firewallEventsAdaptive(
            filter: { datetime_geq: $since, datetime_leq: $until }
            limit: 1000
            orderBy: [datetime_ASC]
          ) {
            action
            clientASNDescription
            clientAsn
            clientCountryName
            clientIP
            clientRequestHTTPHost
            clientRequestHTTPMethodName
            clientRequestHTTPProtocol
            clientRequestPath
            clientRequestQuery
            datetime
            rayName
            ruleId
            source
            userAgent
          }
        }
      }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "zoneTag": CF_ZONE_ID,
            "since": since,
            "until": until
        }
    }
    try:
        resp = requests.post(
            "https://api.cloudflare.com/client/v4/graphql",
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        data = resp.json()
        zones = (data.get("data") or {}).get("viewer", {}).get("zones") or []
        if zones:
            return zones[0].get("firewallEventsAdaptive", [])
    except Exception as e:
        log.error(f"Erro firewall events: {e}")
    return []

# ──────────────────────────────────────────────
# 2. WAF / SECURITY EVENTS (GraphQL)
# ──────────────────────────────────────────────
def fetch_security_events(since: str, until: str):
    query = """
    query SecurityEvents($zoneTag: String!, $since: Time!, $until: Time!) {
      viewer {
        zones(filter: { zoneTag: $zoneTag }) {
          securityEventsAdaptive(
            filter: { datetime_geq: $since, datetime_leq: $until }
            limit: 1000
            orderBy: [datetime_ASC]
          ) {
            action
            clientIP
            clientCountryName
            clientRequestHTTPHost
            clientRequestHTTPMethodName
            clientRequestHTTPPath
            datetime
            rayName
            ruleId
            source
            userAgent
            matchIndex
          }
        }
      }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "zoneTag": CF_ZONE_ID,
            "since": since,
            "until": until
        }
    }
    try:
        resp = requests.post(
            "https://api.cloudflare.com/client/v4/graphql",
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        data = resp.json()
        zones = (data.get("data") or {}).get("viewer", {}).get("zones") or []
        if zones:
            return zones[0].get("securityEventsAdaptive", [])
    except Exception as e:
        log.error(f"Erro security events: {e}")
    return []

# ──────────────────────────────────────────────
# 3. AUDIT LOGS (REST API)
# ──────────────────────────────────────────────
def fetch_audit_logs(since: str, cursor: dict):
    params = {
        "since": since,
        "per_page": 100,
        "direction": "asc"
    }
    if cursor.get("audit_since_id"):
        params["id.gt"] = cursor["audit_since_id"]

    try:
        resp = requests.get(
            f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/audit_logs",
            headers=HEADERS,
            params=params,
            timeout=30
        )
        data = resp.json()
        results = data.get("result") or []
        if results:
            cursor["audit_since_id"] = results[-1]["id"]
        return results, cursor
    except Exception as e:
        log.error(f"Erro audit logs: {e}")
    return [], cursor

# ──────────────────────────────────────────────
# 4. DDOS ANALYTICS (GraphQL - Pro+)
# ──────────────────────────────────────────────
def fetch_ddos_events(since: str, until: str):
    query = """
    query DDoSEvents($zoneTag: String!, $since: Time!, $until: Time!) {
      viewer {
        zones(filter: { zoneTag: $zoneTag }) {
          ddosAnalyticsAdaptiveGroups(
            filter: { datetime_geq: $since, datetime_leq: $until }
            limit: 100
            orderBy: [datetime_ASC]
          ) {
            dimensions {
              attackId
              attackType
              clientCountryName
              clientIP
              destinationPort
              ipProtocol
              ruleId
              datetime: datetimeHour
            }
            sum {
              packets
              bits
            }
          }
        }
      }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "zoneTag": CF_ZONE_ID,
            "since": since,
            "until": until
        }
    }
    try:
        resp = requests.post(
            "https://api.cloudflare.com/client/v4/graphql",
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        data = resp.json()
        zones = (data.get("data") or {}).get("viewer", {}).get("zones") or []
        if zones:
            return zones[0].get("ddosAnalyticsAdaptiveGroups", [])
    except Exception as e:
        log.error(f"Erro DDoS events: {e}")
    return []

# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def main():
    now   = datetime.now(timezone.utc)
    since = (now - timedelta(minutes=LOOKBACK_MIN)).strftime("%Y-%m-%dT%H:%M:%SZ")
    until = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    cursor = load_cursor()

    # Firewall Events
    fw_events = fetch_firewall_events(since, until)
    log.info(f"Firewall events: {len(fw_events)}")
    for e in fw_events:
        send_to_wazuh("firewall", e)

    # Security / WAF Events
    sec_events = fetch_security_events(since, until)
    log.info(f"Security events: {len(sec_events)}")
    for e in sec_events:
        send_to_wazuh("waf", e)

    # Audit Logs
    audit_events, cursor = fetch_audit_logs(since, cursor)
    log.info(f"Audit logs: {len(audit_events)}")
    for e in audit_events:
        send_to_wazuh("audit", e)

    # DDoS Analytics
    ddos_events = fetch_ddos_events(since, until)
    log.info(f"DDoS events: {len(ddos_events)}")
    for e in ddos_events:
        event = {**e.get("dimensions", {}), **e.get("sum", {})}
        send_to_wazuh("ddos", event)

    save_cursor(cursor)
    log.info("Coleta finalizada.")

if __name__ == "__main__":
    main()
