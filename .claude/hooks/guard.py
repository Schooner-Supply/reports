#!/usr/bin/env python3
"""PreToolUse-vartija: pyytää vahvistuksen vain poikkeustapauksissa.

Lukee hook-syötteen stdinistä ja palauttaa permissionDecision "ask"
(syineen) kun kutsu on jokin näistä:
  - rahaa liikuttava / kirjanpitoon kirjoittava (Netvisor, Revolut, Stripe-maksut)
  - ulospäin lähtevä viestintä (sähköpostin lähetys, Klaviyo-lähetys)
  - tuhoava kantamuutos (DROP, TRUNCATE, DELETE/UPDATE ilman WHERE,
    kirjoitus auth-/vault-skeemaan, GRANT/REVOKE, migraatiot tuotantoon)
  - salaisuuksien käsittely (secret set, env add, .env)
  - git push --force tai push päähaaraan
  - deploy tuotantoon (wrangler deploy, vercel --prod, supabase db push)
Muuten ei tee mitään (permissions.allow / defaultMode päättää).
"""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool = data.get("tool_name", "")
inp = data.get("tool_input", {}) or {}


def ask(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def sql_reason(sql):
    """Palauttaa syyn jos SQL on tuhoava tai koskee auth-/salaisuusskeemoja."""
    for stmt in re.split(r";", sql):
        s = re.sub(r"--[^\n]*", " ", stmt)          # rivikommentit pois
        s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S)
        s = " ".join(s.split())
        if not s:
            continue
        u = s.upper()
        if re.search(r"\bDROP\s+(TABLE|SCHEMA|DATABASE|VIEW|FUNCTION|TRIGGER|POLICY|ROLE|INDEX|TYPE|EXTENSION|SEQUENCE|MATERIALIZED)\b", u):
            return "DROP-lause: " + s[:120]
        if re.search(r"\bTRUNCATE\b", u):
            return "TRUNCATE: " + s[:120]
        if re.search(r"\bDELETE\s+FROM\b", u) and not re.search(r"\bWHERE\b", u):
            return "DELETE ilman WHERE-ehtoa: " + s[:120]
        if re.search(r"\bUPDATE\s+\S+\s+SET\b", u) and not re.search(r"\bWHERE\b", u):
            return "UPDATE ilman WHERE-ehtoa: " + s[:120]
        if re.search(r"\bALTER\s+TABLE\b.*\bDROP\b", u):
            return "ALTER TABLE ... DROP: " + s[:120]
        if re.search(r"\b(GRANT|REVOKE)\b", u):
            return "Oikeuksien muutos (GRANT/REVOKE): " + s[:120]
        if re.search(r"\b(INSERT|UPDATE|DELETE|ALTER|DROP|CREATE)\b", u) and re.search(r"\b(AUTH|VAULT|PGSODIUM)\.", u):
            return "Kirjoitus auth-/vault-skeemaan: " + s[:120]
    return None


# ---------- SQL-työkalut (Supabase, Lovable) ----------
if tool in ("mcp__Supabase__execute_sql", "mcp__Lovable__query_database"):
    sql = inp.get("query") or inp.get("sql") or ""
    r = sql_reason(str(sql))
    if r:
        ask("Tuhoava tai arkaluonteinen kantamuutos – " + r)
    sys.exit(0)

# ---------- GitHub Actions -käynnistys ----------
if tool == "mcp__github__actions_run_trigger":
    wf = str(inp.get("workflow_id") or inp.get("workflowId") or inp.get("workflow") or "")
    if re.search(r"deploy|release|prod", wf, re.I):
        ask("Tuotantodeploy GitHub Actionsista: " + wf)
    sys.exit(0)

# ---------- Bash ----------
if tool == "Bash":
    cmd = str(inp.get("command", ""))
    c = cmd.lower()

    # Raha ja kirjanpito
    if re.search(r"netvisor|revolut|procountor", c):
        ask("Kirjanpito-/pankkirajapinta komennossa (Netvisor/Revolut)")
    if re.search(r"api\.stripe\.com/v\d+/(charges|payouts|transfers|refunds|payment_intents|invoices|subscriptions)", c) and not re.search(r"-x\s*get|--get", c):
        ask("Stripe-kirjoitus (maksut/siirrot)")

    # Ulospäin lähtevä viestintä
    if re.search(r"\b(sendmail|mailx?|msmtp|swaks)\b|gmail\.googleapis\.com/.*/send|/campaign-send-jobs|klaviyo.*(send|schedule)|api\.sendgrid|api\.resend\.com|api\.postmarkapp|slack\.com/api/chat\.postmessage", c):
        ask("Ulospäin lähtevä viesti (sähköposti/kampanja)")

    # Git: force push, päähaara, historian uudelleenkirjoitus
    if re.search(r"\bgit\s+push\b", c):
        if re.search(r"--force|--force-with-lease|(^|\s)-f(\s|$)|--mirror|--delete|\s\+\S", c):
            ask("git push --force / --delete")
        if re.search(r"\bgit\s+push\b[^|&;]*\b(main|master)\b", c):
            ask("git push päähaaraan (main/master)")
    if re.search(r"\bgit\s+(reset\s+--hard|branch\s+-D|clean\s+-\w*f|push\s+--mirror|filter-branch|filter-repo)\b", c):
        ask("Tuhoava git-komento (reset --hard / branch -D / clean -f)")

    # Deploy tuotantoon
    if re.search(r"\bwrangler\s+deploy\b", c):
        ask("wrangler deploy julkaisee Workerin tuotantoon")
    if re.search(r"\bvercel\b.*(--prod|--production)", c) or re.search(r"\bvercel\s+promote\b|\bvercel\s+rollback\b", c):
        ask("Vercel tuotantodeploy/promote")
    if re.search(r"\bsupabase\s+(db\s+push|migration\s+up|db\s+reset\s+--linked|functions\s+deploy|secrets\s+set)", c):
        ask("Supabase-muutos linkitettyyn (tuotanto)projektiin")
    if re.search(r"\bgh\s+workflow\s+run\b.*(deploy|release|prod)", c):
        ask("Tuotantodeploy GitHub Actionsista")

    # Salaisuudet
    if re.search(r"\b(gh\s+secret\s+set|wrangler\s+secret\s+(put|bulk)|vercel\s+env\s+(add|rm|pull)|supabase\s+secrets|doppler\s+secrets\s+set|op\s+item\s+(create|edit))\b", c):
        ask("Salaisuuksien kirjoitus/haku")
    if re.search(r"(^|[\s/])\.env(\.\w+)?(\s|$)", c) and not re.search(r"\.env\.example", c):
        ask("Komento koskee .env-tiedostoa")

    # SQL suoraan shellistä (psql / supabase db query)
    if re.search(r"\bpsql\b|\bsupabase\s+db\s+query\b", c):
        r = sql_reason(cmd)
        if r:
            ask("Tuhoava SQL komentorivillä – " + r)

sys.exit(0)
