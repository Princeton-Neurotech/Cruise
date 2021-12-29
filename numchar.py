import math
import tkinter as tk
import time
import msvcrt
import numpy as np

print("Press ENTER to start the stopwatch")
print("and, press CTRL + C to stop the stopwatch")

"""
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

# sec_list = []
start_time = time.time()
count = 0
while True:     
    curr_time = time.time()
    
    if msvcrt.kbhit(): # returns true if keypress is waiting to be read
        k = msvcrt.getch() # reads keypress and returns resulting char
        # sec_list.append(round(curr_time - start_time, 2))
        # sec_array = np.array(sec_list)
        # (sec_array >= (round(curr_time - start_time, 2) - 60)).sum()
        count += 1
        print("Key Pressed", k, "Count", count)

        count_stack = []
        if ((round(curr_time - start_time) % 5) == 0):
            # create a stack to store all counts within 1s timeframe
            while(round(curr_time - start_time) % 5 == 0):
                count_stack.append(count)
            # pop the last count within 1s timeframe
            saved_num_char = count_stack.pop()
            print(saved_num_char)

        # print(round(math.fmod(round((curr_time - start_time), 3), 5.000), 3) == 0.000)

        # bool(has_been_printed)
        # has_been_printed = False

        # print(round(curr_time - start_time))

        # if ((round(curr_time - start_time) % 5) == 0):
            # save array to keep track of num of char
            # time.sleep(0.9999)
            # print_start_time = time.time()
            # print_curr_time = time.time()
            # print(print_curr_time - print_start_time)
            # while (print_curr_time - print_start_time != 1.0):
                # print_curr_time = time.time()
                # if ((print_curr_time - print_start_time) == 0.9999):
                    # saved_num_char = count
                    # print(saved_num_char)
            # print(print_curr_time - print_start_time)
           
        
            # if has_been_printed == False:
                # saved_num_char = count
                # print(saved_num_char)

                # if 
                # has_been_printed = 
            
        # total_num_char = [saved_num_char]

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