import asyncio
import time
import websockets
import tkinter as tk
import math
import random
import string
import ctypes as ct
import threading
import json
import socket

selectedport = "8765" #Must match client port, keep as is. this is fine

local_player_name = "replace_me" # Roblox username that you want to use on aka, the main account or whatever, ITS CAP SENSITIVE, example: local_player_name = "MyUsername" or local_player_name = "diddy" 
scale = .8  # Sensitivity. high number = less range but more detail, lower number = see more but less detail

players = [ # example of the table if u need
    {"name": "1", "pos": {"x": 0.715251, "y": 14.214783, "z": 27.765238}, "lookY": 0.039152},
    {"name": "2", "pos": {"x": -16.991959, "y": 14.500198, "z": 18.413366}, "lookY": -0.000000},
    {"name": "3", "pos": {"x": -22.925060, "y": 15.092392, "z": 9.573876}, "lookY": -0.024037},
    {"name": "4", "pos": {"x": 174.949448, "y": 34.713249, "z": -129.439438}, "lookY": -0.286728},
    {"name": "5", "pos": {"x": -15.380619, "y": 14.486805, "z": 21.755400}, "lookY": -0.004612},
    {"name": "6", "pos": {"x": -21.999247, "y": 14.388788, "z": -29.339712}, "lookY": 0.049785},
    {"name": "7", "pos": {"x": -32.115555, "y": 14.388966, "z": 8.045435}, "lookY": 0.049563},
    {"name": "8", "pos": {"x": -1.154718, "y": 14.403685, "z": -57.062904}, "lookY": 0.039968},
    {"name": "9", "pos": {"x": -13.745327, "y": 14.500198, "z": 27.113207}, "lookY": -0.000000},
    {"name": "10", "pos": {"x": 11.542368, "y": 14.464349, "z": -3.675619}, "lookY": -0.000438},
    {"name": "11", "pos": {"x": -20.061098, "y": 13.816854, "z": 17.180052}, "lookY": -0.054914},
    {"name": "12", "pos": {"x": -25.111540, "y": 15.096415, "z": 18.599770}, "lookY": 0.411733},
    {"name": "13", "pos": {"x": -11.896634, "y": 14.695921, "z": 14.885968}, "lookY": 0.000027},
    {"name": "14", "pos": {"x": 3.004156, "y": 14.399904, "z": 0.858800}, "lookY": 0.041320},
    {"name": "15", "pos": {"x": -16.180504, "y": 14.348451, "z": 16.641346}, "lookY": 0.083773},
    {"name": "16", "pos": {"x": -34.766155, "y": 14.489213, "z": -30.657543}, "lookY": 0.006161},
    {"name": "17", "pos": {"x": 1.089664, "y": 14.688935, "z": -29.612572}, "lookY": -0.164429},
    {"name": "18", "pos": {"x": 3.540582, "y": 14.466355, "z": -26.059437}, "lookY": 0.001059},
    {"name": "19", "pos": {"x": -14.411165, "y": 16.037186, "z": 3.373582}, "lookY": 0.077026},
    {"name": "20", "pos": {"x": -22.941170, "y": 15.430579, "z": 11.098089}, "lookY": 0.051587},
    {"name": "21", "pos": {"x": -15.238773, "y": 14.330139, "z": 16.671242}, "lookY": 0.002334}
]

#print("Local IP Address:", socket.gethostbyname(socket.gethostname())) doesnt work sometimes, idk why
local_ip = "0.0.0.0" # dont change, this is good enough

async def handle_client(websocket, path):
    print("Client connected")
    await websocket.send("Welcome to the WebSocket server!")
    try:
        async for message in websocket:
            global players
            players = json.loads(message)  
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    server = await websockets.serve(handle_client, local_ip, selectedport)
    print("Server running on ws://" + local_ip + ":" + selectedport)
    await server.wait_closed()

async def run_async():

    await main()


thread = threading.Thread(target=lambda: asyncio.run(run_async()))
thread.start()


def random_string(length=15): # naming the window will do probably nothing, but, whatever!
    letters = string.ascii_letters  
    return ''.join(random.choice(letters) for _ in range(length))


def dark_title_bar(window):
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))

# Tkinter GUI setup (chatgpt carry)
root = tk.Tk()
root.attributes("-topmost", True)
root.title(random_string())


root.resizable(False, False)  


canvas_size = 400
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg='black')
canvas.pack()

def draw_radar(players):
    global local_player

    if not hasattr(globals(), 'local_player'):
        local_player_candidates = [player for player in players if player['name'] == local_player_name]
        if local_player_candidates:
            local_player = local_player_candidates[0]
        else:
            print(f"Waiting for {local_player_name} to appear in players list...")
            return

    canvas.delete("all")
    local_x, local_y, local_z = local_player['pos']['x'], local_player['pos']['y'], local_player['pos']['z']

    for i in range(1, 5):
        radius = i * (canvas_size // 9)
        color = f'#{int(2 + i * 10):02x}{int(2 + i * 10):02x}{int(2 + i * 10):02x}'
        canvas.create_oval(
            (canvas_size // 2) - radius, (canvas_size // 2) - radius,
            (canvas_size // 2) + radius, (canvas_size // 2) + radius,
            outline=color, width=1
        )

    canvas.create_line(canvas_size // 2, canvas_size // 2, canvas_size // 2, 0 + 23, fill='#333333', width=1)

    for player in players:
        if player['name'] == local_player_name:
            continue

        x, y, z = player['pos']['x'], player['pos']['y'], player['pos']['z']
        distance = math.sqrt((x - local_x) ** 2 + (z - local_z) ** 2)

        if distance < 1000: 
            radar_x = ((x - local_x) * scale) + (canvas_size // 2)
            radar_y = ((z - local_z) * scale) + (canvas_size // 2)

            canvas.create_oval(radar_x - 3, radar_y - 3, radar_x + 3, radar_y + 3, fill='red')

    canvas.create_oval((canvas_size // 2) - 5, (canvas_size // 2) - 5, (canvas_size // 2) + 5, (canvas_size // 2) + 5, fill='blue')

dark_title_bar(root) # dark mode!!


def loop_render():
    global players
    draw_radar(players)
    root.after(10, loop_render)   # lower number = server checks for client data more often BUT CAN TAKE UP ALLOT OF BANDWIDTH


loop_render()

root.mainloop()
