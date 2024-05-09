"""
COMPSCI 424 Program 3
Name: Tyler Roob
"""

from math import e
import os
from platform import release
from random import randint
import sys
from threading import Thread, Lock
import threading
from token import LESSEQUAL
from turtle import setup  # standard Python threading library

# When you start a thread with a call to "threading.Thread", you will
# need to pass in the name of the function whose code should run in
# that thread.
class my_thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = None

    def run(self):
        self.value = self._target(*self._args, **self._kwargs)
    
    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.value
# If you want your variables and data structures for the banker's
# algorithm to have global scope, declare them here. This may make
# the rest of your program easier to write. 
#  
# Most software engineers say global variables are a Bad Idea (and 
# they're usually correct!), but systems programmers do it all the
# time, so I'm allowing it here.


#R = Avalible   #Allocation = Current   #Request = Current Requests #P = Max Claims #[n] = process [M] = Resource
g_Available,g_Current,g_Requests,g_Max,g_Total,g_potential=0,0,0,0,0,0
g_num_resources = 0
g_num_processes = 0
mutex = Lock()
print_lock = Lock()
# Let's write a main method at the top
def main():
    global g_Available,g_Current,g_Requests,g_Max,g_Total, g_num_resources, g_num_processes,g_potential
    # Code to test command-line argument processing.
    # You can keep, modify, or remove this. It's not required.
    if len(sys.argv) < 3:
        sys.stderr.write("Not enough command-line arguments provided, exiting.")
        sys.exit(1)

    print("Selected mode:", sys.argv[1])
    print("Setup file location:", sys.argv[2])

    # 1. Open the setup file using the path in argv[2]
    #READ input into program
    with open(sys.argv[2], 'r') as setup_file:
        # 2. Get the number of resources and processes from the setup
        # file, and use this info to create the Banker's Algorithm
        # data structures
        g_num_resources = int(setup_file.readline().split()[0])
        print(f"{g_num_resources}, resources")
        g_Available = [0]*g_num_resources
        g_Total= [0]*g_num_resources
        g_num_processes = int(setup_file.readline().split()[0])
        print(f"{g_num_processes}, processes")
        g_Current=[[0 for x in range(g_num_resources)] for y in range(g_num_processes)]
        g_Max=[[0 for x in range(g_num_resources)] for y in range(g_num_processes)]
        g_Requests=[[0 for x in range(g_num_resources)] for y in range(g_num_processes)]
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
        print("Available")
        print(g_Available)
        print("MAX")
        for m in g_Max:
            print(m)
        #print(g_Max)
        print("Current")
        for c in g_Current:
            print(c)
        
        #print(g_Current)

    
    # 4. Check initial conditions to ensure that the system is
    # beginning in a safe state: see "Check initial conditions"
    # in the Program 3 instructions
        #4.1
        for i in range(g_num_processes):
            for j in range (g_num_resources):
                if g_Current[i][j] <= g_Max[i][j]:
                    continue
                else:
                    print("Check 1 Failed")
                    sys.exit(2)
        print("Check 1 passed")
        #4.2     
        #calc g_total
        current_transposed = [[g_Current[j][i] for j in range(len(g_Current))] for i in range(len(g_Current[0]))]
        print("Total:")
        for index, t in enumerate(current_transposed):
            g_Total[index] =sum(t)+g_Available[index]
        print(g_Total)
        #4.3 Safe State
        #true Claim graph is fully reducible
        if not request(0,0,0):
            sys.stderr.write("This test is not started in a safe state.  Do better.")
            sys.exit(4)

    # 5. Go into either manual or automatic mode, depending on
    # the value of args[0]; you could implement these two modes
    # as separate methods within this class, as separate classes
    # with their own main methods, or as additional code within
    # this main method.
    if sys.argv[1] == "manual": manual()
    elif sys.argv[1] == "auto": auto()
   
def bankers(t_available,t_current):
    global g_Available,g_Current,g_Requests,g_Max,g_Total, g_num_resources, g_num_processes,g_potential
    

    ########################
    # print("Potential Requests:")
    # g_potential = [[0 for x in range(g_num_resources)] for y in range(g_num_processes)]
    # g_potential = [[g_Max[p][r] - t_current[p][r] for r in range(g_num_resources)] for p in range(g_num_processes)]
    # for p in range(g_num_processes):
    #     print(g_potential[p])
    ########################
    
    

    safe=[]
    while len(safe) != g_num_processes:
        bad_block=True
        for p in range(g_num_processes):
            if p in safe:
                continue
            blocked=False
            for r in range(g_num_resources):
                if g_Max[p][r] - t_current[p][r] > t_available[r]:
                    blocked=True
                    break
            if not blocked:
                for r in range(g_num_resources):
                    t_available[r] += t_current[p][r]
                #print(f"Available p{p}: {t_available}")
                safe.append(p)
                bad_block=False
        if bad_block:
            return False
            
    return True

def manual():
    global g_Available,g_Current,g_Requests,g_Max,g_Total, g_num_resources, g_num_processes,g_potential
    while ...:
        print("Enter a command that follows one of the following formats:\n\trequest I of J for K\n\trelease I of J for K\n\tend")#I=num resources of Resource J for process K
        command = input().lower()
        c_parts=command.split();
        c_parts;
        match c_parts[0]:
            case "end":
                exit(69)
            case "request":
                #I = num Resources
                #J = Resource
                #K = process
            
                I = int(c_parts[1])
                J = int(c_parts[3])
                K = int(c_parts[5])
                if I not in range(0,g_Max[K][J]+1):
                    print("Invalid Request") 
                elif J not in range(0,g_num_resources):
                    print("Invalid Request") 
                elif K not in range(0,g_num_processes):
                    print("Invalid Request") 
                else:
                    if request(I,J,K):
                        print(f"Process {K} requests {I} units of resource {J}: Granted")
                    else:
                        print(f"Process {K} requests {I} units of resource {J}: Denied")
                    print("Available")
                    print(g_Available)
                    print("MAX")
                    for m in g_Max:
                        print(m)
                    #print(g_Max)
                    print("Current")
                    for c in g_Current:
                        print(c)
            case "release":
                I = int(c_parts[1])
                J = int(c_parts[3])
                K = int(c_parts[5])
                if I not in range(0,g_Current[K][J]+1) or J not in range(0,g_num_resources) or K not in range(0,g_num_processes):
                    print("Invalid Request")
                else:
                    if release_resource(I,J,K):
                        print(f"Process {K} release {I} units of resource {J}: Granted")
                    else:
                        print(f"Process {K} release {I} units of resource {J}: Denied")
                    print("Available")
                    print(g_Available)
                    print("MAX")
                    for m in g_Max:
                        print(m)
                    #print(g_Max)
                    print("Current")
                    for c in g_Current:
                        print(c)
                 
def request(num,resource,process):
    global g_Available,g_Current,g_Requests,g_Max,g_Total, g_num_resources, g_num_processes,g_potential,mutex
    mutex.acquire()
    # t_requests=two_d_copy(g_Requests)
    # t_requests[process][resource]=num
    
    if num > g_Max[process][resource]-g_Current[process][resource]:
        mutex.release()
        return False
    if num > g_Available[resource]:
        mutex.release()
        return False

    # for p, proc in enumerate(t_requests):
    #     for r,reso in enumerate(proc):
    #         if t_requests[p][r] > g_Max[p][r]-g_Current[p][r]:
    #             mutex.release()
    #             return False
    #         if t_requests[p][r] > g_Available[r]:
    #             mutex.release()
    #             return False
    t_Available = one_d_copy(g_Available)
    t_Current = two_d_copy(g_Current)
    t_Available[resource]-=num
    t_Current[process][resource]+=num
    
    if bankers(t_Available,t_Current):
        g_Available[resource]-=num
        g_Current[process][resource]+=num
        mutex.release()
        return True
    mutex.release()
    return False

def release_resource(num,resource,process):
    global g_Available,g_Current,g_Requests,g_Max,g_Total, g_num_resources, g_num_processes
    mutex.acquire()
    if num is not range(0,g_Current[process][resource]+1):
        g_Available[resource]+=num
        g_Current[process][resource]-=num
        mutex.release()
        return True
    mutex.release()
    return False

def auto():
    global mutex
    num_customers = int(input("Num Customers: "))
    threads = []
    n=0
    while n < num_customers:
        thread = my_thread(target=create_thread_requests, args=(n,))
        threads.append(thread)
        thread.start()
        n+=1
    for thread in threads:
        thread.join()

def create_thread_requests(thread_name):
    global g_Available,g_Current,g_Requests,g_Max,g_Total, g_num_resources, g_num_processes,g_potential
    #I = num Resources
    #J = Resource
    #K = process
    
    for _ in range(3):
        
        J = randint(0,g_num_resources-1)
        K = randint(0,g_num_processes-1)
        I = randint(1,g_Max[K][J])
        #print(f"\nt{thread_name}: Process {K} requesting {I} units of resource {J}")
        if request(I,J,K):
            print(f"\nt{thread_name}: Process {K} request of {I} units of resource {J}: Granted")
            continue
        else: print(f"\nt{thread_name}: Process {K} request of {I} units of resource {J}: Denied")
        
        
        
        J = randint(0,g_num_resources-1)
        K = randint(0,g_num_processes-1)
        I = randint(1,g_Current[K][J]+1)
        #print(f"\nt{thread_name}: Process {K} Releasing {I} units of resource {J}")
        if release_resource(I,J,K):
            print(f"\nt{thread_name}: Process {K} release of {I} units of resource {J}: Granted")
            continue
        else: print(f"\nt{thread_name}: Process {K} release of {I} units of resource {J}: Denied")
    
def one_d_copy(array):
    new_array=[]
    for i in array:
        new_array.append(i) 
    return new_array
def two_d_copy(array):
    new_array=[[0] for y in range(len(array))]
    for index, f in enumerate(array):
        new_array[index]=one_d_copy(f)
    return new_array
            
        
main()
