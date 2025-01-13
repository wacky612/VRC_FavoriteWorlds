#!/usr/bin/env python

import os
import sys
import json
from pathlib import Path

data = []

for i in range(1, len(sys.argv)):
    data = json.loads(Path(sys.argv[i]).read_text())
    data['Worlds'].sort(key=lambda w: w['Name'])
    Path(sys.argv[i]).write_text(json.dumps(data, indent=4, ensure_ascii=False))
