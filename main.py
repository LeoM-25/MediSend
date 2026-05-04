from imports import *
# (future reference) https://kivy.org/doc/stable/gettingstarted/properties.html
Window.size = (1000, 1000)
Window.clearcolor = (1, 1, 1)

# Make tables if not exists
create_tables()

# main app
class MediSend(App):
    def build(self):
        self.main_widget = Main()
        return self.main_widget
    def on_start(self):
        self.main_widget.display()

# Main window
class Main(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        # title text area
        self.title_label = Label(text='MediSend', bold=True, font_size='24sp',size_hint_y=None, height=45, color=(0, 0, 0, 1))
        self.add_widget(self.title_label)

        sync_text = 'Last Synced: Never'
        sync_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=10, spacing=10, padding=10)
        sync_bar.add_widget(Label(text=sync_text, color=(0, 0, 0, 1)))
        self.add_widget(sync_bar)


        # top bar
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10, padding=5)
        self.search_input = TextInput(hint_text='Search by barcode number, location or product...')
        top_bar.add_widget(self.search_input)
        search_btn = Button(text='Search MediSend Database')
        search_btn.bind(on_press=self.display)
        top_bar.add_widget(search_btn)
        self.add_widget(top_bar)

        # medicine list area
        # tables container (top only now)
        tables_container = BoxLayout(orientation='vertical', size_hint=(1, 1), spacing=10)

        # location selector
        location_bar = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=60)
        location_inner = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(300, 40), spacing=10)
        location_inner.add_widget(Label(text="Select Your Location:", size_hint_x=None, width=140, color=(0, 0, 0, 1)))
        self.location_spinner = Spinner(
            text="All Pharmacies",
            values=("All Pharmacies", "Pharmacy_A", "Pharmacy_B"),
            size_hint_x=None,
            width=200,
            color=(1, 1, 1)
        )
        location_inner.add_widget(self.location_spinner)
        location_bar.add_widget(location_inner)
        tables_container.add_widget(location_bar)

        # top table (only table now)
        top_scroll = ScrollView(size_hint=(1, 1))
        self.top_grid = GridLayout(cols=6, size_hint_y=None, spacing=20, padding=10)
        self.top_grid.bind(minimum_height=self.top_grid.setter('height'))

        # columns
        headers = ["Product Name", "Expiry Date", "Quantity", "Dosage", "Location","Request"]
        for header in headers:
            self.top_grid.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))

        top_scroll.add_widget(self.top_grid)
        tables_container.add_widget(top_scroll)

        self.add_widget(tables_container)

        # bind dropdown to refresh table
        self.location_spinner.bind(text=self.display)

        # bottom bar
        bottom_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10, padding=5)

        self.add_button = Button(text='Add Item')
        bottom_bar.add_widget(self.add_button)
        self.add_button.bind(on_press=self.add_medicine_popup)

        self.add_barcode_btn = Button(text='Add Barcode')
        self.add_barcode_btn.bind(on_press=self.add_barcode_popup)
        bottom_bar.add_widget(self.add_barcode_btn)

        self.barcode_search_btn = Button(text='Search DB By Barcode ID')
        self.barcode_search_btn.bind(on_press=self.search)
        bottom_bar.add_widget(self.barcode_search_btn)

        self.manage_stock_btn = Button(text='Manage Stock')
        self.manage_stock_btn.bind(on_press=self.show_requests)
        bottom_bar.add_widget(self.manage_stock_btn)

        self.analysis_btn = Button(text='Data Analysis')
        self.analysis_btn.bind(on_press=self.show_analysis)
        bottom_bar.add_widget(self.analysis_btn)

        self.add_widget(bottom_bar)

    def show_analysis(self, *args):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Label(text='Waste Analysis (Expired Medicines)', bold=True))

        results = get_waste_analysis()

        grid = GridLayout(cols=2, size_hint_y=None, spacing=10)
        grid.bind(minimum_height=grid.setter('height'))

        # headers
        grid.add_widget(Label(text="Medicine", bold=True))
        grid.add_widget(Label(text="Wasted Qty", bold=True))

        # top 5 worst items
        for product, qty in results[:5]:
            grid.add_widget(Label(text=str(product)))
            grid.add_widget(Label(text=str(qty)))

        scroll = ScrollView()
        scroll.add_widget(grid)
        layout.add_widget(scroll)

        # suggestion text
        if results:
            worst = results[0][0]
            suggestion = f"Suggestion: Order less of {worst}"
        else:
            suggestion = "No waste detected."

        layout.add_widget(Label(text=suggestion))

        close_btn = Button(text="Close", size_hint_y=None, height=40)
        layout.add_widget(close_btn)

        popup = Popup(title="Data Analysis", content=layout, size_hint=(0.6, 0.6))
        close_btn.bind(on_press=popup.dismiss)

        popup.open()

    def add_medicine_popup(self, *args):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Label(text='Enter medicine details:', bold=True))

        # Inputs
        name_input = TextInput(hint_text='Item Name')
        expiry_input = TextInput(hint_text='Expiry Date (DD/MM/YY)')
        quantity_input = TextInput(hint_text='Quantity', input_filter='int')
        dosage_input = TextInput(hint_text='Dosage')
        location_input = Spinner(text='Select Location',values=('Pharmacy_A', 'Pharmacy_B'),height=40)
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

        button_layout.add_widget(close_btn)
        button_layout.add_widget(add_btn)
        layout.add_widget(button_layout)

        popup = Popup(title='Add Medicine', content=layout, size_hint=(0.5, 0.5))
        close_btn.bind(on_press=popup.dismiss)

        def show_analysis(self, *args):
            layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

            layout.add_widget(Label(text='Waste Analysis (Expired Medicines)', bold=True))

            results = get_waste_analysis()

            grid = GridLayout(cols=2, size_hint_y=None, spacing=10)
            grid.bind(minimum_height=grid.setter('height'))

            # headers
            grid.add_widget(Label(text="Medicine", bold=True))
            grid.add_widget(Label(text="Wasted Qty", bold=True))

            # top 5 worst items
            for product, qty in results[:5]:
                grid.add_widget(Label(text=str(product)))
                grid.add_widget(Label(text=str(qty)))

            scroll = ScrollView()
            scroll.add_widget(grid)
            layout.add_widget(scroll)

            # suggestion text
            if results:
                worst = results[0][0]
                suggestion = f"Suggestion: Order less of {worst}"
            else:
                suggestion = "No waste detected."

            layout.add_widget(Label(text=suggestion))

            close_btn = Button(text="Close", size_hint_y=None, height=40)
            layout.add_widget(close_btn)

            popup = Popup(title="Data Analysis", content=layout, size_hint=(0.6, 0.6))
            close_btn.bind(on_press=popup.dismiss)

            popup.open()

        def do_add(instance):
            item_name = name_input.text.strip()
            expiry_date = expiry_input.text.strip()
            quantity = quantity_input.text.strip()
            dosage = dosage_input.text.strip()
            location = location_input.text
            if location == 'Select Location':
                location = 'Pharmacy_A'
            barcode = barcode_input.text.strip()

            # passed to database functions
            data_to_add = [item_name, expiry_date, quantity, dosage, location, barcode]
            add(data_to_add)
            popup.dismiss()

        add_btn.bind(on_press=do_add)
        popup.open()

    def add_barcode_popup(self, *args):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Label(text='Scan / Enter Barcode:'))
        barcode_input = TextInput(hint_text='Barcode ID', multiline=False, input_filter='int')
        product_input = TextInput(hint_text='Product Name')

        layout.add_widget(product_input)
        layout.add_widget(barcode_input)

        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        add_btn = Button(text='Add')
        close_btn = Button(text='Close')

        button_layout.add_widget(close_btn)
        button_layout.add_widget(add_btn)
        layout.add_widget(button_layout)

        popup = Popup(title='Add Barcode', content=layout, size_hint=(0.4, 0.4))

        def do_add(instance):
            barcode = barcode_input.text.strip()
            product = product_input.text.strip()

            if barcode and product:
                add_barcode(int(barcode), product)
                print(f"Added barcode {barcode} for {product}")

            popup.dismiss()

        add_btn.bind(on_press=do_add)
        close_btn.bind(on_press=popup.dismiss)

        popup.open()

    def sync_popup(self, *args):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        close_btn = Button(text='Close', size_hint_y=None, height=40)
        layout.add_widget(close_btn)
        popup = Popup(title='Sync', content=layout, size_hint=(0.7, 0.7))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def add_to_top_table(self, rows):
        self.top_grid.clear_widgets()

        headers = ["Product Name", "Expiry Date", "Quantity", "Dosage", "Location", "Request Item"]
        for header in headers:
            self.top_grid.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))

        for row in rows:
            expiry_str = row[1]
            expiry_date = datetime.strptime(expiry_str, "%d/%m/%y")
            days_left = (expiry_date - datetime.now()).days

            colour = (0, 0, 0, 1)
            if days_left < 7:
                colour = (1, 0, 0, 1)
            elif days_left < 14:
                colour = (1, 0.5, 0, 1)
            # adds row
            for cell in row:
                self.top_grid.add_widget(Label(text=str(cell), color=colour))

            request_btn = Button(text="Request", size_hint_y=None, height=30)
            request_btn.bind(on_press=lambda btn, r=row: self.request_popup(r))
            self.top_grid.add_widget(request_btn)

    def search(self, *args):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text='Enter barcode number:'))

        barcode_entry = TextInput(hint_text='Barcode ID', multiline=False, input_filter='int', height=40)
        layout.add_widget(barcode_entry)

        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        search_btn = Button(text='Search')
        close_btn = Button(text='Close')
        button_layout.add_widget(close_btn)
        button_layout.add_widget(search_btn)
        layout.add_widget(button_layout)

        popup = Popup(title='Search for Medicine', content=layout, size_hint=(0.25, 0.25))

        def do_search(instance):
            if barcode_entry.text.strip():
                barcode = int(barcode_entry.text)
                results = find_item(barcode)

                display_rows = []
                for r in results:
                    display_rows.append([
                        r["product"] if r["product"] else "Unknown",
                        r["expiry"],
                        r["quantity"],
                        "-",
                        r["location"]
                    ])

                print(display_rows)

            popup.dismiss()

        search_btn.bind(on_press=do_search)
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def request_popup(self, r, *args):
        item_name = r[0]
        from_location = r[4]

        to_location = self.location_spinner.text
        if to_location == "All Pharmacies":
            to_location = "Pharmacy_A"

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text=f'Request Item: {item_name} from {from_location}?'))

        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        close_btn = Button(text='Cancel')
        request_btn = Button(text='Request')

        button_layout.add_widget(close_btn)
        button_layout.add_widget(request_btn)
        layout.add_widget(button_layout)

        popup = Popup(title='Request Item?', content=layout, size_hint=(0.45, 0.2))

        def confirm_request(instance):
            with sqlite3.connect("MediSend.db") as db:
                cursor = db.cursor()
                cursor.execute("""
                    INSERT INTO requests (item_name, from_location, to_location)
                    VALUES (?, ?, ?)
                """, (item_name, from_location, to_location))
                db.commit()

            print(f"Requested {item_name} from {from_location} to {to_location}")
            popup.dismiss()

        request_btn.bind(on_press=confirm_request)
        close_btn.bind(on_press=popup.dismiss)

        popup.open()

    def show_requests(self, *args):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        grid = GridLayout(cols=3, size_hint_y=None, spacing=20, padding=10)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ["Item", "From", "To"]
        for h in headers:
            grid.add_widget(Label(text=h, bold=True))

        with sqlite3.connect("MediSend.db") as db: # From DB
            cursor = db.cursor()
            cursor.execute("SELECT item_name, from_location, to_location FROM requests")
            rows = cursor.fetchall()

            for row in rows:
                for cell in row:
                    grid.add_widget(Label(text=str(cell)))

        scroll = ScrollView()
        scroll.add_widget(grid)
        layout.add_widget(scroll)

        close_btn = Button(text="Close", size_hint_y=None, height=40)
        layout.add_widget(close_btn)

        popup = Popup(title="Manage Stock (Requests)", content=layout, size_hint=(0.6, 0.6))
        close_btn.bind(on_press=popup.dismiss)

        popup.open()

    def display(self, *args): # modified database code
        import sqlite3
        all_rows = []

        with sqlite3.connect("MediSend.db") as db:
            cursor = db.cursor()
            for loc in ["A", "B"]:
                table_name = f"Pharmacy_{loc}"
                cursor.execute(f"SELECT Product, Expiry_Date, Quantity FROM {table_name}")
                for row in cursor.fetchall():
                    all_rows.append([
                        row[0],
                        row[1],
                        row[2],
                        "-",
                        f"Pharmacy_{loc}"
                    ])

        # filter
        search_text = self.search_input.text.strip()
        selected = self.location_spinner.text

        # if input is a barcode (must be int)
        if search_text.isdigit():
            barcode = int(search_text)
            results = find_item(barcode)

            filtered_rows = []
            for r in results:
                filtered_rows.append([
                    r["product"] if r["product"] else "Unknown",
                    r["expiry"],
                    r["quantity"],
                    "-",
                    r["location"]
                ])
        else:
            search_text = search_text.lower()

            # location filter
            if selected == "All Pharmacies":
                filtered_rows = all_rows
            else:
                filtered_rows = [r for r in all_rows if r[4] == selected]

            # text search filter
            if search_text:
                filtered_rows = [
                    r for r in filtered_rows
                    if search_text in str(r[0]).lower()  # product
                       or search_text in str(r[1]).lower()  # expiry
                       or search_text in str(r[2]).lower()  # quantity
                       or search_text in str(r[4]).lower()  # location
                ]

        # updates the table
        self.add_to_top_table(filtered_rows)


MediSend().run()
