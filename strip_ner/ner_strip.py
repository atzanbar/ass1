with open("dev-input",'w') as out:
    for line in open("dev"):
            s_line  = " ".join([p1 for p1,p2 in [pair.rsplit('/',1) for pair  in  line.strip().split(" ")]])
            out.write(s_line+"\n")

