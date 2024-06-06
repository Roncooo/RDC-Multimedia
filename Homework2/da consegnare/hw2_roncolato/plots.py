
from statistics import mean
import statistics
from typing import List
import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
from utilities import *

def plot_save_multiple_results(
    x: List[int], 
    all_y: List[List[float]], 
    filename: str, 
    K: int,
    target_name: int,
    L_byte_step: int,
    p=None, 
    ymin: int=None, 
    ymax: int=None,
    
):
    plt.figure(filename)
    # Create the plot
    for i in range(len(x)):
        plt.scatter([x[i]] * len(all_y[i]), all_y[i], s=20, alpha=0.6, edgecolors='w', linewidth=0.5, label=f'Group {x[i]}')
        
    plt.title(f'Results of {K} pings to {target_name} with L step of {L_byte_step} bytes')
    
    if(p!=None):
        y_fit = p(np.array(x))
        plt.plot(x, y_fit, color='blue', label='Fitted Polynomial')
    if(ymin!=None and ymax!=None):
        plt.ylim(ymin, ymax)
        plt.title(f'zoom with y between {ymin} and {ymax} ms')
        
    # Add titles and labels
    plt.xlabel('L (pkt size) - bytes')
    plt.ylabel('RTT - ms')
    plt.savefig(filename)


def plot_save_single_results(x: List[int], min_y: List[float], filename: str, title: str, p=None):
    plt.figure(filename)
    # Create the plot
    plt.scatter(x, min_y, s=20, alpha=0.6, edgecolors='w', linewidth=0.5)
    
    p_string = ""
    if(p!=None):
        y_fit = p(np.array(x))
        plt.plot(x, y_fit, color='blue', label='Fitted Polynomial')
        p_string = f"  -   r={p}"
    
    # Add titles and labels
    plt.title(f'{title} {p_string}')
    plt.xlabel('L (pkt size) - bytes')
    plt.ylabel(f'{title} - ms')
    plt.savefig(filename)


def plot_all_and_save(
    results: List[Result], 
    K: int,
    L_byte_step: int,
    source_name: str,
    target_name: str,
    max_threads: int
) -> None:
    
    execution_name = f"{source_name}_{target_name}_K{K}_step{L_byte_step}_th{max_threads}"

    x = [result.L_bytes for result in results]
    all_y = [result.rtt_list for result in results]
    all_results_plot_filename = f"{execution_name}_all.png"
    plot_save_multiple_results(
        x=x, 
        all_y=all_y, 
        filename=all_results_plot_filename,
        K=K,
        target_name=target_name,
        L_byte_step=L_byte_step
    )

    min_results_plot_filename = f"{execution_name}_min.png"
    min_y = [min(result.rtt_list) for result in results]
    p = Polynomial.fit(x, min_y, 1)
    plot_save_single_results(x, min_y, min_results_plot_filename, "Min RTT value", p)

    min_err_results_plot_filename = f"{execution_name}_min_err.png"
    min_y_err = [abs(p(result.L_bytes) - min(result.rtt_list)) for result in results]
    plot_save_single_results(x, min_y_err, min_err_results_plot_filename, "Absolute error")

    ymin = 25
    ymax = 40
    all_results_ylim_plot_filename = f"{execution_name}_all_ylim_{ymin}_{ymax}.png"
    plot_save_multiple_results(
        x=x, 
        p=p, 
        ymin=ymin, 
        ymax=ymax,
        all_y=all_y, 
        filename=all_results_ylim_plot_filename,
        K=K,
        target_name=target_name,
        L_byte_step=L_byte_step
    )

    avg_y = [mean(result.rtt_list) for result in results]
    avg_results_plot_filename = f"{execution_name}_avg.png"
    plot_save_single_results(x, avg_y, avg_results_plot_filename, "Avg RTT value")

    max_y = [max(result.rtt_list) for result in results]
    max_results_plot_filename = f"{execution_name}_max.png"
    plot_save_single_results(x, max_y, max_results_plot_filename, "Max RTT value")

    stdev_y = [statistics.stdev(result.rtt_list) for result in results]
    stdev_results_plot_filename = f"{execution_name}_stdev.png"
    plot_save_single_results(x, stdev_y, stdev_results_plot_filename, "stdev")
