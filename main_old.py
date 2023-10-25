from nicegui import ui, app
from datetime import datetime
from pymongo import MongoClient
from list_subjects import get_data
from plot import plot_pie
import pandas as pd
import numpy as np
from  matplotlib import pyplot as plt

app.native.window_args['resizable'] = True
#app.native.start_args['debug'] = True

ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">')

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["woxsen"]
col = mydb["Degree"]
result = col.find()
st = []
col_dat = mydb["data"]

def end_and_reset_stepper() -> None:
    stepper.set_value('Basic Inputs')


for i in result:
    st.append(i['Branch'])
with ui.stepper().props('vertical').classes('w-full') as stepper:  

    with ui.step('Basic Inputs'):       
        with ui.grid(columns=2):
            e = ''
            def nx(en):
                #ui.notify(e)
                global e
                e = en
            noc = ui.number(label='Number of Credits', format='%d',min=1, max=300, step=1, placeholder="Number of Credits")

            #selectbranch = ui.select(st,label="Select Program", value="Select Program")
            selectbranch = ui.select(st,label="Select Program", value="Select Program", on_change=lambda e: nx(str(e.value)))

            def nxt():
                #ui.notify(e)
                if noc.value==None:
                    ui.notify("No. of Credits cannot be empty")
                elif e == "None":
                    ui.notify("Select Valid Program")
                else:
                    i = {"noc":noc.value, "prg":e}
                    col_dat.delete_many({})
                    col_dat.replace_one(i, i, upsert=True)
                    stepper.next()
        with ui.stepper_navigation():
            ui.button('Next', on_click=nxt)
    with ui.step('Categories'):
        #ui.notify(noc.value)
        
        
        with ui.row():
            res_dat = col_dat.find({},{"_id":0,"noc":1,"prg":1})
            #ui.label(res_dat)
            
            # for i in res_dat:
                # ui.markdown("**Number of Credits** : " + str(i['noc']))
                # ui.markdown("**Program** : " + i['prg'])
            # ui.notify(noc)
            #ui.label(program)

        #ui.button("testt",on_click=testt)
        col_cat = mydb["categories"]
        result_cat = col_cat.find({},{'CName':1,"_id":0})
        #ui.notify(result_cat)
        avail_cat=[]
        for i in result_cat:
            #ui.notify(i)
            avail_cat.append(i)
        
        with ui.grid(columns=4):
            
            
            columns = [
            {'name': 'CName', 'label': 'Available Categories','field': 'CName', 'align': 'left', 'sortable': True,'checkboxSelection': True},
            # {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
            ]
            columns1 = [
            {'name': 'CName', 'label': 'Selected Categories', 'field': 'CName', 'align': 'left', 'sortable': True,'checkboxSelection': True},
            # {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
            ]
            columns2 = [
            {'name': 'CName', 'label': 'Final Categories', 'field': 'CName', 'align': 'left', 'sortable': True},
            # {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
            ]
            
            rows_avail = avail_cat
            rows_sel=[]
            rows_final=[]
            def add():
                flag = 0
                # rows = table.selected
                # ui.notify(rows)
                for i in rows_avail:
                    for k,v in i.items():
                        if cat.value.lower() == v.lower():
                            flag=1
                            ui.notify("Category already exists in Available List")
                        elif cat.value == '':
                            flag=2
                        else:
                            pass
                for i in rows_sel:
                    for k,v in i.items():
                        if cat.value.lower() == v.lower():
                            flag=1
                            ui.notify("Category already exists in Selected List")
                        elif cat.value == '':
                            flag=2
                        else:
                            pass

                if flag==1:
                    pass
                elif flag==2:
                    ui.notify("No category entered")
                else:
                    table.add_rows({'CName': str(cat.value)})
                    
            def move():
                rows = table.selected
                #ui.notify(rows)
                if rows:
                    # # if not any(d['name'] == 'Carol' for d in rows_sel):
                    #     # ui.notify("Same category entered")
                    #     for row in rows:
                    #ui.notify(rows[0]["CName"])
                    table1.add_rows({"CName":rows[0]['CName']})
                    table2.add_rows({"CName":rows[0]['CName']})
                    table.remove_rows({"CName":rows[0]['CName']})
                            # ui.notify(rows_sel)                               
                else:
                    ui.notify('No rows selected.')
            def rmove():
                rows = table1.selected
                #ui.notify(table2['CName'])
                if rows:
                    for row in rows:
                        #ui.notify(i)                        
                        table.add_rows({"CName":row['CName']})
                        table1.remove_rows({"CName":row['CName']})
                        table2.remove_rows({"CName":row['CName']})
                        #ui.notify(f"{row['name']}") 
                else:
                    ui.notify('No rows selected.')
                    
            def csave():
                #ui.notify(rows_final)
                flag = 0
                for i in rows_final:
                    #col_cat.insert_one(i)
                    newvalues = { "$set": i }
                    col_cat.replace_one(i, i, upsert=True)
                    flag=1
                if flag==1:
                    ui.notify("Saved Successfully")

            #ui.label()
            #f = ui.input('Filter Available Categories')          
            #f1 = ui.input('Filter Selected Categories')          
            #ui.label()
            
            cat = ui.input(label="Enter Category", placeholder='Enter Category').tooltip("Add additional categories apart from what you see in the table next to this field.") 
            #table = ui.table(columns=columns, rows=rows_avail,  row_key='CName', selection='single').bind_filter_from(f, 'value')
            with  ui.table(title='Avail. Categ.',columns=columns, rows=rows_avail,  row_key='CName', selection='single') as table:#.bind_filter_from(f, 'value') as table:
                with table.add_slot('top-right'):
                    with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
                        ui.icon('search')
                # with table.add_slot('bottom-row'):
                #     with table.row():
                #         with table.cell():
                #             ui.button(on_click=lambda: (
                #                 table.add_rows({'CName': CName.value}),
                #                 CName.set_value(None),
                #             ), icon='add').props('flat fab-mini')
                #         with table.cell():
                #             CName = ui.input('Category Name')
                
            with ui.table(title='Selec. Categ.',columns=columns1, rows=rows_sel, row_key='CName', selection='single') as table1:
            # table1= ui.table(title='Selec. Categ.',columns=columns1, rows=rows_sel, row_key='CName', selection='single')
            # as table1:
                with table1.add_slot('top-right'):
                    with ui.input(placeholder='Search').props('type=search').bind_value(table1, 'filter').add_slot('append'):
                        ui.icon('search')
                
                #.bind_filter_from(f1, 'value')
            table2 = ui.table(columns=columns2, rows=rows_final, row_key='CName',pagination=6)
            
            
            with ui.button('add ', on_click=add, color='orange'):
                ui.element('i').classes('eva eva-plus-circle-outline').classes('text-xl')
            with ui.button("Select Category", on_click=move, color='orange'):
                ui.element('i').classes('eva eva-arrowhead-right-outline').classes('text-xl')
            with ui.button("Remove Category", on_click=rmove, color='orange'):
                ui.element('i').classes('eva eva-arrowhead-left-outline').classes('text-xl')
            with ui.button("Save Categories", on_click=csave, color='lightgreen'):
                ui.element('i').classes('eva eva-arrow-circle-down-outline').classes('text-xl')
     
        with ui.stepper_navigation():
            ui.button('Next', on_click=stepper.next)
            ui.button('Back', on_click=stepper.previous).props('flat')
    
    with ui.step('Select Final Categories'):
        x = 0

        sl_list =[]
        check_list=[]
        col_cat1 = mydb["categories"]
        result_cat1 = col_cat1.find()
        st_cat = []
        for i in result_cat1:
            st_cat.append(i['CName'])
        for i in st_cat:
            check  = "check"+str(x+1)
            sl ="sl"+str(x+1)
            with ui.row():
                check = ui.checkbox(i).classes("w-80")
                sl = ui.number(label="Percentage", format="%d", min=0, max=50, step=1).bind_enabled(check,'value').classes("w-32")
                #.props('label-always').classes('w-32').on('update:model-value', lambda e: add(e.args),
                check_list.append(check)
                sl_list.append(sl)
                #throttle=1.0)
        #sm = 0
        def add():
            #sm = 0
            #global sm
            sm =0
            #sm += e
            check_list_1 =[]
            sl_list_1 =[]
            #ui.notify(sl_list)
            for i in check_list:
                if i.enabled==True:
                    check_list_1.append(i.value)     
                
            for i in sl_list:
                if i.enabled==True:
                    #ui.notify(i.value)
                    sl_list_1.append(i)
                    sm = sm + i.value
            final_cat_per=[]
            for i in range(len(check_list_1)):
                if check_list_1[i]==True:
                    final_cat_per.append({"CName":st_cat[i],"CValue":sl_list[i].value})
            
            if sm==100:
                ui.notify(sm, type="positive")
                #ui.notify(check_list_1)
                #ui.notify(final_cat_per)
                final_cat_col = mydb['final_cat']
                final_cat_col.delete_many({})
                for i in final_cat_per:
                    final_cat_col.replace_one(i,i,upsert=True)
                
                
                # final_cat_col.insert_many(final_cat_per)
                return sm
            else:
                ui.notify("Total percentage cannot be less or more than 100. Current percentage is: "+str(sm),type='negative')
        ui.button("Calculate",on_click=add, color='orange')
        with ui.stepper_navigation():
            ui.button('Next', on_click=stepper.next)
            ui.button('Back', on_click=stepper.previous).props('flat')
    
        
    with ui.step('Add Subject -> Categories'):
        def get_data_caller():
            btn_get.enabled=False
            get_data()
        #Child/SUb Stepper Begin
        btn_get = ui.button("get data", on_click = get_data_caller, color='orange')
        
        #Chid Stepper end
        with ui.stepper_navigation():
            ui.button('Generate Report', on_click=stepper.next)
        #ui.button('Back', on_click=stepper.previous).props('flat')
    with ui.step('Report Generation'):
        def get_plot():
            btn_plot.enabled=False
            
            plot_pie()
            df = pd.read_csv("subject_list_cat.csv")

            df = df.sample(frac = 1)
            df_list = np.array_split(df, 8)
            with ui.grid(columns=2):
                x = 0
                for i in df_list:
                    # df =  pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
                    with ui.table(title="Semester - "+str(x+1),row_key='Sub_Code',selection='single',columns=[{'name': col, 'label': col, 'field': col} for col in i.columns], rows=i.to_dict('records'),) as table15:
                        with table15.add_slot('bottom-row'):
                            with table.row():
                                with table.cell():
                                    ui.label()
                                with table.cell():
                                    sem=[1,2,3,4,5,6,7,8]
                                    sem.remove(x+1)
                                    select20 = ui.select(sem, label='Move to',value='Move to')
                    x += 1   
            f = open("Final_Report.csv", 'w', newline='')
            x = 0
            for df in df_list:
                f.write("Semester - "+str(x+1)+"\n")
                df.to_csv(f, index=None)
                x +=1
                
            f.close()
        #Child/SUb Stepper Begin
        btn_plot = ui.button("Generate Final Report and plot", on_click = get_plot, color='orange')

            
        with ui.stepper_navigation():
            ui.button('Start Again', on_click=end_and_reset_stepper)
            #ui.button('Back', on_click=stepper.previous).props('flat')
    #___________________________________________________________________________________________
        # with ui.step('Add Subject -> Categories'):
        #     avail_sub=[]
        #     with ui.grid(columns=3):    
        #         col = mydb["categories"]
        #         result = col.find()
        #         st = []
        #         for i in result:
        #             st.append(i['CName'])
                

        #         col_sub = mydb["subjects"]
                

        #         def swap_keys_values(dictionary):
        #             swapped_dict=[]
        #             for key, value in dictionary.items():
        #                 swapped_dict.append({value: key})
        #             return swapped_dict
        #         def nx1(e1):
        #             global avail_sub
        #             # global swapped_dict
        #             avail_sub=[]
        #             temp = []
        #             result_sub = col_sub.find({'CName': e1},{'SName':1,"_id":0})
        #             for i in result_sub:
        #                 temp.append(i)
        #             for i in temp[0]['SName']:
        #                 #ui.notify(i)
        #                 table3.add_rows({'SName':i})
        #                 #        ui.notify(temp)
        #             #
        #         selectbranch = ui.select(st,label="Select Category", on_change=lambda e1: nx1(str(e1.value)))
                
        #         columns3 = [
        #         {'name': 'SName', 'label': 'List of Subjects', 'field': 'SName', 'align': 'left', 'sortable': True},
        #         ]

        #         #keys = ['SName']
        #         rows_ss = avail_sub
                
        #         def tet():
        #             # ui.notify(swapped_dict)
        #             ui.notify("hello")
        #             ui.notify(rows_ss)
        #         ui.button ("te",on_click=tet)

        #         table3 = ui.table(columns=columns3, rows=rows_ss, row_key='SName', selection='single', pagination=6).classes('h-80')
        #     with ui.stepper_navigation():
        #         ui.button('Done', on_click=lambda: ui.notify('Yay!', type='positive'))
        #         ui.button('Back', on_click=stepper.previous).props('flat')
#ui.button('shutdown', on_click=app.shutdown)

#ui.run(reload=False, native=True, window_size=(700, 500), fullscreen=False) 
ui.run()

