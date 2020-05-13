Edith Flores
Homework 1: Naive Bayes

Files Submitted:
naivebayes.py
evaluate.py
contact-lenses.arff
predictions.txt
result.txt
ROCData.txt
training.txt
sampleinput.arff
sampletraining.arff
summary.txt
test.txt
ROCCurveAUC.ods
Homework Cover Sheet ML-1.pdf
MLHW1.Report.pdf
readme.txt


-------naivebayes.py-------

The program naivebayes.py takes two files, a file with training samples and a file with testing samples. naivebayes.py then trains using the training sample using the Naive Bayes algorithm. Once trained, The program, naivebayes.py, calculates the probability of each sample to be each of the categories. The predicted category and each of the probabilities are written in an output file.

To run for homework: python3 naivebayes.py sampletraining.arff sampleinput.arff predictions.txt
To run (general): python3 naivebayes.py <training set filename> <testing set filename> <output filename>

--------evaluate.py---------

The program evaluate.py takes one file, a data file. The program, evaluate.py, takes the data file and splits it into a training and a testing file in order to do N-fold. Each of these training and testing files gets placed through naivebayes.py to determine the predictions. The program, evaluate then creates a file that puts all of the sample predictions and probabilities. Once these probabilities are in place, evaluate.py determines the confusion matrix and overall accuracy. Lastly, evaluate.py determines all the PTR and FPR of each category and places all the threshold, TPR, and FPR for each category in a new file.

To run for homework: python3 evaluate.py contact-lenses.arff
To run (general): python3 evaluate.py <data filename>

