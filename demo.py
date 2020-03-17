# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 18:29:26 2020

@author: keerthika02.TRN

"""
from manager import Manager
from situation import Situation
from collections import defaultdict
from enum_p import  Status,Feelings,ProjectExpand,ProjectType
from service import Service
from flask import Flask, render_template,jsonify,request
import game
import copy
import time
import random


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/level')
def level():
    return render_template('level.html')

@app.route('/level/level1')
def level1():
    return render_template('Levels/Level1.html')
@app.route('/level/level2')
def level2():
    return render_template('Levels/Level2.html')
@app.route('/level/level3')
def level3():
    return render_template('Levels/Level3.html')
@app.route('/level/level4')
def level4():
    return render_template('Levels/Level4.html')
@app.route('/level/level5')
def level5():
    return render_template('Levels/Level5.html')
@app.route('/level/level6')
def level6():
    return render_template('Levels/Level6.html')
@app.route('/level/level7')
def level7():
    return render_template('Levels/Level7.html')
@app.route('/level/level8')
def level8():
    return render_template('Levels/Level8.html')
@app.route('/level/level9')
def level9():
    return render_template('Levels/Level9.html')
@app.route('/level/level10')
def level10():
    return render_template('Levels/Level10.html')
@app.route('/level/level1/Employees')
def employees():
    return render_template('Levels/Employees.html')


manager=Manager(5)
client_level1=None
team_size=3
list_emp=[]
ser=Service()
otherdict=defaultdict(int)
otherdict['Hardware']=1
otherdict['Software']=1
otherdict['Employee']=1


######### Level 1,Level 2,Level 3, Level 4 ############################

@app.route("/level/getProjectSkills")
def getProjectTypeDetails():
    d_l=[]
    for i in ProjectType:
         d_list=dict()
         d_list["name"]=ProjectExpand[i.name].value
         d_list['skills']=list(i.value)
         d_l.append(d_list)
    print(d_l)
    return jsonify(d_l)
        

######## Level 1,Level 2,Level 3,Level 4, Level 5 #########################

#@app.route("/getEmployee/<e_id>")
#def output(e_id):
 #   emp=game.getEmployee(e_id)
  #  return emp.__dict__
  
@app.route("/level/getEmployee")
def output():
    list_Employee=[]
    for i in game.list_employee:
        list_Employee.append(i.__dict__)
    return jsonify(list_Employee)


       

######## Level 1,Level 2,Level 3 #########################

@app.route("/level/level1-4/getClient")
def getClient():
    c=Situation.getSituation()
    #print(c.getDetails())
    global otherdict
    otherdict[c.projectExp]=1
    otherdict['deadline']=c.project.duration
    otherdict['cost']=c._Client__cost
    otherdict['c_patientLevel']=c._Client__patient_level
    otherdict['estimated_days_to_complete']=c.project.duration-8
    otherdict['project_deadline']=c.project.duration-12
    manager.addProject(c)
    for i in c.project.project_type.value:
        otherdict[i]=1
    
    global client_level1
    client_level1=c
    dict_client={}
    dict_client['Project_Type']=ProjectExpand[c.projectExp].value
    dict_client['deadline']=c.project.duration
    dict_client['cost']=c._Client__cost
    dict_client['patient_level']=c._Client__patient_level
    return dict_client



######## Level 1,Level 2,Level 3,Level 4,Level 5,Level 6 #########################

@app.route("/level/allocation",methods=['POST'])
def allocation():
    emp_list=request.json["emp_list"]
    global client_level1,otherdict
    
    #setting the Team size
    if(len(emp_list)!=0):
        client_level1.project.teamSize=len(emp_list)
        otherdict['team_size']=len(emp_list)
        
        #Allocating the each employee in the list to project
        
        for i in emp_list:
            if not  game.Allocation(i['e_id'],client_level1.project.project_id):
                return "Some Problem"
            project=copy.copy(manager.findProject(client_level1.project.project_id))
            project.allocate(i['e_id'])
    
    return "allocated"


######## Level 1,Level 2,Level 3, Level 4,Level 5,Level 6 #########################
    
@app.route("/level/updateStatus/InProgress")
def change_P():
    project=copy.copy(client_level1.project)
    
    global otherdict
    for i in project.employees_allocated:
        emp1=game.getEmployee(i)
        for j in emp1.skills:
            if otherdict["E_"+j]==0:
                otherdict["E_"+j]=1   
    #time.sleep(15)
    project.updateStatus(Status.inProgress)
    manager.updateProjectStatus(client_level1.project.project_id,Status.inProgress)
    print(otherdict)
    return "InProgress"

######## Level 2,Level 3 #########################
    
@app.route("/level/updateStatus/Completed")
def change_C_2():
    project=copy.copy(client_level1.project)
    #time.sleep(30)
    project.updateStatus(Status.completed)
    print(project.status)
    client_level1.changeFeelings(Feelings.happy)
    for i in project.employees_allocated:
        emp1=copy.copy(game.getEmployee(i))
        emp1.projectCompleted()
    set_keys=['web','app','VR','deadline','cost','c_patientLevel','html','css','bootstrap','kotlin','java','c#','A-Frame','Babylon','estimated_days_to_complete','team_size','E_bootstrap','E_html','E_css','E_kotlin','E_java','E_A-Frame','E_Babylon','E_c#','leaves','project_deadline','Hardware','Software','Employee']
    list_ser=[]
    for i in set_keys:
        list_ser.append(otherdict[i])
    result=ser.getResult(list_ser)
    print(result)
    return "Completed"

########  Level 1 ,Level 5, Level 6 ###################
    
#/level1-4/getClient - to get Client Information
#/level/allocation/<e_id> - to allocate the employee with e_id
#/level/updateStatus/InProgress 
#/level1/updateStatus/Completed
        
@app.route("/level/level1/updateStatus/Completed")
def change_C():
    project=copy.copy(client_level1.project)
    time.sleep(30)
    project.updateStatus(Status.completed)
    for i in project.employees_allocated:
        copy.copy(game.getEmployee(i)).changeFeelings(Feelings.happy)
    manager.changeFeelings(Feelings.happy)
    client_level1.changeFeelings(Feelings.happy)
    for i in project.employees_allocated:
        emp1=copy.copy(game.getEmployee(i))
        emp1.projectCompleted()
    set_keys=['web','app','VR','deadline','cost','c_patientLevel','html','css','bootstrap','kotlin','java','c#','A-Frame','Babylon','estimated_days_to_complete','team_size','E_bootstrap','E_html','E_css','E_kotlin','E_java','E_A-Frame','E_Babylon','E_c#','leaves','project_deadline','Hardware','Software','Employee']
              

    list_ser=[]
    #print(type(set_keys))
    
    for i in set_keys:
        list_ser.append(otherdict[i])
    
    result=ser.getResult(list_ser)
    print(result)
        
    return "Completed"

##############  Level 2  #################################
    
############# Eco-System - Personal#######################
    
#/level1-4/getClient - to get Client Information
#/level/allocation/<e_id> - to allocate the employee with e_id
#/level/updateStatus/InProgress 
#/level2/Eco-System/Personal
#/level2/Eco_System/Personal/requestProcess - POST method - get the list of accepted 
#/level/updateStatus/Completed

    
@app.route("/level/level2/Eco-System/Personal")
def Personal_EcoSystem():
    project=copy.copy(client_level1.project)
    global list_emp
    list_emp=[]
    while(len(list_emp)==0):
        for emp in project.employees_allocated:
            r=random.randint(1,200)
            reason_for_leaves={}
            if(r%2==0 or r%5==0):
                reason_for_leaves['employee']=emp
                reason_for_leaves['reason']="---------"
                list_emp.append(reason_for_leaves)
    
    otherdict['leaves']=1
    return jsonify(list_emp)
            
@app.route("/level/level2/Eco_System/Personal/requestProcess",methods=['POST'])
def personal_request():
    global otherdict
    list_a=request.json['list_accept']
    if len(list_a) == len(client_level1.project.employees_allocated):
        for emp in client_level1.project.employees_allocated :
            game.changeEmployee_Feeling(emp,Feelings.happy)
        return "all the Employees were granted with a leaves so project deadline will be crossed.So it tends to failure"
    #some peoples applied for leave no one granted with leave
    #list_emp -list of employees applied for leave
    #list_a -list of employeed=s granted with leave
    if len(list_a)==0 and len(list_emp)!=0:
        otherdict['leaves']=0
        for i in list_a:
            game.changeEmployee_Feeling(emp,Feelings.sad)
        return "all the employees feelings changed to sad who were applied for leave"
    
    for i in client_level1.project.employees_allocated:
        if i not in list_a:
            game.changeEmployee_Feeling(emp,Feelings.sad)
        else:
            game.changeEmployee_Feeling(emp,Feelings.happy)
    return "if some employees were leave so that work load falls on other team member so other feelings changed to sad"
    
    
############ Level 3 ##########################
    
############ weather ##########################
    
#/level1-4/getClient - to get Client Information
#/level/allocation/<e_id> - to allocate the employee with e_id
#/level/updateStatus/InProgress
#/level3/Eco_System/weather - return the list of options
#/level3/Eco_System/weather/action/<option> - option - option choosen by the user
#/level/updateStatus/Completed

@app.route('/level/level3/Eco_System/weather')
def weather_change():
    list_option=["Work from Home",
                 "declared Leave",
                 "come to office"]
    return jsonify(list_option)

@app.route('/level/level3/Eco_System/weather/action/<option>')
def weather_change_action(option):
    d_msg={}
    if option=="Work from Home":
        for i in client_level1.project.employees_allocated:
            game.changeEmployee_Feeling(i,Feelings.ok)
        d_msg['Status']="Completed"
        d_msg['Message']="It is a good decision eventhough the employees were not happy but they are ok with the situation"
    elif option=="declared Leave":
        for i in client_level1.project.employees_allocated:
            game.changeEmployee_Feeling(i,Feelings.happy)
        client_level1.changeFeelings(Feelings.sad)
        d_msg['Status']="InComplete"
        d_msg['Message']="Failed Because eventhough the employee was happy.The client were not Happy because all the Employees were granted with a leaves so project deadline will be crossed.So it tends to failure"
    elif option=="come to office":
        for i in client_level1.project.employees_allocated:
            game.changeEmployee_Feeling(i,Feelings.sad)
        client_level1.changeFeelings(Feelings.happy)
        d_msg['Status']="Completed"
        d_msg['Message']= "Partial Success Because All the Employees were not Happy with the Decision"
    
    return d_msg

################################# Level 4 ##############################################
    
################################ Holiday ##############################################

#/level1-4/getClient - to get Client Information
#/level/allocation/<e_id> - to allocate the employee with e_id
#/level/updateStatus/InProgress
#/level4/Eco_System/Holidays/action 
#/level/updateStatus/Completed

list_Reasons=[
              'Every year we celebrate this festival in grand manner.',
              'This year we are planning to celebrate this festival in grand manner.',
              'I need leave Because for last few years we didn’t celebrate this festival So this year we are planning to celebrate this festival in our home town.',
              'Every year I celebrate this festival with my family and friends.',
              'My sister is getting married on next day.',
              'My brother is getting married on next day.',
              'My sister Engagement falls on next day.',
              'My Brother Engagement falls on next day.',
              'first time we are planned to celebrate this festival.',
              'Every year we celebrate this festival in our home town',
              'I am only child to my parents So I would like to be with my parent on that day',
              'I want to see cricket watch that will be telecasted on that day.',
              'I need leave because all my family and friends will have a small get-together on next day of the festival.'
             ]
@app.route("/level/level2/Eco-System/Holiday")
def Holiday_EcoSystem():
    project=copy.copy(client_level1.project)
    global list_emp
    list_emp=[]
    while(len(list_emp)==0):
        for emp in project.employees_allocated:
            r=random.randint(1,200)
            reason_for_leaves={}
            if(r%2==0 or r%5==0):
                reason_for_leaves['employee']=emp
                reason_for_leaves['reason']=list_Reasons[random.randint(0,12)]
                list_emp.append(reason_for_leaves)
    
    otherdict['leaves']=1
    return jsonify(list_emp)

@app.route('/level/level4/Eco_System/Holidays/action',methods=['POST'])
def Holidays_Action():
    list_a=request.json['list_accept']
    d_msg={}
    if(len(list_a)==len(list_emp)):
        for emp in list_emp :
            game.changeEmployee_Feeling(emp,Feelings.happy)
        d_msg['Status']="InComplete"
        d_msg['Message']= "all the Employees were granted with a leaves so project deadline will be crossed.So it tends to failure"
    elif(len(list_a)==0):
        otherdict['leaves']=0
        for i in list_a:
            game.changeEmployee_Feeling(i,Feelings.sad)
        d_msg['Status']="Completed"
        d_msg['Message']= "all the employees feelings changed to sad who were applied for leave"
    elif len(list_a)<len(list_emp):
        for i in client_level1.project.employees_allocated:
            if i not in list_a:
                game.changeEmployee_Feeling(emp,Feelings.sad)
            else:
                game.changeEmployee_Feeling(emp,Feelings.happy)
        d_msg['Status']="Completed"
        d_msg['Message']="if some employees were leave so that work load falls on other team member so other feelings changed to sad"
    return d_msg
        


################################# Level 5  #################################################
            
################# Selecting the Skills required manually by user(Manager) ##################
            
        
#/level5/getClient - to get Client Information
#/level5/getSkills - to get a list of skills
#/level5/setSkills - to set a list of value selected by user(Manager)
#/level/checkSkills
#/level/allocation/<e_id> - to allocate the employee with e_id
#/level/updateStatus/InProgress 
#/level1/updateStatus/Completed
            
@app.route('/level/checkSkills',methods=['POST'])
def check_Skills():
    list_selected_skills=request.json['Selected']
    for i in client_level1.project.project_type.value:
        if i not in list_selected_skills:
            return "Select the required skills to continue the game"
    return "OK"
        
        
@app.route('/level/level5/getClient')
def getClient_():
    c=Situation.getSituation()
    otherdict[c.projectExp]=1
    otherdict['deadline']=c.project.duration
    otherdict['cost']=c._Client__cost
    otherdict['c_patientLevel']=c._Client__patient_level
    otherdict['estimated_days_to_complete']=c.project.duration-8
    otherdict['project_deadline']=c.project.duration-12
    manager.addProject(c)
    global client_level1
    client_level1=c
    dict_client={}
    dict_client['Project_Type']=ProjectExpand[c.projectExp].value
    dict_client['deadline']=c.project.duration
    dict_client['cost']=c._Client__cost
    dict_client['patient_level']=c._Client__patient_level
    return dict_client


@app.route('/level/level5/getSkills')
def getSkills():
    list_of_Skills=[]
    for i in ProjectType:
        list_of_Skills.extend(list(i.value))
    return jsonify(list_of_Skills)
        

@app.route('/level/level5/setSkills',methods=['POST'])
def setSkills():
    list_skills=request.json["list_skills"]
    for i in list_skills:
        otherdict[i]=1
    return "setted"
    
####################################### Level 6 ################################################## 

########## Selecting the Skills required manually by user(Manager) and Team Size #################

      
#/level5/getClient - to get Client Information
#/level5/getSkills - to get a list of skills
#/level5/setSkills - to set a list of value selected by user(Manager)
#/getTeamSize/<size> - to set the teamSize 
#/level6/allocation - to allocate the list of employee to project
#/level/updateStatus/InProgress 
#/level1/updateStatus/Completed


@app.route("/level/getTeamSize/<size>")
def TeamSize(size):
    global client_level1
    global otherdict
    client_level1.project.team_size=int(size)
    print(size)
    print(client_level1.project.team_size)
    otherdict['team_size']=size
    return "setted"

@app.route("/level/level6/allocation",methods=['POST'])
def allocation_():
    emp_list=request.json["emp_list"]
    global client_level1
    
    #checking the Team Size
    print(client_level1.project.team_size)
    if len(emp_list) != client_level1.project.team_size:
        msg=((lambda : "your team size is not matching So remove some Employee" ,lambda : "your team size is not matching So add some Employee")[len(emp_list) < client_level1.project.team_size]())
        return msg 
    
    #Allocating the each employee in the list to project
    
    for i in emp_list:
        if not  game.Allocation(i['e_id'],client_level1.project.project_id):
            return "Some Problem"
        project=copy.copy(manager.findProject(client_level1.project.project_id))
        project.allocate(i['e_id'])
    return "Allocated"

##################################### Level 7 #################################################

###### Eco System -personal - with replacement of persons and Discussion with Employee ########

#/level1-4/getClient - to get Client Information
#/level/allocation/ - to allocate the employee 
#/level/updateStatus/InProgress 
#/level2/Eco-System/Personal
#/level7/Eco_System/Personal/requestProcess - POST method - get the list of accepted 
#For Replace
    ##/level7/Eco_system/personal/requestProcess/Replace
    #           -return a list of Employee who not allocated to any project
    #           -return a msg as "Employees not Available" when there is no Employee 
    ##/level7/Eco_system/personal/requestProcess/Replace/Process
    #           - accept a list of employees Selected for replacement

#For Discussion 
    ##/level7/Eco_system/personal/requestProcess/Discussion
    #           - return a list of Employee who applied for leaves  with reason for there leave
    ##/level7/Eco_system/personal/requestProcess/Discussion/Result
    
#/level/updateStatus/Completed

replace_Employee=[]
@app.route("/level/level7/Eco_System/Personal/requestProcess",methods=['POST'])
def personal_request_():
    global otherdict
    Eco_Msg={}
    list_a=request.json['list_accept']
    if len(list_a) == len(client_level1.project.employees_allocated):
        #for emp in client_level1.project.employees_allocated :
        #   game.changeEmployee_Feeling(emp,Feelings.happy)
        
        Eco_Msg['status']=''
        Eco_Msg['msg']=""
        Eco_Msg['option']=['Discussion','cancel']
    #some peoples applied for leave no one granted with leave
    #list_emp -list of employees applied for leave
    #list_a -list of employeed=s granted with leave
    if len(list_a)==0 and len(list_emp)!=0:
        otherdict['leaves']=0
        for i in list_emp:
            game.changeEmployee_Feeling(i,Feelings.sad)
        Eco_Msg['status']="Completed"
        Eco_Msg['msg']="all the employees feelings changed to sad who were applied for leave"
        Eco_Msg['option']=[]
    
    else:
        for i in client_level1.project.employees_allocated:
            if i in list_a:
                game.changeEmployee_Feeling(i,Feelings.happy)
        global replace_Employee
        replace_Employee=list_a    
        Eco_Msg['status']=""
        Eco_Msg['msg']=""
        Eco_Msg['option']=['Replace','Cancel']
    return Eco_Msg    

@app.route("/level/level7/Eco_system/personal/requestProcess/Discussion",methods=['POST'])
def Personal_Discussion():
    option=request.json['option']
    Eco_Msg={}
    if(option=='cancel'):
        for emp in client_level1.project.employees_allocated :
            game.changeEmployee_Feeling(emp,Feelings.happy)
        Eco_Msg['status']='InComplete'
        Eco_Msg['msg']="all the Employees were granted with a leaves so project deadline will be crossed.So it tends to failure"
        Eco_Msg['list_emp']=[]
    else :
        list_Reasons=[
                      'Family Trip',
                      'Medical emergency',
                      'Relatives Marriage Function',
                      'family function',
                      'Festival celebration',
                      'going to native',
                      'Friends get-together',
                      'Friends Brithday party',
                      'My sister Engagement',
                      "My brother's Engagement ",
                      "My sister is getting married",
                      "My brother is getting married"
                      ]
        global list_emp
        for i in list_emp:
            i['reason']=list_Reasons[random.randint(0,11)]
        Eco_Msg['status']=''
        Eco_Msg['msg']=""
        Eco_Msg['list_emp']=list_emp
    return Eco_Msg
   
@app.route("/level/level7/Eco_system/personal/requestProcess/Discussion/Result",methods=['POST'])
def Personal_Discussion_Process():
    list_a=request.json['list_accept']
    Eco_Msg={}
    if len(list_a)== len(list_emp):
        for emp in client_level1.project.employees_allocated :
            game.changeEmployee_Feeling(emp,Feelings.happy)
        Eco_Msg['status']='InComplete'
        Eco_Msg['msg']="all the Employees were granted with a leaves so project deadline will be crossed.So it tends to failure"
    elif(len(list_a))==0:
        for emp in client_level1.project.employees_allocated :
            game.changeEmployee_Feeling(emp,Feelings.sad)
        Eco_Msg['status']='Completed'
        Eco_Msg['msg']="all the employees feelings changed to sad"    
    else:
        for i in client_level1.project.employees_allocated:
            if i in list_a:
                game.changeEmployee_Feeling(i,Feelings.happy)
            else:
                game.changeEmployee_Feeling(i,Feelings.sad)
        Eco_Msg['status']="Complete"
        Eco_Msg['msg']="if some employees were leave so that work load falls on other team member so other feelings changed to sad"
    return Eco_Msg

@app.route("/level/level7/Eco_system/personal/requestProcess/Replace",methods=['POST'])
def Personal_Replace():
    option=request.json['option']
    Eco_Msg={}
    list_employee=game.employee_not_Allocated()
    if option == "cancel" or  len(list_employee) == 0:
        for i in client_level1.project.employees_allocated:
            if i not in replace_Employee:
                game.changeEmployee_Feeling(i,Feelings.sad)
        Eco_Msg['status']="Complete"
        Eco_Msg['msg']="if some employees were leave so that work load falls on other team member so other feelings changed to sad"
        Eco_Msg['reason']=((lambda : "Employees not Available not available for Replacement",lambda : "")[option=="cancel"]())
        Eco_Msg['Employee']=[]
    else:
        Eco_Msg['status']=""
        Eco_Msg['msg']=""
        Eco_Msg['reason']=""
        Eco_Msg['Employee']=list_employee
        
    return Eco_Msg

@app.route("/level/level7/Eco_system/personal/requestProcess/Replace/Process",methods=['POST'])
def Personal_Replace_():
    list_allocated=request.json['Selected']
    global client_level1
    for i in replace_Employee:
        game.De_allocation(i)
        #client_level1.project.de_allocate(i)
    
    #print(client_level1.project.employees_allocated)
    for i in list_allocated:
        if not  game.Allocation(i['e_id'],client_level1.project.project_id):
            return "Some Problem"
        project=copy.copy(client_level1.project)
        project.allocate(i['e_id'])
    #print(client_level1.project.employees_allocated)
    return "Allocation Process Completed"

        
############################# Level 8 #########################################

############ Discussion with Replacement ######################################
    
#/level1-4/getClient - to get Client Information
#/level/allocation/ - to allocate the employee with e_id
#/level/updateStatus/InProgress 
#/level2/Eco-System/Personal
#/level7/Eco_System/Personal/requestProcess - POST method - get the list of accepted 
#For Discussion 
    ##/level7/Eco_system/personal/requestProcess/Discussion
    #           - return a list of Employee who applied for leaves  with reason for there leave
    ##/level7/Eco_system/personal/requestProcess/Discussion/Result
                ####/level7/Eco_system/personal/requestProcess/Replace
                #           -return a list of Employee who not allocated to any project
                #           -return a msg as "Employees not Available" when there is no Employee 
                ##/level8/Eco_system/personal/requestProcess/Replace/Process
                #           - accept a list of employees Selected for replacement

    
#/level/updateStatus/Completed

@app.route("/level/level8/Eco_system/personal/requestProcess/Discussion/Result",methods=['POST'])
def Personal_Discussion_Process_():
    list_a=request.json['list_accept']
    Eco_Msg={}
    if len(list_a)== len(list_emp):
        for emp in client_level1.project.employees_allocated :
            game.changeEmployee_Feeling(emp,Feelings.happy)
        Eco_Msg['status']='InComplete'
        Eco_Msg['msg']="all the Employees were granted with a leaves so project deadline will be crossed.So it tends to failure"
        Eco_Msg=[]
    elif(len(list_a))==0:
        for emp in client_level1.project.employees_allocated :
            game.changeEmployee_Feeling(emp,Feelings.sad)
        Eco_Msg['status']='Completed'
        Eco_Msg['msg']="all the employees feelings changed to sad"  
        Eco_Msg=[]
    else:
        for i in client_level1.project.employees_allocated:
            if i in list_a:
                game.changeEmployee_Feeling(i,Feelings.happy)
        global replace_Employee
        replace_Employee=list_a    
        Eco_Msg={}
        Eco_Msg['status']=''
        Eco_Msg['msg']=""
        Eco_Msg['option']=['Replace','Cancel']
    return Eco_Msg    
    

################################ Level 9 ########################################
    
########### Selecting the skills and team size along with replacement ########### 

#/level5/getClient - to get Client Information
#/level5/getSkills - to get a list of skills
#/level5/setSkills - to set a list of value selected by user(Manager)
#/getTeamSize/<size> - to set the teamSize 
#/level/allocation/ - to allocate the employee with e_id
#/level/updateStatus/InProgress 
#/level2/Eco-System/Personal
#/level7/Eco_System/Personal/requestProcess - POST method - get the list of accepted 
#For Replace
    ##/level7/Eco_system/personal/requestProcess/Replace
    #           -return a list of Employee who not allocated to any project
    #           -return a msg as "Employees not Available" when there is no Employee 
    ##/level7/Eco_system/personal/requestProcess/Replace/Process
    #           - accept a list of employees Selected for replacement

#For Discussion 
    ##/level7/Eco_system/personal/requestProcess/Discussion
    #           - return a list of Employee who applied for leaves  with reason for there leave
    ##/level7/Eco_system/personal/requestProcess/Discussion/Result
    
#/level/updateStatus/Completed





################################ Level 10 #######################################
        
############ Selecting the skills and team size along with replacement ##########

#/level5/getClient - to get Client Information
#/level5/getSkills - to get a list of skills
#/level5/setSkills - to set a list of value selected by user(Manager)
#/getTeamSize/<size> - to set the teamSize 
#/level/allocation/ - to allocate the employee with e_id
#/level/updateStatus/InProgress 
#/level2/Eco-System/Personal
#/level7/Eco_System/Personal/requestProcess - POST method - get the list of accepted 
#For Discussion 
    ##/level7/Eco_system/personal/requestProcess/Discussion
    #           - return a list of Employee who applied for leaves  with reason for there leave
    ##/level7/Eco_system/personal/requestProcess/Discussion/Result
                ####/level7/Eco_system/personal/requestProcess/Replace
                #           -return a list of Employee who not allocated to any project
                #           -return a msg as "Employees not Available" when there is no Employee 
                ##/level8/Eco_system/personal/requestProcess/Replace/Process
                #           - accept a list of employees Selected for replacement

        



if __name__ == '__main__':
    app.run(port='1000')
