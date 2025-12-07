from pathlib import Path

path = Path("backend/main.py")
text = path.read_text()
start = text.find("# CSV Sprint Plans endpoints")
if start == -1:
    raise SystemExit("start marker not found")
marker = '\n@app.get("/api/risk-assessments")'
end = text.find(marker, start)
if end == -1:
    raise SystemExit("end marker not found")
path.write_text(text[:start] + text[end:])

