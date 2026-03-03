import sys, os, pathlib
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'countryinfo_project.settings')

import django
django.setup()

from django.template.loader import get_template
from django.template.exceptions import TemplateSyntaxError

templates_dir = pathlib.Path('Countryinfo_app/templates/countryinfo_app')
errors = []

for p in sorted(templates_dir.glob('*.html')):
    tname = f'Countryinfo_app/{p.name}'
    try:
        get_template(tname)
        print(f'  OK  {p.name}')
    except TemplateSyntaxError as e:
        print(f'FAIL  {p.name}: {e}')
        errors.append((p.name, str(e)))
    except Exception as e:
        print(f'ERR   {p.name}: {e}')

print()
if errors:
    print(f'{len(errors)} template(s) FAILED:')
    for name, msg in errors:
        print(f'  {name}: {msg}')
    sys.exit(1)
else:
    print('All templates parsed successfully.')

