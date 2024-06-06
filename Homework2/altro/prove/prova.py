from commands import *
from utilities import *

win_psping(target_name="atl.speedtest.clouvider.net", K=5, L=100, result_file="prova_win_ping.txt")
print(parse_ping_result(open("prova_win_ping.txt").read(), win_psping))