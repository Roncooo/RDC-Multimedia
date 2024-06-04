import os
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures._base import Future
from typing import List
from commands import win_ping
from commands import linux_ping
from commands import win_psping
from commands import traceroute

class Result:
    def __init__(self, l_bytes: int, list: List[float]):
        self.L_bytes = l_bytes
        self.rtt_list = list
    def __str__(self):
        return f"[{self.L_bytes}, {self.rtt_list}]"

def parse_win_psping(result_string: str) -> List[float]:
    result_array = []
    time_unit = "ms"
    first_word_of_result_line = "Reply from"
    time_prefix = ": "
    for line in result_string.splitlines():
        if line=="" or line[:len(first_word_of_result_line)]!=first_word_of_result_line:
            continue
        index = line.find(time_prefix)
        if index == -1:
            continue
        time_word = line[index + len(time_prefix):]
        time = float(time_word[0:time_word.find(time_unit)])
        result_array.append(time)
    return result_array


def parse_win_ping(result_string: str) -> List[float]:
    result_array = []
    time_prefix = "durata="
    measure_unit = "ms"
    for line in result_string.splitlines():
        if line=="":
            continue
        index = line.find(time_prefix)
        if index == -1:
            continue
        time_word = line[index + len(time_prefix):].split()[0]
        time = float(time_word[:len(time_word)-len(measure_unit)])
        result_array.append(time)
    return result_array

def parse_linux_ping(result_string: str) -> List[float]:
    result_array = []
    time_prefix = "time="
    for line in result_string.splitlines():
        if line=="":
            continue
        index = line.find(time_prefix)
        if index == -1:
            continue
        time_word = line[index + len(time_prefix):]
        time = float(time_word.split()[0])
        result_array.append(time)
    return result_array


def parse_ping_result(result_string: str, function) -> List[float]:
    """
    Returns:
    np.array with the RTTs of the K packages 
    """
    if function==win_psping:
        return parse_win_psping(result_string)
    if function==win_ping:
        return parse_win_ping(result_string)
    if function==linux_ping:
        return parse_linux_ping(result_string)


def find_nodes_with_ping_callback(future: Future) -> None:
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
            future = executor.submit(win_ping, target_name, ttl, K, L, True, temp_file_name)
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