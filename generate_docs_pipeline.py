import os
import json
import subprocess
import markdown

# === CONFIGURATION ===
INPUT_FILE = "datapackage.json"
OUTPUT_DIR = "docs"
LIVEMARK_YML = os.path.join(OUTPUT_DIR, "livemark.yml")
USE_EMOJI = True  # Use ✅/❌ for required fields
RUN_LIVEMARK_BUILD = True  # Set False to skip building
GENERATE_HTML = True

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load datapackage
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    package = json.load(f)

resources = package.get("resources", [])

# Generate Markdown and HTML docs for each resource
for resource in resources:
    resource_name = resource["name"]
    title = resource_name.replace("-", " ").title()
    schema = resource.get("schema", {})
    fields = schema.get("fields", [])
    path = resource.get("path", "unknown")

    md_lines = [
        "---",
        f"title: {title}",
        "---",
        "",
        f"# {title}",
        "",
        f"_Path_: `{path}`",
        "",
        "| Column | Type | Required |",
        "|--------|------|----------|"
    ]

    for field in fields:
        name = field["name"]
        ftype = field.get("type", "string")
        required_raw = field.get("constraints", {}).get("required", False)
        required = "✅" if USE_EMOJI and required_raw else "❌" if USE_EMOJI else "Yes" if required_raw else "No"
        md_lines.append(f"| {name} | {ftype} | {required} |")

    md_content = "\n".join(md_lines)
    md_path = os.path.join(OUTPUT_DIR, f"{resource_name}.md")

    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)
    print(f"✅ Wrote schema doc: {md_path}")

    # Optionally generate HTML
    if GENERATE_HTML:
        html_content = markdown.markdown(md_content)
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5.2.0/github-markdown.min.css">
  <style>
    body {{
      max-width: 960px;
      margin: 2em auto;
      padding: 1em;
    }}
  </style>
</head>
<body class="markdown-body">
{html_content}
</body>
</html>
"""
        html_path = os.path.join(OUTPUT_DIR, f"{resource_name}.html")
        with open(html_path, "w", encoding="utf-8") as html_file:
            html_file.write(html_template)
        print(f"🌐 Wrote HTML doc: {html_path}")

# Generate index.md with links to all interface docs
index_lines = [
    "# File-Based Interface Documentation",
    "",
    "Welcome to the documentation portal for all file-based interfaces.",
    "",
    "## Interfaces",
    ""
]

for res in resources:
    name = res["name"]
    title = name.replace("-", " ").title()
    filename = f"{name}.md"
    index_lines.append(f"- [{title}]({filename})")

index_path = os.path.join(OUTPUT_DIR, "index.md")
with open(index_path, "w", encoding="utf-8") as index_file:
    index_file.write("\n".join(index_lines))
print(f"✅ Wrote index page: {index_path}")

# Generate livemark.yml nav section
nav_interfaces = []
for res in resources:
    name = res["name"]
    title = name.replace("-", " ").title()
    filename = f"{name}.md"
    nav_interfaces.append(f"      - {title}: {filename}")

nav_section = "\n".join(nav_interfaces)

livemark_content = f"""site:
  title: File-Based Interface Documentation
  description: Documentation portal for all file-based data interfaces and schemas
  logo: https://yourcompany.com/logo.png
  favicon: https://yourcompany.com/favicon.ico
  baseurl: ""
  keywords:
    - file interface
    - csv schema
    - frictionless
    - datapackage
  repository: https://github.com/your-org/your-docs-repo
  license: MIT

theme:
  palette: light
  highlight: github

nav:
  - Home: index.md
  - Interfaces:
{nav_section}
"""

with open(LIVEMARK_YML, "w", encoding="utf-8") as yml_file:
    yml_file.write(livemark_content)
print(f"✅ Wrote Livemark config: {LIVEMARK_YML}")

# Optionally run livemark build
if RUN_LIVEMARK_BUILD:
    try:
        print("\n🚧 Running `livemark build` ...")
        subprocess.run(["livemark", "build", os.path.join(OUTPUT_DIR, "index.md")], check=True)
        print("✅ Livemark build completed successfully!")
    except Exception as e:
        print(f"❌ Error running livemark build: {e}")
