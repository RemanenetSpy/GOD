import sys
import os
import urllib.request
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Helper to load from local gitignored .env if present
def load_env():
    env_path = os.path.abspath(".env")
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    if k not in os.environ:
                        os.environ[k] = v

load_env()

token = os.environ.get("HF_TOKEN", "")
base_url = 'https://huggingface.co/datasets/Explorerp/sovereign-civilization-memory/raw/main/'
files = ['civilization_universe_a.json', 'civilization_universe_b.json', 'civilization_universe_c.json']

data = {}
for f in files:
    url = base_url + f
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        data[f] = json.loads(response.read().decode('utf-8'))

for f, d in data.items():
    print('======================================================================')
    print('FILE:', f)
    print('Mode:', d.get('mode_name'))
    print('Substrate:', d.get('substrate_name'))
    print('Step Count:', d.get('step_num'))
    print('Population:', d.get('population'))
    print('Total Subroutines:', d.get('total_subroutines'))
    c = d.get('climate') or {}
    print(f"Climate: Season={c.get('season')} | Temp={c.get('ambient_temp')} | Regrowth={c.get('regrowth_rate')} | Solar%={c.get('solar_phase')} | Caches={c.get('cache_count')} | Famine={c.get('is_famine')}")
    print('Subroutines:')
    subs = d.get('subroutines', {})
    for sig, code in subs.items():
        first_line = code.strip().split('\n')[0]
        print(f"  • [{sig}] -> {first_line}")
