#import libraries
from numpy import *
import random
import operator

class Loan (object):#create a class for the data
    loan_amount = 0
    term = 0
    int_tate = 0
    emp_year = 0
    installment = 0
    home_ownership = 0
    annual_income = 0
    dti = 0
    status = ""
    deling_2yrs = ""
    
def selectRandom():#function to select data to be classified from testset
    data = []    
    f = open("E:\\LoanStats3c.csv","r")
    lines = f.read().splitlines()
    del lines[0]
    line = random.choice(lines)
    col = line.split(",")
    col_3 = float(col[3].strip("%"))/100
    data = [float(col[1]),float(col[2]),col_3,float(col[4]),float(col[5]),float(col[6]),float(col[7]),float(col[8])]
    return data    

def NormalizeData(list):#function to normalize features
    newlist = []
    minL = min(list)
    maxL = max(list)
    for l in list:
        l = 1.0*(l - minL) / (maxL - minL)
        newlist.append(l)
    return newlist

def CreateMatrix(n,m,Matrix,List):#function to create matrix
    for i in range(n):
        Matrix[i][m] = List[i]
    return Matrix
    
def kNN(x, Matrix, Label, k):#function for kNN algorithm
    targetM = tile(x,(Matrix.shape[0],1))
    diffSq = (targetM - Matrix)*(targetM - Matrix)
    distance = (diffSq.sum(axis=1))**0.5
    sort_dis = distance.argsort()    
    classCount={}          
    for i in range(k):
        voteIlabel = Label[sort_dis[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
        sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

#read data file
f = open("E:\\LoanStats3b.csv","r")
lines = f.read().splitlines()
del lines[0]

#Create lists for the data
LoanData = []
loan_amount = []
term = []
int_rate = []
emp_year = []
installment = []
home_ownership = []
annual_income = []
dti = []
status = []

#put data in the class
for line in lines:
    col = line.split(",")
    
    if col[6]=="NONE" or col[6] == "OTHER":
        continue
    if col[9]=="0":
        continue

    loan = Loan()    
    loan.loan_amount = float(col[1])
    loan.term = float(col[2])
    loan.int_rate = float(col[3].strip("%"))/100
    loan.emp_year = float(col[4])
    loan.installment = float(col[5])               
    loan.home_ownership = float(col[6])
    loan.annual_income = float(col[7])
    loan.dti = float(col[8])
    loan.status = col[9]
    #loan.deling_2yrs = col[10]
    
    loan_amount.append(loan.loan_amount)
    term.append(loan.term)    
    int_rate.append(loan.int_rate)
    emp_year.append(loan.emp_year)
    installment.append(loan.installment)    
    home_ownership.append(loan.home_ownership)
    annual_income.append(loan.annual_income)
    dti.append(loan.dti)  
    status.append(loan.status)

LoanData.append(loan_amount)
LoanData.append(term)
LoanData.append(int_rate)
LoanData.append(emp_year)
LoanData.append(installment)
LoanData.append(home_ownership)
LoanData.append(annual_income)
LoanData.append(dti)
status = asarray(status)

#get data to be classified from another data file or user
print "Welcome to the Loan Data Classification Model.\n"
print "This model applies the kNN(k-Nearest Neighbors) classification algorithm.\n"
k = input("Please enter \"k\": ")
inputX = raw_input("Enter A to use data from file.\nEnter B to enter new data: ")
if inputX == 'A':
    dataX = selectRandom()
elif inputX =='B':
    amountX = input("Please enter the value for classification.\nLoan amount = ")
    termX = input("Term = ")
    i_rX = input("interest rate(%) = ")/100
    e_yearX = input("employed year(s) = ")
    installX = input("installment = ")
    home_ownX = input("# of home owned = ")
    incX = input("annual income = ")
    dtiX = input("debit to income ratio = ")
    dataX = [amountX,termX,i_rX,e_yearX,installX,home_ownX,incX,dtiX]
print dataX

#Normalize the data to be classified
for r in range(8):
    minD = min(LoanData[r])
    maxD = max(LoanData[r])
    dataX[r] = (dataX[r] - minD)/(maxD - minD)
dataX = array(dataX)

#normalize data using NormalizeData function
for r in range(8):
    LoanData[r] = NormalizeData(LoanData[r])
    
#create the matrix with dataset using CreateMatrix function
length = len(loan_amount)
TestMatrix = [ [0 for x in range(8)] for x in range(length)]

for r in range(8):
    TestMatrix = CreateMatrix(length,r,TestMatrix,LoanData[r])
TestMatrix = array(TestMatrix)

#apply kNN function to classify dataX
label = kNN(dataX,TestMatrix,status,k)

#show the result to user
label_ = ""
if label == "2":
    label_ = "fullpaid"
elif label == "1":
    label_ = "other"
#elif label == "0":
    #label_ = "current"
elif label == "-1":
        label_ = "chargeoff"
print "The target variable is most likely to be classified as " + label_ + "."
print "Thank you for using the Loan Data Classification Model."