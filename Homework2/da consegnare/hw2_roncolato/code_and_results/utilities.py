import os
import time
import ast
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures._base import Future
from typing import List
from commands import win_ping, win_traceroute
from parsers import win_ping_reached_ita, parse_ping_result


class Result:
    """
    Represents the results of a ping command
    
    Attributes:
        L_bytes:    size of the packets sent by the ping command
        rtt_list:   list of round trip times of the packets
    """
    def __init__(self, l_bytes: int, list: List[float]):
        self.L_bytes = l_bytes
        self.rtt_list = list
    def __str__(self):
        return f"[{self.L_bytes}, {self.rtt_list}]"


def number_of_nodes_with_ping_and_traceroute(
    min_ttl: int, 
    max_ttl: int, 
    max_threads: int, 
    target_name:str, 
    source_name: str
) -> int:
    """
    Calculates the number of nodes to reach the target using both ping and traceroute. 
    Prints the output and returns the value if they coincide, otherwise raises the error.
    """
    
    print(f"Calculating numeber of nodes to reach {target_name} from {source_name} using ping and traceroute")
    print(f"Could take around 2 minutes")
    title_pattern = "{:^12}|{:^10}|{:^10}"
    elements_pattern = "{:^12}|{:^10}|{:^10.3f}s"
    print(title_pattern.format("Command", "# Nodes", "Ex. time"))
    
    start_time = time.time()
    n_ping = find_nodes_with_ping(
        target_name=target_name, 
        min_ttl=min_ttl, 
        max_ttl=max_ttl, 
        max_workers=max_threads
    ) 
    end_time = time.time()
    print(elements_pattern.format("ping", n_ping, end_time-start_time))
    
    start_time = time.time()
    n_traceroute = find_min_ttl_with_traceroute(target_name=target_name) 
    end_time = time.time()
    print(elements_pattern.format("traceroute", n_traceroute, end_time-start_time))
    
    if n_traceroute==n_ping:
        return n_ping
    else:
        raise Exception("Number of nodes differ from ping to traceroute")


def find_nodes_with_ping_callback(future: Future) -> None:
    """
    Callback for the parallelized threads in find_nodes_with_ping function. 
    Reads, parses and deletes the file associated to future.
    Used to understand if the ping command associated to future does reach destination or not.
    """
    file_name, ttl = future.args
    f = open(file_name)
    result_string = f.read()
    f.close()
    os.remove(file_name)
    reached_destination = win_ping_reached_ita(result_string)
    future.result = ttl, reached_destination
    

def find_nodes_with_ping(
    target_name, 
    min_ttl=1, 
    max_ttl=40, 
    max_workers=10
) -> int:
    """
    Simultaneously performs n different ping commands from min_ttl to max_ttl.
    Uses find_nodes_with_ping_callback to find the minimum value of ttl that lets the packet reach the destination.
    Returns the minimum ttl, that is the number of nodes between source and target.
    """
    K=1 # number of packets sent for each ping
    L=1 # number of bytes sent for each packet
    temp_file_name_pattern = "temp_ping_ttl_{}.txt"
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        # Submit tasks to the executor
        for ttl in range(min_ttl, max_ttl+1):
            temp_file_name = temp_file_name_pattern.format(str(ttl))
            future = executor.submit(win_ping, target_name=target_name, ttl=ttl, K=K, L=L, result_file=temp_file_name)
            future.args = temp_file_name, ttl
            future.add_done_callback(find_nodes_with_ping_callback)
            futures.append(future)

    number_of_nodes = 0
    for future in futures:
        if(future.result[1]==True):
            number_of_nodes = future.result[0]
            return number_of_nodes


def find_min_ttl_with_traceroute(
    target_name, 
    output_file="temp_traceroute_result.txt"
) -> int:
    """
    Finds the number of nodes between source and target using a single call to traceroute function.
    """
    win_traceroute(target_name=target_name, result_file=output_file)
    f = open(output_file)
    result_string = f.read()
    f.close()
    os.remove(output_file)
    
    # retreive the first number of the last row with numbers (third to last)
    last_row = result_string.splitlines()[-3]
    first_word = last_row.split()[0]
    number_of_nodes = int(first_word)
    
    return number_of_nodes


def perform_pings_callback(future: Future) -> None:
    """
    Callback for the parallelized threads in perform_pings_and_save_into_file.
    Reads, parses and deletes the file associated to future.
    Used to create a Result object that represents the results of a ping call.
    """
    temp_file_name, L_byte, function = future.args
    f = open(temp_file_name)
    result_string = f.read()
    f.close()
    os.remove(temp_file_name)
    list = parse_ping_result(result_string, function)
    future.result = Result(L_byte, list)


def perform_pings_and_save_into_file(
    K: int, 
    min_L_byte: int, 
    max_L_byte: int,
    max_threads: int, 
    L_byte_step: int, 
    output_file: str, 
    target_name: str, 
    function
):
    """
    Performs simultaneous call to the ping function represented by function parameter.
    Saves the results in outpout file
    """
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        # Submit tasks to the executor
        for L_byte in range(min_L_byte,max_L_byte+1,L_byte_step):
            temp_file_name = f"temp_ping_result_L_{L_byte}.txt"
            future = executor.submit(function, target_name=target_name, K=K, result_file=temp_file_name)
            
            future.args = temp_file_name, L_byte, function
            future.add_done_callback(perform_pings_callback)
            futures.append(future)

    with open(output_file, "w") as file:
        for future in futures:
            result: Result = future.result
            file.write(str(result))
            file.write("\n")


def parse_ping_result_data(file_name: str) -> List[Result]:
    """
    Reads a ping result file (as produced in perform_pings_and_save_into_file) and returns a list of results.
    """
    list = []
    with open(file_name, "r") as file:
        result_string = file.read()
        for line in result_string.splitlines():
            parsed_data = ast.literal_eval(line)
            list.append(Result(parsed_data[0], parsed_data[1]))
    return list
