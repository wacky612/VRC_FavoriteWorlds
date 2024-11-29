#!/usr/bin/env python

import sys
import time
import json
from pathlib import Path
import vrchatapi
from vrchatapi.api.worlds_api import WorldsApi

with vrchatapi.ApiClient() as api_client:
    api_client.user_agent = "VRC_FavoriteWorlds"
    world_api = WorldsApi(api_client)

    for i in range(1, len(sys.argv)):

        data = json.loads(Path(sys.argv[i]).read_text())

        for j in range(0, len(data['Worlds'])):
            if not ('Description' in data['Worlds'][j]):
                world = world_api.get_world(data['Worlds'][j]['ID'])
                data['Worlds'][j]['Name']                = world.name
                data['Worlds'][j]['RecommendedCapacity'] = world.recommended_capacity
                data['Worlds'][j]['Capacity']            = world.capacity
                data['Worlds'][j]['Description']         = world.description
                time.sleep(1)

        Path(sys.argv[i]).write_text(json.dumps(data, indent=4, ensure_ascii=False))
