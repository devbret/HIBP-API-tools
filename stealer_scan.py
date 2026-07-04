from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Callable
from urllib.parse import quote

import requests

from hibp import get_api_key, get_setting, hibp_get

def handle_common(resp: requests.Response) -> dict[str, Any]:
    if resp.status_code == 200:
        return {"ok": True, "data": resp.json()}
    if resp.status_code == 404:
        return {"ok": True, "data": None, "note": "No stealer log entries found."}
    if resp.status_code in (401, 403):
        return {"ok": False, "error": f"{resp.status_code} {resp.text.strip()}"}
    return {"ok": False, "error": f"Unexpected response: {resp.status_code} {resp.text.strip()}"}

def stealer_by_email(email: str, api_key: str, user_agent: str) -> dict[str, Any]:
    enc = quote(email.strip(), safe="")
    resp = hibp_get(f"/stealerlogsbyemail/{enc}", user_agent, api_key=api_key)
    out = handle_common(resp)
    out["query"] = {"type": "email", "value": email}
    return out

def stealer_by_website_domain(domain: str, api_key: str, user_agent: str) -> dict[str, Any]:
    enc = quote(domain.strip(), safe="")
    resp = hibp_get(f"/stealerlogsbywebsitedomain/{enc}", user_agent, api_key=api_key)
    out = handle_common(resp)
    out["query"] = {"type": "website_domain", "value": domain}
    return out

def stealer_by_email_domain(domain: str, api_key: str, user_agent: str) -> dict[str, Any]:
    enc = quote(domain.strip(), safe="")
    resp = hibp_get(f"/stealerlogsbyemaildomain/{enc}", user_agent, api_key=api_key)
    out = handle_common(resp)
    out["query"] = {"type": "email_domain", "value": domain}
    return out

def run_command(
    args: argparse.Namespace,
    fetch: Callable[[str], dict[str, Any]],
    render: Callable[[Any], None],
) -> int:
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: Provide --api-key or set HIBP_API_KEY.", file=sys.stderr)
        return 2

    res = fetch(api_key)
    if not res["ok"]:
        print(f"Error: {res['error']}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    data = res.get("data")
    if data is None:
        print(f"{res['query']['value']}: no stealer log entries found.")
        return 0

    render(data)
    return 0

def cmd_email(args: argparse.Namespace) -> int:
    email = args.email or get_setting("HIBP_EMAIL")
    if not email:
        print("Error: provide an email argument or set HIBP_EMAIL.", file=sys.stderr)
        return 2

    def render(data: Any) -> None:
        print(f"Stealer log domains for {email}:")
        for d in data:
            print(f" - {d}")

    return run_command(args, lambda key: stealer_by_email(email, key, args.user_agent), render)

def cmd_website(args: argparse.Namespace) -> int:
    domain = args.domain or get_setting("HIBP_DOMAIN")
    if not domain:
        print("Error: provide a domain argument or set HIBP_DOMAIN.", file=sys.stderr)
        return 2

    def render(data: Any) -> None:
        print(f"Stealer log email addresses seen against {domain}:")
        for e in data:
            print(f" - {e}")

    return run_command(args, lambda key: stealer_by_website_domain(domain, key, args.user_agent), render)

def cmd_email_domain(args: argparse.Namespace) -> int:
    domain = args.domain or get_setting("HIBP_DOMAIN")
    if not domain:
        print("Error: provide a domain argument or set HIBP_DOMAIN.", file=sys.stderr)
        return 2

    def render(data: Any) -> None:
        print(f"Stealer log aliases for email domain {domain}:")
        for alias, websites in sorted(data.items()):
            print(f" - {alias}@{domain}: {', '.join(websites)}")

    return run_command(args, lambda key: stealer_by_email_domain(domain, key, args.user_agent), render)

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="HIBP Stealer Logs CLI")
    p.add_argument("--api-key", help="HIBP API key")
    p.add_argument("--user-agent", default="StealerScanCLI", help="User-Agent header value")
    p.add_argument("--json", action="store_true", help="Print raw JSON result")

    sub = p.add_subparsers(dest="cmd", required=True)

    email = sub.add_parser("email", help="Get stealer log website domains for an email address")
    email.add_argument("email", nargs="?", help="Full email address, e.g. jane@example.com (defaults to HIBP_EMAIL from .env)")
    email.set_defaults(func=cmd_email)

    website = sub.add_parser("website-domain", help="Get stealer log email addresses for a website domain")
    website.add_argument("domain", nargs="?", help="Website domain, e.g. netflix.com (defaults to HIBP_DOMAIN from .env)")
    website.set_defaults(func=cmd_website)

    ed = sub.add_parser("email-domain", help="Get stealer log email aliases for an email domain")
    ed.add_argument("domain", nargs="?", help="Email domain, e.g. example.com (defaults to HIBP_DOMAIN from .env)")
    ed.set_defaults(func=cmd_email_domain)

    return p

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
