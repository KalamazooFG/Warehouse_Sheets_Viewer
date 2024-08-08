import tkinter as tk
from utils.config import *
from utils.logger import logging

class MainWindow:
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager
        self.labels = []

    def setup(self):
        self.root.geometry('1920x1080')
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', self.stop_application)

        df = self.data_manager.get_data()
        max_rows = self.root.winfo_screenheight() // 30
        self.create_labels(df, max_rows)
        self.refresh_grid(max_rows)

    def create_labels(self, df, max_rows):
        if df is None or df.empty:
            logging.error('The DataFrame is None or empty in create_labels.')
            return

        num_rows = min(df.shape[0] + 1, max_rows)
        num_columns = df.shape[1]
        
        for column in range(num_columns):
            cell_data = str(df.columns[column])
            label = tk.Label(self.root, text=cell_data, font=('Arial', 40, 'bold'), bg='black', fg='white', bd=1, relief='solid', justify='center',padx=10)  
            label.grid(row=0, column=column, sticky="nsew")
            self.root.grid_columnconfigure(column, weight=1)  
        
        even_column_colors = ['#6D9DE9', '#CAD7F7', '#92C47D', '#D8EAD2', '#FF9A00','#F9CA9C', '#FFFF01','#FFF2CD']
        
        for row in range(1, num_rows):
            row_labels = [] 
            
            for column in range(num_columns):
                cell_data = str(df.iloc[row-1, column])
                
                if 'new load' in cell_data:
                    label = tk.Label(self.root, text="nload", bg='#BF40BF', fg='#BF40BF', bd=1, relief='solid',justify='center',padx=10)  
                elif 'clear' in cell_data.lower():
                    label = tk.Label(self.root, text="clear", bg='#EBEEED', fg='#EBEEED', bd=1, relief='solid',justify='center',padx=10)
                elif 'load' in cell_data.lower():
                    label = tk.Label(self.root, text="loads", bg='#66ff00', fg='#66ff00', bd=1, relief='solid',justify='center',padx=10)
                elif 'stop' in cell_data.lower():
                    label = tk.Label(self.root, text="stops", bg='#EE4B2B', fg='#EE4B2B', bd=1, relief='solid',justify='center',padx=10)
                elif 'caution' in cell_data.lower():
                    label = tk.Label(self.root, text="cauti", bg='FFFF00' , fg='FFFF00',  bd=1, relief='solid',justify='center',padx=10)
                else:
                    label = tk.Label(self.root, text=cell_data, font=('Helvetica ', 65, 'bold'), bd=1, relief='solid',justify='center',padx=6)  
                
                if column in [3, 7, 11]:
                    label.configure(bg='black', bd=0, relief='flat')  

                label.grid(row=row, column=column, sticky="nsew")
                row_labels.append(label) 
                
                if column % 2 == 0:
                    color_index = (column // 2) % len(even_column_colors)
                    even_column_color = even_column_colors[color_index]
                    label.configure(bg=even_column_color)  
                    
                    self.root.grid_columnconfigure(column, weight=4) 
                else:
                    self.root.grid_columnconfigure(column, weight=1) 

            self.labels.append(row_labels)

        for row in range(num_rows):
            self.root.grid_rowconfigure(row, weight=1)

    def update_labels(self, df):
        if df is None or df.empty:
            logging.error('The DataFrame is None or empty in update_labels.')
            return
        num_rows, num_columns = df.shape
        
        for row in range(min(num_rows, len(self.labels))):
            for column in range(min(num_columns, len(self.labels[row]))):
                cell_data = str(df.iloc[row, column])
                label = self.labels[row][column]
                
                if 'new load' in cell_data:
                    label.configure(bg='#BF40BF', text=" ")
                elif 'clear' in cell_data.lower():
                    label.configure(bg='#EBEEED', text=" ")
                elif 'load' in cell_data.lower():
                    label.configure(bg='#66ff00', text=" ")
                elif 'stop' in cell_data.lower():
                    label.configure(bg='#EE4B2B', text=" ")
                elif 'caution' in cell_data.lower():
                    label.configure(bg='#FFFF00', text=" ")
                else:
                    label.configure(text=cell_data)

    def refresh_grid(self, max_rows):
        try:
            df = self.data_manager.get_data()
            if df is not None:
                self.update_labels(df)
            self.root.after(REFRESH_RATE, self.refresh_grid, max_rows)
        except Exception as e:
            logging.error(f"Error occurred in refresh_grid: {e}")

    def stop_application(self, event):
        self.root.quit()
