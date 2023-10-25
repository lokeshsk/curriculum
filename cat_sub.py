from nicegui import ui
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["woxsen"]
li_sc, li_sn,li_scc = [],[],[]
li_sn_new=[]
li_sc_new=[]
li_scc_new=[]
li_cat_new=[]
li_cat_1 =[]
li_cat_1_new=[]
y = 0
def get_data():
    with ui.stepper().props('vertical').classes('w-full') as stepper_sub:
        final_cat_col = mydb['final_cat']
        res_final_cat = final_cat_col.find({},{"_id":0})
        l = []
        x = 0
        data = pd.read_csv("subject_list.csv", encoding="ISO-8859-1")
        data = data.drop_duplicates()
        # data[0] = data[0].str.strip()
        # data[1] = data[1].str.strip()
        # converting column data to list
        sub_code = data['sub_code'].tolist()
        sub_name = data['sub_name'].tolist()
        # sub_name1 = ['match','mathematics','machine learning','english','physics']
        # sub_code1 = ['match101','mathematics102','machine103','english101','physics104']
        cnt = final_cat_col.count_documents({})
        for i in res_final_cat:
            with ui.step(i['CName']):
                li_cat_new.append(i['CName'])
                cred = i['CValue']
                cred = int((cred/100) * 160)
                ui.label("Max. allowed Credits for this category: "+str(cred))
                with ui.grid(columns=3):
                    def add_textbox():
                        # Create a new text box
                        #textbox = ui.number(label='Text')
                        sc = ui.input(label = "Subject Code", placeholder="Subject Code", autocomplete=sub_code)
                        sn = ui.input(label = "Subject Name", placeholder = "Subject Name", autocomplete=sub_name)
                        scc = ui.number(label = "Subject Credits", min=1, max=30, step=1)
                        # label = ui.label().bind_text_from(sn, 'value')
                        li_sc.append(sc)
                        li_sn.append(sn)
                        li_scc.append(scc)
                    def nxt():
                        global li_scc
                        global li_sc
                        global li_sn
                        global li_sn_new
                        global li_sc_new
                        global li_scc_new
                        global y
                        global li_cat_1_new
                        global li_cat_1
                        for ix in range(len(li_sn)):
                            # sub_cd = str(li_sc[x].value)+" (" + cat_to_add +")"
                            li_sn_new.append(li_sn[ix].value)
                            li_sc_new.append(li_sc[ix].value)
                            li_scc_new.append(li_scc[ix].value)
                            li_cat_1.append(li_cat_new[y])
                        # data = [[li_sn_new[x]]]
                        ui.notify(li_cat_1)
                        li_sc=[]
                        li_sn = []
                        y +=1
                        for i in li_cat_1:
                            li_cat_1_new.append(i)
                        li_cat_1=[]
                        # ui.notify("blank")
                        li_scc = []
                        
                        # ui.notify(cnt)
                        stepper_sub.next()
                    def fin_save():
                        for ix in range(len(li_sn)):
                            li_sn_new.append(li_sn[ix].value)
                            li_sc_new.append(li_sc[ix].value)
                            li_scc_new.append(li_scc[ix].value)
                        #Create a DataFrame object
                        df = pd.DataFrame({'Category': li_cat_1_new,'Sub_Name':li_sn_new,'Sub_Code':li_sc_new,'Sub_Credits':li_scc_new})
                        df.to_csv("subject_list_cat.csv",index=None)
                    def verify():
                        sm = 0
                        for i in li_scc:
                            sm += i.value
                        #sm = sm - cred
                        # nxt_sub_final.enabled=True
                        ui.notify(sm)
                        nxt_sub.props('enabled')
                    with ui.button('Add More', on_click=add_textbox, color='orange'):
                        ui.element('i').classes('eva eva-plus-circle-outline').classes('text-xl')
                    ui.label()
                    with ui.button('Verify', on_click=verify, color='orange'):
                        ui.element('i').classes('eva eva-plus-circle-outline').classes('text-xl')
                x += 1
                with ui.stepper_navigation():
                    if x==cnt:
                        nxt_sub_final = ui.button('Save Changes', on_click=fin_save)
                        ui.button('Previous Step', on_click=stepper_sub.previous).props('flat')
                    else:
                        nxt_sub = ui.button('Save and Next', on_click=nxt)
                        ui.button('Previous Step', on_click=stepper_sub.previous).props('flat')
                        

            
            