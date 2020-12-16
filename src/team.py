from random import choice, shuffle
from player import Player
from game_data import IDLE_SINGLE_MESSAGES, IDLE_PAIR_MESSAGES, IDLE_TEAM_MESSAGES

class Team:
    def __init__(self, names, indexes):
        self._members = [Player(name, index) for name, index in zip(names, indexes)]
        self._index = 0
        self._idle_queue = []
    
    def get_random_member(self):
        return choice(self._members)
    
    def remove_member_if_dead(self, member):
        if member.get_health() == 0:
            self._members.remove(member)
    
    def tick(self, other_team):
        if self._index == 0:
            shuffle(self._members)
        ret = None
        while ret is None and self._index < len(self._members):
            member = self._members[self._index]
            other_member = other_team.get_random_member()
            ret = member.tick(other_member)
            other_team.remove_member_if_dead(other_member)
            self.remove_member_if_dead(member)
            if ret is None:
                self._idle_queue.append(member)
            self._index += 1
        if ret is None:
            if len(self._idle_queue) == 1:
                ret = [
                    choice(IDLE_SINGLE_MESSAGES)(self._idle_queue[0].get_name()),
                    self._idle_queue.copy()
                ]
            elif len(self._idle_queue) == 2:
                ret = [
                    choice(IDLE_PAIR_MESSAGES)(self._idle_queue[0].get_name(),
                    self._idle_queue[1].get_name()),
                    self._idle_queue.copy()
                ]
            else:
                ret = [
                    choice(IDLE_TEAM_MESSAGES)(self.to_string(self._idle_queue)),
                    self._idle_queue.copy()
                ]
            self._idle_queue.clear()
            self._index = 0
        if self._index == len(self._members) and len(self._idle_queue) == 0:
            self._index = 0
        return ret
    
    def get_member_count(self):
        return len(self._members)
    
    def get_members(self):
        return self._members.copy()
    
    def to_string(self, members = None):
        if members is None:
            members = self._members
        ret = members[0].get_name()
        for i in range(1, len(self._members)):
            if i != len(members) - 1:
                ret +=  ', ' + members[i].get_name()
            else:
                ret += ' and ' + members[i].get_name()
        return ret
    
    def is_turn_done(self):
        return self._index == 0
        