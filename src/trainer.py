# trainer.py
import time
import random
from memory import Memory

class Trainer:
    def __init__(self, memory):
        self.mem = memory
        self.active = {f: False for f in ["farm", "sniper", "bounty", "safezone", "killaura", "raid"]}
    
    def toggle_farm(self):
        self.active["farm"] = not self.active["farm"]
        print(f"Auto-Farm: {'ON' if self.active['farm'] else 'OFF'}")
    
    def toggle_sniper(self):
        self.active["sniper"] = not self.active["sniper"]
        print(f"Fruit Sniper: {'ON' if self.active['sniper'] else 'OFF'}")
    
    def toggle_bounty(self):
        self.active["bounty"] = not self.active["bounty"]
        print(f"Auto-Bounty: {'ON' if self.active['bounty'] else 'OFF'}")
    
    def toggle_safezone(self):
        self.active["safezone"] = not self.active["safezone"]
        print(f"Safezone Teleport: {'ON' if self.active['safezone'] else 'OFF'}")
    
    def toggle_killaura(self):
        self.active["killaura"] = not self.active["killaura"]
        print(f"Kill Aura: {'ON' if self.active['killaura'] else 'OFF'}")
    
    def toggle_raid(self):
        self.active["raid"] = not self.active["raid"]
        print(f"Auto-Raid: {'ON' if self.active['raid'] else 'OFF'}")
    
    def run_farm(self):
        # Simulate auto-farm: read player, teleport to mobs, increase attack speed
        player = self.mem.get_localplayer()
        if not player:
            return
        # Increase attack speed
        speed_addr = player + self.mem.get_offset("attack_speed")
        self.mem.write_float(speed_addr, 999.0)
        # Increase damage
        dmg_addr = player + self.mem.get_offset("damage_multiplier")
        self.mem.write_float(dmg_addr, 9999.0)
        # Teleport to mobs (mock)
        # In real implementation, we would read mob list and teleport
        # Here we just set position to a nearby spot
        pos = self.mem.get_position(player)
        new_pos = (pos[0] + random.uniform(-10, 10), pos[1], pos[2] + random.uniform(-10, 10))
        # Write position (simplified)
        self.mem.write_float(player + self.mem.get_offset("position"), new_pos[0])
        self.mem.write_float(player + self.mem.get_offset("position") + 4, new_pos[1])
        self.mem.write_float(player + self.mem.get_offset("position") + 8, new_pos[2])
    
    def run_sniper(self):
        # Simulate fruit sniper: scan for fruit, teleport
        # Use ESP to find fruit (mock: random teleport)
        player = self.mem.get_localplayer()
        if not player:
            return
        # Teleport to random location (simulate fruit spawn)
        new_pos = (random.uniform(0, 1000), 100, random.uniform(0, 1000))
        self.mem.write_float(player + self.mem.get_offset("position"), new_pos[0])
        self.mem.write_float(player + self.mem.get_offset("position") + 4, new_pos[1])
        self.mem.write_float(player + self.mem.get_offset("position") + 8, new_pos[2])
        print("Teleported to fruit location.")
    
    def run_bounty(self):
        # Auto-combo and hitbox expansion
        player = self.mem.get_localplayer()
        if not player:
            return
        # Set hitbox expander (mock: increase localplayer scale)
        # We'll increase damage and speed
        self.mem.write_float(player + self.mem.get_offset("damage_multiplier"), 9999.0)
        # Execute combo by writing to combo function (mock)
        combo_addr = player + self.mem.get_offset("combo_function")
        self.mem.write_int(combo_addr, 0x01)  # activate combo
    
    def run_safezone(self):
        # If health low, teleport to safe coordinates
        player = self.mem.get_localplayer()
        if not player:
            return
        health = self.mem.get_health(player)
        if health < 50.0:
            # Teleport to safe zone (0,0,0)
            self.mem.write_float(player + self.mem.get_offset("position"), 0.0)
            self.mem.write_float(player + self.mem.get_offset("position") + 4, 0.0)
            self.mem.write_float(player + self.mem.get_offset("position") + 8, 0.0)
            print("Teleported to safezone.")
    
    def run_killaura(self):
        # Automatically attack NPCs in range
        # Mock: set attack speed high and damage high
        player = self.mem.get_localplayer()
        if not player:
            return
        self.mem.write_float(player + self.mem.get_offset("attack_speed"), 999.0)
        self.mem.write_float(player + self.mem.get_offset("damage_multiplier"), 9999.0)
    
    def run_raid(self):
        # Auto-complete raid
        player = self.mem.get_localplayer()
        if not player:
            return
        # Set raid status to complete
        raid_addr = player + self.mem.get_offset("raid_status")
        self.mem.write_int(raid_addr, 1)  # 1 = complete
        print("Raid completed.")
    
    def update(self):
        if self.active["farm"]:
            self.run_farm()
        if self.active["sniper"]:
            self.run_sniper()
        if self.active["bounty"]:
            self.run_bounty()
        if self.active["safezone"]:
            self.run_safezone()
        if self.active["killaura"]:
            self.run_killaura()
        if self.active["raid"]:
            self.run_raid()
