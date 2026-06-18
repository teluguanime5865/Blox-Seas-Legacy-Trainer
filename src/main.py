# main.py
import ctypes
from ctypes import wintypes
import time
import sys
import signal
from memory import Memory
from trainer import Trainer
from config import PROCESS_NAME, OFFSETS_FILE

# Windows API for hotkeys
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Hotkey IDs
HK_F1 = 1
HK_F2 = 2
HK_F3 = 3
HK_F4 = 4
HK_F5 = 5
HK_F6 = 6
# HK_F7, HK_F8 reserved

def register_hotkeys():
    """Register F1-F6 as global hotkeys."""
    # F1 = 0x70, F2=0x71, ... F6=0x75
    mod = 0  # no modifier
    for i, key in enumerate([0x70, 0x71, 0x72, 0x73, 0x74, 0x75], start=1):
        if not user32.RegisterHotKey(None, i, mod, key):
            print(f"Failed to register hotkey F{i}")
            return False
    return True

def unregister_hotkeys():
    for i in range(1, 7):
        user32.UnregisterHotKey(None, i)

def main():
    print("Initializing Blox Seas: Legacy Trainer...")
    mem = Memory(PROCESS_NAME, OFFSETS_FILE)
    try:
        mem.attach()
    except Exception as e:
        print(f"Error attaching to process: {e}")
        print("Make sure the game is running and you have Administrator privileges.")
        input("Press Enter to exit...")
        return
    
    trainer = Trainer(mem)
    
    if not register_hotkeys():
        print("Failed to register hotkeys. Run as Administrator.")
        mem.detach()
        return
    
    print("Trainer ready. Hotkeys: F1-F6 to toggle features.")
    print("Press Ctrl+C to exit.")
    
    # Message loop
    msg = wintypes.MSG()
    running = True
    try:
        while running:
            # PeekMessage/GetMessage
            ret = user32.GetMessageA(ctypes.byref(msg), None, 0, 0)
            if ret == -1:
                break
            elif ret == 0:
                # WM_QUIT
                break
            else:
                if msg.message == 0x0312:  # WM_HOTKEY
                    hk_id = msg.wParam
                    if hk_id == HK_F1:
                        trainer.toggle_farm()
                    elif hk_id == HK_F2:
                        trainer.toggle_sniper()
                    elif hk_id == HK_F3:
                        trainer.toggle_bounty()
                    elif hk_id == HK_F4:
                        trainer.toggle_safezone()
                    elif hk_id == HK_F5:
                        trainer.toggle_killaura()
                    elif hk_id == HK_F6:
                        trainer.toggle_raid()
                # Update trainer logic periodically (every 100ms)
                # We can't block the message loop, so we use a timer or a separate thread.
                # For simplicity, we'll update in the loop with a counter.
                # Actually, we can use SetTimer or just check time.
                # Here we'll call trainer.update() inside the message loop with a non-blocking approach.
                # We'll use a simple counter.
                # Better: use a separate thread for updates, but we keep it simple.
                # We'll just call update on each message, but that may be too often.
                # We'll use a time check.
                if hasattr(main, "_last_update"):
                    if time.time() - main._last_update > 0.1:
                        trainer.update()
                        main._last_update = time.time()
                else:
                    trainer.update()
                    main._last_update = time.time()
    except KeyboardInterrupt:
        pass
    finally:
        unregister_hotkeys()
        mem.detach()
        print("Trainer stopped.")

if __name__ == "__main__":
    main()
