import os
import shutil
import PyInstaller.__main__

def build_exe():
    # 清理之前的构建文件
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # 创建图标
    try:
        from create_icon import create_icon
        create_icon()
    except Exception as e:
        print(f"创建图标失败: {e}")
    
    # 打包参数
    params = [
        'gui.py',                # 主程序文件
        '--name=账号管理系统',    # 程序名称
        '--windowed',           # 不显示控制台
        '--noconfirm',         # 不确认覆盖
        '--clean',             # 清理临时文件
        '--add-data=README.md;.',  # 添加额外文件
    ]
    
    # 如果存在图标文件，添加图标
    if os.path.exists('icon.ico'):
        params.append('--icon=icon.ico')
    
    # 执行打包
    PyInstaller.__main__.run(params)
    
    print("打包完成！")
    print("可执行文件位于 dist/账号管理系统 目录下")

if __name__ == "__main__":
    build_exe() 