import os

root_dir = "."

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".py"):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    if "class Storage" in line:
                        print(f"Found in {filepath} at line {i}: {line.strip()}")
