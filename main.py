from pymem import Pymem
from pymem.process import module_from_name
import keyboard
import time
import math

process_name = 'atg-steam-engine-demo.exe'
base_address_offset = 0x00097A90
ptr_player_struct = [0x48, 0x1A8, 0x430, 0x40, 0x280, 0x320, 0x578, 0x118]
ptr_water_ctrl = ptr_player_struct + [0xC38]
ptr_heat_ctrl = ptr_player_struct + [0xC18]
ptr_brake_ctrl = ptr_player_struct + [0xC08]
ptr_water_qty = ptr_player_struct + [0x918]

pm = Pymem(process_name)
module = module_from_name(pm.process_handle, process_name)
base_address = module.lpBaseOfDll

def calculate_pointer(offsets):
    pointer_address = base_address + base_address_offset
    for offset in offsets:
        pointer_address = pm.read_ulonglong(pointer_address) + offset
    return pointer_address

def read_memory(offsets):
    pointer_address = calculate_pointer(offsets)
    value = pm.read_double(pointer_address)
    return value

def write_memory(offsets, value):
    pointer_address = calculate_pointer(offsets)
    pm.write_double(pointer_address, value)

class PlayerStruct:
    def __init__(self):
        self.water_ctrl = read_memory(ptr_water_ctrl)
        self.heat_ctrl = read_memory(ptr_heat_ctrl)
        self.brake_ctrl = read_memory(ptr_brake_ctrl)
        self.water_qty = read_memory(ptr_water_qty)

    def update(self):
        w = keyboard.is_pressed('w')
        s = keyboard.is_pressed('s')
        g = keyboard.is_pressed('g')
        shift = keyboard.is_pressed('shift')
        alt = keyboard.is_pressed('ctrl')

        if w:
            self.heat_ctrl = max(min((0.003 - 0.002 * int(alt)) * self.heat_ctrl * self.heat_ctrl + (2.887 - 1.8 * int(alt)) * self.heat_ctrl - 0.344, 1e5 + 4e6 * int(shift) - 9e4 * int(alt)), 1.0)
            self.brake_ctrl = 0.0
            self.water_qty = float(g)
        elif s:
            self.brake_ctrl = 20.0 + 50.0 * shift - 15.0 * int(alt) 
            self.heat_ctrl = 0.0
            self.water_ctrl = 0.0
        else:
            if not alt:
                # Decrease only if not holding ALT
                if self.heat_ctrl > 1:
                    self.heat_ctrl /= 2
                else:
                    self.heat_ctrl = 0.0
                self.brake_ctrl = 0.0
        self.water_ctrl = min(pow(self.heat_ctrl, 0.08), 10.0) # Water control, up to 10x normal, based on current heat ctrl


        write_memory(ptr_water_ctrl, self.water_ctrl)
        write_memory(ptr_heat_ctrl, self.heat_ctrl)
        write_memory(ptr_brake_ctrl, self.brake_ctrl)
        write_memory(ptr_water_qty, self.water_qty)

def main():
    player = PlayerStruct()
    while True:
        player.update()
        time.sleep(0.1)


if __name__ == "__main__":
    main()
