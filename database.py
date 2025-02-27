import pandas as pd
from typing import List, Dict
import os

class Database:
    def __init__(self, excel_file: str = "accounts.xlsx"):
        self.excel_file = excel_file
        self.init_database()

    def init_database(self):
        """初始化Excel数据文件"""
        if not os.path.exists(self.excel_file):
            # 创建新的DataFrame并保存为Excel
            df = pd.DataFrame(columns=[
                'id', 'name', 'username', 'encrypted_password',
                'platform', 'category', 'create_time'
            ])
            df.to_excel(self.excel_file, index=False)

    def _read_df(self) -> pd.DataFrame:
        """读取Excel文件"""
        try:
            if not os.path.exists(self.excel_file):
                self.init_database()
            return pd.read_excel(self.excel_file, dtype={
                'id': 'Int64',
                'name': 'str',
                'username': 'str',
                'encrypted_password': 'str',
                'platform': 'str',
                'category': 'str'
            })
        except Exception as e:
            print(f"读取数据文件失败: {str(e)}")
            return pd.DataFrame(columns=[
                'id', 'name', 'username', 'encrypted_password',
                'platform', 'category', 'create_time'
            ])

    def _save_df(self, df: pd.DataFrame):
        """保存DataFrame到Excel"""
        df.to_excel(self.excel_file, index=False)

    def add_account(self, account_data: Dict) -> int:
        """添加新账号"""
        df = self._read_df()
        
        # 生成新的ID
        new_id = 1 if df.empty else df['id'].max() + 1
        
        # 创建新记录
        new_record = {
            'id': int(new_id),  # 确保ID是整数类型
            'name': str(account_data['name']),
            'username': str(account_data['username']),
            'encrypted_password': str(account_data['encrypted_password']),
            'platform': str(account_data['platform']),
            'category': str(account_data['category']) if account_data['category'] else None,
            'create_time': pd.Timestamp.now()
        }
        
        # 添加新记录
        df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)  # 使用concat替代已废弃的append
        self._save_df(df)
        
        return int(new_id)

    def get_all_accounts(self) -> List[Dict]:
        """获取所有账号"""
        df = self._read_df()
        
        if df.empty:
            return []
        
        # 将DataFrame转换为字典列表
        return df.to_dict('records')

    def update_account(self, account_id: int, account_data: Dict) -> bool:
        """更新账号信息"""
        df = self._read_df()
        
        # 查找要更新的记录
        mask = df['id'] == account_id
        if not any(mask):
            return False
        
        # 更新记录
        df.loc[mask, 'name'] = account_data['name']
        df.loc[mask, 'username'] = account_data['username']
        df.loc[mask, 'encrypted_password'] = account_data['encrypted_password']
        df.loc[mask, 'platform'] = account_data['platform']
        df.loc[mask, 'category'] = account_data['category']
        
        self._save_df(df)
        return True

    def delete_account(self, account_id: int) -> bool:
        """删除账号"""
        df = self._read_df()
        
        # 查找要删除的记录
        mask = df['id'] == account_id
        if not any(mask):
            return False
        
        # 删除记录
        df = df[~mask]
        self._save_df(df)
        return True

    def search_accounts(self, keyword: str) -> List[Dict]:
        """搜索账号"""
        df = self._read_df()
        
        if df.empty:
            return []
        
        # 在多个列中搜索关键词
        mask = (
            df['name'].str.contains(keyword, na=False, case=False) |
            df['username'].str.contains(keyword, na=False, case=False) |
            df['platform'].str.contains(keyword, na=False, case=False) |
            df['category'].str.contains(keyword, na=False, case=False)
        )
        
        # 返回匹配的记录
        return df[mask].to_dict('records') 