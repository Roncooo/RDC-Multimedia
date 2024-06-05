import os
import ast
from concurrent.futures import Future, ThreadPoolExecutor
from concurrent.futures._base import Future
from statistics import mean
import statistics
from typing import List
from utilities import Result, parse_ping_result
from commands import *
import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt


min_L_byte = 10
max_L_byte = 1472

def callback(future: Future) -> None:
    temp_file_name, L_byte, function = future.args
    f = open(temp_file_name)
    result_string = f.read()
    f.close()
    os.remove(temp_file_name)
    list = parse_ping_result(result_string, function)
    future.result = Result(L_byte, list)

def perform_pings_and_save_into_file(K: int, L_byte_step: int, output_file: str, target_name: str, function=win_psping, max_threads: int=10, min_L_byte: int=10, max_L_byte: int=1472):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        # Submit tasks to the executor
        for L_byte in range(min_L_byte,max_L_byte+1,L_byte_step):
            temp_file_name = f"temp_ping_result_L_{L_byte}.txt"
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


def plot_save_multiple_results(x: List[int], all_y: List[List[float]], filename: str, p=None):
    plt.figure(filename)
    # Create the plot
    for i in range(len(x)):
        plt.scatter([x[i]] * len(all_y[i]), all_y[i], s=20, alpha=0.6, edgecolors='w', linewidth=0.5, label=f'Group {x[i]}')
        
    if(p!=None):
        y_fit = p(np.array(x))
        plt.plot(x, y_fit, color='blue', label='Fitted Polynomial')
    # Add titles and labels
    plt.title(f'Results of {K} pings to {target_name} with L step of {L_byte_step} bytes')
    plt.xlabel('L (pkt size) - bytes')
    plt.ylabel('RTT - ms')
    plt.savefig(filename)

def plot_save_single_results(x: List[int], min_y: List[float], filename: str, type: str, p=None):
    plt.figure(filename)
    # Create the plot
    plt.scatter(x, min_y, s=20, alpha=0.6, edgecolors='w', linewidth=0.5)
    
    p_string = ""
    if(p!=None):
        y_fit = p(np.array(x))
        plt.plot(x, y_fit, color='blue', label='Fitted Polynomial')
        p_string = f"  -   r={p}"
    
    # Add titles and labels
    plt.title(f'{type} RTT value {p_string}')
    plt.xlabel('L (pkt size) - bytes')
    plt.ylabel(f'RTT_{type} - ms')
    plt.savefig(filename)


K = 200 # number of packets sent for each L_byte value
target_name = "lyon.testdebit.info"
L_byte_step=20
max_threads=10
execution_name = f"pings_{target_name}_K{K}_step{L_byte_step}_th{max_threads}"
# execution_name = "pings_lyon.testdebit.info_K100_step20_th10"
output_file = f"{execution_name}.txt"
perform_pings_and_save_into_file(K=K, L_byte_step=L_byte_step, output_file=output_file, target_name=target_name, function=win_psping, max_threads=max_threads)
results: List[Result] = parse_ping_result_data(output_file)

x = [result.L_bytes for result in results]
all_y = [result.rtt_list for result in results]
all_results_plot_filename = f"{execution_name}_all.png"
plot_save_multiple_results(x, all_y, all_results_plot_filename)

min_results_plot_filename = f"{execution_name}_min.png"
min_y = [min(result.rtt_list) for result in results]
p = Polynomial.fit(x, min_y, 1)
print(p)
plot_save_single_results(x, min_y, min_results_plot_filename, "Min", p)

avg_y = [mean(result.rtt_list) for result in results]
avg_results_plot_filename = f"{execution_name}_avg.png"
plot_save_single_results(x, avg_y, avg_results_plot_filename, "Avg")

max_y = [max(result.rtt_list) for result in results]
max_results_plot_filename = f"{execution_name}_max.png"
plot_save_single_results(x, max_y, max_results_plot_filename, "Max")

stdev_y = [statistics.stdev(result.rtt_list) for result in results]
stdev_results_plot_filename = f"{execution_name}_stdev.png"
plot_save_single_results(x, stdev_y, stdev_results_plot_filename, "stdev")

