from nicegui import ui, app
import pandas as pd

df = pd.read_csv("subject_list.csv", encoding="ISO-8859-1")
df.drop_duplicates()
sub_code_dict = df['sub_code'].to_list()
sub_name_dict = df['sub_name'].to_list()
sub_code_new=[]
sub_name_new=[]
for value in range(len(sub_code_dict)):
    print(sub_code_dict[value])
    sub_code_new.append(sub_code_dict[value])
for i in range(102):
    sub_name_new.append('sub_code')
    
res = {}
for key in sub_name_new:
    for j in sub_code_new:
        res[key] = j
        sub_code_new.remove(j)
        break
 
# Printing resultant dictionary
for m in res:
    print(m, ':', res[m])
# grid = ui.aggrid({
    # 'columnDefs': [
        # {'headerName': 'Name', 'field': 'sub_name', 'checkboxSelection': True},
        # {'headerName': 'Code', 'field': 'sub_code'},
    # ],
    # 'rowData': [
        # {'name': 'Alice', 'age': 18},
        # {'name': 'Bob', 'age': 21},
        # {'name': 'Carol', 'age': 42},
    # ],
    # 'rowSelection': 'single',
# }).classes('max-h-40')

# async def output_selected_rows():
    # rows = await grid.get_selected_rows()
    # if rows:
        # for row in rows:
            # ui.notify(f"{row['sub_name']}, {row['sub_code']}")
    # else:
        # ui.notify('No rows selected.')

# async def output_selected_row():
    # row = await grid.get_selected_row()
    # if row:
        # ui.notify(f"{row['sub_name']}, {row['sub_code']}")
    # else:
        # ui.notify('No row selected!')

# ui.button('Output selected rows', on_click=output_selected_rows)
# ui.button('Output selected row', on_click=output_selected_row)


ui.run()









