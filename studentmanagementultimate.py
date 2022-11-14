#Student Management System
'''Program containing all the basic functions to manage a student database.'''
#importing the modules
import mysql.connector as mycon
import time
import sys
#establishing connections
con=mycon.connect(host='localhost', database='data', user='root', passwd='sobs', autocommit=True)
#initial values
Studid=0
Name=''
Class=''
Age=0
Email=''
Phoneno=''
Feedues=0.0
Installments=0
#functions
def op_delay():                                                                     #Function to create a small delay between the heavy operations.
    abc='''....
....
....\n'''
    for i in abc:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.3)

def verifyEmail(input_email):
    input_email=input_email.strip()
    valid=True
    str1=input_email.split("@")
    if(len(str1)==2 and str1[0].isalpha()==True):
        if(str1[1].endswith(".com")==False) and (str1[1].endswith(".ae")==False) and (str1[1].endswith(".in")==False):
            valid=False
    else:
        valid=False
    return valid

def verifyName(input_name):
    input_name=input_name.strip()
    valid=True
    if(len(input_name)<1):
        valid=False
    str1=input_name.split(" ")
    for word in str1:
        if(word.isalpha()==False):
            valid=False
    return valid
def verifyAge(input_age):
    input_age=input_age.strip()
    if(len(input_age)>0) and input_age.isdigit():
        input_age=int(input_age)
        if(input_age<=0):
            return False
        else:
            return True
    else:
        return False

def verifyPhone(input_phone):
    input_phone=input_phone.strip()
    if(len(input_phone)>0 and len(input_phone)==10 and input_phone.isdigit()==True):
        return True
    else:
        return False

def verifyAllValues(Name,Class,Age,Email,Phoneno):
    valid=True
    if(verifyName(Name)==False):
        print("!!! Invalid Name Entered!")
        valid=False
    if(verifyAge(Age) ==False):
        print("!!! Invalid Age Entered!")
        valid=False
    if(verifyEmail(Email) ==False):
        print("!!! Invalid Email Entered!")
        valid=False
    if(verifyPhone(Phoneno) ==False):
        print("!!! Invalid Phone Number Entered!")
        valid=False
    return valid

def readValues():
    while(True):
        Name=input('Name of the student                  :')
        Class=input('Class of the student                 :')
        Age=input('Age of the student                   :')
        Email=input('E-mail of the student                :')
        Phoneno=input('Phone number of the guardian         :')
        if(verifyAllValues(Name,Class,Age,Email,Phoneno)==True):
            Age=int(Age)
            break
        else:
            print('---------------------------')
            print("Re-Enter All Values")
            print('---------------------------')
    return Name,Class,Age,Email,Phoneno

def verifyFeedue(input_feedue):
    if(len(input_feedue)>0) and input_feedue.isdecimal():
        input_feedue=float(input_feedue)
        if (input_feedue<0):
            return False
        else:
            return True
    else:
        return False
    
def verifyInstallment(input_installment):
    if(len(input_installment)>0) and input_installment.isdigit():
        input_installment=int(input_installment)
        if(input_installment<0):
            return False
        else:
            return True
    else:
        return False
    
def verifyTransaction(Feedues,Installments):
    valid=True
    if(verifyFeedue(Feedues)==False):
        print('!!! Invalid Fee amount!')
        valid=False
    if(verifyInstallment(Installments)==False):
        print('!!! Invalid number of installments!')
        valid=False
    return valid

def readTransaction():
    while True:
        Feedues=input('Enter the fee due amount             :')
        Installments=input('Enter the number of installments done:')
        if(verifyTransaction(Feedues,Installments)==True):
            break
        else:
            print('---------------------------')
            print('   Re-enter fee values')
            print('---------------------------')
    return Feedues,Installments

def add_student():
    '''Adds a new student entry to the database.'''
    sta='''select Studid from studentsdata;'''
    cur.execute(sta)
    rows=cur.fetchall()
    count=cur.rowcount
    if count==0:
        Studid=1                                                                     #The first student ID
    else:
        Studid=rows[-1][0]+1                                                         #The next ID after the existing number
    print('The Student ID is                    :',Studid)
    Name,Class,Age,Email,Phoneno=readValues()
    add='''insert into studentsdata(Studid, Name, Class, Age, Email, Phoneno)
values({}, '{}', '{}', {}, '{}', '{}');'''.format(Studid, Name, Class, Age, Email, Phoneno)
    cur.execute(add)
    Feedues,Installments=readTransaction()
    addfees='''insert into academicfees(Studid, Feedues, Installments)
    values({}, {}, {});'''.format(Studid, Feedues, Installments)
    cur.execute(addfees)
    con.commit()
    print('Registering all the details, Please wait.')
    op_delay()
    print('Student details successfully registered.')

def students_list():
    '''Shows the names of students in the database.'''
    st2='''select Studid,Name from studentsdata order by Studid asc;'''
    cur.execute(st2)
    rows=cur.fetchall()
    print('Acquiring the list, Please wait.')
    op_delay()
    for i in rows:
        print(i)

def show_student():
    Studid=int(input('Enter the ID of the student:'))
    st3='''select * from studentsdata NATURAL JOIN academicfees where Studid={};'''.format(Studid)
    cur.execute(st3)
    rows=cur.fetchall()
    count=cur.rowcount
    print('Acquiring results, Please wait.')
    op_delay()
    if count!=0:
        row=rows[0]
        print('---------------------------')
        print('~~~~| Student Details |~~~~')
        print('---------------------------')
        print('ID             :',row[0])
        print('Name           :',row[1])
        print('Class          :',row[2])
        print('Age            :',row[3])
        print('E-mail         :',row[4])
        print('Phone No.      :',row[5])
        print('Fee due        :',row[6])
        print('Installments   :',row[7])
    else:
        print('The student data does not exist.')

def update_student():
    Studid=int(input('Enter the ID of the student to be updated:'))
    st4='''select * from studentsdata NATURAL JOIN academicfees where Studid={};'''.format(Studid)
    cur.execute(st4)
    rows=cur.fetchall()
    count=cur.rowcount
    print('Acquiring results, Please wait.')
    op_delay()
    if count!=0:
        row=rows[0]
        print('---------------------------')
        print('~~~~| Student Details |~~~~')
        print('---------------------------')
        print('ID             :',row[0])
        print('Name           :',row[1])
        print('Class          :',row[2])
        print('Age            :',row[3])
        print('E-mail         :',row[4])
        print('Phone No.      :',row[5])
        print('Fee due        :',row[6])
        print('Installments   :',row[7])
        print('---------------------------')
        while(True):
            conf=input("Do you want to update the student's details?(y/n):")
            if conf=='y':
                print('Enter the new details')
                Name,Class,Age,Email,Phoneno=readValues()
                st5='''update studentsdata set Name='{0}', Class='{1}', Age={2}, Email='{3}', Phoneno='{4}' where Studid={5};'''.format(Name, Class, Age, Email, Phoneno, Studid)
                cur.execute(st5)
                Feedues,Installments=readTransaction()
                st6='''update academicfees set Feedues={0}, Installments={1} where Studid={2};'''.format(Feedues,Installments,Studid)
                cur.execute(st6)
                print('Updating the details, Please wait.')
                op_delay()
                st6='''select * from studentsdata NATURAL JOIN academicfees where Studid={};'''.format(Studid)
                cur.execute(st6)
                rows=cur.fetchall()
                count=cur.rowcount
                if count!=0:
                    row=rows[0]
                    print('-----------------------------------')
                    print('~~~~| Updated Student Details |~~~~')
                    print('-----------------------------------')
                    print('ID             :',row[0])
                    print('Name           :',row[1])
                    print('Class          :',row[2])
                    print('Age            :',row[3])
                    print('E-mail         :',row[4])
                    print('Phone No.      :',row[5])
                    print('Fee due        :',row[6])
                    print('Installments   :',row[7])
                    print('-----------------------------------')
                break
            elif conf=='n':
                print('Details updation aborted.')
                break
            else:
                print('!!! Invalid option!')
            
    else:
        print("The student's data does not exist.")

def delete_student():
    Studid=int(input('Enter the ID of the student to be deleted:'))
    st5='''DELETE FROM studentsdata where Studid={};'''.format(Studid)
    cur.execute(st5)
    st6='''DELETE FROM academicfees where Studid={};'''.format(Studid)
    cur.execute(st6)
    op_delay()
    print("Student's data successfully wiped out.")

#test connection
if con.is_connected:
    print('Connected to MySQL 5.7')
    #create a cursor object to execute DDL and DML commands
    cur=con.cursor()
    #Create a query string
    st1='''show tables;'''
    cur.execute(st1)
    rows=cur.fetchall()
    if ('studentsdata',) not in rows:
        st2='''create table studentsdata (Studid int(10), Name varchar(20), Class varchar(50), Age int(10), Email varchar(80), Phoneno varchar(70));'''.format(Studid, Name, Class, Age, Email, Phoneno)
        cur.execute(st2)
    if ('academicfees',) not in rows:
        st3='''create table academicfees (Studid int(10), Feedues decimal(15,2), Installments int(10));'''.format(Studid, Feedues, Installments)
        cur.execute(st3)
    else:
        pass

    menu='''
    -------------------------------------------
    ~~~~~~~~~~| Student Management |~~~~~~~~~~~
    -------------------------------------------
    Possible options:
    1. Add a new student
    2. Show the list of students
    3. Show a student's details
    4. Update the details of a student
    5. Delete a student
    6. Quit the portal
    -------------------------------------------'''
    while True:
        print(menu)
        ch=input('Please enter an option:')
        if ch.isdigit():
            ch=int(ch)
            if 0<ch<7:
                if ch==1:
                    add_student()
                elif ch==2:
                    students_list()
                elif ch==3:
                    show_student()
                elif ch==4:
                    update_student()
                elif ch==5:
                    delete_student()
                elif ch==6:
                    break
            else:
                print('Enter an option from 1 to 6')
        else:
            print('Enter a valid option.')
    con.close()
else:
    print('Not Connected to MySQL 5.7')
