from utilities import find_nodes_with_ping
from utilities import find_min_ttl_with_traceroute
import time

def number_of_nodes_with_ping_and_traceroute(target_name):
    print(f"Calculating numeber of nodes to reach {target_name} using ping and traceroute")
    print(f"Could take around 2 minutes")
    title_pattern = "{:^12}|{:^10}|{:^10}"
    elements_pattern = "{:^12}|{:^10}|{:^10.3f}s"
    print(title_pattern.format("Command", "# Nodes", "Ex. time"))
    
    start_time = time.time()
    n_ping = find_nodes_with_ping(target_name)  # takes around 10 seconds
    end_time = time.time()
    print(elements_pattern.format("ping", n_ping, end_time-start_time))
    
    start_time = time.time()
    n_traceroute = find_min_ttl_with_traceroute(target_name) # takes around 90 seconds
    end_time = time.time()
    print(elements_pattern.format("traceroute", n_traceroute, end_time-start_time))


target_name = "atl.speedtest.clouvider.net"
number_of_nodes_with_ping_and_traceroute(target_name)