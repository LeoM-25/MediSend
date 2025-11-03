from imports import *

Window.size = (1000, 800)
Window.clearcolor = (1, 1, 1)
# main app
class MediSend(App):
    def build(self):
        return Main()
# Main window
class Main(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        # title text area
        self.title_label = Label(text='MediSend', bold=True, font_size='24sp', size_hint_y=None, height=45,color=(0, 0, 0, 1))
        self.add_widget(self.title_label)
        sync_text = 'Last synced 12:09'
        # Sync Bar
        sync_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=10, spacing=10, padding=10)
        sync_bar.add_widget(Label(text=sync_text, color=(0, 0, 0, 1)))
        self.add_widget(sync_bar)
        # top
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10, padding=5)
        top_bar.add_widget(TextInput(hint_text='Search by barcode number, location or product...'))
        top_bar.add_widget(Button(text='Search MediSend Database'))
        # adds top bar to the window
        self.add_widget(top_bar)
        # medicine list area
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=5, size_hint_y=None, spacing=20, padding=10)
        grid.bind(minimum_height=grid.setter('height'))

        main_content = BoxLayout(orientation='vertical', size_hint_y=1, height=750, spacing=5, padding=10)
        # Column headers
        headers = ["Product Name","Expiry Date", "Quantity", "Dosage", "Location"]
        for header in headers:
            grid.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))
            
        # data, placeholder
        stock = [
            ["Paracetamol","05/11/25","2", "500mg", "Hertford"],
        ]
        
        for row in stock:
            for cell in row:
                grid.add_widget(Label(text=cell, color=(0, 0, 0, 1)))

        scroll.add_widget(grid)
        self.add_widget(scroll)
        self.add_widget(main_content)
        # bottom bar
        bottom_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10, padding=5)
        self.add_button = Button(text='Add Item')
        bottom_bar.add_widget(self.add_button)
        #self.add_button.bind(on_press=add_medicine_popup)
        bottom_bar.add_widget(Button(text='Sync'))
        bottom_bar.add_widget(Button(text='Help'))
        self.add_widget(bottom_bar)
        
MediSend().run()
