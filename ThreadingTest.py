#Threading library is preinstalled on python.  No need to download
import threading 
#Declare global variables for communicating between functions
run = 1
move_forward=0
def print_one():
#Tell the function that these variables are global 
    global run
    global move_forward
#This function will stop as soon as either function finishes.  This is just to demonstrate functionality of global variables and how to stop both functions at the same time
    while(run):
#Print 10,000 times
        for i in range(10000):
#If i is divisible by 10 then set "move_forward" signal to on, else disable move forward signal
#This is an example of the vision function giving the movement function a signal.
#Condition can be anything.  It is just i%10 for example reasons
            if i%10 == 0:
                #Send signal to movement thread to print move forward
                move_forward=1
            else:
                move_forward=0
#If run signal is 1 then do the task.
            if(run):
                print("Running Vision")
#If run signal is 0 then exit the for loop
            else:
                continue
#If function finishes set run to 0 which will stop the other function.  
        run=0

#Pretty much works the same way as print_one but to simulate movement thread
def print_two(): 
    global run
    global move_forward
    while(run):
        for i in range(10000):
            if(move_forward):
                print("Moving forward")
            if(run):
                print("Running Movement")
            else:
                continue
        run=0


    # create threads
t1 = threading.Thread(target=print_one) 
t2 = threading.Thread(target=print_two) 

    # start thread 1 
t1.start() 
    # start thread 2 
t2.start() 

    # wait until thread 1 is completely executed 
t1.join() 
    # wait until thread 2 is completely executed 
t2.join() 
    # both threads completely executed 

print("Done!")