import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# 初始化主窗口
root = tk.Tk()
root.title("DataFrame管理器")
root.geometry("400x200")

# 全局变量存储当前的DataFrame
current_df = None


def read_dataframe():
    global current_df
    file_path = filedialog.askopenfilename(title="选择要读取的文件",
                                           filetypes=(("CSV files", "*.csv"),
                                                      ("Excel files", "*.xlsx;*.xls"),
                                                      ("All files", "*.*")))
    if file_path:
        if file_path.endswith('.csv'):
            current_df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            current_df = pd.read_excel(file_path)
        else:
            messagebox.showerror("错误", "不支持的文件格式")
            return
        messagebox.showinfo("成功", "数据已读取")


def insert_dataframe():
    global current_df
    if current_df is None:
        messagebox.showerror("错误", "请先读取一个数据集")
        return
    insert_path = filedialog.askopenfilename(title="选择要插入的文件",
                                             filetypes=(("CSV files", "*.csv"),
                                                        ("Excel files", "*.xlsx;*.xls"),
                                                        ("All files", "*.*")))
    if insert_path:
        if insert_path.endswith('.csv'):
            new_df = pd.read_csv(insert_path)
        elif insert_path.endswith(('.xlsx', '.xls')):
            new_df = pd.read_excel(insert_path)
        else:
            messagebox.showerror("错误", "不支持的文件格式")
            return
        # 假设按行追加
        current_df = pd.concat([current_df, new_df], ignore_index=True)
        messagebox.showinfo("成功", "数据已插入")


def export_dataframe():
    global current_df
    if current_df is None:
        messagebox.showerror("错误", "没有数据可供导出")
        return
    file_path = filedialog.asksaveasfilename(title="选择保存路径",
                                             defaultextension=".csv",
                                             filetypes=(("CSV files", "*.csv"),
                                                        ("Excel files", "*.xlsx"),
                                                        ("All files", "*.*")))
    if file_path:
        if file_path.endswith('.csv'):
            current_df.to_csv(file_path, index=False)
        elif file_path.endswith('.xlsx'):
            current_df.to_excel(file_path, index=False)
        else:
            messagebox.showerror("错误", "不支持的文件格式")
            return
        messagebox.showinfo("成功", "数据已导出")


# 创建按钮
read_button = tk.Button(root, text="读取数据", command=read_dataframe)
read_button.pack(pady=10)

insert_button = tk.Button(root, text="插入数据", command=insert_dataframe)
insert_button.pack(pady=10)

export_button = tk.Button(root, text="导出数据", command=export_dataframe)
export_button.pack(pady=10)

# 运行主循环
root.mainloop()