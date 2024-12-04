#!/usr/bin/env python

from http.cookiejar import Cookie

import vrchatapi
from vrchatapi.api import authentication_api
from vrchatapi.api.worlds_api import WorldsApi

import time
import json
from pathlib import Path

import sys

auth   = json.loads(Path('private/auth.json').read_text())
cookie = json.loads(Path('private/cookie.json').read_text())

def make_cookie(name, value):
    return Cookie(0, name, value,
                  None, False,
                  "api.vrchat.cloud", True, False,
                  "/", False,
                  False,
                  173106866300,
                  False,
                  None,
                  None, {})

configuration = vrchatapi.Configuration(
    username = auth['Username'],
    password = auth['Password'],
)

with vrchatapi.ApiClient(configuration) as api_client:
    api_client.user_agent = 'WorldInformationFetcher'
    api_client.rest_client.cookie_jar.set_cookie(make_cookie('auth', cookie['AuthCookie']))
    api_client.rest_client.cookie_jar.set_cookie(make_cookie('twoFactorAuth', cookie['TwoFactorAuthCookie']))

    auth_api = authentication_api.AuthenticationApi(api_client)
    current_user = auth_api.get_current_user()
    print("Logged in as:", current_user.display_name)

    worlds_api = WorldsApi(api_client)

    for i in range(1, len(sys.argv)):
        data = json.loads(Path(sys.argv[i]).read_text())

    
        for w in range(0, len(data['Worlds'])):
            if (data['Worlds'][w]['ID'] is not None) and (not ('Platform' in data['Worlds'][w])):
                try:
                    world = worlds_api.get_world(data['Worlds'][w]['ID'])
                    data['Worlds'][w]['Name']                = world.name
                    data['Worlds'][w]['RecommendedCapacity'] = world.recommended_capacity
                    data['Worlds'][w]['Capacity']            = world.capacity
                    data['Worlds'][w]['Description']         = world.description

                    pc      = True in [p.platform == 'standalonewindows' for p in world.unity_packages]
                    android = True in [p.platform == 'android'           for p in world.unity_packages]
                    data['Worlds'][w]['Platform']            = {}
                    data['Worlds'][w]['Platform']['PC']      = pc
                    data['Worlds'][w]['Platform']['Android'] = android
                        
                    print(f'{w+1:02}     Found ワールド名: {world.name}')

                except vrchatapi.exceptions.NotFoundException:
                    data['Worlds'][w]['ID'] = None
                    print(f'{w+1:02} Not Found ワールド名: {data['Worlds'][w]['Name']}')

                except Exception as e:
                    print(f'{w+1:02} Crashed!! ワールド名: {data['Worlds'][w]['Name']}')
                    Path(sys.argv[i]).write_text(json.dumps(data, indent=4, ensure_ascii=False))
                    raise e

                time.sleep(3)
            else:
                print(f'{w+1:02} Skipped   ワールド名: {data['Worlds'][w]['Name']}')

        Path(sys.argv[i]).write_text(json.dumps(data, indent=4, ensure_ascii=False))
