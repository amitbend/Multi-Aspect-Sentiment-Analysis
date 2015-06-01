import nltk 
from nltk.tokenize import RegexpTokenizer
import math
import re
import sys
import time
import difflib #Tomer 05-12-14

stop_words = stopwords.words('english') #Tomer 05-12-14


#Tomer 05-12-14
def Pre_Procc(needs_correcting):            #The func will receive a sentence in a form of a List and correct it with respect to AFINN file.
    corrected_words = []

    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    needs_correcting =  pattern.sub(r"\1\1", needs_correcting)     #'gooood' -> 'good'

    """
    LOAD FROM SERVER, NOT PC
    """
    with open('C:\Users\user\Desktop\AFINN-111.txt') as AFINN_file:     #Load AFINN file to a List
        file_words = AFINN_file.read().splitlines()
                      
    for w in needs_correcting:
        flag = 0                             #flag is 0 when no match was found in the AFINN file, 1 if a match was found.
        if (w in stop_words) == True:        #stop words are not likely to be misspelled. do not correct stop words.
            continue
        for f_word in file_words:
            fixed_f_word = f_word.split()[0] #remove every character to the right of the word, ('good -2' -> 'good')
            seq = difflib.SequenceMatcher(None, a = w, b = fixed_f_word)
            if seq.ratio() >= 0.8 :          #Correct the original word only if there is atleast 80% match with AFINN word
                corrected_words.append(fixed_f_word)
                flag = 1
                break
            else:
                continue
        if flag == 0:
            corrected_words.append(w)        #couldn't find a match in AFINN file, original word remains
    return corrected_words
#End Tomer 05-12-14

def sentiment(text,pattern_split,afinn):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence. 
    """
    words = pattern_split.split(text.lower())
    #Tomer 11-12-14
    words_corrected = Pre_Procc(words)  
    sentiments = map(lambda word: afinn.get(word, 0), words_corrected)
    #End Tomer 11-12-14
    if sentiments:
        # How should you weight the individual word sentiments? 
        # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
        sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
        
    else:
        sentiment = 0
    return sentiment


def Semantic_analysis(Reviews,AFINN_File):
    reload(sys)
    tokenizer = RegexpTokenizer(r'\w+')
    r = Reviews

    D_Features= {}
    D_Features['water & ice']= [('water' ,'ice','icemaker','dispenser'),(),[]]
    D_Features['freezer']= [('freezer','freezer'),(),[]]
    D_Features['drawer & shelf']= [('drawer', 'shelf','drawers', 'shelves'),(),[]]
    D_Features['service']= [('warranty', 'service'),(('customer', 'service'), ('service',' plans'),('service','plan')),[]]
    D_Features['doors']= [('door' , 'doors'),(),[]]
    D_Features['power usage']= [('efficiency','efficient'),(('power','usage'),('power','saving'),('door' ,'alarm')),[]]
    D_Features['noise']= [('quiet','noise','loud','sound','noisy','buzz','buzzing','humming','noises'),(),[]]
    D_Features['size']= [('size', 'dimensions', 'proportions','cu','ft','small','large','big','space','spaciousness','width','volume','room','fits','fit' ),(('storage','capacity')),[]]
    D_Features['price']= [('price','cost'),(),[]]
    D_Features['Design']= [('design','modern','color'),(('looks','good'),('good','looking'),('looks','beautiful'),('looks','great')),[]]
    d={}
    for f in D_Features.keys(): 
        d[f] = 0
    
    print "Analysing..."
    timeBefore = time.clock()
    
    for revi in r:                                      #r is of type : [   [[review_ID],[review_text]]  ,  [[review_ID],[review_text]]  ]
        print "."
        #Tomer 05-12-14
        revi = revi.replace(";",".")                    #Replace all ";" with "." in a given sentence.
        #End Tomer 05-12-14\
        all_sentences_in_a_review = nltk.sent_tokenize(revi[1].lower())
        Review_ID = revi[0]

        for t in all_sentences_in_a_review:             #For each of the Review's sentences
            sent_p = nltk.pos_tag(tokenizer.tokenize(t))
            l = len(sent_p)
            for f in D_Features.keys(): 
                d[f]=0
            """
            D_Features[f][0] == One word features
            D_Features[f][1] == Two worded features
            D_Features[f][2] == Sentences containing the feature
            """
            """
            The following For-Loop will iterate over sentences and words that a review consists of, and update the 
            Features Dictionary.
            """
            for s in sent_p:                            #For each of the Sentence's words:
                for f in D_Features.keys():             #For each of the known features:
                                        
                    for f_1 in D_Features[f][0]:        #Features consists of one word.
                        
                        if s[0]==f_1 and (s[1]=='NN' or s[1]=='NNS') and d[f]==0:
                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])   
                            d[f]=1
                            
                    if ( d[f]==0):
                        for f_2 in D_Features[f][1]:    #Features consists of two words
                            word1 = f_2[0]              #First word in the Feature
                            word2 = f_2[1]              #Second word in the Feature
                            for i in range (0,l):       #Check if the feature's two words exists in the sentence with at most 3 words seperating them.
                                if (sent_p[i][0]==word1) and d[f]==0: 
                                    if(i<l-3):
                                        if sent_p[i+1][0]==word2:
                                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])
                                            d[f]=1
                                        elif sent_p[i+2][1]== word2 :
                                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])
                                            d[f]=1
                                        elif sent_p[i+3][1]== word2  :
                                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])
                                            d[f]=1
                                    elif(i<l-2):
                                        if sent_p[i+1][1]==word2  :
                                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])
                                            d[f]=1
                                        elif sent_p[i+2][1]==word2 :
                                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])
                                            d[f]=1
                                    elif(i<l-1):
                                        if sent_p[i+1][1]==word2 and d[f]==0 :
                                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])
                                            d[f]=1
                           
                                elif sent_p[i][0]==word2 and d[f]==0:
                                    if(i<l-3):
                                        if sent_p[i+1][0]==word1 :
                                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])
                                            d[f]=1
                                        elif sent_p[i+2][1]== word1 :
                                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])
                                            d[f]=1
                                        elif sent_p[i+3][1]== word1 :
                                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])
                                            d[f]=1
                                    elif(i<l-2):
                                        if sent_p[i+1][1]==word1 :
                                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])
                                            d[f]=1
                                        elif sent_p[i+2][1]==word1 :
                                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])
                                            d[f]=1
                                    elif(i<l-1):    
                                        if sent_p[i+1][1]==word1 :
                                            D_Features[f][2].append([[Review_ID], [t.decode('utf-8')]])
                                            d[f]=1
    
    timeAfter = time.clock()
    print "elapsed time = "+ str(timeAfter - timeBefore) +"Sec"             
    print "Done\n"

    afinn = dict(map(lambda (w, s): (w, int(s)), [ws.strip().split('\t') for ws in AFINN_File ]))
    print "Done\n"            
    # Word splitter pattern
    pattern_split = re.compile(r"\W+")
    Results=[]

    for f in D_Features.keys(): 
        ID_List = []                             #A list of Review ID's that the feature "f" was already observed on.
        l = len(D_Features[f][2])                #Number of sentences containing this feature. 
        for i in range(0,l):
            ID =  D_Features[f][2][i][0]          #Review's ID
            if (ID in ID_List) == True:          #Do not build a temp list to be analyzed in case a list for this review&feature already exists.
                continue
            ID_List.append(ID)
            temp = []                            #A List of Sentences that contains the Feature in the same Review.
            temp.append(D_Features[f][2][i][1])  
            temp.append(" .")
            for j in range(0,l):                 #Append to temp all sentences containing current feature (f) and Are in the same Review.
                if (D_Features[f][2][j][0] == ID) and (j != i):
                    temp.append(D_Feature[f][2][j][1])
                    temp.append(" .")
            """
            while (i < l-1) and (ID == D_Feature[f][2][i + 1][0]):
                temp.append(D_Feature[f][2][i + 1][1])     #Append to temp all sentences containing current feature (f) and 
                i = i + 1                                  #Are in the same Review.
            """
            to_be_analyzed = []
            to_be_analyzed = temp
            if (len(temp) > 1):                 
                to_be_analyzed = ' '.join(temp)     #['aa','bb'] -> ['aa bb']
            Results.append([f,sentiment(to_be_analyzed,pattern_split,afinn), to_be_analyzed, ID])
    """print str(sentiment(text,pattern_split,afinn)) + "," + text"""
    #return D_Features
    return Results  

    
