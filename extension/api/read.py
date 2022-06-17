
while True:
    trade_buffer=open("./api/publication.buf", 'r')
    lines=trade_buffer.readlines()
    trade_buffer=open("./api/thr.buf", 'r')
    thrLines=trade_buffer.readlines()
    print(lines)
    print(thrLines[0]+ ' '+ thrLines[1])