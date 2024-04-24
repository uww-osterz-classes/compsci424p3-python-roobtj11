"""
COMPSCI 424 Program 3
Name: 
"""

import os
import sys
import threading
from turtle import setup  # standard Python threading library

# (Comments are just suggestions. Feel free to modify or delete them.)

# When you start a thread with a call to "threading.Thread", you will
# need to pass in the name of the function whose code should run in
# that thread.

# If you want your variables and data structures for the banker's
# algorithm to have global scope, declare them here. This may make
# the rest of your program easier to write. 
#  
# Most software engineers say global variables are a Bad Idea (and 
# they're usually correct!), but systems programmers do it all the
# time, so I'm allowing it here.


#R = Avalible   #Allocation = Current   #Request = Current Requests #P = Max Claims #[n] = process [M] = Resource
g_Available,g_Current,g_Requests,g_Max,g_Total=0,0,0,0,0
g_num_resources = 0
g_num_processes = 0

# Let's write a main method at the top
def main():
    # Code to test command-line argument processing.
    # You can keep, modify, or remove this. It's not required.
    if len(sys.argv) < 3:
        sys.stderr.write("Not enough command-line arguments provided, exiting.")
        sys.exit(1)

    print("Selected mode:", sys.argv[1])
    print("Setup file location:", sys.argv[2])

    # 1. Open the setup file using the path in argv[2]
    with open(sys.argv[2], 'r') as setup_file:
        # 2. Get the number of resources and processes from the setup
        # file, and use this info to create the Banker's Algorithm
        # data structures
        g_num_resources = int(setup_file.readline().split()[0])
        print(g_num_resources, "resources")
        g_Available = [0]*g_num_resources
        g_num_processes = int(setup_file.readline().split()[0])
        print(g_num_processes, "processes")
        g_Current=[[0]*g_num_resources]*g_num_processes
        g_Max=[[0]*g_num_resources]*g_num_processes
        #possibly requests here too
        setup_file.readline() #skip line with AVAILABLE
        tmp = setup_file.readline().split() #get line and split on white space
        for i in range(g_num_resources): # get available resoruces
            g_Available[i] = int(tmp[i])

        # 3. Use the rest of the setup file to initialize the data structures
        # (you fill in this part)
        setup_file.readline() #skip Max
        
        for p in range(g_num_processes):
            tmp = setup_file.readline().split() #get line and split on white space
            for i in range(g_num_resources): # get max resoruces
                g_Max[p][i] = int(tmp[i])  
        setup_file.readline() #skip current
        for p in range(g_num_processes):
            tmp = setup_file.readline().split() #get line and split on white space
            for i in range(g_num_resources): # get current resoruces
                g_Current[p][i] = int(tmp[i])
    
    # 4. Check initial conditions to ensure that the system is
    # beginning in a safe state: see "Check initial conditions"
    # in the Program 3 instructions
        #4.1
        #4.2
        #4.3           

    # 5. Go into either manual or automatic mode, depending on
    # the value of args[0]; you could implement these two modes
    # as separate methods within this class, as separate classes
    # with their own main methods, or as additional code within
    # this main method.
    if sys.argv[1] == "manual": manual()
    elif sys.argv[1] == "auto": auto()
    

def manual():
     return
def auto():
     return
# fill in other methods here as desired

main() # call the main function