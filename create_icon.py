from PIL import Image, ImageDraw, ImageFont

def create_icon():
    # 创建一个 256x256 的图像
    img = Image.new('RGBA', (256, 256), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制一个圆形背景
    draw.ellipse([20, 20, 236, 236], fill='#2196F3')
    
    # 添加文字（如果有中文字体的话）
    try:
        font = ImageFont.truetype("simhei.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    draw.text((85, 70), "账", font=font, fill='white')
    
    # 保存为ico文件
    img.save('icon.ico', format='ICO')

if __name__ == "__main__":
    create_icon() 