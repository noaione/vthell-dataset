import json
from os.path import splitext
from pathlib import Path

import jsonschema

dataset_path = Path(__file__).absolute().parent.parent


all_json_files = list(dataset_path.glob("*.json"))
print("[*] Loading datasets")
compiled_dataset = {}
for json_f in all_json_files:
    name, _ = splitext(json_f.name)
    with json_f.open() as f:
        compiled_dataset[name] = json.load(f)
print(f"[*] Datasets loaded ({len(compiled_dataset)} entries)")

with open(dataset_path / "_schema.schema") as fp:
    schema = json.load(fp)


print("[*] Validating datasets...")
errors = []
for name, content in compiled_dataset.items():
    try:
        print(f"[*] Validating {name}...", end="\r")
        jsonschema.validate(content, schema)
        print(f"[+] Validating {name}... OK", end="\r")
    except jsonschema.ValidationError as e:
        print(f"[-] Validating {name}... FAILED", end="\r")
        print()
        print(e)
        errors.append(name)
    print()

if errors:
    print("\n[*] Validation failed for the following datasets:")
    for name in errors:
        print(f"  - {name}")
    exit(1)

print("\n[*] Validation successful")
