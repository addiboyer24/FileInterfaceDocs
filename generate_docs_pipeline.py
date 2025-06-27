import os
import subprocess

docs_dir = "docs"
index_file = os.path.join(docs_dir, "index.md")
livemark_config = os.path.join(docs_dir, "livemark.yml")

# Ensure docs directory exists
os.makedirs(docs_dir, exist_ok=True)

# Create .nojekyll file to avoid Jekyll processing on GitHub Pages
with open(os.path.join(docs_dir, ".nojekyll"), "w") as f:
    f.write("")

# Create livemark.yml config if it doesn't exist
if not os.path.exists(livemark_config):
    with open(livemark_config, "w") as f:
        f.write("title: Interface Documentation\nsource: .\n")

# Create index.md with links to other .md files
if not os.path.exists(index_file):
    md_files = [
        f for f in os.listdir(docs_dir)
        if f.endswith(".md") and f != "index.md"
    ]
    with open(index_file, "w") as f:
        f.write("# 📚 Interface Documentation Index\n\n")
        for md in sorted(md_files):
            title = md.replace("-", " ").replace(".md", "").title()
            f.write(f"- [{title}]({md})\n")

# Try to run livemark and capture output
try:
    result = subprocess.run(
        ["livemark", "build", docs_dir],
        check=True,
        capture_output=True,
        text=True
    )
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("❌ Livemark build failed!")
    print("STDOUT:\n", e.stdout)
    print("STDERR:\n", e.stderr)
    raise
