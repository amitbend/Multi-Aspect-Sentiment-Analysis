"Ver5.1-This version separates functions,connects to DB and gets reviews (GetReviews.py), analyses them (Analysis.py), and print results in main"






import os
from Analysis import Semantic_analysis
import DBfuncs
def main(): 
    Path = os.getcwd()+'\AFINN-111.txt'
    f=open(Path)    
    Data=DBfuncs.QuerryDB("Select distinct p_id,review_id from reviews")    #Tuples of : (product_ID, Review_ID)
    "Connects to DB and gets Reviews Without html tags"
    for Prod in Data:
        pid="%d" % Prod[0]                                                  #For each Product_ID
        reviews=DBfuncs.GetReviews(pid)                                     #Retreive all Reviews of Product_ID
        Results=Semantic_analysis(reviews,f)                                #Analyze Reviews
        for res in Results:
            print "Product id: %d, attr: %s score: %6.2f review: %s" % (Prod[0],res[0],res[1],res[2])
            os.system('pause')
    "IMPORTENT: The AFINN-111.txt file most be in the same folder as the main.py file"
    Path = os.getcwd()+'\AFINN-111.txt'
    f=open(Path)
    Results=Semantic_analysis(reviews,f)
    print "end of program"
    for rev in Results:
        print rev[0], rev[1]
    os.system('pause')
main()
