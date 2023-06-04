from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QGroupBox, QPushButton, QLabel, QListWidget, QLineEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QImage, QResizeEvent
from PIL import ImageQt
import photo_editor
import os
from style import themes


app = QApplication([])

# main window
main_win = QWidget()
main_win.setStyleSheet(themes["main"])
main_win.setWindowTitle('Easy Editor')
main_win.resize(800, 500)



main_layout = QHBoxLayout()

layout_work_with_folder = QVBoxLayout()
button_open_folder = QPushButton("Папка")
button_save_file = QPushButton("Зберегти")
list_photos = QListWidget()
layout_work_with_folder.addWidget(button_open_folder)
layout_work_with_folder.addWidget(button_save_file)
layout_work_with_folder.addWidget(list_photos)

button_layout = QVBoxLayout()

first_row = QHBoxLayout()
button_rotate_left = QPushButton("Вліво")
button_rotate_right = QPushButton("Вправо")   # 90°
button_set_black_white = QPushButton("Ч/Б")
button_blur = QPushButton("Розмити")
first_row.addWidget(button_rotate_left)
first_row.addWidget(button_rotate_right)
first_row.addWidget(button_set_black_white)
first_row.addWidget(button_blur)


second_row = QHBoxLayout()
groupbox_mirror = QGroupBox("Відобразити дзеркально")
layout_mirror = QVBoxLayout()
button_revers_vertical = QPushButton("Дзеркально по вертикалі")
button_revers_horizontal = QPushButton("Дзеркально по горизонталі")
layout_mirror.addWidget(button_revers_vertical)
layout_mirror.addWidget(button_revers_horizontal)
groupbox_mirror.setLayout(layout_mirror)

groupbox_contrast = QGroupBox("Змінити контраст")
layout_contrast = QVBoxLayout()
field_contrast = QLineEdit()
field_contrast.setPlaceholderText("Введіть контраст:")
button_set_contrast = QPushButton("Застосувати")
layout_contrast.addWidget(field_contrast)
layout_contrast.addWidget(button_set_contrast)
groupbox_contrast.setLayout(layout_contrast)

groupbox_reset = QGroupBox("Відмінити")
layout_reset = QVBoxLayout()
button_reset_one_work = QPushButton("Скасувати останню дію")
button_reset_all_works = QPushButton("Відновити оригінал")
layout_reset.addWidget(button_reset_one_work)
layout_reset.addWidget(button_reset_all_works)
groupbox_reset.setLayout(layout_reset)

second_row.addWidget(groupbox_mirror)
second_row.addWidget(groupbox_contrast)
second_row.addWidget(groupbox_reset)

button_layout.addLayout(first_row)
button_layout.addLayout(second_row)

layout_redactor = QVBoxLayout()
photo_place = QLabel(alignment=Qt.AlignCenter)
photo_place.setStyleSheet(themes["photo_place"])
layout_redactor.addWidget(photo_place, stretch=4)
layout_redactor.addLayout(button_layout, stretch=1)


main_layout.addLayout(layout_work_with_folder, stretch=1)
main_layout.addLayout(layout_redactor, stretch=3)
main_win.setLayout(main_layout)

editor = None

def show_mess(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle('Easy Editor')
    msg.exec_()
def show_warning(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle('Easy Editor')
    msg.exec_()


# dirname = "D:/Nazar/Logika/lessons_11_my_variant/images"
# for file in os.listdir(dirname):
#     if os.path.isfile(f"{dirname}/{file}"):
#         if file.endswith((".jpg", ".png")):
#             list_photos.addItem(file)
dirname = None

def scan_dir():
    files = os.listdir(dirname)
    list_photos.clear()
    for file in files:
        if os.path.isfile(f"{dirname}/{file}"):
            if file.endswith((".jpg", ".png")):
                list_photos.addItem(file)

def open_folder():
    if editor:
        check_edited_photo()
        return
    global dirname
    dirname_or_none = QFileDialog.getExistingDirectory(None, "Оберіть папку з фото")
    if dirname_or_none:
        photo_place.setPixmap(QPixmap())
        dirname = dirname_or_none
        scan_dir()
        if not list_photos.count():
            show_mess("В даній папці зображення відсуні!")
    else:
        show_mess("Ви не обрали папку!")

def save_file():
    global editor
    if editor:
        filepath, check = QFileDialog.getSaveFileName(None, "Збереження фото", "", "Image (*.jpg)") # ;;Image (*.png)
        if check:
            editor.new_image.save(filepath)
            # set_photo(QPixmap(editor.path))
            set_photo(QPixmap())
            editor = None
            scan_dir()
            show_mess(f"Збережено успішно!\nШлях - {filepath}")
    else:
        show_mess("Фото не редагувалося!")


def qwestion_save_or_not():
    global editor
    msg = QMessageBox()
    msg.setWindowTitle("Easy Editor")
    msg.setIcon(QMessageBox.Question)
    msg.setText("Чи бажаєте ви зберегти відредаговане фото?\nЦе фото зараз на екрані.")
    msg.setDetailedText("Save - збереження\nNo - редагування стирається\nCancel - не зберігати і не стирати\nЗакриття вікна - не зберігати і не стирати")
    msg.setStandardButtons(QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)
    result = msg.exec_()
    if result == QMessageBox.Save:
        save_file()
    elif result == QMessageBox.No:
        image = QPixmap(editor.path)
        set_photo(image)
        editor = None
def check_edited_photo():
    items = list_photos.findItems(editor.filename, Qt.MatchExactly)
    if items:
        item = items[0]
        list_photos.setCurrentItem(item)
        set_pillow_photo()
    qwestion_save_or_not()
    

def set_photo(image):
    if image.width() > photo_place.width() or image.height() > photo_place.height():
        image = image.scaled(photo_place.width()-5, photo_place.height()-5, Qt.KeepAspectRatio)
    photo_place.setPixmap(image)                                          # KeepAspectRatio - зберегти співвідношення сторін
def set_pillow_photo():
    # new_image = ImageQt.toqpixmap(editor.new_image)                             # don't work
    # new_image = QPixmap.fromImage( ImageQt.ImageQt(editor.new_image) )          # don't work
    new_image = editor.new_image.convert("RGBA")                                  # the most important command !!!
    new_image = ImageQt.ImageQt( new_image )
    new_image = QPixmap( QImage( new_image ) )
    set_photo(new_image)


def show_photo():
    if list_photos.selectedItems():
        photoname = list_photos.selectedItems()[0].text()
        if editor:
            if photoname == editor.filename:
                set_pillow_photo()
                return
        image = QPixmap(f"{dirname}/{photoname}")
        set_photo(image)


def check(function):
    def wrapper():
        global editor
        if list_photos.selectedItems():
            photoname = list_photos.selectedItems()[0].text()
            if not editor:
                editor = photo_editor.ImageEditor(f"{dirname}/{photoname}")
            elif editor.filename != photoname:
                check_edited_photo()
                return
            function()
            set_pillow_photo()    
        else:
            show_mess("Ви не обрали фото!")
    return wrapper


@check
def rotate_left():
    editor.rotate(90)
@check
def rotate_right():
    editor.rotate(-90)
@check
def do_black_white():
    editor.do_black_white()
@check
def do_mirror_vertical():
    editor.do_mirror("v")
@check
def do_mirror_horizontal():
    editor.do_mirror("h")
@check
def contrast():
    contrast = field_contrast.text()
    try:
        contrast = contrast.replace(",", ".")
        contrast = float(contrast)
        editor.contrast(contrast) 
    except:
        show_warning("Дані некоректні!")
        field_contrast.setFocus()
        field_contrast.selectAll()
@check
def blur():
    editor.blur()
@check
def reset_one_work():
    editor.cancel_one_work()
@check
def reset_all_works():
    global editor
    msg = QMessageBox()
    msg.setWindowTitle("Easy Editor")
    msg.setIcon(QMessageBox.Question)
    msg.setText("Ви впевнені, що хочете скинути все редагування?\nЦя дія незворотна!!!")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
    result = msg.exec_()
    if result == QMessageBox.Yes:
        editor.reset_all()


button_open_folder.clicked.connect(open_folder)
button_save_file.clicked.connect(save_file)
button_rotate_left.clicked.connect(rotate_left)
button_rotate_right.clicked.connect(rotate_right)
button_set_black_white.clicked.connect(do_black_white)
button_revers_vertical.clicked.connect(do_mirror_vertical)
button_revers_horizontal.clicked.connect(do_mirror_horizontal)
button_set_contrast.clicked.connect(contrast)
list_photos.itemClicked.connect(show_photo)
button_blur.clicked.connect(blur)
button_reset_one_work.clicked.connect(reset_one_work)
button_reset_all_works.clicked.connect(reset_all_works)


main_win.show()
app.exec_()



# Pillow-9.1.0 - was

# Pillow-9.4.0 - current version