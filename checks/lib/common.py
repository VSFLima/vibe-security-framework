from __future__ import annotations
from pathlib import Path

SKIP_DIRS = {
    ".git", ".idea", ".vscode", ".dart_tool", ".gradle", "build", "dist",
    "node_modules", "vendor", ".venv", "venv", "__pycache__", ".next", ".cache"
}
TEXT_EXTS = {
    ".py",".js",".ts",".tsx",".jsx",".dart",".java",".kt",".kts",".go",".rs",
    ".rb",".php",".cs",".c",".h",".cpp",".hpp",".sh",".bash",".zsh",".ps1",
    ".json",".yaml",".yml",".toml",".ini",".conf",".env",".properties",".xml",
    ".gradle",".md",".txt",".sql"
}
def files_under(root: Path):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p

def read_small_text(p: Path, max_bytes=2_000_000):
    try:
        if p.stat().st_size > max_bytes:
            return None
        if p.suffix.lower() not in TEXT_EXTS and p.name not in {".env",".env.local",".npmrc",".pypirc"}:
            return None
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
