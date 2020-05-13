import sys
import os
import subprocess
def main():
    #allData Set Files
    originalFileName=sys.argv[1]
    originalFile=open(originalFileName,"r")
    originalLine=originalFile.readline()
    while("@attribute" not in originalLine):
        originalLine=originalFile.readline()
    while("@attribute" in originalLine):
        originalLine=originalLine.replace("{","")
        originalLine=originalLine.replace("}","")
        originalLine=originalLine.replace(",","")
        originalLine=originalLine.replace("@attribute","")
        classes=originalLine.split()
        classes=classes[1:]
        originalLine=originalFile.readline()
    predData={} #Keep track of overall prediction vs actual
    trueClassSize={}
    for i in range(len(classes)):
        predData[classes[i]]={}
        trueClassSize[classes[i]]=0
        for j in range(len(classes)):
            predData[classes[i]][classes[j]]=0
    while("@data" not in originalLine):
        originalLine=originalFile.readline()
    originalLine=originalFile.readline() #reading @data
    while(originalLine.split()[0]=="%"):#skip
        originalLine=originalFile.readline()
    totalN=1 #first line read
    for originalLine in originalFile:#counting the rest of the lines
        totalN=totalN+1
    originalFile.close()
    predictionsFile=open("summary.txt","w+")
    predictionsFile.write("@predictions ( Actual Prediction pSoft pHard pNone)\n")
    selectedSample=0
    for i in range(totalN):
        #Reopen files to do a new set of files
        originalFile=open(originalFileName,"r")
        originalLine=originalFile.readline()
        trainingFile=open("training.txt","w+")
        testFile=open("test.txt","w+")
        testFile.write("@relation testFile")
        trainingFile.write("@relation trainingFile")
        while("@relation" not in originalLine):
            originalLine=originalFile.readline()
        while("@relation" in originalLine):
            originalLine=originalFile.readline()
        while("@data" not in originalLine):
            testFile.write(originalLine)
            trainingFile.write(originalLine)
            originalLine=originalFile.readline()
        testFile.write(originalLine)
        trainingFile.write(originalLine)
        originalLine= originalFile.readline()
        while(originalLine.split()[0]=="%"): ##skip all the %
            originalLine=originalFile.readline()
        #Determine which data will be the test
        for i in range(selectedSample): #training samples when test is not 1st
            trainingFile.write(originalLine)
            originalLine=originalFile.readline()
        selectedSample=selectedSample+1 #What sample will be used next turn
        testFile.write(originalLine) #the single test sample
        correctClass=originalLine.replace('\n','')
        correctClass=correctClass.split(",")[-1] # will be used for summary
        trueClassSize[correctClass]=trueClassSize[correctClass]+1
        for originalLine in originalFile: #the rest of the training set
            trainingFile.write(originalLine)
        trainingFile.close()
        testFile.close()
        originalFile.close()
        #Naive Bayes calculation STARTS
        subprocess.call('python3 naivebayes.py training.txt test.txt result.txt', shell=True)
        #Naive Bayes calculation ENDS
        resultFile=open("result.txt","r")
        newData=resultFile.readline()
        predictionsFile.write(correctClass+" ") #This is the actual class
        predictionsFile.write(newData)
        resultFile.close()
        newData=newData.replace('\n','')
        predData[correctClass][newData.split()[0]]=predData[correctClass][newData.split()[0]]+1


    #Once every single N fold has been completed and all predictions are noted for
    predictionsFile.write('\n')
    #Creating the Matrix on the summary.txt file
    #Confusion Matrix STARTS
    predictionsFile.write("@confusionMatrix\n")
    for i in range(len(classes)):
        for j in range(len(classes)):
            predictionsFile.write(str(predData[classes[i]][classes[j]])+" ")
        predictionsFile.write("\n")
    predictionsFile.write('\n')
    #Confusion Matrix ENDS
    #Calculating the accuracy of my predictions on the summary.txt file
    predictionsFile.write("@accuracy\n")
    TP=0
    TN=0
    FP=0
    FN=0
    #Calculating accuracy STARTS
    for i in range(len(classes)):
        tFP=0
        for j in range(len(classes)):
            if(i==j):
                TP=TP+predData[classes[i]][classes[j]]
                FN=FN+trueClassSize[classes[i]]-predData[classes[i]][classes[j]]
            else:
                tFP=tFP+predData[classes[j]][classes[i]]
                FP=FP+predData[classes[j]][classes[i]]
        TN=TN+totalN-(trueClassSize[classes[i]]-predData[classes[i]][classes[i]])-(predData[classes[i]][classes[i]])-tFP
                
    accuracy=(TP+TN)/(TN+TP+FN+FP)
    predictionsFile.write(str(accuracy)+""+'\n')
    predictionsFile.close()
    #Calculating accuracy ENDS

    #Creating ROC Curves
    curveROCData=open("ROCData.txt","w+")
    for i in range(len(classes)):
        curveROCData.write("@Class"+ " "+classes[i]+" \n")
        threshold=0
        while(threshold<=1.0):
            TP=0
            FP=0
            TN=0
            FN=0
            predFile=open("summary.txt","r")
            rLine=predFile.readline()
            while("@prediction" not in rLine):
                rLine=predFile.readline()
            rLine=predFile.readline() #Read past @predictions
            while ("@confusionMatrix" not in rLine and rLine!="\n"):
                rLine=rLine.replace("\n","")
                lineData=rLine.split()
                actualClass=lineData[0]
                predClass=lineData[2+i]
                predClass=float(predClass)>=threshold
                if(actualClass==classes[i]):
                    #actualClass=Pos so we can determine TP and FN
                    if(predClass):
                        TP=TP+1 #Correctly predicted Positive
                    else:
                        FN=FN+1 #Actual is Positive but it was predicted Negative
                else: #actualClass=Neg
                    if(predClass):
                        FP=FP+1 #Actual is Negative but it was predicted Positive
                    else:
                        TN=TN+1 #Correctly predicted Negative
                rLine=predFile.readline()
            TPR=TP/(TP+FN)
            FPR=1-(TN/(TN+FP))
            curveROCData.write(str(threshold)+" "+ str(FPR)+" "+str(TPR)+" \n")
             
            threshold=threshold+0.1
        curveROCData.write("\n")
             
                    
            

    curveROCData.close()
        

main()
