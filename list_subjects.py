from mimetypes import knownfiles
from nicegui import ui, app
import pandas as pd
from pymongo import MongoClient
import csv
import numpy 
ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">')
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["woxsen"]
    # else:
    #     ui.notify('No rows selected.')
li1,li2,li3,li4={},{},{},{}
final_list_cat=[]
final_list_code=[]
final_list_name=[]
final_list_credits=[]
final_list_rows=[]
l =[]
total_credits=''
total_code=''
total_name=''
df1not= pd.DataFrame()
def get_data():
    with ui.stepper().props('vertical header-nav').classes('w-full') as stepper_sub:
        final_cat_col = mydb['final_cat']
        res_final_cat = final_cat_col.find({},{"_id":0})
        l = []
        x = 0
        y=0
        cnt = final_cat_col.count_documents({})
        for i in res_final_cat:
            print(i)
            # data7 = pd.DataFrame(data={'sub_name': ['A', 'B'], 'sub_code': [1, 2]})
            data7 = pd.read_csv("subject_list.csv", encoding="ISO-8859-1")
            
            # data8 = pd.read_csv("subject_list_cat.csv", encoding="ISO-8859-1")
            # data8.drop(['Category'],axis=1)
            data7.drop_duplicates()
            # data8.drop_duplicates()
            # data9 = pd.concat([data7,data8])
            # data9.drop_duplicates(keep=False)
            # test = data9.to_dict('records')

            rows_avail_7 = data7.to_dict('records')

            rows_avail_8 = []
            rows_avail_9 =[]
            columns7 = [
                        {'name': 'sub_name', 'label': 'Sub_Name','field': 'sub_name', 'align': 'left', 'sortable': True,'checkboxSelection': True},
                        {'name': 'sub_code', 'label': 'Sub_Code','field': 'sub_code', 'align': 'left', 'sortable': True,'checkboxSelection': True},
                        {'name': 'sub_credits', 'label': 'Sub_Credits','field': 'sub_credits', 'align': 'left', 'sortable': True,'checkboxSelection': True},
            ]
            columns8 = [
            {'name': 'sub_name', 'label': 'Sub_Name','field': 'sub_name', 'align': 'left', 'sortable': True,'checkboxSelection': True},
            {'name': 'sub_code', 'label': 'Sub_Code','field': 'sub_code', 'align': 'left', 'sortable': True,'checkboxSelection': True},
            {'name': 'sub_credits', 'label': 'Sub_Credits','field': 'sub_credits', 'align': 'left', 'sortable': True,'checkboxSelection': True},
            ]
            columns9 = [
            {'name': 'sub_cat', 'label': 'Category','field': 'sub_cat', 'align': 'left', 'sortable': True},
            {'name': 'sub_name', 'label': 'Sub_Name','field': 'sub_name', 'align': 'left', 'sortable': True},
            {'name': 'sub_code', 'label': 'Sub_Code','field': 'sub_code', 'align': 'left', 'sortable': True},
            {'name': 'sub_credits', 'label': 'Sub_Credits','field': 'sub_credits', 'align': 'left', 'sortable': True},
           ]
            with ui.step(i['CName']):
                cr = (int(i['CValue'])/100)*160
                ui.markdown("**Maximum available credits for this category is:** ")
                cr_text = ui.input(label='Credits',value=cr)
                li4[i['CName']]=cr_text
                with ui.grid(columns=3):
                    table10 = "table"+str(x+10)
                    table11 = "table"+str(x+11)
                    table12 = "table"+str(x+12)
                    with  ui.table(title='Available Subjects',columns=columns7,rows=rows_avail_7, row_key='sub_code', selection='single', pagination=8)as table10:
                        with table10.add_slot('top-right'):
                            with ui.input(placeholder='Search').props('type=search').bind_value(table10, 'filter').add_slot('append'):
                                ui.icon('search')
                        with table10.add_slot('bottom-row'):
                            with table10.row():
                                with table10.cell():
                                    ui.button(on_click=lambda: (
                                        table10.add_rows({'sub_code': sub_cod.value, 'sub_name': sub_nam.value, 'sub_credits': sub_cr.value}),
                                        sub_nam.set_value(None),
                                        sub_cod.set_value(None),
                                        sub_cr.set_value(None),
                                    ), icon='add').props('flat fab-mini')
                                with table10.cell():
                                    sub_nam = ui.input('Sub_Name')
                                with table10.cell():
                                    sub_cod = ui.input('Sub_Code')
                                with table10.cell():
                                    sub_cr = ui.number('Sub_Credit')
                    with  ui.table(title='Selected. Subj.',columns=columns8, rows=rows_avail_8,  row_key='sub_code', selection='single', pagination=8) as table11:
                        with table11.add_slot('top-right'):
                            with ui.input(placeholder='Search').props('type=search').bind_value(table11, 'filter').add_slot('append'):
                                ui.icon('search')
                    table12 =  ui.table(title='Selected. Subj.',columns=columns9, rows=rows_avail_9,  row_key='sub_code',  pagination=8)
                    #ui.label()
                    li1[i['CName']]=table10
                    li2[i['CName']]=table11
                    li3[i['CName']]=table12
                    # li11={}
                    # li22={}
                    # li33=[]
                    #print(stepper_sub.value)
                    #print(li1)
                    def add_sub(i):
                        global final_list_rows
                        global final_list_cat
                        # global total_credits
                        # global total_code
                        # global total_name
                        rows7 = li1[i].selected
                        final_list_code.append(rows7[0]['sub_code'])
                        final_list_name.append(rows7[0]['sub_name'])
                        final_list_credits.append(rows7[0]['sub_credits'])
                        if rows7:
                            total_credits=rows7[0]['sub_credits']
                            total_code=rows7[0]['sub_code']
                            total_name=rows7[0]['sub_name']
                            
                            li2[i].add_rows({"sub_name":rows7[0]['sub_name'],"sub_code":rows7[0]['sub_code'],"sub_credits":rows7[0]['sub_credits']})
                            li3[i].add_rows({"sub_cat":i,"sub_name":rows7[0]['sub_name'],"sub_code":rows7[0]['sub_code'],"sub_credits":rows7[0]['sub_credits']})
                            li1[i].remove_rows({"sub_name":rows7[0]['sub_name'],"sub_code":rows7[0]['sub_code'],"sub_credits":rows7[0]['sub_credits']})
                            #final_list_cat.append(i)
                            final_list_rows.append([i,total_code,total_name,total_credits])
                            # ui.notify(final_list_rows)
                        else:
                            ui.notify('No rows selected.')
                    def remove_sub(i):
                        global final_list_cat
                        rows7 = li2[i].selected
                        if rows7:
                            total_credits=rows7[0]['sub_credits']
                            total_code=rows7[0]['sub_code']
                            total_name=rows7[0]['sub_name']
                            li1[i].add_rows({"sub_name":rows7[0]['sub_name'],"sub_code":rows7[0]['sub_code'],"sub_credits":rows7[0]['sub_credits']})
                            li3[i].remove_rows({"sub_name":rows7[0]['sub_name'],"sub_code":rows7[0]['sub_code'],"sub_credits":rows7[0]['sub_credits']})
                            li2[i].remove_rows({"sub_name":rows7[0]['sub_name'],"sub_code":rows7[0]['sub_code'],"sub_credits":rows7[0]['sub_credits']})
                            final_list_rows.remove([i,total_code,total_name,total_credits])
                            #ui.notify(final_list_rows)
                        else:
                            ui.notify('No rows selected.')
                    def save_sub(i):
                        sm =0
                        kk = li3[i]
                        # for j in kk.rows:
                        #     sm+=j['sub_credits']
                        # #ui.notify(li4[i].value)
                        # if sm==int(li4[i].value):
                        
                        #ui.notify(sm)
                        sum_credits=0
                        
                        file = open('subject_list_cat.csv', 'w+', newline ='')
                        # identifying header  
                        header = ['Category','sub_code','sub_name','sub_credits']
                        writer = csv.DictWriter(file, fieldnames = header)
                        
                        # writing data row-wise into the csv file
                        writer.writeheader()
                        file.close()
                        flagg=0
                        data_list = len(final_list_rows)
                        if(data_list==0):
                            ui.notify("No data to save")
                        else:
                            for j in final_list_rows:
                                # for k in j:
                                
                                data9 = pd.read_csv('subject_list_cat.csv')
                                
                                if data9.empty:
                                    sm=0
                                    for k in kk.rows:
                                        sm+=k['sub_credits']
                                    #ui.notify(li4[i].value)
                                    if sm==int(li4[i].value):
                                        with open('subject_list_cat.csv', 'a', newline ='') as file:

                                            # identifying header  
                                            writer = csv.DictWriter(file,fieldnames = header)
                                            
                                            # writing data row-wise into the csv file
                                            # writer.writeheader()
                        
                                            writer.writerow({'Category' : j[0],'sub_code' : j[1],'sub_name' : j[2],'sub_credits' : j[3]})                            
                                            flagg=1
                                    else:
                                        ui.notify("Max. credits allowed: "+str(li4[i].value)+". Total current credits is: "+str(sm),type='negative')
                                
                                else:
                                    sm=0
                                    sub_code_list = data9['sub_code'].to_list()
                                    flagg=0

                                    if j[1] in sub_code_list:
                                        for k in kk.rows:
                                            sm+=k['sub_credits']
                                        # ui.notify("Error", type="negative")
                                        ui.notify(j[1]+" "+ j[2]+ " has been removed as already selected in previous category, add another subject", type="negative")
                                        flagg=0
                                        sm = sm-j[3]
                                        kk.remove_rows({"Category":j[0],"sub_name":j[2],"sub_code":j[1],"sub_credits":j[3]})
                                
                                        #ui.notify(sm)
                                    else:
                                        flagg=0
                                        for k in kk.rows:
                                            sm+=k['sub_credits']
                                        #ui.notify(li4[i].value)
                                        if sm==int(li4[i].value):
                                            with open('subject_list_cat.csv', 'a', newline ='') as file:

                                                # identifying header  
                                                writer = csv.DictWriter(file,fieldnames = header)
                                                
                                                # writing data row-wise into the csv file
                                                # writer.writeheader()
                            
                                                writer.writerow({'Category' : j[0],'sub_code' : j[1],'sub_name' : j[2],'sub_credits' : j[3]})                            
                                                flagg=1
                                        else:
                                            ui.notify("Max. credits allowed: "+str(li4[i].value)+". Total current credits is: "+str(sm),type='negative')
                                
                            if flagg==1:
                                ui.notify("Successfully saved")
                            else:
                                pass    
                        # else:
                        #     file = open('subject_list_cat.csv', 'w', newline ='')
                        #     file.close()
                        #     ui.notify("Max. credits allowed: "+str(li4[i].value)+",current total credits is: "+str(sm),type='negative')
                            
                    with ui.button('Select Subject ', on_click=lambda i=i: add_sub(i['CName']), color='orange'):
                        ui.element('i').classes('eva eva-arrowhead-right-outline').classes('text-xl')
                    with ui.button('Remove Subject ', on_click=lambda i=i: remove_sub(i['CName']), color='orange'):
                        ui.element('i').classes('eva eva-arrowhead-left-outline').classes('text-xl')
                    with ui.button('Save Subjects ', on_click=lambda i=i: save_sub(i['CName']), color='lightgreen'):
                        ui.element('i').classes('eva eva-arrow-circle-down-outline').classes('text-xl')
                x+=2
                y+=1
                def nextt():
                    stepper_sub.next
                    ui.notify("All changes saved, now click on Generate Report Button above")
                """"
                def nextt1():
                    global rows_avail_7
                    global df1not
                    ui.notify("h")
                    data8 = pd.read_csv("subject_list_cat.csv")
                    data8 = data8.drop(['Category'],axis=1)
                    
                    # data8 = data8.drop_duplicates()
                    # print("data-7",data7)
                    # print("data-8",data8)
                    # data9 = pd.concat([data7,data8])
                    # print("data-9",data9)
                    # data9 = data9.drop_duplicates()
                    # print(data9)
                    df1not = data7[~(data7['sub_name'].isin(data8['sub_name']) & data7['sub_code'].isin(data8['sub_code']))].reset_index(drop=True)
                    print(df1not)
                    stepper_sub.next
                """
                with ui.stepper_navigation():
                    if y!=cnt:
                        ui.button('Next', on_click=stepper_sub.next)
                    else:
                        ui.button('Save Changes', on_click=nextt)
                    ui.button('Back', on_click=stepper_sub.previous).props('flat')














