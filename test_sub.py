from nicegui import ui, app
import pandas as pd
columns = [
            {'name': 'sub_name', 'label': 'Sub_Name','field': 'sub_name', 'align': 'left', 'sortable': True,'checkboxSelection': True},
            {'name': 'sub_code', 'label': 'Sub_Code','field': 'sub_code', 'align': 'left', 'sortable': True,'checkboxSelection': True},
            {'name': 'sub_credits', 'label': 'Sub_Credits','field': 'sub_credits', 'align': 'left', 'sortable': True,'checkboxSelection': True}
            # {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
            ]
data = pd.read_csv("subject_list.csv")
# data.drop_duplicates()
sub_code = tuple(list(data['sub_code']))
sub_name = tuple(list(data['sub_name']))
sub_credits = tuple(list(data['sub_credits']))
rows_avail = []

with ui.tabs().classes('w-full') as tabs:
    one = ui.tab('One')
    two = ui.tab('Two')
with ui.tab_panels(tabs, value=two).classes('w-full'):
    with ui.tab_panel(one):
        with  ui.table(title='Avail. Subj.',columns=columns, rows=rows_avail,  row_key=['sub_code'], selection='single', pagination=8) as table:#.bind_filter_from(f, 'value') as table:
            for i in range(len(sub_code)):
                table.add_rows({"sub_name":sub_name[i],"sub_code":sub_code[i],"sub_credits":sub_credits[i]})
            with table.add_slot('top-right'):
                with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
                    ui.icon('search')
            with table.add_slot('bottom-row'):
                with table.row():
                    with table.cell():
                        ui.button(on_click=lambda: (
                            table.add_rows({'sub_code': sub_cod.value, 'sub_name': sub_nam.value, 'sub_credits': sub_cr.value}),
                            sub_nam.set_value(None),
                            sub_cod.set_value(None),
                            sub_cr.set_value(None),
                        ), icon='add').props('flat fab-mini')
                    with table.cell():
                        sub_nam = ui.input('Sub. Name')
                    with table.cell():
                        sub_cod = ui.input('Sub. Code')
                    with table.cell():
                        sub_cr = ui.number('Sub. Credit')
                    
    with ui.tab_panel(two):
        ui.label('Second tab')

# for i in range(3):
    # def test1():
        # ui.notify(i)
    # with ui.stepper().props('vertical').classes('w-full') as stepper:
        # with ui.step(i):
            # ui.label('Preheat the oven to 350 degrees')
            
            # with ui.stepper_navigation():
                # ui.button('Next', on_click=stepper.next)
                # ui.button('Check', on_click=test1)
        # with ui.step('Ingredients'):
            # ui.notify()
            # ui.label('Mix the ingredients')
            # with ui.stepper_navigation():
                # ui.button('Next', on_click=stepper.next)
                # ui.button('Back', on_click=stepper.previous).props('flat')
        # with ui.step('Bake'):
            # ui.notify(i)
            # ui.label('Bake for 20 minutes')
            # with ui.stepper_navigation():
                # ui.button('Done', on_click=lambda: ui.notify('Yay!', type='positive'))
                # ui.button('Back', on_click=stepper.previous).props('flat')

ui.run()