import os #need this package to scrape the locally stored data files
import nltk
from nltk.probability import FreqDist #frequency distribution statistics finder
from collections import Counter #another tool to count frequencies
from bs4 import BeautifulSoup # for extracting stuff from htmls   
from collections import defaultdict #import a "dictionary" data type: to create dict of lists 

### important global variables ###
datadir = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) #get parent directory
datadir += '/movie/'
rvfilenames = os.listdir(datadir) #open a file: open(datadir+rvfilenames)
reviewerdir = os.getcwd() + '/reviewerdata/'
moviedir = os.getcwd() + '/moviedata/'


###########################################################################
# Function setup_bymovie():
# First, this function starts by going through the set of all raw reviews.
# It creates a file called "movie_names"; for each review, it extracts
# the movie title and prints it into the new file
#
# Secondly, the function will peruse through the new file, "movie_names"
# and, for each name encountered, it will store the index of the line in
# which that name was encountered in a dictionary, which has keys corresp-
# onding to names, and values corresponding to lists of indices.
#
# FUNCTIONALITY: this function can be used to count the number of reviews
# for each movie. It can also be used to find the indices of movie X's
# reviews within the directory of raw reviews.
###########################################################################
def setup_bymovie():
    #find the title and authors of all movie reviews & store?
    if not os.path.isfile(os.getcwd() + '/movie_names'): #if there is no file with all titles, create it.
        f = open("movie_names", 'w')
        for rvfile in rvfilenames:
            try: #in some rare cases, the movie's name cannot be found this way. If it can, record it.
                soup = BeautifulSoup(open(datadir + rvfile))
                title = soup.find("title").get_text().encode('utf8')
                print title
                f.write( title+'\n' )
            except:
                print "error: couldn't find title\n"
                f.write(' \n')
        f.close()

    #get the titles of movies from the file of movies
    movienames = defaultdict(list)
    fileno = 0
    with open("movie_names") as openfileobject:
        for line in openfileobject:
            if not movienames:
                movienames[line] = [fileno]
            elif line in movienames:
                movienames[line].extend([fileno])
            else:
                movienames[line] = [fileno]
            fileno += 1
    return movienames


###########################################################################
# Function setup_byreviewer():
# First, this function starts by going through the set of all raw reviews.
# It creates a file called "reviewer_names"; for each review, it extracts
# the reviewer and prints it into the new file
#
# Secondly, the function will peruse through the new file, "reviewer_names"
# and, for each name encountered, it will store the index of the line in
# which that name was encountered in a dictionary, which has keys corresp-
# onding to names, and values corresponding to lists of indices.
#
# FUNCTIONALITY: this function can be used to count the number of reviews
# for each author. It can also be used to find the indices of author X's
# reviews within the directory of raw reviews.
###########################################################################
def setup_byreviewer():
    #find the title and authors of all movie reviews & store?
    if not os.path.isfile(os.getcwd() + '/reviewer_names'): #if there is no file with all titles, create it.
        f = open("reviewer_names", 'w')
        for rvfile in rvfilenames:
            try:
                soup = BeautifulSoup(open(datadir + rvfile))
                #try to work with exceptional control flow on the below.
                reviewer = soup.find("h3").a.text
                print reviewer
                f.write( reviewer+'\n' )
            except:
                print "error: couldn't find file \n"
                f.write(' \n')
                continue
        f.close()

    #get the indices of the reviewers from the file of reviewers.              
    reviewernames = defaultdict(list)
    fileno = 0
    with open("reviewer_names") as openfileobject:
        for line in openfileobject: #on each line is an author name: create a dictionary with the name as the key.
            if not reviewernames:
                reviewernames[line] = [fileno]
            elif line in reviewernames:
                reviewernames[line].extend([fileno])
            else:
                reviewernames[line] = [fileno]
            fileno += 1
    return reviewernames

#output the number of reviews that each reviewer has
def write_num_reviewers():
    revnames = setup_byreviewer()
    for k in revnames:
        print len(revnames[k])

#output the number of reviews that each movie has
def write_num_movies():
    movienames = setup_bymovie()
    for k in movienames:
        print len(movienames[k])


############################################################################
# Function: collect_revs_bycritic()
# first, calls the setup_bycritic function, which returns a dictionary
# of reviewer names vs. indices in the data directory. This function
# goes through all the data in the data directory and sorts into files
# by reviewer names. 
# Creates n = num_reviewers files. In each file is a short header formatted:
# "Author"
# "%s", author_name
# "Number of Reviews"
# "%s\n", num_reviews_of_current_author
# {
# "Title"
# "%s", title_i
# "%s", text_of_review_i
# }, repeated for all i \in {reviews of current author}
############################################################################
def collect_revs_bycritic():
    #start with just one critic
    numfiles = 0
    reviewerfiles = setup_byreviewer()
    for key in reviewerfiles:
        #open the next file.
        print "review number " + str(numfiles)
        numfiles += 1
        #only add a file if it hasn't already been added.
        if os.path.isfile(reviewerdir + 'reviewers' + str(numfiles)):
            continue
        f = open(reviewerdir + "reviewers" + str(numfiles), 'w')    
        try:
            #start writing to the file
            f.write("Authors\n")
            f.write(str(key))
            f.write( "Number of Reviews\n")
            f.write( str(len(reviewerfiles[key])) + '\n')
            #find all the files with the given author and do the following:
            for index in reviewerfiles[key]:
                rvfile = rvfilenames[index]
                soup = BeautifulSoup(open(datadir + rvfile))
                title = soup.find("title").get_text().encode('utf8')
                f.write("\nTitle\n")
                f.write(title+'\n')
                #get all the text of the review and print it on the screen.
                paragraphs = soup.findAll("p")
                for p in paragraphs:
                    if p.get("class") == ['flush']:
                        break
                    f.write(p.get_text().encode('utf8'))
                    f.write('\n')
                    #allfiles += p.get_text()
        except:
            f.write('fatal error: could not extract text\n');                        
        f.close()

############################################################################
# Function: collect_revs_bymovie()
# first, calls the setup_bymovie function, which returns a dictionary
# of movie names vs. indices in the data directory. This function
# goes through all the data in the data directory and sorts into files
# by movie names. 
# Creates n = num_movies files. In each file is a short header formatted:
# "Title"
# "%s", movie_name
# "Number of Reviews"
# "%s\n", num_reviews_of_current_movie
# {
# "Author"
# "%s", author_i
# "%s", text_of_review_i
# }, repeated for all i \in {reviews of current movie}
############################################################################
def collect_revs_bymovie():
    #start with just one critic
    numfiles = 0
    moviefiles = setup_bymovie()
    for key in moviefiles:
        #open the next file.
        print "movie number " + str(numfiles)
        numfiles += 1
        #only add a file if it hasn't already been added.
        if os.path.isfile(moviedir + 'movie' + str(numfiles)):
            continue
        f = open(moviedir + "movie" + str(numfiles), 'w')    
        try:
            #start writing to the file
            f.write("Title\n")
            f.write(str(key))
            f.write( "Number of Reviews\n")
            f.write( str(len(moviefiles[key])) + '\n')
            #find all the files with the given author and do the following:
            for index in moviefiles[key]:
                rvfile = rvfilenames[index]
                soup = BeautifulSoup(open(datadir + rvfile))
                try:
                    reviewer = soup.find("h3").a.text.encode('utf8')
                except:
                    reviewer = "unknown"
                f.write("\nAuthor\n")
                f.write(reviewer+'\n')
                #get all the text of the review and print it on the screen.
                paragraphs = soup.findAll("p")
                for p in paragraphs:
                    if p.get("class") == ['flush']:
                        break
                    f.write(p.get_text().encode('utf8'))
                    f.write('\n')
                    #allfiles += p.get_text()
        except:
            f.write('fatal error: could not extract text\n');                        
        f.close()

    
##main method: for now, just want to write movies
collect_revs_bymovie()
