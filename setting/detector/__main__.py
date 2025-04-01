import os
import subprocess
import sys

device = sys.argv[1]
command = os.getenv("RASER_SETTING_PATH")+"/detector/"+device+".py"
subprocess.run(["python3"+' '+command], shell=True, executable='/bin/bash')