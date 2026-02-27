from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from urllib.parse import quote

import requests

HIBP_BASE = "https://haveibeenpwned.com/api/v3"

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

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

def load_state(state_path: str) -> Dict[str, Any]:
    if not os.path.exists(state_path):
        return {}
    try:
        with open(state_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_state(state_path: str, state: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def get_subscribed_domains(api_key: str, user_agent: str) -> Dict[str, Any]:
    resp = hibp_get("/subscribeddomains", api_key, user_agent)
    if resp.status_code == 200:
        return {"ok": True, "domains": resp.json()}
    if resp.status_code in (401, 403):
        return {"ok": False, "error": f"{resp.status_code} {resp.text.strip()}"}
    return {"ok": False, "error": f"Unexpected response: {resp.status_code} {resp.text.strip()}"}

def get_latest_breach(api_key: str, user_agent: str) -> Dict[str, Any]:
    resp = hibp_get("/latestbreach", api_key, user_agent)
    if resp.status_code == 200:
        return {"ok": True, "latest": resp.json()}
    if resp.status_code in (401, 403):
        return {"ok": False, "error": f"{resp.status_code} {resp.text.strip()}"}
    return {"ok": False, "error": f"Unexpected response: {resp.status_code} {resp.text.strip()}"}

def get_breached_domain(domain: str, api_key: str, user_agent: str) -> Dict[str, Any]:
    enc_domain = quote(domain.strip(), safe="")
    resp = hibp_get(f"/breacheddomain/{enc_domain}", api_key, user_agent)

    if resp.status_code == 200:
        return {"ok": True, "domain": domain, "results": resp.json()}
    if resp.status_code == 404:
        return {"ok": True, "domain": domain, "results": {}, "note": "No breached email addresses found."}
    if resp.status_code in (401, 403):
        return {"ok": False, "domain": domain, "error": f"{resp.status_code} {resp.text.strip()}"}
    return {"ok": False, "domain": domain, "error": f"Unexpected response: {resp.status_code} {resp.text.strip()}"}

def summarize_domain_results(domain: str, results: Dict[str, Any]) -> str:
    alias_count = len(results)
    breach_hits = sum(len(v) for v in results.values())
    unique_breaches = sorted({b for v in results.values() for b in v})
    return (
        f"{domain}: {alias_count} aliases breached, {breach_hits} breach hits, "
        f"{len(unique_breaches)} unique breaches"
    )

def cmd_run(args: argparse.Namespace) -> int:
    api_key = args.api_key or os.getenv("HIBP_API_KEY")
    if not api_key:
        print("Error: Provide --api-key or set HIBP_API_KEY.", file=sys.stderr)
        return 2

    user_agent = args.user_agent
    state_path = os.path.expanduser(args.state_file)
    state = load_state(state_path)

    latest_res = get_latest_breach(api_key, user_agent)
    if not latest_res["ok"]:
        print(f"Error fetching latest breach: {latest_res['error']}", file=sys.stderr)
        return 1

    latest = latest_res["latest"]
    latest_name = latest.get("Name")
    latest_added = latest.get("AddedDate")

    previous_latest = state.get("latestbreach", {})
    prev_name = previous_latest.get("Name")
    prev_added = previous_latest.get("AddedDate")

    changed = (latest_name != prev_name) or (latest_added != prev_added)

    if args.print_latest:
        print(f"Latest breach: {latest_name} (AddedDate: {latest_added})")

    if not changed and not args.force:
        print("No new breach since last run. (Use --force to run anyway.)")
        return 0

    subs = get_subscribed_domains(api_key, user_agent)
    if not subs["ok"]:
        print(f"Error fetching subscribed domains: {subs['error']}", file=sys.stderr)
        return 1

    domains = [d["DomainName"] for d in subs["domains"] if "DomainName" in d]
    if not domains:
        print("No subscribed domains found for this API key.")
        return 0

    if args.list_domains:
        print("Subscribed domains:")
        for d in domains:
            print(f" - {d}")

    run_record: Dict[str, Any] = {
        "ranAt": _now_iso(),
        "latestbreach": latest,
        "domainsQueried": domains,
        "domainResults": {},
    }

    for domain in domains:
        res = get_breached_domain(domain, api_key, user_agent)
        run_record["domainResults"][domain] = res

        if res.get("ok"):
            results_dict = res.get("results", {})
            print(summarize_domain_results(domain, results_dict))
            if args.verbose and results_dict:
                for alias, breaches in sorted(results_dict.items()):
                    print(f"   - {alias}@{domain}: {', '.join(breaches)}")
        else:
            print(f"{domain}: ERROR — {res.get('error')}", file=sys.stderr)

    state["latestbreach"] = latest
    state.setdefault("history", [])
    state["history"].append(run_record)

    if isinstance(state["history"], list) and len(state["history"]) > args.keep_history:
        state["history"] = state["history"][-args.keep_history :]

    save_state(state_path, state)

    if args.json_out:
        out_path = os.path.expanduser(args.json_out)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(run_record, f, indent=2, ensure_ascii=False)
        print(f"Wrote run output to: {out_path}")

    return 0

def cmd_show_state(args: argparse.Namespace) -> int:
    state_path = os.path.expanduser(args.state_file)
    state = load_state(state_path)
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="HIBP Domain Breach Monitor")
    p.add_argument("--api-key", help="HIBP API key")
    p.add_argument("--user-agent", default="BreachWatchCLI", help="User-Agent header value")
    p.add_argument(
        "--state-file",
        default="~/.hibp_breachwatch.json",
        help="Path to persistent state JSON file",
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Check latest breach and query subscribed domains if changed")
    run.add_argument("--force", action="store_true", help="Query domains even if latest breach is unchanged")
    run.add_argument("--print-latest", action="store_true", help="Print latest breach name and AddedDate")
    run.add_argument("--list-domains", action="store_true", help="Print subscribed domains before querying")
    run.add_argument("--verbose", action="store_true", help="Print per-alias breakdown when results exist")
    run.add_argument("--json-out", help="Write this run's record to a JSON file")
    run.add_argument("--keep-history", type=int, default=25, help="Number of historical runs to keep in state file")
    run.set_defaults(func=cmd_run)

    show = sub.add_parser("show-state", help="Print the current stored state JSON")
    show.set_defaults(func=cmd_show_state)

    return p

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())