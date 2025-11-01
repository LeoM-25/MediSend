# Main.py file
from imports import *
Window.size = (800, 800)
Window.clearcolor = (1, 1, 1)
# main app
class MediSend(App):
    def build(self):
        return Main()

class Main(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        # title text area
        self.title_label = Label(text='MediSend', bold=True, font_size='24sp', size_hint_y=None, height=50,color=(0, 0, 0, 1))
        self.add_widget(self.title_label)
        # top
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10, padding=5)
        top_bar.add_widget(TextInput(hint_text='Search by barcode number, location or product...'))
        top_bar.add_widget(Button(text='Search'))
        # adds top bar to the window
        self.add_widget(top_bar)

        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=3, size_hint_y=None, spacing=20, padding=10)
        grid.bind(minimum_height=grid.setter('height'))

        # medicine list area
        main_content = BoxLayout(orientation='vertical', size_hint_y=1, height=750, spacing=10, padding=5)
        # Column headers
        headers = ["Name", "Dosage", "Location"]
        for header in headers:
            grid.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))

        # data
        stock = [
            ["Paracetamol", "500mg", "Hertford"],
        ]

        for row in stock:
            for cell in row:
                grid.add_widget(Label(text=cell, color=(0, 0, 0, 1)))

        scroll.add_widget(grid)
        self.add_widget(scroll)
        self.add_widget(main_content)

        bottom_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10, padding=5)
        bottom_bar.add_widget(Button(text='Add Item'))
        bottom_bar.add_widget(Button(text='Sync'))
        bottom_bar.add_widget(Button(text='Help'))
        self.add_widget(bottom_bar)

MediSend().run()
