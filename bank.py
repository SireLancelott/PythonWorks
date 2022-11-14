#Banking project
'''Contains functions to implement a Banking program'''
#import modules
import mysql.connector as mycon
import datetime
#create a connection object
con=mycon.connect(host='localhost', database='data', user='root', passwd='sobs')
#functions
def Create_account():
    '''Function create a new account for the customer'''
    st1='''select accno from bank_customer;'''
    cur.execute(st1)
    rows=cur.fetchall()
    count=cur.rowcount
    if count==0:
        accno=1001  #first account no is 1001
    else:
        accno=rows[-1][0]+1   #last accno +1
    print('Your account no is               :',accno)
    name=input('Enter the name of account holder        :')
    address=input('Enter the address of account holder :')
    balance=float(input('Enter the amount to deposit    :'))
    date_now=datetime.datetime.now()
    from_date=datetime.datetime.date(date_now)
    st2='''insert into bank_customer(accno, name, address, balance,from_date)
values({},'{}','{}',{},'{}');'''.format(accno, name, address, balance, from_date)
    cur.execute(st2)
    con.commit()
    st3='''insert into transaction(accno, amount, trans_type, trans_date) values({},{},'{}','{}');'''.format(accno,balance,'D',from_date)
    cur.execute(st3)
    con.commit()
    print('Your account is successfully created')
def Display_account():
    '''Function to print the details for an account'''
    accno=int(input('Enter your account no get details :'))
    st1='''Select accno, name, address, balance, from_date, end_date from bank_customer where accno={};'''.format(accno)
    cur.execute(st1)
    rows=cur.fetchall()
    count=cur.rowcount
    if count!=0:
        row=rows[0]
        print("Your account details are")
        print("------------------------------")
        print('Account no           :',row[0])
        print('Name                    :',row[1])
        print('Address                 :',row[2])
        print('Account balancec :',row[3])
        print('The account was opened on :',row[4])
        if row[5] !=None:
            print('This account was cancelled on :',row[5])
    else:
        print('!!This account no does not exist')
def Deposit_withdraw(trans_type='D'):
    '''Function to deposit or withdrw an amount'''
    accno=int(input('Enter the account no :'))
    st3='''select accno, balance ,end_date from bank_customer where accno={};'''.format(accno)
    cur.execute(st3)
    rows=cur.fetchall()
    count=cur.rowcount
    if count!=0:
        row=rows[0]
        if trans_type=='D' and row[2]==None:
            amount=float(input('Enter the amount to deposit :'))
            balance=float(row[1])+amount  # previous balance + new amount
        elif trans_type=='W' and row[2]==None:
            amount=float(input('Enter the amount to withdraw :'))
            if float(row[1])-amount >1000:
                balance=float(row[1])-amount  # previous balance - new amount
            else:
                print('!! Insufficent amount so tansaction aborted')
                return
        else:
            print('!!This account is cancelled so no transaction')
            return
        date_now=datetime.datetime.now()
        trans_date=datetime.datetime.date(date_now)
        st1='''insert into transaction (accno, amount, trans_type, trans_date) values({},{},'{}','{}');'''.format(accno, amount, trans_type,trans_date)
        cur.execute(st1)
        con.commit()
        st2='''update bank_customer set balance={} where accno={};'''.format(balance, accno)
        cur.execute(st2)
        con.commit()
        print('Your transaction completed')
    else:
        print('!!The account not does not exist')
def Cancel_account():
    '''Function to cancel an account for the customer'''
    accno=int(input('Enter the account no '))
    st1='''select accno, end_date, balance from bank_customer where accno={};'''.format(accno)
    cur.execute(st1)
    rows=cur.fetchall()
    count=cur.rowcount
    if count==0:
        print('!!This account no does not exist')
    else:
        row=rows[0]
        if row[1]==None:
            ch=input('Do you really wish to cancel this account (y/n) :').upper()
            if ch =='N':
                print('!!Transaction cancelled  by user')
                return
            else:
                date_now=datetime.datetime.now()
                end_date=datetime.datetime.date(date_now)
                st2='''update bank_customer set end_date='{}', balance={} where accno={};'''.format(end_date,0,accno)
                cur.execute(st2)
                con.commit()
                st3='''insert into transaction (accno, amount, trans_type, trans_date) values({},{},'{}','{}');'''.format(accno, row[2], 'W',end_date)
                cur.execute(st3)
                con.commit()
                print('This account is now cancelled ')
        else:
            print('!!This account is already cancelled')
def report_deposit(trans_type):
    '''Function to display all deposits and withdrawls for a particular period'''
    from_date=input('Enter the start date in the format yyyy-mm-dd :')
    end_date=input('Enter the end date in the format   yyyy-mm-dd :')
    if trans_type=='D':
        transaction='Deposits'
    else:
        transaction='Withdrawls'
    report_head1='''
    All %s for the period of :%s   To %s'''%(transaction,from_date,end_date)
    print(report_head1)
    report_head2='''\
    --------------------------------------------------------------------
   %8s|%25s    |%10s     |%15s
    --------------------------------------------------------------------'''%('Accno','Name','Date','Amount')
    print(report_head2)
    st1='''Select accno, name, trans_date, amount, trans_type from bank_customer
natural join transaction where trans_date between '{}' and '{}' and trans_type ='{}';'''.format(from_date,end_date,trans_type)
    cur.execute(st1)
    rows=cur.fetchall()
    for row in rows:
        report_body='''\
    %8s|%25s|%10s|%15s  
    ---------------------------------------------------------------------'''%(str(row[0]),row[1],str(row[2]),str(row[3]))
        print(report_body)
def report_individual():
    '''Function to display all deposits and withdrawls for a particular Account'''
    accno=int(input('Enter the account no to display :'))
    report_head1='''
    All Deposits/ Withdrawls for the account of :%s'''%(str(accno))
    print(report_head1)
    report_head2='''\
    -------------------------------------------------------------------------------
   %8s|%25s    |%10s     |%10s|%15s
    -------------------------------------------------------------------------------'''%('Accno','Name','Date','Trans. Type','Amount')
    print(report_head2)
    st1='''Select accno, name, trans_date, amount, trans_type from bank_customer
natural join transaction where accno={};'''.format(accno)
    cur.execute(st1)
    rows=cur.fetchall()
    count=cur.rowcount
    for row in rows:
        report_body='''\
    %8s|%25s|%10s|%15s|%15s  
    --------------------------------------------------------------------------------'''%(str(row[0]),row[1],str(row[2]),row[4],str(row[3]))
        print(report_body)
    if count==0:
        print('!!This account no does not exist''')
def Reports():
    '''Function to show different reports  of account'''
    menu='''
         Report Of Accounts
    --------------------------------
     1. All deposits
     2. All withdrawls
     3. Individual account
     4. Return to main menu'''
    while True:
        print(menu)
        ch=int(input('Enter you choice of report :'))
        if ch==1:
            report_deposit('D')
        elif ch==2:
            report_deposit('W')
        elif ch==3:
            report_individual()
        elif ch==4:
            return
        else:
            print('!!Wrong choice entered by user')
  
                
def Transaction():
    '''Function to make tansaction on account'''
    menu='''
           Transaction Menu
        --------------------------
        1.  To deposit amount
        2.  To Withdraw amount
        3.  To cancel an account
        4.  To return to main menu'''
    while True:
        print(menu)
        ch=int(input('Enter your choice :'))
        if ch==1:
            Deposit_withdraw()
        elif ch==2:
            Deposit_withdraw('W')
        elif ch==3:
            Cancel_account()
        elif ch==4:
            return
    
#test connection
if con.is_connected:
    print('Connected to MySQL')
    #create a cursor object to execute DDL and DML commands
    cur=con.cursor()
    #Create a query string
    st1='''show tables;'''
    cur.execute(st1)
    rows=cur.fetchall()
    if ('bank_customer',) not in rows:
        st2='''create table bank_customer (accno int(10), name varchar(20), address varchar(50),balance decimal(15,3),
from_date date, end_date date);'''
        cur.execute(st2)
    if ('transaction',) not in rows:
        st3='''create table transaction (accno int(10), amount decimal(15,3), trans_type char(1),
trans_date date);'''
        cur.execute(st3)
    menu='''
          Banking Menu
        ---------------------
        1.Create account
        2.Display account
        3.Transaction
        4.Reports
        5.Exit the program'''
    while True:
        print(menu)
        ch=int(input('Enter the choice :'))
        if ch==1:
            Create_account()
        elif ch==2:
            Display_account()
        elif ch==3:
            Transaction()
        elif ch==4:
            Reports()
        elif ch==5:
            break
    con.close()
else:
    print('Not connected to MySQL')

