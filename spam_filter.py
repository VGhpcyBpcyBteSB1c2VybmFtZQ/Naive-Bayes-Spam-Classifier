import os
import re
import csv

if (not os.path.isfile("Dataset.csv")):
    print("\nDataset.csv file not found\n")
    exit()

fileCSV = open("Dataset.csv", "r")
data = csv.DictReader(fileCSV)

if (not os.path.isfile("stopwords.txt")):
    print("\n stopwords.txt file not found\n")
    exit()

file = open("stopwords.txt", "r")
stopwords = file.read()
stopwords = stopwords.split("\n")
file.close()

#                   DICTIONARY CONSTRUCTION                  #

#######################################################################

mainDictionary = {}  # main dictionary to store the counts for each word: the format is {word1: [totalCount, spamcount], word2: [totCount, spamCount]...}
totalSpam = 0
totalOverall = 0
totalSentences = 0
totalSpamSentences = 0

#######################################################################

print("Constructing dictionary...")

for row in data:
    totalSentences += 1
    if (row['v1'] == 'spam'):
        totalSpamSentences += 1

    row['v2'] = row['v2'].casefold()                          # convert to lowercase
    words = re.findall(r'\w+', row['v2'])               # split sentence into words

    for word in words:
        if (word not in mainDictionary):
            if (row['v1'] == 'spam'):
                mainDictionary[word] = [1, 1]
            else:
                mainDictionary[word] = [1, 0]
        else:
            mainDictionary[word][0] += 1  # add to totalcount
            if (row['v1'] == 'spam'):
                mainDictionary[word][1] += 1  # add to spam count if it is in a spam sentence

keyList = list(mainDictionary.keys())
for key in keyList:                          # remove stopwords
    for word in stopwords:
        if (key == word):
            del mainDictionary[key]
            break
    if key in mainDictionary:
        totalSpam += mainDictionary[key][1]
        totalOverall += mainDictionary[key][0]

print("Dictionary constructed\n")

#####################################################################

test = input("Enter test sentence: ")
test = test.casefold()
test = re.findall(r'\w+', test)

spamProb = 1           # probability for spam
nonSpamProb = 1        # probaility for non spam

for word in test:
    if word in mainDictionary:
        spamProb *= (mainDictionary[word][1] + 1) / (totalSpam + 2)
        nonSpamProb *= (mainDictionary[word][0] - mainDictionary[word][1] + 1) / (totalOverall - totalSpam + 2)

spamProb *= totalSpamSentences / totalSentences

nonSpamProb *= (totalSentences - totalSpamSentences) / totalSentences

t = (spamProb + nonSpamProb)
spamProb /= t
nonSpamProb /= t

print("\nSpam: ", spamProb * 100, " Not Spam: ", nonSpamProb * 100, "\n")
if (spamProb > nonSpamProb):
    print("Final Verdict: SPAM\n")
else:
    print("Final Verdict: NOT SPAM\n")
fileCSV.close()

os.system("pause")
