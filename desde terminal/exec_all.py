import os
direccion_ejecutables="/home/rodrigo/codigo/"

cmd1="python " + direccion_ejecutables +  "malla_gen.py"

cmd2="python " + direccion_ejecutables + "call_pygbe.py"

cmd3="python " + direccion_ejecutables + "results_gen.py"

os.system(cmd1)
os.system(cmd2)
os.system(cmd3)
