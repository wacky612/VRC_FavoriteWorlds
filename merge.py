#!/usr/bin/env python

import os
import json
from pathlib import Path

data = []

for filename in os.listdir('category'):
    path     = Path('category') / filename
    category = json.loads(path.read_text())
    data.append(category)

Path('gh-pages/data.json').write_text(json.dumps(data, indent=4, ensure_ascii=False))
