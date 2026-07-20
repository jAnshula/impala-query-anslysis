from dataclasses import dataclass


@dataclass
class FragmentExecution:


    query_id:str=""

    fragment:str=""

    operator:str=""


    host:str=""

    instance:str=""


    runtime_ms:int=0


    read_bytes:int=0

    write_bytes:int=0


    rows:int=0


    peak_memory:int=0


    cpu_time_ms:int=0


    io_wait_ms:int=0


    network_time_ms:int=0

