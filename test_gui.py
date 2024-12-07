import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd


class Data_manager:
    def __init__(self, data=None):
        if data is not None:
            self.df = data
        else:
            self.df = pd.DataFrame()

    def read(self, file_path):
        self.df = pd.read_csv(file_path)

    def export(self, file_path):
        self.df.to_csv(file_path, index=False)

    def insert(self, data_dict):
        new_row = pd.DataFrame([data_dict])
        self.df = pd.concat([self.df, new_row], ignore_index=True)

    def search(self, column, value):
        return self.df[self.df[column] == value]

    def sort(self, column, ascending=True):
        self.df = self.df.sort_values(by=column, ascending=ascending)


# 创建主窗口
root = tk.Tk()
root.title("Data Manager GUI")

# 创建菜单栏
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# 创建文件菜单
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="文件", menu=file_menu)
file_menu.add_command(label="读取数据", command=lambda: read_data())
file_menu.add_command(label="导出数据", command=lambda: export_data())
file_menu.add_separator()
file_menu.add_command(label="退出", command=root.quit)

# 创建编辑菜单
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="编辑", menu=edit_menu)
edit_menu.add_command(label="插入数据", command=lambda: insert_data())
edit_menu.add_command(label="查找数据", command=lambda: search_data())

# 创建查看菜单
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="查看", menu=view_menu)
view_menu.add_command(label="排序数据", command=lambda: sort_data())

# 创建Treeview来显示数据
tree = ttk.Treeview(root)
tree.pack(fill='both', expand=True)

data_manager = Data_manager()


def read_data():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        data_manager.read(file_path)
        display_data(data_manager.df)


def export_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        data_manager.export(file_path)
        messagebox.showinfo("导出成功", "数据已导出到 {}".format(file_path))


def insert_data():
    insert_window = tk.Toplevel(root)
    insert_window.title("插入数据")

    columns = data_manager.df.columns
    entries = {}
    for col in columns:
        tk.Label(insert_window, text=col).pack()
        entry = tk.Entry(insert_window)
        entry.pack()
        entries[col] = entry

    def save_data():
        data_dict = {col: entry.get() for col, entry in entries.items()}
        data_manager.insert(data_dict)
        display_data(data_manager.df)
        insert_window.destroy()

    tk.Button(insert_window, text="保存", command=save_data).pack()


def search_data():
    search_window = tk.Toplevel(root)
    search_window.title("查找数据")

    column_var = tk.StringVar()
    column_var.set(data_manager.df.columns[0])
    column_menu = tk.OptionMenu(search_window, column_var, *data_manager.df.columns)
    column_menu.pack()

    value_entry = tk.Entry(search_window)
    value_entry.pack()

    def do_search():
        column = column_var.get()
        value = value_entry.get()
        result_df = data_manager.search(column, value)
        display_data(result_df)
        search_window.destroy()

    tk.Button(search_window, text="查找", command=do_search).pack()


def sort_data():
    sort_window = tk.Toplevel(root)
    sort_window.title("排序数据")

    column_var = tk.StringVar()
    column_var.set(data_manager.df.columns[0])
    column_menu = tk.OptionMenu(sort_window, column_var, *data_manager.df.columns)
    column_menu.pack()

    order_var = tk.BooleanVar()
    tk.Radiobutton(sort_window, text="升序", variable=order_var, value=True).pack()
    tk.Radiobutton(sort_window, text="降序", variable=order_var, value=False).pack()

    def do_sort():
        column = column_var.get()
        ascending = order_var.get()
        data_manager.sort(column, ascending)
        display_data(data_manager.df)
        sort_window.destroy()

    tk.Button(sort_window, text="排序", command=do_sort).pack()


def display_data(df):
    for item in tree.get_children():
        tree.delete(item)

    tree["columns"] = list(df.columns)
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))


root.mainloop()