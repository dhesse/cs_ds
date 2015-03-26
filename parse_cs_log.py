import sys
import re

kill_pattern = re.compile('.+"(.+?)" killed "(.+?)" with "(.+?)"')
name_pattern = re.compile('(.+?)\\<(.+?)\\>\\<(.+?)\\>\\<(.+?)\\>')

header = "round, killer, killer_ptype, killer_team, victim, victim_ptype, victim_team, weapon"
print header

game_round = 0
for line in open(sys.argv[1]):
    if "Round_End" in line:
        game_round += 1
    else:
        match = re.search(kill_pattern, line)
        if match:
            print "{},".format(game_round),
            who, whom, weapon = match.groups()
            for person in (who, whom):
                name, _, kind, team = re.search(name_pattern, person).groups()
                print "{}, {}, {},".format(name, kind, team),
            print weapon
