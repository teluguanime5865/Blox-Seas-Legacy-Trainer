# utils.py
import ctypes
from ctypes import wintypes
import struct

# Windows API constants
PROCESS_ALL_ACCESS = 0x1F0FFF
TH32CS_SNAPPROCESS = 0x00000002
INVALID_HANDLE_VALUE = -1

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
user32 = ctypes.WinDLL("user32", use_last_error=True)

# Structures
class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", ctypes.c_char * 260)
    ]

def get_process_id_by_name(name):
    """Return PID of first process matching the executable name."""
    snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snapshot == INVALID_HANDLE_VALUE:
        return None
    entry = PROCESSENTRY32()
    entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
    if kernel32.Process32First(snapshot, ctypes.byref(entry)):
        while True:
            if entry.szExeFile.decode().lower() == name.lower():
                kernel32.CloseHandle(snapshot)
                return entry.th32ProcessID
            if not kernel32.Process32Next(snapshot, ctypes.byref(entry)):
                break
    kernel32.CloseHandle(snapshot)
    return None

def read_memory(handle, address, size):
    """Read bytes from process memory."""
    buffer = ctypes.create_string_buffer(size)
    bytes_read = ctypes.c_size_t()
    if kernel32.ReadProcessMemory(handle, address, buffer, size, ctypes.byref(bytes_read)):
        return buffer.raw
    return None

def write_memory(handle, address, data):
    """Write bytes to process memory."""
    bytes_written = ctypes.c_size_t()
    return kernel32.WriteProcessMemory(handle, address, data, len(data), ctypes.byref(bytes_written)) != 0

def get_module_base(pid, module_name):
    """Get base address of a module in the target process."""
    # Simplified: we assume the main module is at the base address returned by GetModuleHandleEx?
    # For a real implementation, use EnumProcessModules.
    # Here we return a placeholder (will be scanned dynamically).
    return 0x400000  # placeholder

def pattern_scan(handle, module_base, pattern, mask):
    """Scan memory for a byte pattern (simple implementation)."""
    # For demonstration, we just return a dummy address.
    # In practice, you would scan the module's memory region.
    return module_base + 0x1000
