from os import chdir, path, remove
from pathlib import Path

from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

from set_vars import ABOOK, ConfSets, cs_conf_path, refresh_profiles
from configs import edit_config

# Data Path VARS;
dir_path = Path.cwd()
chdir(dir_path)

# Global's Var's;
abook_path = "None"
mv_conf_path = "None"

# (Окно ABook) Инициализация GUI;
Form, Window = uic.loadUiType("bin/ui/abook.ui")
app = QApplication([])
window4 = Window()
form4 = Form()
form4.setupUi(window4)
window4.setFixedSize(285, 285)
# Задаем размер Столбцов;
form4.tableWidget.setColumnWidth(0, 130)
form4.tableWidget.setColumnWidth(1, 45)
form4.tableWidget.setColumnWidth(2, 75)
# Column count;
# form4.tableWidget.setColumnCount(3)
# Row count;
# form4.tableWidget.setRowCount(0)

# (Окно ABook) - Add;
Form, Window = uic.loadUiType("bin/ui/ab_add_item.ui")
window5 = Window()
form5 = Form()
form5.setupUi(window5)
window5.setFixedSize(217, 135)

# (Окно ABook) - Edit;
Form, Window = uic.loadUiType("bin/ui/ab_edit_item.ui")
window6 = Window()
form6 = Form()
form6.setupUi(window6)
window6.setFixedSize(217, 135)

# (Окно ABook) - Add Profile;
Form, Window = uic.loadUiType("bin/ui/ab_add_profile.ui")
window7 = Window()
form7 = Form()
form7.setupUi(window7)
window7.setFixedSize(217, 80)

# (Окно ABook) - Edit Profile;
Form, Window = uic.loadUiType("bin/ui/ab_edit_profile.ui")
window8 = Window()
form8 = Form()
form8.setupUi(window8)
window8.setFixedSize(217, 80)


class Tools:
    # Создание файла таблицы ABook;
    @staticmethod
    def create_abook() -> None:
        global abook_path, mv_conf_path
        # Очищаем таблицу от строк;
        form4.tableWidget.setRowCount(0)

        # Обновление данных с нужного конфига;
        refresh_profiles(cs_conf_path, "ConfSets")
        mv_conf_path = Path(f"conf/{ConfSets.profiles[ConfSets.index]}/mv.ini")

        refresh_profiles(mv_conf_path, "ABOOK")
        abook_path = Path(f"conf/{ConfSets.profiles[ConfSets.index]}/{ABOOK.profiles[ABOOK.index]}.mv")
        if not Path(abook_path).exists():
            abook_path.parent.mkdir(parents=False, exist_ok=True)
            with open(abook_path, "w", encoding="utf8"):
                pass

    # Установка местоположения дочернего окна на базе местоположения родительского;
    @staticmethod
    def set_child_window_pos(child_window: any, parent_window: any) -> None:
        child_window.move(parent_window.pos().x() + 20, parent_window.pos().y() + 20)

    # Подсчет количества строк;
    @staticmethod
    def counting_rows(cr: any) -> None:
        form4.label_total_row.setText(f"Всего: {cr}")

    # Сортируем по 1 столбцу, используем после заполнения данными;
    @staticmethod
    def sort_items() -> None:
        # form4.tableWidget.setSortingEnabled(True)
        form4.tableWidget.sortItems(0, Qt.SortOrder.AscendingOrder)


class Window:
    @staticmethod
    def show_add_item() -> None:
        # Очищаем от предыдущих введенных данных;
        form5.lineEdit_name.setText("")
        form5.lineEdit_id.setText("")
        form5.lineEdit_pw.setText("")

        window5.show()
        Tools.set_child_window_pos(window5, window4)

    @staticmethod
    def close_add_item() -> None:
        window5.close()

    @staticmethod
    def show_edit_item() -> None:
        row_position = form4.tableWidget.currentRow()

        try:
            line_name = form4.tableWidget.item(row_position, 0).text()
            line_id = form4.tableWidget.item(row_position, 1).text()
            line_pw = form4.tableWidget.item(row_position, 2).text()

            form6.lineEdit_name.setText(line_name)
            form6.lineEdit_id.setText(line_id)
            form6.lineEdit_pw.setText(line_pw)
            window6.show()
            Tools.set_child_window_pos(window6, window4)
        except AttributeError:
            pass

    @staticmethod
    def close_edit_item() -> None:
        window6.close()

    @staticmethod
    def show_add_profile() -> None:
        # Очищаем от предыдущих введенных данных;
        form7.lineEdit_name.setText("")

        window7.show()
        Tools.set_child_window_pos(window7, window4)

    @staticmethod
    def close_add_profile() -> None:
        window7.close()

    @staticmethod
    def show_edit_profile() -> None:
        profile_name = form4.comboBox_profiles.currentText()

        form8.lineEdit_name.setText(profile_name)

        window8.show()
        Tools.set_child_window_pos(window8, window4)

    @staticmethod
    def close_edit_profile() -> None:
        window8.close()


class Table:
    @staticmethod
    def add_row() -> None:
        line_name = form5.lineEdit_name.text()
        # Удаляем пробелы перед добавлением записи;
        line_id = (form5.lineEdit_id.text()).replace(" ", "")
        line_pw = (form5.lineEdit_pw.text()).replace(" ", "")

        # Проверка, чтобы строка была не пустой;
        if line_name and line_id and line_pw:
            row_position = form4.tableWidget.rowCount()
            form4.tableWidget.insertRow(row_position)

            form4.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(line_name))
            form4.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(line_id))
            form4.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(line_pw))

            with open(abook_path, "a", encoding="utf8") as file:
                file.write(f"{line_name},,,{line_id},,,{line_pw}\n")

            Tools.sort_items()
            Tools.counting_rows(form4.tableWidget.rowCount())
            window5.close()

    @staticmethod
    def edit_row() -> None:
        row_position = form4.tableWidget.currentRow()

        line_name = form4.tableWidget.item(row_position, 0).text()
        line_id = form4.tableWidget.item(row_position, 1).text()
        line_pw = form4.tableWidget.item(row_position, 2).text()

        with open(abook_path, "r", encoding="utf8") as file:
            new_f = file.readlines()
            # 0 - Начало отсчета;
            for num, line in enumerate(new_f, 0):
                if f"{line_name},,,{line_id},,,{line_pw}" in line:
                    match = num
                    break

        new_line_name = form6.lineEdit_name.text()
        # Удаляем пробелы перед обновлением записи;
        new_line_id = (form6.lineEdit_id.text()).replace(" ", "")
        new_line_pw = (form6.lineEdit_pw.text()).replace(" ", "")

        # Проверка, чтобы строка была не пустой;
        if new_line_name and new_line_id and new_line_pw:
            new_f[match] = f"{new_line_name},,,{new_line_id},,,{new_line_pw}\n"

            with open(abook_path, "w", encoding="utf8") as file2:
                file2.writelines(new_f)

            form4.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(new_line_name))
            form4.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(new_line_id))
            form4.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(new_line_pw))

            Tools.sort_items()
            window6.close()

    # Удаление по номеру строки;
    @staticmethod
    def delete_row() -> None:
        row_position = form4.tableWidget.currentRow()

        if row_position != -1:
            ques_out = QMessageBox.question(window4, "microViewer: Удалить запись", "Действительно удалить запись?",
                                            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if ques_out == QMessageBox.StandardButton.Ok:

                line_name = form4.tableWidget.item(row_position, 0).text()
                line_id = form4.tableWidget.item(row_position, 1).text()
                line_pw = form4.tableWidget.item(row_position, 2).text()

                form4.tableWidget.removeRow(row_position)

                with open(abook_path, "r+", encoding="utf8") as file:
                    new_f = file.readlines()
                    file.seek(0)
                    for line in new_f:
                        if f"{line_name},,,{line_id},,,{line_pw}" not in line:
                            file.write(line)
                    file.truncate()

                Tools.counting_rows(form4.tableWidget.rowCount())

    # Поиск значений в таблице (Вариант для QTableWidget);
    @staticmethod
    def find_items(filter_text: any) -> None:
        for rc in range(form4.tableWidget.rowCount()):
            for cc in range(form4.tableWidget.columnCount()):
                item = form4.tableWidget.item(rc, cc)
                match = filter_text.lower() not in item.text().lower()
                form4.tableWidget.setRowHidden(rc, match)
                if not match:
                    break


def ab_insert_data_connect() -> tuple:
    row_position = form4.tableWidget.currentRow()
    try:
        line_name = form4.tableWidget.item(row_position, 0).text()
        line_id = form4.tableWidget.item(row_position, 1).text()
        line_pw = form4.tableWidget.item(row_position, 2).text()
        line_data = (line_name, line_id, line_pw)
    except AttributeError:
        line_data = ('', '', '')
    return line_data


def ab_adding_records_iteration(data_name: any, data_id: any, data_pw: any) -> None:
    row_position = form4.tableWidget.rowCount()
    form4.tableWidget.insertRow(row_position)
    form4.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(data_name))
    form4.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(data_id))
    form4.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(data_pw))


def ab_load_data() -> None:
    Tools.create_abook()
    with open(abook_path, 'r', encoding="utf8") as file:
        for line in file:
            # list -> tuple;
            data = tuple(line.split(',,,'))
            # Усекаем все, начиная со строки не соответствующей заданному разделителю;
            try:
                name, id_ab, pw = data
                ab_adding_records_iteration(name, id_ab, pw.rstrip("\n"))
            except ValueError:
                with open(abook_path, "r+", encoding="utf8") as file2:
                    new_f = file2.readlines()
                    file2.seek(0)
                    for line2 in new_f:
                        if data[0] not in line2:
                            file2.write(line2)
                    file2.truncate()
    Tools.sort_items()
    Tools.counting_rows(form4.tableWidget.rowCount())


ab_load_data()


class Profile:
    @staticmethod
    def add() -> None:
        # Удаляем пробелы перед добавлением записи;
        profile_name = (form7.lineEdit_name.text()).replace(" ", "")

        # Проверка, чтобы строка была не пустой и добавляемый элемент не находился в списке;
        if profile_name and profile_name not in ABOOK.profiles:
            ABOOK.profiles.append(profile_name)
            edit_config(mv_conf_path, "ABOOK", "profiles", str(ABOOK.profiles))
            form4.comboBox_profiles.addItem(profile_name)
            window7.close()

    @staticmethod
    def delete() -> None:
        cur_index = form4.comboBox_profiles.currentIndex()
        count_index = form4.comboBox_profiles.count()

        # Элемент должен быть не последним в списке;
        if count_index != 1:
            ques_out = QMessageBox.question(window4, "microViewer: Удалить профиль", "Действительно удалить профиль?",
                                            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if ques_out == QMessageBox.StandardButton.Ok:
                ABOOK.profiles.pop(cur_index)
                cur_text = form4.comboBox_profiles.currentText()
                cur_file = f"conf/{ConfSets.profiles[ConfSets.index]}/{cur_text}.mv"

                if path.isfile(cur_file):
                    remove(cur_file)
                edit_config(mv_conf_path, "ABOOK", "index", str(cur_index-1))
                edit_config(mv_conf_path, "ABOOK", "profiles", str(ABOOK.profiles))

                form4.comboBox_profiles.removeItem(cur_index)

    @staticmethod
    def edit() -> None:
        global abook_path
        cur_index = form4.comboBox_profiles.currentIndex()
        old_profile_name = form4.comboBox_profiles.itemText(cur_index)
        # Удаляем пробелы перед обновлением записи;
        new_profile_name = (form8.lineEdit_name.text()).replace(" ", "")

        # Проверка, чтобы строка была не пустой и измененный элемент не находился в списке;
        if new_profile_name and new_profile_name not in ABOOK.profiles:
            ABOOK.profiles[cur_index] = new_profile_name
            form4.comboBox_profiles.setItemText(cur_index, new_profile_name)
            cur_path = f"conf/{ConfSets.profiles[ConfSets.index]}"

            edit_config(mv_conf_path, "ABOOK", "profiles", str(ABOOK.profiles))
            Path(f"{cur_path}/{old_profile_name}.mv").rename(f"{cur_path}/{new_profile_name}.mv")

            abook_path = Path(f"{cur_path}/{new_profile_name}.mv")
            window8.close()

    @staticmethod
    def tracking_index() -> None:
        global mv_conf_path
        cur_index = form4.comboBox_profiles.currentIndex()

        # Обновление данных с нужного конфига;
        refresh_profiles(cs_conf_path, "ConfSets")
        mv_conf_path = Path(f"conf/{ConfSets.profiles[ConfSets.index]}/mv.ini")

        edit_config(mv_conf_path, "ABOOK", "index", str(cur_index))

        ab_load_data()


# (Окно ABook) - Основные кнопки;
form4.pushButton_add_row.clicked.connect(Window.show_add_item)
form4.pushButton_edit_row.clicked.connect(Window.show_edit_item)
form4.pushButton_delete_row.clicked.connect(Table.delete_row)
form4.lineEdit_find_items.textChanged.connect(Table.find_items)
# form4.pushButton_connect.clicked.connect(ab_connect)
form4.comboBox_profiles.addItems(ABOOK.profiles)
form4.comboBox_profiles.setCurrentIndex(ABOOK.index)
form4.pushButton_add_profile.clicked.connect(Window.show_add_profile)
form4.pushButton_delete_profile.clicked.connect(Profile.delete)
form4.pushButton_edit_profile.clicked.connect(Window.show_edit_profile)
form4.comboBox_profiles.currentIndexChanged.connect(Profile.tracking_index)

# (Окно ABook) - Add;
form5.pushButton_ok.clicked.connect(Table.add_row)
form5.pushButton_cancel.clicked.connect(Window.close_add_item)

# (Окно ABook) - Edit;
form6.pushButton_ok.clicked.connect(Table.edit_row)
form6.pushButton_cancel.clicked.connect(Window.close_edit_item)

# (Окно ABook) - Add Profile;
form7.pushButton_ok.clicked.connect(Profile.add)
form7.pushButton_cancel.clicked.connect(Window.close_add_profile)

# (Окно ABook) - Edit Profile;
form8.pushButton_ok.clicked.connect(Profile.edit)
form8.pushButton_cancel.clicked.connect(Window.close_edit_profile)


if __name__ == "__main__":
    window4.show()
    app.exec()
