from nicegui import ui
import pandas as pd
import numpy as np

df = pd.read_csv("subject_list_cat.csv")
# ui.table(
#     columns=[{'name': col, 'label': col, 'field': col} for col in df.columns],
#     rows=df.to_dict('records'),
# )
df = df.sample(frac = 1)


df_list = np.array_split(df, 8)
with ui.grid(columns=2):
    x = 0
    for i in df_list:
        # df =  pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        ui.table(title="Semester - "+str(x+1),columns=[{'name': col, 'label': col, 'field': col} for col in i.columns],
        rows=i.to_dict('records'),) 
        x += 1   


# final_df = pd.concat(df_list)
# final_df.to_csv("Final_Report.csv", index=None)
f = open("Final_Report.csv", 'w', newline='')
x = 0
for df in df_list:
    f.write("Semester - "+str(x+1)+"\n")
    df.to_csv(f, index=None)
    x +=1
    
f.close()
    # df =  pd.DataFrame( data={'col1': [1, 2], 'col2': [3, 4]})
    # ui.table(title="Semester-2", columns=[{'name': col, 'label': col, 'field': col} for col in df.columns],
    # rows=df.to_dict('records'),)
    
    # df =  pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    # ui.table(title="Semester-3", columns=[{'name': col, 'label': col, 'field': col} for col in df.columns],
    # rows=df.to_dict('records'),)    
    # df =  pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    # ui.table(title="Semester-4", columns=[{'name': col, 'label': col, 'field': col} for col in df.columns],
    # rows=df.to_dict('records'),)
    
    # df =  pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    # ui.table(title="Semester-5", columns=[{'name': col, 'label': col, 'field': col} for col in df.columns],
    # rows=df.to_dict('records'),)    
    # df =  pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    # ui.table(title="Semester-6", columns=[{'name': col, 'label': col, 'field': col} for col in df.columns],
    # rows=df.to_dict('records'),)
    
    # df =  pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    # ui.table(title="Semester-7", columns=[{'name': col, 'label': col, 'field': col} for col in df.columns],
    # rows=df.to_dict('records'),)    
    # df =  pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    # ui.table(title="Semester-8", columns=[{'name': col, 'label': col, 'field': col} for col in df.columns],
    # rows=df.to_dict('records'),)
    
ui.run()