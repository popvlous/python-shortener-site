import random
import string

# Image:一個畫布
# ImageDraw:一個畫筆
# ImageFont:畫筆的字體
from PIL import Image, ImageDraw, ImageFont


# Captcha驗證碼
class Captcha(object):
    # 生成4位數的驗證碼
    numbers = 4
    # 驗證碼圖片的寬度和高度
    size = (100, 30)
    # 驗證碼字體大小
    fontsize = 25
    # 加入干擾線的條數
    line_number = 2

    # 構建一個驗證碼源文本
    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))

    # 用來繪製干擾線
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.__gene_random_color(), width=2)

    # 用來繪製干擾點
    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        # 大小限在【0， 100】中
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=cls.__gene_random_color())

    # 生成隨機顏色
    @classmethod
    def __gene_random_color(cls, start=0, end=255):
        random.seed()
        return (random.randint(start, end),
                random.randint(start, end),
                random.randint(start, end))

    # 隨機選擇一個字體
    @classmethod
    def __gene_random_font(cls):
        fonts = [
            "Inkfree.ttf",
            "PAPYRUS.ttf"
            #"Inkfree.ttf",
            #"verdana.ttf",
        ]
        font = random.choice(fonts)
        return "app/util/captcha/"+font

    # 用來隨機生成一個字元串（包括英文和數字）
    @classmethod
    def gene_text(cls, numbers):
        # numbers是生成驗證碼的位數
        return " ".join(random.sample(cls.SOURCE, numbers))

    # 生成驗證碼
    @classmethod
    def gene_graph_captcha(cls):
        # 驗證碼圖片的寬高
        width, height = cls.size
        # 創建圖片
        image = Image.new("RGBA", (width, height), cls.__gene_random_color(0, 100))
        # 驗證碼的字體
        font = ImageFont.truetype(cls.__gene_random_font(), cls.fontsize)
        #font = ImageFont.load_default()
        # 創建畫筆
        draw = ImageDraw.Draw(image)
        # 生成字元串
        text = cls.gene_text(cls.numbers)
        # 獲取字體的尺寸
        font_width, font_height = font.getsize(text)
        # 填充字元串
        draw.text(((width-font_width)/2, (height-font_height)/2),
                  text, font=font, fill=cls.__gene_random_color(150, 255))
        # 繪製干擾線
        for x in range(0, cls.line_number):
            cls.__gene_line(draw, width, height)
        # 繪製干擾點
        # cls.__gene_points(draw, 10, width, height)
        # with open("captcha.png", "wb") as fp:
        #     image.save(fp)
        return text, image
