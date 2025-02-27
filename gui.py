import tkinter as tk
from tkinter import ttk, messagebox
import getpass
from database import Database
from encryption import EncryptionManager

class AccountManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("账号管理系统")
        self.root.geometry("800x600")
        
        self.db = Database()
        self.encryption = EncryptionManager()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建左侧账号列表
        self.create_account_list()
        
        # 创建右侧操作区
        self.create_operation_panel()
        
        # 刷新账号列表
        self.refresh_account_list()

    def create_account_list(self):
        """创建账号列表区域"""
        # 创建列表框架
        list_frame = ttk.LabelFrame(self.main_frame, text="账号列表", padding="5")
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # 创建Treeview
        columns = ("ID", "名称", "登录账号", "平台", "分类")
        self.account_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # 设置列标题
        for col in columns:
            self.account_tree.heading(col, text=col)
            self.account_tree.column(col, width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.account_tree.yview)
        self.account_tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.account_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 搜索框
        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(search_frame, text="搜索:").grid(row=0, column=0, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

    def create_operation_panel(self):
        """创建操作面板"""
        # 创建操作框架
        op_frame = ttk.LabelFrame(self.main_frame, text="操作面板", padding="5")
        op_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # 添加按钮
        ttk.Button(op_frame, text="添加账号", command=self.show_add_dialog).grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
        ttk.Button(op_frame, text="编辑账号", command=self.show_edit_dialog).grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
        ttk.Button(op_frame, text="删除账号", command=self.delete_account).grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)
        ttk.Button(op_frame, text="查看密码", command=self.show_password).grid(row=3, column=0, pady=5, padx=5, sticky=tk.W)
        ttk.Button(op_frame, text="刷新列表", command=self.refresh_account_list).grid(row=4, column=0, pady=5, padx=5, sticky=tk.W)

    def show_add_dialog(self):
        """显示添加账号对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加账号")
        dialog.geometry("300x400")
        dialog.transient(self.root)
        
        # 创建输入框
        ttk.Label(dialog, text="账号名称:").grid(row=0, column=0, pady=5, padx=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(dialog, text="登录账号:").grid(row=1, column=0, pady=5, padx=5)
        username_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=username_var).grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(dialog, text="密码:").grid(row=2, column=0, pady=5, padx=5)
        password_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=password_var, show="*").grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(dialog, text="平台:").grid(row=3, column=0, pady=5, padx=5)
        platform_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=platform_var).grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(dialog, text="分类:").grid(row=4, column=0, pady=5, padx=5)
        category_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=category_var).grid(row=4, column=1, pady=5, padx=5)
        
        ttk.Label(dialog, text="主密钥:").grid(row=5, column=0, pady=5, padx=5)
        master_key_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=master_key_var, show="*").grid(row=5, column=1, pady=5, padx=5)
        
        def save_account():
            try:
                # 获取输入数据
                account_data = {
                    'name': name_var.get(),
                    'username': username_var.get(),
                    'encrypted_password': self.encryption.encrypt_password(
                        password_var.get(), 
                        master_key_var.get()
                    ),
                    'platform': platform_var.get(),
                    'category': category_var.get()
                }
                
                # 保存账号
                self.db.add_account(account_data)
                messagebox.showinfo("成功", "账号添加成功！")
                dialog.destroy()
                self.refresh_account_list()
            except Exception as e:
                messagebox.showerror("错误", f"添加账号失败: {str(e)}")
        
        ttk.Button(dialog, text="保存", command=save_account).grid(row=6, column=0, columnspan=2, pady=20)

    def show_edit_dialog(self):
        """显示编辑账号对话框"""
        selected = self.account_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要编辑的账号")
            return
            
        item = self.account_tree.item(selected[0])
        account_id = item['values'][0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑账号")
        dialog.geometry("300x400")
        dialog.transient(self.root)
        
        # 创建输入框
        ttk.Label(dialog, text="账号名称:").grid(row=0, column=0, pady=5, padx=5)
        name_var = tk.StringVar(value=item['values'][1])
        ttk.Entry(dialog, textvariable=name_var).grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(dialog, text="登录账号:").grid(row=1, column=0, pady=5, padx=5)
        username_var = tk.StringVar(value=item['values'][2])
        ttk.Entry(dialog, textvariable=username_var).grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(dialog, text="新密码:").grid(row=2, column=0, pady=5, padx=5)
        password_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=password_var, show="*").grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(dialog, text="平台:").grid(row=3, column=0, pady=5, padx=5)
        platform_var = tk.StringVar(value=item['values'][3])
        ttk.Entry(dialog, textvariable=platform_var).grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(dialog, text="分类:").grid(row=4, column=0, pady=5, padx=5)
        category_var = tk.StringVar(value=item['values'][4])
        ttk.Entry(dialog, textvariable=category_var).grid(row=4, column=1, pady=5, padx=5)
        
        ttk.Label(dialog, text="主密钥:").grid(row=5, column=0, pady=5, padx=5)
        master_key_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=master_key_var, show="*").grid(row=5, column=1, pady=5, padx=5)
        
        def update_account():
            try:
                # 获取输入数据
                account_data = {
                    'name': name_var.get(),
                    'username': username_var.get(),
                    'encrypted_password': self.encryption.encrypt_password(
                        password_var.get(), 
                        master_key_var.get()
                    ),
                    'platform': platform_var.get(),
                    'category': category_var.get()
                }
                
                # 更新账号
                if self.db.update_account(account_id, account_data):
                    messagebox.showinfo("成功", "账号更新成功！")
                    dialog.destroy()
                    self.refresh_account_list()
                else:
                    messagebox.showerror("错误", "账号更新失败")
            except Exception as e:
                messagebox.showerror("错误", f"更新账号失败: {str(e)}")
        
        ttk.Button(dialog, text="保存", command=update_account).grid(row=6, column=0, columnspan=2, pady=20)

    def delete_account(self):
        """删除选中的账号"""
        selected = self.account_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的账号")
            return
            
        if messagebox.askyesno("确认", "确定要删除选中的账号吗？"):
            item = self.account_tree.item(selected[0])
            account_id = item['values'][0]
            
            if self.db.delete_account(account_id):
                messagebox.showinfo("成功", "账号删除成功！")
                self.refresh_account_list()
            else:
                messagebox.showerror("错误", "账号删除失败")

    def show_password(self):
        """显示选中账号的密码"""
        selected = self.account_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要查看的账号")
            return
            
        item = self.account_tree.item(selected[0])
        account_id = item['values'][0]
        
        # 获取账号信息
        accounts = self.db.get_all_accounts()
        account = next((acc for acc in accounts if acc['id'] == account_id), None)
        
        if not account:
            messagebox.showerror("错误", "未找到账号信息")
            return
            
        # 创建密码查看对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("查看密码")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        
        ttk.Label(dialog, text="请输入主密钥:").grid(row=0, column=0, pady=5, padx=5)
        master_key_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=master_key_var, show="*").grid(row=0, column=1, pady=5, padx=5)
        
        def show_decrypted_password():
            try:
                password = self.encryption.decrypt_password(
                    account['encrypted_password'],
                    master_key_var.get()
                )
                result_text = f"账号名称: {account['name']}\n"
                result_text += f"登录账号: {account['username']}\n"
                result_text += f"平台: {account['platform']}\n"
                result_text += f"密码: {password}"
                
                messagebox.showinfo("账号信息", result_text)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"解密失败: {str(e)}")
        
        ttk.Button(dialog, text="确认", command=show_decrypted_password).grid(row=1, column=0, columnspan=2, pady=20)

    def refresh_account_list(self):
        """刷新账号列表"""
        # 清空现有项目
        for item in self.account_tree.get_children():
            self.account_tree.delete(item)
        
        # 获取并显示账号列表
        accounts = self.db.get_all_accounts()
        for account in accounts:
            self.account_tree.insert('', 'end', values=(
                account['id'],
                account['name'],
                account['username'],
                account['platform'],
                account['category'] if account['category'] else "无分类"
            ))

    def on_search(self, *args):
        """搜索功能"""
        keyword = self.search_var.get()
        if not keyword:
            self.refresh_account_list()
            return
            
        # 清空现有项目
        for item in self.account_tree.get_children():
            self.account_tree.delete(item)
        
        # 搜索并显示结果
        accounts = self.db.search_accounts(keyword)
        for account in accounts:
            self.account_tree.insert('', 'end', values=(
                account['id'],
                account['name'],
                account['username'],
                account['platform'],
                account['category'] if account['category'] else "无分类"
            ))

def main():
    root = tk.Tk()
    app = AccountManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 