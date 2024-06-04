import os
import ast
from concurrent.futures import Future, ThreadPoolExecutor
from concurrent.futures._base import Future
from typing import List
from utilities import Result, parse_ping_result
from commands import win_psping
# pip install matplotlib
# import matplotlib.pyplot as plt


min_L_byte = 10
max_L_byte = 1472

def callback(future: Future) -> None:
    temp_file_name, L_byte, function = future.args
    f = open(temp_file_name)
    result_string = f.read()
    f.close()
    os.remove(temp_file_name)
    list = parse_ping_result(function, result_string)
    future.result = Result(L_byte, list)

def perform_pings_and_save_into_file(K: int, L_byte_step: int, output_file: str, target_name: str, function=win_psping, max_threads: int=10, min_L_byte: int=10, max_L_byte: int=1472,):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        # Submit tasks to the executor
        for L_byte in range(min_L_byte,max_L_byte+1,L_byte_step):
            temp_file_name = f"ping_result_L_{L_byte}.txt"
            future = executor.submit(function, target_name=target_name, K=K, result_file=temp_file_name)
            
            future.args = temp_file_name, L_byte, function
            future.add_done_callback(callback)
            futures.append(future)

    with open(output_file, "w") as file:
        for future in futures:
            result: Result = future.result
            file.write(str(result))
            file.write("\n")


def parse_ping_result_data(file_name: str) -> List[Result]:
    list = []
    with open(file_name, "r") as file:
        result_string = file.read()
        for line in result_string.splitlines():
            parsed_data = ast.literal_eval(line)
            list.append(Result(parsed_data[0], parsed_data[1]))
    return list



K = 100 # number of packets sent for each L_byte value
target_name = "atl.speedtest.clouvider.net"
L_byte_step=50
max_threads=10
output_file = f"lots_of_pings_K{K}_step{L_byte_step}_th{max_threads}.txt"
perform_pings_and_save_into_file(K=K, L_byte_step=L_byte_step, output_file=output_file, target_name=target_name, function=win_psping)
results: List[Result] = parse_ping_result_data(output_file)


'''
x = [result.L_bytes for result in results]
y = [result.rtt_list for result in results]
plt.figure(1)
# Create the plot
for i in range(len(x)):
    plt.scatter([x[i]] * len(y[i]), y[i], s=20, alpha=0.6, edgecolors='w', linewidth=0.5, label=f'Group {x[i]}')

# Add titles and labels
plt.title(f'Results of {K} pings to {target_name} with L step of {L_byte_step} bytes')
plt.xlabel('L (pkt size) - bytes')
plt.ylabel('RTT - ms')
plt.savefig(f"lots_of_pings_K{K}_step{L_byte_step}_th{max_threads}_all.png")



plt.figure(2)
min_y = [min(result.rtt_list) for result in results]
# Create the plot
plt.scatter(x, min_y, s=20, alpha=0.6, edgecolors='w', linewidth=0.5, label=f'Group {x[i]}')

# Add titles and labels
plt.title(f'Min RTT value')
plt.xlabel('L (pkt size) - bytes')
plt.ylabel('RTT_min - ms')

plt.savefig(f"lots_of_pings_K{K}_step{L_byte_step}_th{max_threads}_min.png")
'''
