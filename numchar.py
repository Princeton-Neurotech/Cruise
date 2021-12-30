import math
import tkinter as tk
import time
import msvcrt
import numpy as np
from threading import Timer,Thread
from pynput import keyboard

print("Press ENTER to start the stopwatch")
print("and, press CTRL + C to stop the stopwatch")

"""
Stopwatch
while True:
    try:
        input() # for ENTER 
        start_time = time.time()
        print("Stopwatch started...")
        end_time = time.time()
         
    except KeyboardInterrupt:
        print("Stopwatch stopped...")
        print("The total time:", round(end_time-start_time, 2),"seconds")
        break
"""

"""from threading import Timer

timeout = 10
t = Timer(timeout, print, ['Sorry, times up'])
t.start()
prompt = "You have %d seconds to choose the correct answer...\n" % timeout
answer = input(prompt)
t.cancel()"""

def key_press(key, could_put_anything):
    """Aysnc key press handler
    """
    print("Key press detected: ", key)

    # end loop if return False  --> q = quitting
    if key=='q':
        return False
    
    return True










check = False
sec_list = []
count_list = []

start_time = time.time()
#count = 0
sec_array = np.array([])
while True:  

    curr_time = time.time()
    #if msvcrt.kbhit() == False: # returns true if keypress is waiting to be read
    #INPUT
    char = msvcrt.getch() # reads keypress and returns resulting char
    sec_list.append(round(curr_time - start_time, 2))
    sec_array = np.array(sec_list)

    print("Key Pressed", char, "Count", (sec_array >= (round(curr_time - start_time, 2) - 60)).sum())
    
    #PRINTS CHARS WRITTEN IN LAST MIN  EACH 5 SECONDS  
    if (round(curr_time - start_time) % 5) - 1 == 0 and (curr_time - start_time != 0):
        check = True
    elif (round(curr_time - start_time) % 5) == 0 and (curr_time - start_time != 0) and check == True:
        check = False
        print((sec_array >= (round(curr_time - start_time, 2) - 60)).sum())
   
        
        

def charcount():
    output.delete(0.0,"end")
    w=inputUser.get(0.0,"end")
    sp=decision.get()
    c=0
#specifying conditions
    if sp==1:
        for k in w:
            if k=="\n":
                continue
            c=c+1
    elif sp==2:
        for k in w:
            if k==" " or k=="\n":
                continue
            c=c+1

    output.insert(tk.INSERT,c)
#creating interface
window=tk.Tk()
window.title("Count Characters")
window.geometry("500x600")
label=tk.Label(window,text="Input")
#Formatting
inputUser=tk.Text(window,width=450,height=10,font=("Helvetica",16),wrap="word")
decision=tk.IntVar()
#Radio buttons for space counting
r1=tk.Radiobutton(window,text="with spaces",value=1,variable=decision)
r2=tk.Radiobutton(window,text="without spaces",value=2,variable=decision)
#BUtton to count 
button=tk.Button(window,text="Count the number of characters",command=charcount)
label2=tk.Label(window,text="number of characters")
#Output Block
output=tk.Text(window,width=20,height=2,font=("Helvetica",16),wrap="word")

#Function calling
label.pack()
inputUser.pack()
r1.pack()
r2.pack()
label2.pack()
output.pack()
button.pack()

window.mainloop()