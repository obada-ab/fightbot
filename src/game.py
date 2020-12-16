from random import randint, shuffle
from typing import List
from team import Team

class Game:
    def __init__(self, player_names, player_ids):
        players_info = self._split_info(player_names, player_ids)
        self._teams = [Team(names, indexes) for names, indexes in players_info]
        self._index = 0
        self._is_first_loop = True
    
    def tick(self):
        if len(self._teams) == 1:
            return [
                f'{self._teams[0].to_string()} win!',
                self._teams[0].get_members(),
                True
            ]
        if self._is_first_loop:
            text = self._teams[self._index].to_string() + \
             (' goes solo' if self._teams[self._index].get_member_count() == 1 else ' team up')
            ret = [
                text,
                self._teams[self._index].get_members(),
                False
            ]
            self._index += 1
            if self._index == len(self._teams):
                self._index = 0
                self._is_first_loop = False
            return ret
        team = self._teams[self._index]
        other_index = randint(0, len(self._teams) - 2)
        if other_index >= self._index:
            other_index += 1
        other_team = self._teams[other_index]
        ret = team.tick(other_team)
        self._remove_team_if_dead(other_team)
        self._remove_team_if_dead(team)
        if self._index >= len(self._teams):
            if team.is_turn_done():
                self._index = 0
            else:
                self._index -= 1
        elif self._teams[self._index] == team:
            if team.is_turn_done():
                self._index = (self._index + 1) % len(self._teams)
        ret.append(False)
        return ret
    
    def _remove_team_if_dead(self, team) -> None:
        if team.get_member_count() == 0:
            self._teams.remove(team)

    @classmethod
    def _split_info(cls, names, indexes: List, min_chunk: int = 1, max_chunk: int = 3):
        i = 0
        result = []

        temp = list(zip(names, indexes))
        shuffle(temp)

        names, indexes = zip(*temp)

        while i < len(names):
            next_chunk = randint(min_chunk, max_chunk)
            next_chunk = min(next_chunk, len(names) - i)
            result.append([names[i:i+next_chunk], indexes[i:i+next_chunk]])
            i += next_chunk
        return result
