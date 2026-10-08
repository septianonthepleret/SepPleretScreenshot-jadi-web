#!/usr/bin/env python3
"""Extract key frames from a UI screen-recording for screenshot-to-html.

Picks frames at scene changes (ffmpeg) and tops up with evenly spaced frames,
then writes a contact sheet and frames.json.

Usage:
  python3 extract_frames.py video.mp4 --out frames [--max-frames 12]
         [--every SECONDS] [--start S] [--end S] [--scene-threshold 0.2]
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

from PIL import Image, ImageDraw


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,r_frame_rate:format=duration",
             "-of", "json", str(path)])
    if r.returncode != 0:
        sys.exit(f"ffprobe failed: {r.stderr.strip()}")
    d = json.loads(r.stdout)
    s = d["streams"][0]
    num, den = (s["r_frame_rate"].split("/") + ["1"])[:2]
    fps = float(num) / float(den) if float(den) else 0.0
    return {"width": s["width"], "height": s["height"], "fps": round(fps, 2),
            "duration": round(float(d["format"]["duration"]), 2)}


def scene_times(path, thr, start, end):
    cmd = ["ffmpeg", "-hide_banner", "-nostats"]
    if start: cmd += ["-ss", str(start)]
    if end: cmd += ["-to", str(end)]
    cmd += ["-i", str(path), "-vf", f"select='gt(scene,{thr})',showinfo",
            "-an", "-f", "null", "-"]
    r = run(cmd)
    times = [float(m) + (start or 0) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
    return times


def grab(path, t, out):
    r = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.3f}",
             "-i", str(path), "-frames:v", "1", str(out)])
    return r.returncode == 0 and Path(out).exists()


def pick(times, limit):
    if len(times) <= limit:
        return times
    step = (len(times) - 1) / (limit - 1)
    return [times[round(i * step)] for i in range(limit)]


def contact_sheet(items, out, cols=4, thumb_w=360):
    if not items:
        return
    thumbs = []
    for t, p in items:
        im = Image.open(p).convert("RGB")
        h = int(im.height * thumb_w / im.width)
        thumbs.append((t, im.resize((thumb_w, h))))
    th = max(im.height for _, im in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    pad, label = 8, 18
    sheet = Image.new("RGB", (cols * (thumb_w + pad) + pad,
                              rows * (th + label + pad) + pad), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    for i, (t, im) in enumerate(thumbs):
        x = pad + (i % cols) * (thumb_w + pad)
        y = pad + (i // cols) * (th + label + pad)
        d.text((x, y), f"#{i:02d}  {t:.2f}s", fill=(230, 230, 230))
        sheet.paste(im, (x, y + label))
    sheet.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default="frames")
    ap.add_argument("--max-frames", type=int, default=12)
    ap.add_argument("--every", type=float, help="uniform sampling interval (seconds)")
    ap.add_argument("--start", type=float)
    ap.add_argument("--end", type=float)
    ap.add_argument("--scene-threshold", type=float, default=0.2)
    a = ap.parse_args()

    src = Path(a.video)
    if not src.exists():
        sys.exit(f"File not found: {src}")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("frame_*.png"):
        old.unlink()

    info = probe(src)
    start = a.start or 0.0
    end = min(a.end, info["duration"]) if a.end else info["duration"]
    span = max(end - start, 0.1)

    if a.every:
        times = [start + i * a.every for i in range(int(span / a.every) + 1)]
    else:
        times = [start] + scene_times(src, a.scene_threshold, a.start, a.end)
        # top up with evenly spaced frames so quiet videos still get coverage
        want = min(a.max_frames, 6)
        if len(times) < want:
            times += [start + span * (i + 0.5) / want for i in range(want)]
        times.append(max(start, end - 0.1))  # final state

    # de-duplicate close timestamps, keep order, cap count
    times = sorted(t for t in times if start <= t <= end)
    uniq = []
    for t in times:
        if not uniq or t - uniq[-1] >= 0.25:
            uniq.append(t)
    uniq = pick(uniq, a.max_frames)

    items = []
    for i, t in enumerate(uniq):
        p = out / f"frame_{i:03d}.png"
        if grab(src, t, p):
            items.append((t, p))

    contact_sheet(items, out / "contact_sheet.png")
    meta = {"source": str(src), **info,
            "frames": [{"file": p.name, "time": round(t, 2)} for t, p in items]}
    (out / "frames.json").write_text(json.dumps(meta, indent=2))
    print(f"{info['width']}x{info['height']} @ {info['fps']}fps, {info['duration']}s")
    print(f"Wrote {len(items)} frames + contact_sheet.png + frames.json to {out}/")


if __name__ == "__main__":
    main()
