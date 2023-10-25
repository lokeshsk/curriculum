from nicegui import ui
from datetime import datetime
from pymongo import MongoClient
from  matplotlib import pyplot as plt
#ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">')

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["woxsen"]
def plot_pie():
    final_cat_col_1 = mydb['final_cat']
    res_final_cat_1 = final_cat_col_1.find({},{"_id":0})
    cnt_1 = final_cat_col_1.count_documents({})
    cname =[]
    cvalue=[]
    for i in res_final_cat_1:
        cname.append(i['CName'])
        cvalue.append(i['CValue'])

    with ui.pyplot(figsize=(7,4)):
        plt.pie(cvalue, labels = cname, autopct='%1.1f%%')
        plt.savefig('distribution_plot.png')
