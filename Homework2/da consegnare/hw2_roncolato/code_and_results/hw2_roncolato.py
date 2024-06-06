from utilities import number_of_nodes_with_ping_and_traceroute, perform_pings_and_save_into_file, parse_ping_result_data, Result
from typing import List
from commands import win_psping
from plots import plot_all_and_save
from numpy.polynomial import Polynomial


target_name = "lyon.testdebit.info"
source_name = "home"

n_nodes = number_of_nodes_with_ping_and_traceroute(
    min_ttl=1,
    max_ttl=40,
    max_threads=40,
    target_name=target_name, 
    source_name=source_name
) 

K = 200
min_L_byte = 10
max_L_byte = 1472
L_byte_step=20
max_threads=10

execution_name = f"{source_name}_{target_name}_K{K}_step{L_byte_step}_th{max_threads}"
output_file = f"{execution_name}.txt"

# if you already have a result file you can skip the execution of the following function 
# (that takes around half an hour) by commenting it and choosing the correct output_file
perform_pings_and_save_into_file(
    K=K, 
    min_L_byte=min_L_byte,
    max_L_byte=max_L_byte,
    L_byte_step=L_byte_step,
    max_threads=max_threads,
    target_name=target_name,
    output_file=output_file,
    function=win_psping
) 

# reads the results of the previous function and retreives an object that's easier to analize
results: List[Result] = parse_ping_result_data(output_file)

# calculates the linear regression of the minimum values
x = [result.L_bytes for result in results]
min_y = [min(result.rtt_list) for result in results]
p = Polynomial.fit(x, min_y, 1)
print()
print(f'Regression line: y = {p}')
a = p.coef[1]

# calculates the throughputs
R = 1000*2*n_nodes/a
R_bottleneck = 1000*2/a
print(f'Mean throughput: R = {R} byte/s = {R*8/1e6} Mbps')
print(f'Bottleneck throughput: R = {R_bottleneck} byte/s = {R_bottleneck*8/1e6} Mbps')

plot_all_and_save(
    results=results, 
    K=K,
    L_byte_step=L_byte_step,
    source_name=source_name,
    target_name=target_name,
    max_threads=max_threads,
)
