from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
scripts = [
    'src/01_extract_uploaded_prices.py',
    'src/02_clean_price_panel.py',
    'src/03_fort_hills_decision_model.py',
    'src/04_build_figures.py',
]
for script in scripts:
    print(f"\n--- Running {script} ---")
    subprocess.run([sys.executable, str(ROOT / script)], check=True)
print("\nPipeline complete.")
