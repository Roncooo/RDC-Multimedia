from utilities import find_nodes_with_ping
from utilities import find_min_ttl_with_traceroute
from commands import win_ping
from commands import linux_ping
from commands import win_traceroute
from commands import linux_traceroute
import time

def number_of_nodes_with_ping_and_traceroute(target_name:str, ping_function, traceroute_function):
    print(f"Calculating numeber of nodes to reach {target_name} using ping and traceroute")
    print(f"Could take around 2 minutes")
    title_pattern = "{:^12}|{:^10}|{:^10}"
    elements_pattern = "{:^12}|{:^10}|{:^10.3f}s"
    print(title_pattern.format("Command", "# Nodes", "Ex. time"))
    
    start_time = time.time()
    n_ping = find_nodes_with_ping(target_name, ping_function)  # takes around 10 seconds
    end_time = time.time()
    print(elements_pattern.format("ping", n_ping, end_time-start_time))
    
    start_time = time.time()
    n_traceroute = find_min_ttl_with_traceroute(target_name=target_name, traceroute_function=traceroute_function) # takes around 90 seconds
    end_time = time.time()
    print(elements_pattern.format("traceroute", n_traceroute, end_time-start_time))


target_name = "lyon.testdebit.info"
number_of_nodes_with_ping_and_traceroute(target_name, win_ping, win_traceroute)
