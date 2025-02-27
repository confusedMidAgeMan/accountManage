import sys
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
import PyInstaller.config

# 基本配置
block_cipher = None

# 分析程序依赖
a = Analysis(
    ['gui.py'],  # 主程序入口
    pathex=[],
    binaries=[],
    datas=[],    # 添加额外数据文件
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 创建PYZ归档
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# 创建EXE文件
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='账号管理系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为False表示不显示控制台窗口
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # 如果有图标文件的话
) 