"""Extract a de-duplicated action timeline from a Claude Code subagent transcript (.jsonl).
Usage: python3 tools/transcript_actions.py <transcript.jsonl> <TITLE> > <out.md>"""
import json, sys, collections
rows = [json.loads(l) for l in open(sys.argv[1])]
seen, acts = set(), []
for r in rows:
    m = r.get("message", {})
    if not isinstance(m.get("content"), list): continue
    for b in m["content"]:
        if b.get("type") != "tool_use" or b["id"] in seen: continue
        seen.add(b["id"]); acts.append((r.get("timestamp", ""), b))
c = collections.Counter(b["name"] for _, b in acts)
print(f"# {sys.argv[2]}: action timeline (extracted from the raw transcript)\n")
print(f"Source: `{sys.argv[1].split('/')[-1]}`, a verbatim copy of the Claude Code subagent transcript (see the matching `.meta.json`). Times are UTC (IST = UTC+2).\n")
print(f"**First/last record:** {rows[0].get('timestamp')} → {rows[-1].get('timestamp')}\n")
print("**Totals (unique tool calls):** " + ", ".join(f"{k} {v}" for k, v in c.most_common()) + "\n")
print("| # | Time (UTC) | Tool | Target |\n|---|---|---|---|")
for n, (ts, b) in enumerate(acts, 1):
    i = b.get("input", {})
    tgt = i.get("url") or i.get("query") or i.get("file_path") or i.get("pattern") or i.get("path") or ""
    if b["name"] == "SubagentHandback": tgt = "final report to Boss"
    tgt = str(tgt).replace("/Users/dariapetel/Desktop/claude1/", "").replace("|", "\\|")
    print(f"| {n} | {ts[11:19]} | {b['name']} | {tgt[:140]} |")
