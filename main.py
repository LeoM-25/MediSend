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
        self.title_label = Label(
            text='MediSend', bold=True, font_size='24sp',
            size_hint_y=None, height=45, color=(0, 0, 0, 1)
        )
        self.add_widget(self.title_label)

        sync_text = 'Last Synced 16:38'
        sync_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=10, spacing=10, padding=10)
        sync_bar.add_widget(Label(text=sync_text, color=(0, 0, 0, 1)))
        self.add_widget(sync_bar)

        # top bar
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10, padding=5)
        top_bar.add_widget(TextInput(hint_text='Search by barcode number, location or product...'))
        top_bar.add_widget(Button(text='Search MediSend Database'))
        self.add_widget(top_bar)

        # medicine list area
        scroll = ScrollView(size_hint=(1, 1))
        self.grid = GridLayout(cols=5, size_hint_y=None, spacing=20, padding=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        # column headers
        headers = ["Product Name", "Expiry Date", "Quantity", "Dosage", "Location"]
        for header in headers:
            self.grid.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))

        scroll.add_widget(self.grid)
        self.add_widget(scroll)

        # bottom bar
        bottom_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10, padding=5)
        self.add_button = Button(text='Add Item')
        bottom_bar.add_widget(self.add_button)
        self.add_button.bind(on_press=self.add_medicine_popup)

        self.sync_button = Button(text='Sync')
        self.sync_button.bind(on_press=self.display)
        bottom_bar.add_widget(self.sync_button)

        self.help_button = Button(text='Help')
        bottom_bar.add_widget(self.help_button)

        self.barcode_search_btn = Button(text='Search DB With Barcode ID')
        self.barcode_search_btn.bind(on_press=self.search)
        bottom_bar.add_widget(self.barcode_search_btn)

        self.add_widget(bottom_bar)

    def add_medicine_popup(self, *args):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Label(text='Enter medicine details:', bold=True))

        # Inputs
        name_input = TextInput(hint_text='Item Name')
        expiry_input = TextInput(hint_text='Expiry Date (DD/MM/YY)')
        quantity_input = TextInput(hint_text='Quantity', input_filter='int')
        dosage_input = TextInput(hint_text='Dosage')
        location_input = TextInput(hint_text='Location')
        barcode_input = TextInput(hint_text='Barcode')

        layout.add_widget(name_input)
        layout.add_widget(expiry_input)
        layout.add_widget(quantity_input)
        layout.add_widget(dosage_input)
        layout.add_widget(location_input)

        # buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, padding=10)
        close_btn = Button(text='Close', size_hint_y=None, height=40)
        add_btn = Button(text='Add', size_hint_y=None, height=40)

        button_layout.add_widget(add_btn)
        button_layout.add_widget(close_btn)
        layout.add_widget(button_layout)

        popup = Popup(title='Add Medicine', content=layout, size_hint=(0.7, 0.7))
        close_btn.bind(on_press=popup.dismiss)

        # collect inputs so thy can be stored as local variables
        def do_add(instance):
            item_name = name_input.text.strip()
            expiry_date = expiry_input.text.strip()
            quantity = quantity_input.text.strip()
            dosage = dosage_input.text.strip()
            location = location_input.text.strip()
            barcode = barcode_input.text.strip()

            # passed to database functions
            data_to_add = [item_name, expiry_date, quantity, dosage, location, barcode]
            add(data_to_add)
            popup.dismiss()

        add_btn.bind(on_press=do_add)
        popup.open()

    def sync_popup(self, *args):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        close_btn = Button(text='Close', size_hint_y=None, height=40)
        layout.add_widget(close_btn)
        popup = Popup(title='Sync', content=layout, size_hint=(0.7, 0.7))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def add_to_table(self, rows):
        self.grid.clear_widgets()
        headers = ["Product Name", "Expiry Date", "Quantity", "Dosage", "Location"]
        for header in headers:
            self.grid.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))

        for row in rows:
            for cell in row:
                self.grid.add_widget(Label(text=str(cell), color=(0, 0, 0, 1)))

    def search(self, *args):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text='Enter barcode number:'))

        barcode_entry = TextInput(hint_text='Barcode ID', multiline=False, input_filter='int')
        layout.add_widget(barcode_entry)

        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        search_btn = Button(text='Search')
        close_btn = Button(text='Close')
        button_layout.add_widget(search_btn)
        button_layout.add_widget(close_btn)
        layout.add_widget(button_layout)

        popup = Popup(title='Search', content=layout, size_hint=(0.7, 0.7))

        def do_search(instance):
            if barcode_entry.text.strip():
                barcode = int(barcode_entry.text)
                results = find_item(barcode)

                # Convert results into table rows for display
                display_rows = []
                for r in results:
                    display_rows.append([
                        "Unknown", # name
                        r["expiry"],
                        "-", # quantity
                        "-", # dosage
                        r["location"]
                    ])

                self.add_to_table(display_rows)

            popup.dismiss()

        search_btn.bind(on_press=do_search)
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def display(self, *args):
        import sqlite3
        display_rows = []
        with sqlite3.connect("MediSend.db") as db:
            cursor = db.cursor()
            for loc in ["A", "B"]:
                table_name = f"Pharmacy_{loc}"
                cursor.execute(f"SELECT Product, Expiry_Date, Quantity FROM {table_name}")
                for row in cursor.fetchall():
                    display_rows.append([
                        row[0],  # Product Name
                        row[1],  # Expiry Date
                        row[2],  # Quantity
                        "-",  # Dosage (not stored yet)
                        loc  # Location
                    ])

        # Update the main table display
        self.add_to_table(display_rows)


MediSend().run()

