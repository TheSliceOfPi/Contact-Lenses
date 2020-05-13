import sys

def main():
    #Parsing the Training set's data STARTS
    
    trainingFileName=sys.argv[1]
    trainingFile=open(trainingFileName,"r")
    trainingSetData=[]
    line=trainingFile.readline()
    while("@attribute" not in line):
       line= trainingFile.readline()
    attributes=[]
    allpossFeat={}
    while("@data" not in line): 
        if(len(line.split())>0):
            line=line.replace("{","")
            line=line.replace("}","")
            line=line.replace(",","")
            line=line.replace("@attribute","")
            parsedLine=line.split()
            attribute=parsedLine[0]
            allpossFeat[attribute]=[]
            attributes.append(attribute)
            for i in range(1,len(parsedLine)):
                allpossFeat[attribute].append(parsedLine[i])
        line=trainingFile.readline()
    categories=allpossFeat[attributes[-1]]
    del allpossFeat[attributes[-1]]
    catCount={}
    totalTrainingCases=0
    for i in range(len(categories)):
        catCount[categories[i]]={}
        for j in range(len(attributes)):
            catCount[categories[i]][attributes[j]]={}
    while("@data" in line):
        line=trainingFile.readline()
    while line:
        totalTrainingCases=totalTrainingCases+1
        line=line.replace('\n',"")
        parsedLine=line.split(",")
        lineCategory=parsedLine[-1]
        for i in range(len(parsedLine)):
            if (parsedLine[i] in catCount[lineCategory][attributes[i]]):
                catCount[lineCategory][attributes[i]][parsedLine[i]]=catCount[lineCategory][attributes[i]][parsedLine[i]]+1
            else:
                catCount[lineCategory][attributes[i]][parsedLine[i]]=1
        line=trainingFile.readline()
    trainingFile.close()
    #Parsing the Training set's data ENDS
    #Naive Bayes on Test set STARTS
    testingFileName=sys.argv[2]
    testingFile=open(testingFileName,"r")
    outputFileName=sys.argv[3]
    outputFile=open(outputFileName,"w+")
    #outputFile.write("Predicted Soft Hard None\n") #Not necessary
    line=testingFile.readline()
    while ("@data" not in line):
        line=testingFile.readline()
    for line in testingFile:
        percentages={}
        line=line.replace('\n',"")
        testFeatures=line.split(",")
        testFeatures=testFeatures[:-1]
        for cat in categories:
            totalCat=catCount[cat][attributes[-1]][cat]
            percentages[cat]=totalCat/totalTrainingCases
            for i in range(len(testFeatures)):
                percentages[cat]=percentages[cat]*(catCount[cat][attributes[i]].get(testFeatures[i],0)/totalCat)
        #All Categories calculated
        totalPerc=0
        largestNum=0
        for i in range(len(categories)):
            totalPerc=totalPerc+percentages[categories[i]]
            if(percentages[categories[i]]>=percentages[categories[largestNum]]):
                largestNum=i
        outputFile.write(str(categories[largestNum])+" ")
        for i in range(len(categories)):
            percentages[categories[i]]=percentages[categories[i]]/totalPerc
            outputFile.write(str(percentages[categories[i]])+" ")
        outputFile.write("\n")

    testingFile.close()
    outputFile.close()
    #Naive Bayes on Test set ENDS
    

main()
