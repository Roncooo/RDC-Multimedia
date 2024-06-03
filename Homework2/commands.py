import os

def ping(ttl: int, K: int, L: int, target_name: str, result_file:str=None, do_not_fragmentate:bool=True):
    """
    Creates the ping command with the given parameters and, if set, prints the output into result_file.
    
    Parameters:
    ttl (int):      time to live
    K (int):        number of packets sent to the target
    L (int):        number of bytes for each packet
    target_name:    target of the ping command
    result_file:    name of the txt file in which the result is stored
    
    """
    command = 'ping {target_name} -i {ttl} -n {K} -l {L} '.format(target_name=target_name, ttl=ttl, K=K, L=L)
    if(do_not_fragmentate == True):
        command = command + '-f '
    if(result_file != None):
        command = command + '> {result_file}'.format(result_file=result_file)
    
    os.system(command)


def traceroute(target_name: str, result_file:str=None):
    """
    Creates and executes the traceroute command with the given parameters and, if set, prints the output into result_file.
    
    Parameters:
    target_name:    target of the traceroute command
    result_file:    name of the txt file in which the result is stored
    
    """
    
    command = 'tracert {}'.format(target_name)
    if(result_file != None):
        command = command + '> {result_file}'.format(result_file=result_file)
    
    os.system(command)