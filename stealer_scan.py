from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, Optional
from urllib.parse import quote

import requests

HIBP_BASE = "https://haveibeenpwned.com/api/v3"

def hibp_get(
    path: str,
    api_key: str,
    user_agent: str,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 20,
    max_retries: int = 3,
) -> requests.Response:
    url = f"{HIBP_BASE}{path}"
    headers = {
        "User-Agent": user_agent,
        "hibp-api-key": api_key,
    }

    for attempt in range(max_retries + 1):
        resp = requests.get(url, headers=headers, params=params, timeout=timeout)
        if resp.status_code != 429:
            return resp

        retry_after = resp.headers.get("retry-after")
        wait_s = int(retry_after) if (retry_after and retry_after.isdigit()) else 2
        if attempt >= max_retries:
            return resp
        time.sleep(wait_s)

    return resp

def handle_common(resp: requests.Response) -> Dict[str, Any]:
    if resp.status_code == 200:
        return {"ok": True, "data": resp.json()}
    if resp.status_code == 404:
        return {"ok": True, "data": None, "note": "No stealer log entries found."}
    if resp.status_code in (401, 403):
        return {"ok": False, "error": f"{resp.status_code} {resp.text.strip()}"}
    return {"ok": False, "error": f"Unexpected response: {resp.status_code} {resp.text.strip()}"}

def stealer_by_email(email: str, api_key: str, user_agent: str) -> Dict[str, Any]:
    enc = quote(email.strip(), safe="")
    resp = hibp_get(f"/stealerlogsbyemail/{enc}", api_key, user_agent)
    out = handle_common(resp)
    out["query"] = {"type": "email", "value": email}
    return out

def stealer_by_website_domain(domain: str, api_key: str, user_agent: str) -> Dict[str, Any]:
    enc = quote(domain.strip(), safe="")
    resp = hibp_get(f"/stealerlogsbywebsitedomain/{enc}", api_key, user_agent)
    out = handle_common(resp)
    out["query"] = {"type": "website_domain", "value": domain}
    return out

def stealer_by_email_domain(domain: str, api_key: str, user_agent: str) -> Dict[str, Any]:
    enc = quote(domain.strip(), safe="")
    resp = hibp_get(f"/stealerlogsbyemaildomain/{enc}", api_key, user_agent)
    out = handle_common(resp)
    out["query"] = {"type": "email_domain", "value": domain}
    return out

def cmd_email(args: argparse.Namespace) -> int:
    api_key = args.api_key or os.getenv("HIBP_API_KEY")
    if not api_key:
        print("Error: Provide --api-key or set HIBP_API_KEY.", file=sys.stderr)
        return 2

    res = stealer_by_email(args.email, api_key, args.user_agent)
    if not res["ok"]:
        print(f"Error: {res['error']}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    data = res.get("data")
    if data is None:
        print(f"{args.email}: no stealer log entries found.")
        return 0

    print(f"Stealer log domains for {args.email}:")
    for d in data:
        print(f" - {d}")
    return 0

def cmd_website(args: argparse.Namespace) -> int:
    api_key = args.api_key or os.getenv("HIBP_API_KEY")
    if not api_key:
        print("Error: Provide --api-key or set HIBP_API_KEY.", file=sys.stderr)
        return 2

    res = stealer_by_website_domain(args.domain, api_key, args.user_agent)
    if not res["ok"]:
        print(f"Error: {res['error']}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    data = res.get("data")
    if data is None:
        print(f"{args.domain}: no stealer log entries found.")
        return 0

    print(f"Stealer log email addresses seen against {args.domain}:")
    for e in data:
        print(f" - {e}")
    return 0

def cmd_email_domain(args: argparse.Namespace) -> int:
    api_key = args.api_key or os.getenv("HIBP_API_KEY")
    if not api_key:
        print("Error: Provide --api-key or set HIBP_API_KEY.", file=sys.stderr)
        return 2

    res = stealer_by_email_domain(args.domain, api_key, args.user_agent)
    if not res["ok"]:
        print(f"Error: {res['error']}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    data = res.get("data")
    if data is None:
        print(f"{args.domain}: no stealer log entries found.")
        return 0

    print(f"Stealer log aliases for email domain {args.domain}:")
    for alias, websites in sorted(data.items()):
        print(f" - {alias}@{args.domain}: {', '.join(websites)}")
    return 0

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="HIBP Stealer Logs CLI")
    p.add_argument("--api-key", help="HIBP API key")
    p.add_argument("--user-agent", default="StealerScanCLI", help="User-Agent header value")
    p.add_argument("--json", action="store_true", help="Print raw JSON result")

    sub = p.add_subparsers(dest="cmd", required=True)

    email = sub.add_parser("email", help="Get stealer log website domains for an email address")
    email.add_argument("email", help="Full email address, e.g. jane@example.com")
    email.set_defaults(func=cmd_email)

    website = sub.add_parser("website-domain", help="Get stealer log email addresses for a website domain")
    website.add_argument("domain", help="Website domain, e.g. netflix.com")
    website.set_defaults(func=cmd_website)

    ed = sub.add_parser("email-domain", help="Get stealer log email aliases for an email domain")
    ed.add_argument("domain", help="Email domain, e.g. example.com")
    ed.set_defaults(func=cmd_email_domain)

    return p

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())