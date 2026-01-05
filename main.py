from imports import *

Window.size = (1000, 800)
Window.clearcolor = (1, 1, 1)

# Make tables if not exists
create_tables()

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
        sync_text = 'Last Synced 16:38'
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

        main_content = BoxLayout(orientation='vertical', size_hint_y=1, height=900, spacing=5, padding=10)
        # Column headers
        headers = ["Product Name","Expiry Date", "Quantity", "Dosage", "Location"]
        for header in headers:
            grid.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))

    # data, placeholder
        stock = [
            ["Paracetamol","05/11/25","2", "500mg", "Hertford"],
            ["Paracetamol", "03/11/25", "3", "500mg", "Hertford"]
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
        self.add_button.bind(on_press=self.add_medicine_popup)
        self.sync_button = Button(text='Sync')
        self.sync_button.bind(on_press=self.sync_popup)
        bottom_bar.add_widget(self.sync_button)
        self.help_button = Button(text='Help')
        bottom_bar.add_widget(self.help_button)

        self.barcode_search_btn = Button(text='Search DB With Barcode ID')
        self.barcode_search_btn.bind(on_press=self.search)
        bottom_bar.add_widget(self.barcode_search_btn)

        self.add_widget(bottom_bar)

    def add_medicine_popup(self, *args): # Add medicine area
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Label(text='Enter medicine details:',bold=True))
        layout.add_widget(TextInput(hint_text='Item Name'))
        layout.add_widget(TextInput(hint_text='Expiry Date'))
        layout.add_widget(TextInput(hint_text='Quantity'))
        layout.add_widget(TextInput(hint_text='Dosage'))
        layout.add_widget(TextInput(hint_text='Location'))

        button_layout = BoxLayout(orientation='horizontal', spacing=1,padding=10)

        close_btn = Button(text='Close', size_hint_y=None, height=40)
        button_layout.add_widget(close_btn)

        add_to_my_stock_btn = Button(text='Add item to stock', size_hint_y=None, height=40)
        button_layout.add_widget(add_to_my_stock_btn)

        add_to_medisend_db = Button(text='Add to MediSend database', size_hint_y=None, height=40)
        button_layout.add_widget(add_to_medisend_db)

        layout.add_widget(button_layout)

        popup = Popup(title='Add Medicine',content=layout,size_hint=(0.7, 0.7))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def sync_popup(self, *args): # Add medicine area
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        close_btn = Button(text='Close', size_hint_y=None, height=40)
        layout.add_widget(close_btn)
        popup = Popup(title='',content=layout,size_hint=(0.7, 0.7))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def search(self, *args):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Label(text='Enter barcode number:'))

        barcode_entry = TextInput(hint_text='Barcode ID',multiline=False,input_filter='int')
        layout.add_widget(barcode_entry)

        button_layout = BoxLayout(orientation='horizontal',spacing=10,size_hint_y=None,height=40)

        search_btn = Button(text='Search')
        close_btn = Button(text='Close')

        button_layout.add_widget(search_btn)
        button_layout.add_widget(close_btn)

        layout.add_widget(button_layout)

        popup = Popup(title='Search',content=layout,size_hint=(0.7, 0.7)
        )

        def do_search(instance):
            barcode = int(barcode_entry.text)
            results = find_item(barcode)
            print(results)

        popup.dismiss()
        search_btn.bind(on_press=do_search)
        close_btn.bind(on_press=popup.dismiss)

        popup.open()

MediSend().run()
