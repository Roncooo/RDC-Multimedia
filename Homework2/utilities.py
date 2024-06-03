import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from commands import ping
from commands import traceroute

class Result:
    def __init__(self, l, m):
        self.L = l
        self.M = m
    def __str__(self):
        return f"[L:{self.L}\nM:{self.M}]"


def parse_ping_result(result_string: str)->np.ndarray:
    """
    Returns:
    np.ndarray: one row for each one of the K pings, 
                on the first column the values of time
                on the second column the values of TTL
    """
    
    result_matrix = np.empty([0,2], dtype=int)
    
    for line in result_string.splitlines():
        word_before_time = "durata="
        time_unit = "ms"
        index = line.find(word_before_time)
        if index == -1:
            continue
        time_and_ttl = line[index + len(word_before_time):]
        time = (int) (time_and_ttl[0:time_and_ttl.find(time_unit)])
        ttl = (int) (time_and_ttl[time_and_ttl.find("=")+1:])
        
        result_matrix = np.vstack([result_matrix, [time, ttl]])
    
    return result_matrix


def find_nodes_with_ping_callback(future):
    file_name, ttl = future.args
    f = open(file_name)
    result_string = f.read()
    f.close()
    os.remove(file_name)
    
    ttl_expired: bool = result_string.find("TTL scaduto durante il passaggio")!=-1
    request_expired: bool = result_string.find("Richiesta scaduta")!=-1
    reached_destination: bool = (not ttl_expired) and (not request_expired)
    future.result = ttl, reached_destination
    

def find_nodes_with_ping(target_name, min_ttl=1, max_ttl=20, output_file="nodes_with_ping_result.txt") -> int:
    
    K=1 # number of packets sent for each ping
    L=1 # number of bytes sent for each packet
    temp_file_name_pattern = "temp_ping_ttl_{}.txt"
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        # Submit tasks to the executor
        for ttl in range(min_ttl, max_ttl+1):
            temp_file_name = temp_file_name_pattern.format(str(ttl))
            future = executor.submit(ping, ttl, K, L, target_name, temp_file_name)
            future.args = temp_file_name, ttl
            future.add_done_callback(find_nodes_with_ping_callback)
            futures.append(future)

    number_of_nodes = 0
    found_min_number = False
    with open(output_file, "w") as file:
        file.write("TTL\treached destination\n")
        for future in futures:
            if(found_min_number==False and future.result[1]==True):
                number_of_nodes = future.result[0]
                found_min_number = True
            file.write(f'{future.result[0]}\t{future.result[1]}\n')
        file.write(f'\nThe minimum TTL to reach destination (number of nodes) is {number_of_nodes}\n')
        
    return number_of_nodes


def find_min_ttl_with_traceroute(target_name, output_file="nodes_with_traceroute_result.txt") -> int:
    
    traceroute(target_name, output_file)
    f = open(output_file)
    result_string = f.read()
    f.close()
    
    # retreive the first number of the last row with numbers (third to last)
    last_row = result_string.splitlines()[-3]
    first_word = last_row.split()[0]
    number_of_nodes = int(first_word)
    
    with open(output_file, "w") as file:
        file.write(f'\nThe minimum TTL to reach destination (number of nodes) is {number_of_nodes}\n')
    
    return number_of_nodes