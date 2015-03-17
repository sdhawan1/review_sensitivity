
####################################################################################################
# Function: Get_text_from_raw_file
# input: "target": this should be a string, corresponding to the file you want to extract text
#         from. It should be a file from the directory "reviewerdata" or "moviedata"
# output: should output all the text that you get from the file. [text only]
####################################################################################################
def Get_text_from_rev_file(target):
    targetfile = open(target, "r")
    storenext = 0
    alltext = ""
    for line in targetfile:
        #this warns us that the next line is the title or author name; therefore we shouldn't store it.
        if (line == "Title\n") or (line == "Authors\n") or (line == "Number of Reviews\n"):
            storenext = 0
        elif storenext == 0:
            storenext = 1
        else:
            alltext += line
    return alltext


#another potential function: get titles, number of reviews of author from file
