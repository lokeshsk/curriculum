from nicegui import ui, app
import pandas as pd
columns = [
            {'name': 'sub_code', 'label': 'Sub_Code','field': 'sub_code', 'align': 'left', 'sortable': True,'checkboxSelection': True},
            {'name': 'sub_name', 'label': 'Sub_Name','field': 'sub_name', 'align': 'left', 'sortable': True}
           ]
columns1 = [
            {'name': 'sub_code', 'label': 'Sub_Code','field': 'sub_code', 'align': 'left', 'sortable': True,'checkboxSelection': True},
            {'name': 'sub_name', 'label': 'Sub_Name','field': 'sub_name', 'align': 'left', 'sortable': True}
           ]
data = pd.read_csv("subject_list.csv")
# data.drop_duplicates()
sub_code = tuple(list(data['sub_code']))
sub_name = tuple(list(data['sub_name']))

rows_avail = []
rows_sel=[]
print(sub_code)

def move():
    rows = table.selected
    #ui.notify(rows)
    if rows:
        table1.add_rows({"sub_code":rows[0]['sub_code'],"sub_name":rows[0]['sub_name']})
        table.remove_rows({"sub_code":rows[0]['sub_code'],"sub_name":rows[0]['sub_name']})
                # ui.notify(rows_sel)                               
    else:
        ui.notify('No rows selected.')

with  ui.table(title='Avail. Subj.',columns=columns, rows=rows_avail,  row_key=['sub_code'], selection='single', pagination=8) as table:#.bind_filter_from(f, 'value') as table:
    for i in range(len(sub_code)):
        table.add_rows({"sub_code":sub_code[i],"sub_name":sub_name[i]})
with ui.table(title='Selec. Subj.',columns=columns1, rows=rows_sel, row_key='sub_code', selection='single') as table1:
    pass
with ui.button('add ', on_click=move, color='orange'):
    ui.element('i').classes('eva eva-plus-circle-outline').classes('text-xl')
    # with table.add_slot('top-right'):
        # with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
            # ui.icon('search')
    # with table.add_slot('bottom-row'):
        # with table.row():
            # with table.cell():
                # ui.button(on_click=lambda: (
                    # table.add_rows({'sub_code': sub_cod.value, 'sub_name': sub_nam.value, 'sub_credits': sub_cr.value}),
                    # sub_nam.set_value(None),
                    # sub_cod.set_value(None),
                    # sub_cr.set_value(None),
                # ), icon='add').props('flat fab-mini')
            # with table.cell():
                # sub_nam = ui.input('Sub. Name')
            # with table.cell():
                # sub_cod = ui.input('Sub. Code')
            # with table.cell():
                # sub_cr = ui.number('Sub. Credit')
    


ui.run()









