
import requests
from collections import Counter
from nltk.corpus import stopwords
import csv
import threading


def threaded_func():
    ## Variables always needed for BoW
    tokens = Counter()
    #nltk.download('stopwords')
    STOP = stopwords.words("english")
    STOP.append('the')

    ## Get the target (uri) which is a collection of robert frost poems
    response = requests.get("https://www.gutenberg.org/files/59824/59824-0.txt", stream=True) # https://www.gutenberg.org/files/59824/59824-0.txt
    ## if on windows must add:
    response.encoding = "utf-8"

    ## POEMS don't start until "SELECTED POEMS:" and have copywrite after Poems end
    start_flag = True
    start_counter = 0
    end_flag = False
    #print(type(tokens))
    ## quick load and make bag of words
    for curline in response.iter_lines():
        if curline.strip(): # "" = False
            ## Check if we are at start of poems
            if start_flag:
                #skip this lne until SELECTED POEMS
                if curline.startswith(b'SELECTED POEMS'):
                    if start_counter == 1:
                        start_flag = False
                    else:
                        start_counter = 1
            else:
                ## WE have started the Poems!
                if not end_flag and not curline.startswith(b'End of the P'):
                    ## we are officially only looking at Poems!
                    for word in curline.lower().split():
                        if word.decode() not in STOP:
                            ## decode and add word because not in STOP words
                            tokens[word.decode()] += 1
                else:
                    break

    with open('words.csv', mode='w', encoding='utf-8', newline='') as wordsfile:
        writer = csv.writer(wordsfile, dialect='excel')
        writer.writerow(["word", "count"])

        #print(tokens.most_common())
        #for token, count in tokens.items():
        common_phrase_num = 0
        for token, count in tokens.most_common(): # This sorts the csv file from most occurred to least occurred
            if count > 3:
                writer.writerow([token, count])
                if common_phrase_num <= 5: # Print the 5 most common phrases
                    print(token, count)
                    common_phrase_num += 1

threading.Thread(target=threaded_func()).start()