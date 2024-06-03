import os

def ping(target_name: str, ttl: int=None, K: int=None, L: int=None, do_not_fragmentate:bool=True, result_file:str=None):
    """
    Creates the ping command with the given parameters and, if set, prints the output into result_file.
    
    Parameters:
    ttl (int):      time to live
    K (int):        number of packets sent to the target
    L (int):        number of bytes for each packet
    target_name:    target of the ping command
    result_file:    name of the txt file in which the result is stored
    
    """
    command  = f'ping {target_name} '
    command += f'-i {ttl} ' if ttl!=None else ""
    command += f'-n {K} ' if K!=None else ""
    command += f'-l {L} ' if L!=None else ""
    command += f'-f ' if do_not_fragmentate else ""
    command += f'> {result_file}' if result_file!=None else ""
    
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