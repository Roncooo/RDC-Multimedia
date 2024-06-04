import os

def win_ping(target_name: str, ttl: int=None, K: int=None, L: int=None, do_not_fragmentate:bool=True, result_file:str=None):
    """
    Creates the ping command with the given parameters and, if set, prints the output into result_file.
    
    Parameters:
    target_name:        target of the ping command
    ttl (int):          time to live
    K (int):            number of packets sent to the target
    L (int):            number of bytes for each packet
    do_not_fragmentate: if true, avoids fragmentation of IP package
    result_file:        name of the txt file in which the result is stored
    
    """
    command  = f'ping {target_name} '
    command += f'-i {ttl} ' if ttl!=None else ""
    command += f'-n {K} ' if K!=None else ""
    command += f'-l {L} ' if L!=None else ""
    command += f'-f ' if do_not_fragmentate else ""
    command += f'> {result_file}' if result_file!=None else ""
    
    os.system(command)


def linux_ping(target_name: str, ttl: int=None, K: int=None, L: int=None, result_file:str=None):
    """
    Creates the ping command with the given parameters and, if set, prints the output into result_file.
    
    Parameters:
    target_name:        target of the ping command
    ttl (int):          time to live
    K (int):            number of packets sent to the target
    L (int):            number of bytes for each packet
    result_file:        name of the txt file in which the result is stored
    
    """
    command  = f'ping '
    command += f'-i {ttl} ' if ttl!=None else ""
    command += f'-c {K} ' if K!=None else ""
    command += f'-s {L} ' if L!=None else ""
    command += target_name
    command += f'> {result_file}' if result_file!=None else ""
    
    os.system(command)
    

def win_psping(target_name: str, ttl: int=None, K: int=None, L: int=None, do_not_fragmentate:bool=True, result_file:str=None):
    """
    Creates the psping command with the given parameters and, if set, prints the output into result_file.
    
    Parameters:
    target_name:    target of the ping command
    K (int):        number of packets sent to the target
    L (int):        number of bytes for each packet
    result_file:    name of the txt file in which the result is stored
    
    """
    command  = f'psping '
    command += f'-n {K} ' if K!=None else ""
    command += f'-l {L} ' if L!=None else ""
    command += '-nobanner '
    command += f'{target_name} '
    command += f'> {result_file}' if result_file!=None else ""
    os.system(command)


def traceroute(target_name: str, result_file:str=None):
    """
    Creates and executes the traceroute command with the given parameters and, if set, prints the output into result_file.
    
    Parameters:
    target_name:    target of the traceroute command
    result_file:    name of the txt file in which the result is stored
    
    """
    
    command = f'tracert {target_name} '
    command += f'> {result_file}' if(result_file != None) else ""
    
    os.system(command)