import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone

# 在这里填写你准备公开展示的域名
DOMAINS = [
    "z-shop.cc",
    "zz-shop.cc",
]

def check_domain(domain):
    url = f"https://{domain}/"
    result = {
        "domain": domain,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "status": "offline",
        "http_code": None,
    }

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "DomainStatusChecker/1.0"},
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            result["http_code"] = response.status
            result["status"] = (
                "online" if 200 <= response.status < 400 else "offline"
            )
    except urllib.error.HTTPError as error:
        result["http_code"] = error.code
        result["status"] = (
            "online" if 200 <= error.code < 400 else "offline"
        )
    except Exception as error:
        result["error"] = type(error).__name__

    return result

results = [check_domain(domain) for domain in DOMAINS]

with open("status.json", "w", encoding="utf-8") as file:
    json.dump(
        {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "results": results,
        },
        file,
        ensure_ascii=False,
        indent=2,
    )

print(json.dumps(results, ensure_ascii=False, indent=2))
