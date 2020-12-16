from random import choice

WEAPON_USE_PROB = 0.85
WEAPON_EQUIPE_PROB = 0.6

WEAPONS = [
    {
        'name': 'laser gun',
        'get_message': lambda name:
            f'{name} finds a laser gun lying around 🔫',
        'use_message': lambda first, second:
            f'{first} uses the laser beam causing {second} to instantly melt',
        'damage_range': [1000, 2000]
    },
    {
        'name': 'pistol',
        'get_message': lambda name:
            f'{name} obtains a pistol',
        'use_message': lambda first, second:
            f'{first} fires the pistol and shoots {second}',
        'damage_range': [40, 50]
    },
    {
        'name': 'rocket launcher',
        'get_message': lambda name:
            f'A rocket launcher miraculously falls from the sky to {name}\'s hands',
        'use_message': lambda first, second:
            f'{first} sends rockets flying at {second}',
        'damage_range': [70, 90]
    },
    {
        'name': 'stick',
        'get_message': lambda name:
            f'{name} finds a stick',
        'use_message': lambda first, second:
            f'{first} bonks {second} with the stick',
        'damage_range': [10, 15]
    },
    {
        'name': 'knife',
        'get_message': lambda name:
            f'{name} grabs a knife and smiles with murderous intent',
        'use_message': lambda first, second:
            f'{first} stabs {second} with the knife',
        'damage_range': [30, 55]
    },
    {
        'name': 'shotgun',
        'get_message': lambda name:
            f'{name} finds a shotgun inside a crate',
        'use_message': lambda first, second:
            f'{first} fires the shotgun right at {second}',
        'damage_range': [50, 65]
    },
    {
        'name': 'kung fu',
        'get_message': lambda name:
            f'{name} finds an ancient kung fu manuscript containing secret techniques',
        'use_message': lambda first, second:
            f'{first} faces {second} and unleashes a spinning double smash kick',
        'damage_range': [70, 85]
    },
    {
        'name': 'holy hand grenade',
        'get_message': lambda name:
            f'{name} acquires a holy hand grenade',
        'use_message': lambda first, second:
            f'{first} removes the pin of the holy grenade, counts to three, and throws it at {second} ' + \
            'sacred anthems can be heard near the massive explosion',
        'damage_range': [1000, 2000]
    },
    {
        'name': 'fake holy hand grenade',
        'get_message': lambda name:
            f'{name} acquires a holy hand grenade',
        'use_message': lambda first, second:
            f'{first} removes the pin of the holy grenade, and attempts to throws it at {second} ' + \
            'but accidentally counts to four instead of three causing the grenade to explode early',
        'damage_range': [1000, 2000],
        'fake': True
    },
    {
        'name': 'charizord',
        'get_message': lambda name:
            f'{name} captures a wild charizord',
        'use_message': lambda first, second:
            f'{first} command charizord to use dragon breath on {second}, it\'s kinda effictive',
        'damage_range': [32, 37]
    },
    {
        'name': 'red shell',
        'get_message': lambda name:
            f'{name} finds what seems to be an empty red shell of a turtle',
        'use_message': lambda first, second:
            f'{first} throws the red shell at {second}',
        'damage_range': [40, 55]
    },
    {
        'name': 'mega buster',
        'get_message': lambda name:
            f'{name} opens a crate and finds a mega buster',
        'use_message': lambda first, second:
            f'{first} fires a charged shot at {second}',
        'damage_range': [60, 70]
    }
]

IDLE_SINGLE_MESSAGES = [
    lambda name: f'{name} is relaxing',
    lambda name: f'{name} is building a shelter',
    lambda name: f'{name} takes a nap',
    lambda name: f'{name} stares at the clouds',
    lambda name: f'{name} does yoga',
    lambda name: f'{name} wonders: \'what am i doing here?\'',
    lambda name: f'{name} finds a burrito',
    lambda name: f'{name} plays on the 4ds for a while',
    lambda name: f'{name} is in deep sleep',
    lambda name: f'{name} builds a tree house',
    lambda name: f'{name} finds some coins',
    lambda name: f'{name} is doing some boxing exercises'
]

IDLE_PAIR_MESSAGES = [
    lambda first, second: f'{first} and {second} race to test their stamina' + \
        f' {choice([first, second])} wins by miles',
    lambda first, second: f'{first} annoys {second} with bad jokes',
    lambda first, second: f'{first} cooks some food, {second} ' + \
        choice(['thinks it\'s really bad, but eats anyway',
        'thinks it\'s ok',
        'thinks it tastes amazing']),
    lambda first, second: f'{first} and {second} spar a bit',
]

IDLE_TEAM_MESSAGES = [
    lambda names: f'{names} are playing party games',
    lambda names: f'{names} play truth or dare',
    lambda names: f'{names} build a huge mansion',
    lambda names: f'{names} take shifts guarding each other',
    lambda names: f'{names} sing around the camp fire'
]
