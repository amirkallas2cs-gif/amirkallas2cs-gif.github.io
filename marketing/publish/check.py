"""Checks the social media credentials without posting anything; writes marketing/status.json (no secrets)."""
import datetime, json, os, pathlib, urllib.request, urllib.error

GRAPH = "https://graph.facebook.com/v21.0"
out = {"checked_at": datetime.datetime.utcnow().isoformat(timespec="minutes") + "Z"}


def get(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": json.loads(e.read() or b"{}").get("error", {}).get("message", str(e))}


ig, tok, page, ptok = (os.environ.get(k, "") for k in ("IG_USER_ID", "META_TOKEN", "FB_PAGE_ID", "META_PAGE_TOKEN"))
if ig and tok:
    r = get(f"{GRAPH}/{ig}?fields=username,name,followers_count&access_token={tok}")
    out["instagram"] = {k: r.get(k) for k in ("username", "name", "followers_count", "error") if r.get(k) is not None}
    lim = get(f"{GRAPH}/{ig}/content_publishing_limit?fields=quota_usage,config&access_token={tok}")
    out["instagram"]["publishing_limit"] = lim.get("data", lim)
else:
    out["instagram"] = {"error": "IG_USER_ID / META_TOKEN not set"}
if page and ptok:
    r = get(f"{GRAPH}/{page}?fields=name,fan_count&access_token={ptok}")
    out["facebook"] = {k: r.get(k) for k in ("name", "fan_count", "error") if r.get(k) is not None}
else:
    out["facebook"] = {"error": "FB_PAGE_ID / META_PAGE_TOKEN not set"}
for k, names in (("youtube", ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN")), ("pinterest", ("PINTEREST_TOKEN", "PINTEREST_BOARD_ID"))):
    out[k] = {"configured": all(os.environ.get(n) for n in names)}
pathlib.Path("marketing/status.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
