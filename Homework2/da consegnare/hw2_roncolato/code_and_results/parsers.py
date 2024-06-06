
from typing import List
from commands import *

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


def parse_win_ping_ita(result_string: str) -> List[float]:
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


def parse_ping_result(result_string: str, function) -> List[float]:
    """
    Returns:
    np.array with the RTTs of the K packages 
    """
    if function==win_psping:
        return parse_win_psping(result_string)
    if function==win_ping:
        return parse_win_ping_ita(result_string)


def win_ping_reached_ita(result_string) -> bool:
    ttl_expired: bool = result_string.find("TTL scaduto durante il passaggio")!=-1
    request_expired: bool = result_string.find("Richiesta scaduta")!=-1
    reached_destination: bool = (not ttl_expired) and (not request_expired)
    return reached_destination
