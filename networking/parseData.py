import os

l = os.listdir("con_test")
l = sorted(l)
output = open('data.csv', 'w')

for fname in l:
    print fname
    input =  open("con_test/"+fname, 'r')
    if fname[2] == ',':
        output.write(fname[:2] + ",")
    else:
        output.write(fname[:3] + ",")

    input.readline()
    input.readline()
    
    for i in range(1, 21):
        s = input.readline()
        parts = s.split()
        output.write(str(parts[5]) + ',')
        
    s = input.readline()
    parts = s.split()
    output.write(parts[2] + ',')

    output.write("\n")

    input.close()

output.close()
