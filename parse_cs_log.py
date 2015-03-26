import sys
import re
import os

KILL_PATTERN = re.compile('.+"(.+?)" killed "(.+?)" with "(.+?)"')
NAME_PATTERN = re.compile('(.+?)<(.+?)><(.+?)><(.+?)>')
NAME_CHANGE_PATTERN = re.compile('.+?: "(.+?)" changed name to "(.+?)"')

HEADER_KILLS = "map, round, killer, killer_ptype, killer_team, victim, victim_ptype, victim_team, weapon"

ALIASES = {}

class ParseResult(object):
    def __init__(self):
        self.kills = []
        self.map_no = 0
    def append(self, kills):
        if kills:
            self.map_no += 1
            for kill in kills:
                self.kills.append([str(self.map_no)] + kill)
    def __str__(self):
        return "\n".join(",".join(k for k in kill) for kill in self.kills)
        

def read_logs(log_directory):
    assert(os.path.isdir(log_directory))
    result = ParseResult()
    for logfile in sorted(os.listdir(log_directory)):
        result.append(parse_log_file(os.path.join(log_directory, logfile)))
    return result


def parse_log_file(log_file):
    result = []
    game_round = 1
    for line in open(log_file):
        if "Round_End" in line:
            game_round += 1
        match = re.search(KILL_PATTERN, line)
        if match:
            kill = [str(game_round)]
            who, whom, weapon = match.groups()
            for person in (who, whom):
                name, _, kind, team = re.search(NAME_PATTERN, person).groups()
                kill += [ALIASES.setdefault(name, name), kind, team]
            kill.append(weapon)
            result.append(kill)
        match = re.search(NAME_CHANGE_PATTERN, line)
        if match:
            old, new_name = match.groups()
            old_name, _, _, _ = re.search(NAME_PATTERN, old).groups()
            if old_name != "Player":
                ALIASES[new_name] = ALIASES[old_name]
                del ALIASES[old_name]
    return result

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print "Usage: {} path/to/logs".format(sys.argv[0])
        sys.exit()
    result = read_logs(sys.argv[1])
    print HEADER_KILLS
    print result
