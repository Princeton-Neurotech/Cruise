def realtime_charcount():
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
button=tk.Button(window,text="Count the number of characters",command=realtime_charcount)
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
