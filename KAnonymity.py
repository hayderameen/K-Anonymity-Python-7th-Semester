'''
How this project is working:

Inputs: 
    1: CSV File with data
    2: Distinct sequences / tuples are stored in "freq" list
    3: Their respective occurences are stored in "freqOccur" list
    4: k input
    5: "QI" list containing Quasi-Identifiers in specific order which is maintained in all lists throughout program
Output:
    The output table which satisfies k-anonymity after generalization and suppression
Process Flow:
    1: Data is stored from CSV file into freq and occurFreq (Initialization)
    2: while checkAnonymity() returns false (there exist sequences in freq occuring less than k times that account for more than k tuples), do
        2.1: execute findAttributeWithMostDistinctValues() and it returns attribute with most distinct values currently
        2.2: call generalize function of that attribute e.g. generalizeBirthDate()
        2.3: execute reArrageAfterGeneralization() and it updates freq in tempFreq list and freqOccur List and it calls checkAnonymity() funciton at end
    3: if checkAnonymity() returns true
        3.1: updates freq list with values from tempFreq
        3.2: suppress sequences occuring less than k times
        3.3 Prints out the final data with k-Anonymity
'''

# Class of Data objects
class info:
    race = ""
    birthDate = ""
    gender = ""
    zip = ""
    def __init__(self, race, birthDate, gender, zip):
        self.race = race
        self.birthDate = birthDate
        self.gender = gender
        self.zip = zip
    def __eq__(self, other):
        return self.race == other.race and self.birthDate == other.birthDate and self.gender == other.gender and self.zip == other.zip

# Determinig attribute with most distinct values
def findAttributeWithMostDistinctValues():
    #freq - sequences
    race = []
    race.append(freq[0].race)
    birthDate = []
    birthDate.append(freq[0].birthDate)
    gender = []
    gender.append(freq[0].gender)
    zip = []
    zip.append(freq[0].zip)
    for x in range(1,len(freq)):
    
        temp = freq[x]
    
        if temp.race not in race:
            race.append(temp.race)
        

        if temp.birthDate not in birthDate:
            birthDate.append(temp.birthDate)
        

        if temp.gender not in gender:
            gender.append(temp.gender)

        if temp.zip not in zip:
            zip.append(temp.zip)

    tempList = [len(race), len(birthDate), len(gender), len(zip)]
    MostDistinct = tempList.index(max(tempList))
    print ("The attribute with most distinct values is: ", QI[MostDistinct])

    # "Race","BirthDate","Gender","Zip"
    if QI[MostDistinct] == "Race":
        print ("Generalizing Race")
    elif QI[MostDistinct] == "BirthDate":
        print("Gerneralizing BirthDate")
        generalizeBirthDate()
    elif QI[MostDistinct] == "Gender":
        print("Gerneralizing Gender")
    elif QI[MostDistinct] == "Zip":
        print("Gerneralizing Zip")

# Check K-Anonymity function
def checkAnonymity(occurances, TFreq):
    print ("\nChecking Anonymity\n")
    number = 0
    while True:
        if occurances[-1] == 0:
            del occurances[-1]
        else:
            break # It was for discarding zeroes of freqOccur list
    freqOccur = occurances
    for x in freqOccur:
        if x >= k:
            number = number + 1
    if (len(freqOccur))-number > k:
        # It requires more generalization
        #generalizeBirthDate()
        findAttributeWithMostDistinctValues()
    else:
        print ("The data now satisfies K Anonymity given above: ", k)
        print ("\n*********************** FINAL DATA **************************\n")
        freq = TFreq # Updating freq list
        for x in range(len(freqOccur)):
            if freqOccur[x] >= k:
                for z in range(freqOccur[x]):
                    print (freq[x].race + " " + freq[x].birthDate + " " + freq[x].gender + " " + freq[x].zip)



# It contains occurences of sequences
freqOccur = [1 for x in range(12)] # Initial value is set to 1

print ("****************** K-Anonymity ******************\n")

# Inputs
QI = ["Race","BirthDate","Gender","Zip"]
k = 2

# It will contain sequences and frequencies in form of info objects
freq = []

# Function for displaying data in freq list
def displayFreq(Tfreq, FO):
    freq = Tfreq
    freqOccur = FO
    for x in range(len(freq)):
        print (freq[x].race + " " + freq[x].birthDate + " " + freq[x].gender + " " + freq[x].zip)
        print ("Occurances: ", freqOccur[x])
        print ("\n")


# Function to rearrange data in freq and freqOccur after a generalization operation
def reArrageAfterGeneralization():
    tempFreq = []
    freqOccur = [0 for x in range(len(freq))]
    tempFreq.append(freq[0])
    for x in freq:
        if x not in tempFreq:
            tempFreq.append(x)
            # Got unique values from freq
    for x in range(len(tempFreq)):
        for z in freq:
            if tempFreq[x] == z:
                freqOccur[x] = freqOccur[x] + 1
                # Got frequencies of all sequences


    print ("Displaying data after reArrage Function")
    displayFreq(tempFreq, freqOccur)
    # Now checking if further generalization is required
    checkAnonymity(freqOccur, tempFreq)
    

# Functions for generalization
def generalizeBirthDate():
    for x in range(len(freq)):
        BD = freq[x].birthDate
        BDs = BD.split('/')
        if len(BDs) == 3:
            BD = BDs[1] + "/" + BDs[2]
            freq[x].birthDate = BD
        elif len(BDs) == 2:
            BD = BDs[1]
            freq[x].birthDate = BD
        else:
            freq[x].birthDate = "****"
    reArrageAfterGeneralization()
    


# THIS IS THE FIRST CODE TO BE EXECUTED

# Reading data from file
    # Adding first line to freq
file = open("Book1.csv")
lines = file.readlines()
words = lines[0].split(',')
temp = info(words[0],words[1],words[2],words[3])
freq.append(temp)
    # Adding rest of lines to freq with occurences
for x in range(1,len(lines)):
    words = lines[x].split(',')
    temp = info(words[0],words[1],words[2],words[3])
    
    for z in range(0,len(freq)):
        temp1 = freq[z]
        if temp1 == temp:
            freqOccur[z] = freqOccur[z] + 1
            break
        else:
            freq.append(temp)
            break
# Starting the process
checkAnonymity(freqOccur, freq)

# And initial execution stops here and the loop of generalizing and checking anonymity starts