from database import Database
from encryption import EncryptionManager
import getpass
import sys

class AccountManager:
    def __init__(self):
        self.db = Database()
        self.encryption = EncryptionManager()

    def show_menu(self):
        """显示主菜单"""
        print("\n=== 账号管理系统 ===")
        print("1. 添加账号")
        print("2. 查看所有账号")
        print("3. 编辑账号")
        print("4. 删除账号")
        print("5. 搜索账号")
        print("6. 查看密码")
        print("0. 退出")
        return input("请选择操作 (0-6): ")

    def add_account(self):
        """添加新账号"""
        print("\n=== 添加新账号 ===")
        name = input("账号名称: ")
        username = input("登录账号: ")
        password = getpass.getpass("密码: ")
        platform = input("所属平台: ")
        category = input("分类标签: ")
        
        # 获取主密钥并加密密码
        master_key = getpass.getpass("请输入主密钥用于加密: ")
        encrypted_password = self.encryption.encrypt_password(password, master_key)
        
        account_data = {
            'name': name,
            'username': username,
            'encrypted_password': encrypted_password,
            'platform': platform,
            'category': category
        }
        
        self.db.add_account(account_data)
        print("账号添加成功！")

    def list_accounts(self):
        """列出所有账号"""
        accounts = self.db.get_all_accounts()
        if not accounts:
            print("\n暂无账号记录")
            return
        
        print("\n=== 账号列表 ===")
        print("\n{:<5} {:<15} {:<20} {:<15} {:<15}".format(
            "ID", "账号名称", "登录账号", "平台", "分类"))
        print("-" * 70)
        
        for account in accounts:
            try:
                print("{:<5} {:<15} {:<20} {:<15} {:<15}".format(
                    str(account['id']),
                    account['name'][:15],
                    account['username'][:20],
                    account['platform'][:15],
                    account['category'][:15] if account['category'] else "无分类"
                ))
            except Exception as e:
                print(f"显示账号时出错: {str(e)}")
                continue

    def edit_account(self):
        """编辑账号"""
        self.list_accounts()
        account_id = input("\n请输入要编辑的账号ID: ")
        
        name = input("新账号名称: ")
        username = input("新登录账号: ")
        password = getpass.getpass("新密码: ")
        platform = input("新所属平台: ")
        category = input("新分类标签: ")
        
        master_key = getpass.getpass("请输入主密钥用于加密: ")
        encrypted_password = self.encryption.encrypt_password(password, master_key)
        
        account_data = {
            'name': name,
            'username': username,
            'encrypted_password': encrypted_password,
            'platform': platform,
            'category': category
        }
        
        if self.db.update_account(int(account_id), account_data):
            print("账号更新成功！")
        else:
            print("账号更新失败，请检查ID是否正确。")

    def delete_account(self):
        """删除账号"""
        self.list_accounts()
        account_id = input("\n请输入要删除的账号ID: ")
        confirm = input("确认删除？(y/n): ")
        
        if confirm.lower() == 'y':
            if self.db.delete_account(int(account_id)):
                print("账号删除成功！")
            else:
                print("账号删除失败，请检查ID是否正确。")

    def search_accounts(self):
        """搜索账号"""
        keyword = input("\n请输入搜索关键词: ")
        accounts = self.db.search_accounts(keyword)
        
        if not accounts:
            print("未找到匹配的账号")
            return
        
        print("\n=== 搜索结果 ===")
        for account in accounts:
            print(f"\nID: {account['id']}")
            print(f"名称: {account['name']}")
            print(f"登录账号: {account['username']}")
            print(f"平台: {account['platform']}")
            print(f"分类: {account['category']}")

    def view_password(self):
        """查看密码"""
        self.list_accounts()
        try:
            account_id = int(input("\n请输入要查看密码的账号ID: "))
            accounts = self.db.get_all_accounts()
            
            account = next((acc for acc in accounts if acc['id'] == account_id), None)
            if not account:
                print("未找到该账号")
                return
            
            master_key = getpass.getpass("请输入主密钥以解密密码: ")
            try:
                password = self.encryption.decrypt_password(
                    account['encrypted_password'], 
                    master_key
                )
                print(f"\n账号信息:")
                print(f"名称: {account['name']}")
                print(f"登录账号: {account['username']}")
                print(f"平台: {account['platform']}")
                print(f"密码: {password}")
            except ValueError as e:
                print(f"解密失败: {str(e)}")
            except Exception as e:
                print(f"查看密码时出错: {str(e)}")
        except ValueError:
            print("请输入有效的账号ID")
        except Exception as e:
            print(f"操作失败: {str(e)}")

def main():
    manager = AccountManager()
    
    while True:
        choice = manager.show_menu()
        
        if choice == '1':
            manager.add_account()
        elif choice == '2':
            manager.list_accounts()
        elif choice == '3':
            manager.edit_account()
        elif choice == '4':
            manager.delete_account()
        elif choice == '5':
            manager.search_accounts()
        elif choice == '6':
            manager.view_password()
        elif choice == '0':
            print("\n感谢使用，再见！")
            sys.exit(0)
        else:
            print("\n无效的选择，请重试")

if __name__ == "__main__":
    main() 