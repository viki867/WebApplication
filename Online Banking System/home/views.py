from django.shortcuts import render
import mysql.connector
from datetime import datetime
from django.http import HttpResponse
username = ''
email =''
def database():
    mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
    mycur = mydb.cursor()
    return mydb , mycur
def home(request):
    return render(request,'home.html',{})
def ad(request):
    return render(request,'admin.html',{})
def user(request):
    if request.method=="POST":
        global username
        global email
        email=request.POST['mail']
        z=request.POST['pwd'] 
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
        mycursor=mydb.cursor()
        sql = "select mail, pwd from reg where mail = %s and pwd=%s" 
        val=(email,z)
        mycursor.execute(sql,val)
        
        res= mycursor.fetchall()
        print(email)
        print(res)
        if len(res)!=0:
            if res[0][0]==email and res[0][1]==z:
                return render(request,'use/oguser.html',{})
        else:
            return render(request,'use/user.html',{"result":"fail"})
    else:
        return render(request,'use/user.html',{})

def userreg(request):

    if request.method=='POST':
        
        global username
        global email
        a=request.POST['name1']
        b=request.POST['add']
        c=request.POST['cit'] 
        d=request.POST['brn']
        e=request.POST['zip']
        f=request.POST['un']
        g=request.POST['pwd']
        h=request.POST['cpwd']
        i=request.POST['phno']
        j=request.POST['mail']
        k=request.POST['acctype']
        l=request.POST['accno']
        m=request.POST['ifscno']       
        n=request.POST['amt'] 
        email = j
        if g==h:
            mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
            mycursor=mydb.cursor()
            sql="insert into reg(name,address,city,branch,zip,un,pwd,phno,mail,acctype,accno,ifsc,amount) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(a,b,c,d,e,f,g,i,j,k,l,m,n)
            mycursor.execute(sql,values)
            mydb.commit()
            return render(request,'use/oguser.html',{'status':"success"})
        else: 
            return render(request,'use/userreg.html',{"status":"fail"})
    else:
        return render(request,'use/userreg.html',{})

def withdrawamount(amount,an):
    mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
    mycursor=mydb.cursor()
    sql="update reg set  amount=%s where accno=%s"
    val=(amount,an)
    mycursor.execute(sql,val)
    mydb.commit()

def withdraw(request):
    if request.method=='POST':
        a=request.POST['accno']
        b=int(request.POST['amt'])   
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
        mycursor=mydb.cursor()
        sql="select amount from reg where accno=%s "
        val=(a,)    
        mycursor.execute(sql,val)
        amount = mycursor.fetchone()
        amount =int(amount[0])
        amount-=b
        withdrawamount(amount,a)

        return render(request,'use/oguser.html',{'msg':'succesc vc s'})
    else:
        return render(request,'withdraw.html',{})
def depositamount(amount,an):
    mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
    mycursor=mydb.cursor()
    sql="update reg set  amount=%s where accno=%s"
    val=(amount,an)
    mycursor.execute(sql,val)
    mydb.commit()

def deposit(request):
    if request.method=='POST':
        a=request.POST['accno']
        b=int(request.POST['amt'])   
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
        mycursor=mydb.cursor()
        sql="select amount from reg where accno=%s "
        val=(a,)    
        mycursor.execute(sql,val)
        amount = mycursor.fetchone()
        amount =int(amount[0])
        amount+=b
        depositamount(amount,a)

        return render(request,'use/oguser.html',{'msg':'success'})
    else:
        return render(request,'deposit.html',{})
    
def transfer(request):
    return render(request,'use/oguser.html',{})

def detail(request):
    if request.method == "GET":

        if email != None:
            mydb , mycur = database()
            mycur.execute("SELECT name,address,city,branch,zip,un,phno,mail,acctype,accno,ifsc,amount FROM reg WHERE mail = %s", (email,))
            data = mycur.fetchall()
            print(data)
        return render(request,'udetail.html',{'result':data})

    else:
        return render(request,'udetail.html',{})




def admin(request):

    if request.method=="POST":
        global username
        username=request.POST['un']
        z=request.POST['pwd'] 
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
        mycursor=mydb.cursor()
        sql = "select un, pwd from adreg where un = %s and pwd=%s" 
        val=(username,z)
        mycursor.execute(sql,val)
        
        res= mycursor.fetchall()
        print(res)
        if len(res)!=0:
            if res[0][0]==username and res[0][1]==z:
                return render(request,'admin.html',{})
        else:
            return render(request,'adlogin.html',{"result":"fail"})
    else:
        return render(request,'adlogin.html',{})
def adreg(request):
    if request.method=='POST':
        a=request.POST['adun']
        b=request.POST['admail']
        c=request.POST['pwd']
        d=request.POST['cpwd'] 
        print("hlo")
    
        if c==d:
            print("hlo")
            mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
            mycursor=mydb.cursor()
            sql="insert into adreg(un,email,pwd) values(%s,%s,%s)"
            values=(a,b,c)
            mycursor.execute(sql,values)
            mydb.commit()
            return render(request,"adreg.html",{'status':"success"})
        else: 
            return render(request,"adreg.html",{"status":"fail"})
    else:
        print("k")
        return render(request,"adreg.html",{})

def bankdetail(request):
   
    if request.method == "GET":

         
        mydb , mycur = database()
        mycur.execute("SELECT name,address,city,phno,mail,acctype,accno,ifsc,amount FROM reg")
        data = mycur.fetchall()
        print(data)
        return render(request,'bd.html',{'result':data})

    else:
        return render(request,'bd.html',{})

def remove(request):
    if request.method == "POST":
        acno = request.POST['acno']
        mydb, mycur = database()
        mycur.execute("DELETE FROM reg WHERE accno = %s", (acno,))
        mydb.commit()
        return render(request,"admin.html",{})
    else:
        return render(request,"remove.html",{})
    

    
    
def contact(request):
    return render(request,'contact.html',{})
def logout(request):
    return render(request,'home.html',{})


def checkPayment(acno):
    mycon , mycur  = database()
    sql = "select amount from reg where accno = %s"
    val =(acno,)

    mycur.execute(sql,val)
    payment = mycur.fetchall()
    if  payment:
        return int(payment[0][0])
    else:
        return 0

def paymentUpdate(payment ,  acno):
    mycon , mycur  = database()
    sql = "update reg set amount = %s where accno = %s"
    val=(payment , acno)
    mycur.execute(sql,val)
    mycon.commit()
    if mycur.rowcount:
        return True
    else:
        return False
    
def insertTransaction(fromac , toac ,payment,date):
    mycon , mycur  = database()
    sql = "insert into  transactionsdetails (FromAccountNumber ,ToAccountNumber ,TransferPayment ,Date) values(%s,%s,%s,%s)"
    val=(fromac,toac , payment ,date)
    mycur.execute(sql,val)
    mycon.commit()
    if mycur.rowcount:
        return True
    else:
        return False

def findUser():
    mycon , mycur  = database()
    sql = "select accno from reg where mail = %s"
    print(email)
    val=(email , )
    mycur.execute(sql,val)
    acc= mycur.fetchall()
    print(acc)
    return acc[0][0]

def DownloadTransaction():
    mycon , mycur  = database()
    account = findUser()
    sql = "select * from transactionsdetails where  fromaccountnumber = %s"
    val=  (account,)
    mycur.execute(sql,val)
    transaction = mycur.fetchall()
    if  transaction:
        return transaction 
    else:
        return 0



def transfer(request):
    if request.method=="POST":
        current_date = datetime.now()

        date = current_date.strftime("%d/%m/%Y")
        ya = request.POST["from-account"]
        ta = request.POST["to-account"]
        payment =int( request.POST["amount"])
        account = findUser()
        pay1 = checkPayment(ya)
        pay2 = checkPayment(ta)
        if pay1 and pay2 and (ya==account):
                
            if payment<=pay1:
                your_payment = pay1 - payment
                transfer_payment = pay2 + payment
                if (paymentUpdate(your_payment ,  ya) and paymentUpdate(transfer_payment , ta) and insertTransaction(ya , ta, payment , date)):
                    return render(request,'use/oguser.html',{'status':1})
                else:
                    return render(request,'transfer.html',{'status':0})
            else:
                return render(request,'transfer.html',{'result':-1})
        else:
            return render(request,'transfer.html',{'result':404})

    else:
        return render(request,'transfer.html',{})
    

def viewTransaction(request):
    print(email)
    if request.method=="GET":
       
        
        data = DownloadTransaction()
        if data:
            return render(request,'ViewTransactions.html',{'result':data})
        else:
            return render(request,'ViewTransactions.html',{'result':0})

    else:
        return render(request,'ViewTransactions.html',{})
    

def download(request):
    content="Transaction ID ,From Account NO, To Account NO, Transfer Amount, Date\n"
    datas = DownloadTransaction()
    print(datas)
    for data in datas:
        content += str(data[0]) + "," + str(data[1]) + "," + str(data[2])+ ","+str(data[3]) + "," + str(data[4]) +"\n"
    
    response = HttpResponse(content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transaction.csv"'

    return response


