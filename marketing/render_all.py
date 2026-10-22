"""Renders every video (and its Pinterest pin) that is new or changed. Unchanged ones are kept from the cache.
  python marketing/render_all.py <media-dir> [--jobs 3]
A video is re-rendered when its spec, the player, the renderer, the voice settings or the app screenshots change."""
import argparse, hashlib, json, pathlib, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).parent
SPECS = sorted((ROOT / "content" / "videos").glob("*.json"))
ENGINE = [ROOT / "video" / f for f in ("player.html", "render.py", "tts.py", "pin.py")]
SHOTS = sorted((ROOT / "shots").glob("*"))


def digest(spec):
    h = hashlib.sha256()
    for f in [spec, *ENGINE, *SHOTS]:
        h.update(f.name.encode()); h.update(f.read_bytes())
    return h.hexdigest()[:16]


def one(spec, media):
    vid = spec.stem
    want = digest(spec)
    stamp = media / f"{vid}.hash"
    if stamp.exists() and stamp.read_text() == want and (media / f"{vid}.mp4").exists() and (media / f"{vid}_pin.jpg").exists():
        return vid, "cached", None
    r1 = subprocess.run([sys.executable, str(ROOT / "video" / "render.py"), str(spec), str(media), "--shots", str(ROOT / "shots")], capture_output=True, text=True)
    r2 = subprocess.run([sys.executable, str(ROOT / "video" / "pin.py"), str(spec), str(media), "--shots", str(ROOT / "shots")], capture_output=True, text=True)
    if r1.returncode or r2.returncode:
        return vid, "failed", (r1.stdout + r1.stderr + r2.stdout + r2.stderr)[-1500:]
    stamp.write_text(want)
    return vid, "rendered", None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("media"); ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    media = pathlib.Path(a.media); media.mkdir(parents=True, exist_ok=True)
    keep = {s.stem for s in SPECS}
    for f in media.iterdir():  # drop media of videos that no longer exist
        if f.is_file() and not any(f.name.startswith(k) for k in keep):
            f.unlink()
    with ThreadPoolExecutor(a.jobs) as ex:
        results = list(ex.map(lambda s: one(s, media), SPECS))
    failed = [r for r in results if r[1] == "failed"]
    for vid, status, err in results:
        print(f"{vid}: {status}")
        if err:
            print(err)
    (media / "index.json").write_text(json.dumps({v: json.loads((media / f"{v}.json").read_text()) for v, s, _ in results if s != "failed"}, indent=1))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
