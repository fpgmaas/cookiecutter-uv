"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()
mod_symbol = '<code class="doc-symbol doc-symbol-nav doc-symbol-module"></code>'

root = Path(__file__).parent.parent
src = root / "cookiecutter_pytorch_lightning_example"

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    # Skip __init__ and private modules
    if parts[-1] == "__init__" or parts[-1].startswith("_"):
        continue

    nav_parts = [f"{mod_symbol} {part}" for part in parts]
    if len(nav_parts) == 0:
        continue
    nav[tuple(nav_parts)] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        if doc_path.name == "index.md":
            for md in path.parent.glob("*.md"):
                with open(md) as md_fd:
                    fd.write(md_fd.read())
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, ".." / path.relative_to(root))

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
