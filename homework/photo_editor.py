from PIL import Image, ImageEnhance, ImageFilter
import os


class ImageEditor():
    def __init__(self, path: str):
        self.path = path
        self.filename = os.path.basename(path)
        self.original = None
        self.new_image = None
        self.original_contrast = None
        self.works = []
        self.save_history = True
        self.a = {
            "L": self.do_black_white,
            "blur": self.blur,
            "mirror": self.do_mirror,
            "rotate": self.rotate,
            "contrast": self.contrast
        }
        self.open()

    def restart_works(self):
        self.new_image = self.original
        for work in self.works:
            if type(work) == tuple:
                self.a[ work[0] ]( work[1] )
            else:
                self.a[ work ]()

    def cancel_one_work(self):
        if self.works:
            self.save_history = False
            work = self.works.pop()
            if type(work) == tuple:
                if work[0] == "mirror":
                    self.a["mirror"](work[1])
                elif work[0] == "contrast":
                    self.restart_works()
                elif work[0] == "rotate":
                    self.a["rotate"](-work[1])
            elif work == "L" or work == "blur":
                self.restart_works()
            self.save_history = True
    
    def reset_all(self):
        self.new_image = self.original
        self.works.clear()


    def add_to_history(name):
        def wrapper_1(function):
            def wrapper_2(self, *args):
                if args:
                    function(self, *args)
                    if self.save_history:
                        self.works.append((name, *args))
                else:
                    function(self)
                    if self.save_history:
                        self.works.append(name)
            return wrapper_2
        return wrapper_1
        

    def open(self):
        try:
            self.new_image = self.original = Image.open(self.path)
            # self.original.show()
        except:
            print("Файл не знайдено!")
            exit()

    @add_to_history('L')
    def do_black_white(self):
        self.new_image = self.new_image.convert('L')
        # self.new_image.show()


    @add_to_history("blur")
    def blur(self):
        self.new_image = self.new_image.filter(ImageFilter.BLUR)
        # self.new_image.show()
        
    
    @add_to_history("mirror")
    def do_mirror(self, direction="vertical"):
        """
        direction
        'vertical' or 'v'
        'horizontal' or 'h'
        """
        if direction.lower() == "vertical" or direction.lower() == "v":
            self.new_image = self.new_image.transpose(Image.FLIP_LEFT_RIGHT)
            # self.new_image.show()
        elif direction.lower() == "horizontal" or direction.lower() == "h":
            self.new_image = self.new_image.transpose(Image.FLIP_TOP_BOTTOM)
            # self.new_image.show()
        return "error"

    @add_to_history("contrast")
    def contrast(self, contrast=1):
        """
        contrast
        Тоді як коефіцієнт 1 дає оригінальне зображення. 
        Зменшення коефіцієнта до 0 робить зображення сірішим *, 
        Тоді як коефіцієнт > 1 збільшує контрастність зображення.
        """
        pic_contrast = ImageEnhance.Contrast(self.new_image)
        self.new_image = pic_contrast.enhance(contrast)
        # self.new_image.show()
    
    @add_to_history("rotate")
    def rotate(self, angle):
        self.new_image = self.new_image.rotate(angle, expand=True)
        # self.new_image.show()
    
    @add_to_history("crop")
    def do_cropped(self, box):
        self.new_image = self.new_image.crop(box) # (left, top, right, bottom)
        # self.new_image.show()
        

img = ImageEditor("images/new.jpg")

# img.rotate()
# img.new_image.show()
# img.rotate()
# img.new_image.show()

# img.do_black_white()
# img.new_image.show()

# img.new_image.show()
# img.blur()
# img.new_image.show()
# # img.rotate(180)
# img.contrast(2)
# img.new_image.show()
# img.cancel_one_work()
# img.new_image.show()
