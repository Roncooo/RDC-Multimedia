from utilities import find_nodes_with_ping
from utilities import find_min_ttl_with_traceroute
import time

def number_of_nodes_with_ping_and_traceroute(target_name):
    print(f"Calculating numeber of nodes to reach {target_name} using ping and traceroute")
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


def main():
    ttl = 30
    K = 10 # number of packets
    L = 20 # number of bytes
    target_name = "atl.speedtest.clouvider.net"
    result_file = "ping_request.txt"
    
    # number_of_nodes_with_ping_and_traceroute(target_name)
    

if __name__ == "__main__":
    main()