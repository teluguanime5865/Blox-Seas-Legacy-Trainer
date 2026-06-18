# memory.py
import ctypes
from ctypes import wintypes
import json
import os
from utils import get_process_id_by_name, read_memory, write_memory, get_module_base, pattern_scan

class Memory:
    def __init__(self, process_name, offsets_file):
        self.process_name = process_name
        self.offsets_file = offsets_file
        self.pid = None
        self.handle = None
        self.module_base = None
        self.offsets = self.load_offsets()
    
    def load_offsets(self):
        with open(self.offsets_file, 'r') as f:
            return json.load(f)
    
    def attach(self):
        self.pid = get_process_id_by_name(self.process_name)
        if not self.pid:
            raise RuntimeError(f"Process '{self.process_name}' not found.")
        self.handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, self.pid)
        if not self.handle:
            raise RuntimeError("Failed to open process.")
        self.module_base = get_module_base(self.pid, self.process_name)
        return True
    
    def detach(self):
        if self.handle:
            ctypes.windll.kernel32.CloseHandle(self.handle)
            self.handle = None
    
    def read_int(self, address):
        data = read_memory(self.handle, address, 4)
        if data:
            return int.from_bytes(data, 'little')
        return 0
    
    def read_float(self, address):
        data = read_memory(self.handle, address, 4)
        if data:
            return struct.unpack('f', data)[0]
        return 0.0
    
    def read_vec3(self, address):
        x = self.read_float(address)
        y = self.read_float(address + 4)
        z = self.read_float(address + 8)
        return (x, y, z)
    
    def write_int(self, address, value):
        data = value.to_bytes(4, 'little')
        return write_memory(self.handle, address, data)
    
    def write_float(self, address, value):
        data = struct.pack('f', value)
        return write_memory(self.handle, address, data)
    
    def get_offset(self, name):
        return self.offsets.get(name, 0)
    
    def get_localplayer(self):
        return self.read_int(self.module_base + self.get_offset("localplayer"))
    
    def get_health(self, player_addr):
        return self.read_float(player_addr + self.get_offset("health"))
    
    def set_health(self, player_addr, value):
        self.write_float(player_addr + self.get_offset("health"), value)
    
    def get_position(self, player_addr):
        return self.read_vec3(player_addr + self.get_offset("position"))
