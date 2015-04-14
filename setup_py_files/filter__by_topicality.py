
#here, create a script to grab a file with annotated words and topicality scores, sorted by topicality
#the script should filter out the unrelated words, and put the rest of the words in another file

f = open("topical_wds", "r")
fout = open("final_topical_wds", "w")
for line in f:
    linearr = line.split()
    if linearr[0] in badwds:
        continue
    if float(linearr[1] < 0.5):
        break

    #now, store the words that pass these tests
    fout.write(linearr[0]+' '+linearr[1])

f.close()
fout.close()
