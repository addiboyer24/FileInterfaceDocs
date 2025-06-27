import os
import json
import shutil
import subprocess
import markdown

# === CONFIGURATION ===
INPUT_FILE = "datapackage.json"
OUTPUT_DIR = "docs"
CUSTOM_CSS_FILE = "custom.css"  # Optional styling
USE_EMOJI = True
RUN_LIVEMARK_BUILD = True
GENERATE_HTML = True
INCLUDE_BREADCRUMBS = True

# === Setup ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load datapackage
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    package = json.load(f)

resources = package.get("resources", [])
version = package.get("version", None)

# Copy custom.css if present
css_target_path = os.path.join(OUTPUT_DIR, "custom.css")
if os.path.isfile(CUSTOM_CSS_FILE):
    shutil.copy(CUSTOM_CSS_FILE, css_target_path)
    print(f"🎨 Copied custom CSS to: {css_target_path}")
else:
    print("⚠️ No custom.css found – skipping style customization.")

# Generate Markdown and HTML docs
for resource in resources:
    resource_name = resource["name"]
    title = resource_name.replace("-", " ").title()
    schema = resource.get("schema", {})
    fields = schema.get("fields", [])
    path = resource.get("path", "unknown")

    md_lines = [
        "---",
        f"title: {title}",
        f"version: {version or '1.0'}",
        "---",
        "",
        f"# {title}",
        "",
        f"**Path:** `{path}`",
        "",
    ]

    if INCLUDE_BREADCRUMBS:
        md_lines += [f"`📁 {path}`", ""]

    md_lines += [
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

    if GENERATE_HTML:
        html_content = markdown.markdown(md_content, extensions=["tables"])
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5.2.0/github-markdown.min.css">
  {"<link rel='stylesheet' href='custom.css'>" if os.path.isfile(css_target_path) else ""}
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

# Create index.md
index_lines = [
    "# File-Based Interface Documentation",
    "",
    f"_Generated from datapackage.json{f' (v{version})' if version else ''}_",
    "",
    "## Interfaces",
    ""
]

for res in resources:
    name = res["name"]
    title = name.replace("-", " ").title()
    html_link = f"{name}.html"
    index_lines.append(f"- [{title}]({html_link})")

index_path = os.path.join(OUTPUT_DIR, "index.md")
with open(index_path, "w", encoding="utf-8") as index_file:
    index_file.write("\n".join(index_lines))
print(f"✅ Wrote index page: {index_path}")

# Generate livemark.yml
nav_interfaces = []
for res in resources:
    name = res["name"]
    title = name.replace("-", " ").title()
    md_file = f"{name}.md"
    nav_interfaces.append(f"      - {title}: {md_file}")

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

livemark_yml_path = os.path.join(OUTPUT_DIR, "livemark.yml")
with open(livemark_yml_path, "w", encoding="utf-8") as yml_file:
    yml_file.write(livemark_content)
print(f"✅ Wrote Livemark config: {livemark_yml_path}")

# Run Livemark
if RUN_LIVEMARK_BUILD:
    try:
        print("\n🚧 Running `livemark build` ...")
        subprocess.run(["livemark", "build", os.path.join(OUTPUT_DIR, "index.md")], check=True)
        print("✅ Livemark build completed successfully!")
    except Exception as e:
        print(f"❌ Error running livemark build: {e}")
