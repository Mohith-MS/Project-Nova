import subprocess
import time
t1 = time.time()
subprocess.check_call("g++ -o Resources/temp/test.out slicer.cpp", shell=True)
subprocess.call("Resources/temp/test.out")
print()
print(time.time() - t1)
