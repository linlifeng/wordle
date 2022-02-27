from sys import  argv

f = open(argv[1])


letters = "abcdefghijklmnopqrstuvwxyz"
for l in f:
    if len(l.rstrip()) != 5:
        continue
    uniq = {}
    for letter in l.rstrip():
        if letter.lower() not in letters:
            continue
        if letter in uniq:
            continue
        else:
            uniq[letter] = 1
    if len(uniq) >= 4:
        print(l.rstrip().lower())

f.close()