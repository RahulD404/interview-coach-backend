import os

def save_tree(start_path, output_file, exclude=("__pycache__", ".git", ".venv", "venv310", "node_modules","venv")):
    with open(output_file, "w", encoding="utf-8") as f:
        for root, dirs, files in os.walk(start_path):
            # filter directories
            dirs[:] = [d for d in dirs if d not in exclude]

            # skip hidden/system folders
            if any(ex in root for ex in exclude):
                continue

            level = root.replace(start_path, "").count(os.sep)
            indent = " " * 4 * level
            f.write(f"{indent}{os.path.basename(root)}/\n")

            sub_indent = " " * 4 * (level + 1)
            for file in files:
                # skip compiled + temp files
                if file.endswith((".pyc", ".log", ".db")):
                    continue
                f.write(f"{sub_indent}{file}\n")

save_tree(".", "project_structure.txt")
print("✅ Saved to project_structure.txt")