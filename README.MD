# Archon -> ITL Exporter

`{spec}` and `{class}` should be as they appear in the URL on archon.gg when viewing a spec meta build page.

## First Run

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python3 main.py {spec} {class}
```

## Subsequent Runs

```bash
source .venv/bin/activate

python3 main.py {spec} {class}
```
