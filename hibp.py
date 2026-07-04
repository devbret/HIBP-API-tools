from __future__ import annotations

import html
import os
import re
import time
from getpass import getpass
from typing import Any

import requests
from dotenv import load_dotenv

HIBP_BASE = "https://haveibeenpwned.com/api/v3"

MAX_RETRY_WAIT_S = 60

_TAG_RE = re.compile(r"<[^>]+>")

def get_api_key(cli_value: str | None = None, prompt: bool = False) -> str | None:
    load_dotenv()
    api_key = cli_value or os.getenv("HIBP_API_KEY")
    if not api_key and prompt:
        api_key = getpass("Enter your HIBP API key here: ")
    return api_key or None

def get_setting(name: str) -> str | None:
    load_dotenv()
    value = os.getenv(name)
    value = value.strip() if value else ""
    return value or None

def get_input(env_var: str, prompt_text: str) -> str:
    return get_setting(env_var) or input(prompt_text).strip()

def hibp_get(
    path: str,
    user_agent: str,
    api_key: str | None = None,
    params: dict[str, Any] | None = None,
    timeout: int = 20,
    max_retries: int = 3,
) -> requests.Response:
    url = f"{HIBP_BASE}{path}"
    headers = {"User-Agent": user_agent}
    if api_key:
        headers["hibp-api-key"] = api_key

    resp = requests.get(url, headers=headers, params=params, timeout=timeout)
    for _ in range(max_retries):
        if resp.status_code != 429:
            break
        retry_after = resp.headers.get("retry-after")
        wait_s = int(retry_after) if (retry_after and retry_after.isdigit()) else 2
        time.sleep(min(wait_s, MAX_RETRY_WAIT_S))
        resp = requests.get(url, headers=headers, params=params, timeout=timeout)
    return resp

def error_message(resp: requests.Response) -> str:
    body = resp.text.strip()
    return f"HTTP {resp.status_code}" + (f": {body}" if body else "")

def strip_html(text: str) -> str:
    return html.unescape(_TAG_RE.sub("", text or ""))
