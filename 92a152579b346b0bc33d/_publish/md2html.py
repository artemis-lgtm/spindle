"""Render every project .md into a styled sibling .html so the package reads in a browser
(GitHub Pages and local disk alike). Run with a python that has `markdown` installed:
    <venv>/bin/python _publish/md2html.py
Skips site/, cad/.venv, node_modules. Links to other .md files are rewritten to .html.
"""
import pathlib, re, html, markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = ("site/", "cad/.venv", "node_modules", "_publish/", "renders-final/src", "cad/rfq/dome-cap-lit/")

TPL = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | Spindle</title>
<style>
:root{{--bg:#f6f2ea;--ink:#1b1916;--mute:#6b645a;--line:#e3dccf;--accent:#b8732e;--panel:#fffdf8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#121110;--ink:#ece6da;--mute:#a19887;--line:#2c2925;--accent:#e6a456;--panel:#1a1816}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Inter",system-ui,sans-serif}}
main{{max-width:880px;margin:0 auto;padding:28px 16px 80px}}
a{{color:var(--accent)}} .back{{font-size:14px;display:inline-block;margin-bottom:18px}}
h1{{font-size:28px;line-height:1.2}} h2{{margin-top:36px;font-size:21px}} h3{{font-size:17px}}
table{{border-collapse:collapse;width:100%;display:block;overflow-x:auto;font-size:14px}}
th,td{{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}} th{{background:var(--panel)}}
code{{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:0 4px;font-size:.9em}}
pre{{background:var(--panel);border:1px solid var(--line);padding:12px;overflow-x:auto;border-radius:8px}}
img{{max-width:100%}}
</style></head><body><main><a class="back" href="{back}">Back to START HERE</a>
{body}</main></body></html>"""


def main():
    n = 0
    for md in sorted(ROOT.rglob("*.md")):
        rel = md.relative_to(ROOT).as_posix()
        if any(rel.startswith(s) or s in rel for s in SKIP):
            continue
        text = md.read_text(encoding="utf-8")
        body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
        body = re.sub(r'href="([^":#]+)\.md(#[^"]*)?"', lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', body)
        m = re.search(r"^#\s+(.+)$", text, re.M)
        title = html.escape(m.group(1).strip() if m else md.stem)
        depth = len(md.relative_to(ROOT).parts) - 1
        back = "../" * depth + "START-HERE.html"
        md.with_suffix(".html").write_text(TPL.format(title=title, back=back, body=body), encoding="utf-8")
        n += 1
    print(f"rendered {n} markdown files")


if __name__ == "__main__":
    main()
