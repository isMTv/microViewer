import subprocess
import socket
from time import sleep
from shutil import rmtree

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMessageBox

from set_vars import *
from configs import edit_config
from adressbook import window4, form4, ab_insert_data_connect
from cversion import set_title_app_version, set_components_version

# Global's Var's;
rand_id = "None"
rand_pw = "None"
connect_id = "None"
connect_pw = "None"
pids_rd_client = "None"
pids_rd_server = "None"
pids_tun_client = "None"
pids_tun_server = "None"
modes_client = False
modes_server = False


def gen_id() -> any:
    global rand_id
    rand_id = Rand_Id_Pw.id()
    return rand_id


def gen_pw() -> str:
    global rand_pw
    rand_pw = Rand_Id_Pw.pw()
    return rand_pw


def logger(data_in: str) -> None:
    # Если параметр не пустой, то выполняем код;
    if data_in:
        data_out = "[i]: " + str(data_in).strip()
        form.textBrowser_logs.append(data_out)


class ExternalApp:
    # Запуск внешних программ с передачей параметров и обработкой returncode, stdout, stderr
    # (скрывает отображение консоли);
    @staticmethod
    def run(cmd: any) -> bool:
        sp = subprocess.run(
            cmd, capture_output=True, text=True, encoding="cp866", shell=True
        )
        if sp.returncode == 0:
            logger(f"{sp.stdout}")
            return True
        else:
            logger(f"{sp.stderr}")
            return False

    # Запуск внешних программ с передачей параметров (Popen - Позволяет не дожидаться завершения работы процесса);
    @staticmethod
    def popen(cmd: any, run_type: str) -> None:
        global pids_rd_client, pids_rd_server
        sp = subprocess.Popen(
            cmd
        )
        popen_curpid = sp.pid
        if run_type == "client":
            pids_rd_client = popen_curpid
        elif run_type == "server":
            pids_rd_server = popen_curpid
        else:
            pass

    # Запуск внешних программ с передачей параметров и скрытием появления окна;
    @staticmethod
    def popen_hide(cmd: any, run_type: str) -> None:
        global pids_tun_client, pids_tun_server
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        sp = subprocess.Popen(
            cmd, startupinfo=si
        )
        popen_hide_curpid = sp.pid
        if run_type == "client":
            pids_tun_client = popen_hide_curpid
        elif run_type == "server":
            pids_tun_server = popen_hide_curpid
        else:
            pass


class Process:
    # Закрытие процессов по имени;
    @staticmethod
    def kill(proc_list: tuple) -> None:
        for proc in proc_list:
            ExternalApp.run(f"taskkill /F /T /IM {proc}.exe")

    # Закрытие процесса по PID;
    @staticmethod
    def kill_pid(pid: str) -> None:
        ExternalApp.run(f"taskkill /F /T /PID {pid}")


class Check:
    # Проверка прав Администратора;
    @staticmethod
    def admin_right() -> bool:
        command = ["net", "session"]
        sp = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
        if sp.returncode == 0:
            return True
        else:
            logger(f"Ошибка! Необходимы права Администратора.")
            return False

    # Проверка доступности сервера, открыт или закрыт порт;
    @staticmethod
    def status_server(host: any, port: int) -> str:
        if MV.connection_type == "id":
            # Нужны для переключения между профилями;
            host = str(host)
            port = int(port)
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.2)
                    if s.connect_ex((host, port)) == 0:
                        data_status_server = "Online"
                    else:
                        data_status_server = "Offline"
            except Exception:
                data_status_server = "Error"
                logger(f"Ошибка! Не резолвится домен {Tunnel.host}.")
            return data_status_server
        else:
            return "LAN"

    # (RD) Проверка поля для ввода IP-адреса или Доменного-имени;
    @staticmethod
    def ip(ip_or_domain: str) -> bool:
        if MV.connection_type == "ip":
            try:
                # Реезолвим DNS-имя, если введен IP-адрес, то возвращается строка без изменений;
                socket.gethostbyname(ip_or_domain)
                exit_bool = True
            except socket.gaierror:
                logger(f"Ошибка! Неверно задан IP-адрес или DNS-имя.")
                exit_bool = False
            return exit_bool
        else:
            return True

    # (RD) Проверка поля для ввода пароля;
    @staticmethod
    def pw(data: str) -> bool:
        if not data:
            logger(f"Ошибка! Пароль не может быть пустым.")
            return False
        else:
            return True

    # (Tunnel) Проверка ID, это должно быть целое число равное 5, 4;
    @staticmethod
    def id(digit1: str, digit2: str) -> bool:
        if MV.connection_type == "id":
            length1 = len(str(digit1))
            int_digit1 = digit1.isdigit()
            length2 = len(str(digit2))
            int_digit2 = digit2.isdigit()
            if (length1 == 5 and int_digit1) and (
                    length2 == 5 and int_digit2 or length2 == 4 and int_digit2):
                return True
            else:
                logger(f"Ошибка! Неверно задан ID.")
                return False
        else:
            return True

    # Получение текущего локального IP-Адреса хоста;
    @staticmethod
    def cur_ip() -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(('10.255.255.255', 1))
                ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        return ip


class MvApp:
    """"Запуск и остановка основных программ"""

    @staticmethod
    def run_tunnel(srv_port: int, key, mode: str, tunnel_local_port: str, tunnel_remote_port: int, user: str,
                   run_type: str) -> bool:
        # Проверяем, подключение будет по ID или IP;
        if MV.connection_type == "id":
            if Check.id(tunnel_local_port, str(tunnel_remote_port)):
                logger(f"Запускается Tunnel к SSH серверу.")
                # Параметр -send-to-tray отключен, т.к. не пропадает иконка после закрытия процесса;
                ExternalApp.popen_hide(
                    f"{k_app} -P {srv_port} -i {key} -T -N -{mode} :{tunnel_local_port}:127.1:{tunnel_remote_port} "
                    f"{user}@{Tunnel.host} -auto-store-sshkey", run_type)
                sleep(3)
                return True
            else:
                return False
        else:
            return True

    @staticmethod
    def client_on_rd() -> None:
        global modes_client
        if MV.connection_type == "id":
            ExternalApp.popen(f"bin/uvnc/vncviewer.exe -connect 127.0.0.1:{connect_id} -password {connect_pw} -noauto "
                              f"-disablesponsor -config bin/uvnc/viewer.vnc", "client")
        elif MV.connection_type == "ip":
            ExternalApp.popen(f"bin/uvnc/vncviewer.exe -connect {connect_id}:{RemoteDesktop.portnumber} "
                              f"-password {connect_pw} -noauto -disablesponsor -config bin/uvnc/viewer.vnc", "client")
        modes_client = True
        logger(f"Запускается Client Remote Desktop.")

    @staticmethod
    def client_off_rd() -> None:
        global modes_client, pids_tun_client, pids_rd_client
        if MV.connection_type == "id":
            Process.kill_pid(pids_tun_client)
            pids_tun_client = "None"
            Process.kill_pid(pids_rd_client)
            pids_rd_client = "None"
        elif MV.connection_type == "ip":
            Process.kill_pid(pids_rd_client)
            pids_rd_client = "None"
        modes_client = False

    @staticmethod
    def server_on_rd() -> None:
        global modes_server
        modes_server = True
        ExternalApp.popen_hide(f"bin/uvnc/createpassword.exe {rand_pw}", "none")
        edit_config(mv_conf_path, "Server", "id", rand_id)
        edit_config(mv_conf_path, "Server", "password", rand_pw)
        logger(f"Запускается Server Remote Desktop.")
        ExternalApp.popen(f"bin/uvnc/winvnc.exe -run", "none")

    @staticmethod
    def server_off_rd() -> None:
        global modes_server, pids_tun_server, pids_rd_server
        if MV.connection_type == "id":
            Process.kill_pid(pids_tun_server)
            pids_tun_server = "None"
            # Process.kill_pid(pids_rd_server);
            ExternalApp.popen_hide(f"bin/uvnc/winvnc.exe -kill", "none")
            pids_rd_server = "None"
        elif MV.connection_type == "ip":
            # Process.kill_pid(pids_rd_server);
            ExternalApp.popen_hide(f"bin/uvnc/winvnc.exe -kill", "none")
            pids_rd_server = "None"
        modes_server = False

    @staticmethod
    def service_on_rd() -> bool:
        # Для выполнения, необходимы права Администратора;
        if Check.admin_right():
            # Если пароль не изменялся, то оставляем старый, зашифрованный RD_APP;
            if Service.password != "Encrypt":
                logger(f"Задан пользовательский пароль службы RD.")
                ExternalApp.popen_hide(f"bin/uvnc/createpassword.exe {rand_pw}", "none")
            ExternalApp.popen(f"bin/uvnc/winvnc.exe -install", "none")
            # Добавляем параметры в конфиг;
            edit_config(mv_conf_path, "Service", "enabled", "true")
            if MV.connection_type != "ip":
                edit_config(mv_conf_path, "Service", "id", rand_id)
            # Если включена фиксация пароля, то новый не создаем;
            if Service.fix_id_pw == "false":
                edit_config(mv_conf_path, "Service", "password", rand_pw)
            elif Service.fix_id_pw == "true":
                edit_config(mv_conf_path, "Service", "password", "Encrypt")
            edit_config(mv_conf_path, "Modes", "service", "true")
            # Проверяем, подключение будет по ID или IP (Интеграция KiTTY в планировщик);
            if MV.connection_type == "id":
                # k_tunnel;
                ExternalApp.run(f'schtasks /create /xml "{k_task_tunnel}" /tn "Microsoft\Windows\microViewer\k_tunnel"')
                # Экранируем путь, чтобы в пути после пробела оставшаяся часть не воспринималась как аргумент;
                ExternalApp.run(f'schtasks /change /tn "Microsoft\Windows\microViewer\k_tunnel" /tr "\'{k_tunnel}\'"')
                ExternalApp.run(f'schtasks /run /tn "Microsoft\Windows\microViewer\k_tunnel"')
                # k_tunnel_helper;
                if Service.helper == "true":
                    ExternalApp.run(f'schtasks /create /xml "{k_task_tunnel_helper}" /tn "Microsoft\Windows\microViewer'
                                    f'\k_tunnel_helper"')
                    ExternalApp.run(f'schtasks /change /tn "Microsoft\Windows\microViewer'
                                    f'\k_tunnel_helper" /tr "\'{k_tunnel_helper}\'"')
                    ExternalApp.run(f'schtasks /change /tn "Microsoft\Windows\microViewer'
                                    f'\k_tunnel_helper" /ri "{Service.check_interval_helper}"')
            return True
        else:
            return False

    @staticmethod
    def service_remove_rd() -> bool:
        # Для выполнения, необходимы права Администратора;
        if Check.admin_right():
            ExternalApp.popen(f"bin/uvnc/winvnc.exe -uninstall", "none")
            # Проверяем, подключение было по ID или IP (Удаление KiTTY из планировщика);
            if MV.connection_type == "id":
                refresh_classes_vars(mv_conf_path, "Pids")
                ExternalApp.run(f'schtasks /delete /tn "Microsoft\Windows\microViewer\k_tunnel" /f')
                if Service.helper == "true":
                    ExternalApp.run(f'schtasks /delete /tn "Microsoft\Windows\microViewer\k_tunnel_helper" /f')
                ExternalApp.run(f'schtasks /delete /tn "Microsoft\Windows\microViewer" /f')
                # Завершаем процессы;
                Process.kill_pid(Pids.k_tunnel)
                Process.kill(("k_tunnel",))
                # Отключаем параметр в конфиге;
                edit_config(mv_conf_path, "Pids", "k_tunnel", "none")
            # Отключаем параметры в конфиге;
            edit_config(mv_conf_path, "Service", "enabled", "false")
            edit_config(mv_conf_path, "Modes", "service", "false")
            return True
        else:
            return False


# (Окно Main) - Инициализация GUI;
Form, Window = uic.loadUiType("bin/ui/main.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.setFixedSize(283, 235)

# (Окно Settings) - Инициализация GUI;
Form, Window = uic.loadUiType("bin/ui/settings.ui")
window2 = Window()
form2 = Form()
form2.setupUi(window2)
window2.setFixedSize(294, 430)

# (Окно About) - Инициализация GUI;
Form, Window = uic.loadUiType("bin/ui/about.ui")
window3 = Window()
form3 = Form()
form3.setupUi(window3)
window3.setFixedSize(290, 230)

# (Окно Profile - Add) - Инициализация GUI;
Form, Window = uic.loadUiType("bin/ui/ab_add_profile.ui")
window5 = Window()
form5 = Form()
form5.setupUi(window5)
window5.setFixedSize(217, 80)

# (Окно Profile - Edit) - Инициализация GUI;
Form, Window = uic.loadUiType("bin/ui/ab_edit_profile.ui")
window6 = Window()
form6 = Form()
form6.setupUi(window6)
window6.setFixedSize(217, 80)


class Tool:
    # Сохранение местоположения родительского окна при закрытии (если изменилось значение);
    @staticmethod
    def save_parent_window_pos(parent_window: any) -> None:
        if ParentWindow.position_x != str(parent_window.pos().x()):
            edit_config(mv_conf_path, "ParentWindow", "position_x", str(parent_window.pos().x()))
        if ParentWindow.position_y != str(parent_window.pos().y()):
            edit_config(mv_conf_path, "ParentWindow", "position_y", str(parent_window.pos().y()))

    # Установка местоположения дочернего окна на базе местоположения родительского;
    @staticmethod
    def set_child_window_pos(child_window: any, parent_window: any) -> None:
        child_window.move(parent_window.pos().x() + 20, parent_window.pos().y() + 20)

    # Показать/Скрыть взаимодействие с Профилями;
    @staticmethod
    def show_hide_profiles(dataform: any, state: bool) -> None:
        dataform.pushButton_add_profile.setEnabled(state)
        dataform.pushButton_delete_profile.setEnabled(state)
        dataform.pushButton_edit_profile.setEnabled(state)
        dataform.comboBox_profiles.setEnabled(state)

    # Задать состояние кнопок - Подк./Откл. (Клиент), Вкл./Откл. (Сервер, Служба) согласно настройкам из конфига;
    @staticmethod
    def set_modes_button() -> None:
        refresh_classes_vars(mv_conf_path, "Modes")
        if modes_client:
            form.pushButton_conn_disc.setText("Отключиться")
            form.pushButton_conn_disc.setChecked(True)
            # ABook;
            form4.pushButton_connect.setChecked(True)
            # Профили ABook;
            Tool.show_hide_profiles(form4, False)
        else:
            form.pushButton_conn_disc.setText("Подключиться")
            form.pushButton_conn_disc.setChecked(False)
            # ABook;
            form4.pushButton_connect.setChecked(False)
            # Профили ABook;
            Tool.show_hide_profiles(form4, True)
        if modes_server:
            form.radioButton_server.toggle()
            form.pushButton_modes.setText("OFF")
            form.pushButton_modes.setChecked(True)
            # Профили;
            Tool.show_hide_profiles(form, False)
        elif Modes.service == "true":
            form.radioButton_service.toggle()
            form.pushButton_modes.setText("OFF")
            form.pushButton_modes.setChecked(True)
            # Профили;
            Tool.show_hide_profiles(form, False)
        else:
            form.pushButton_modes.setText("ON")
            form.pushButton_modes.setChecked(False)
            # Профили;
            Tool.show_hide_profiles(form, True)

    # Проверка выбранного типа подключения ID или IP;
    @staticmethod
    def check_connection_type() -> None:
        refresh_classes_vars(mv_conf_path, "MV")
        if MV.connection_type == "id":
            form.radioButton_access_by_id.toggle()
        if MV.connection_type == "ip":
            form.radioButton_access_by_ip.toggle()

    # Проверка Чек-Боксов (вывод сохраненных параметров в окна);
    @staticmethod
    def check_box(dataform: any, state: str) -> None:
        if state == "true":
            # dataform.toggle();
            dataform.setChecked(True)
        else:
            # dataform.toggle();
            dataform.setChecked(False)

    # Показать/Скрыть поля для ввода статических ID/PW;
    @staticmethod
    def show_hide_service_fix_id_pw() -> None:
        if form2.checkBox_id_pass.isChecked():
            form2.label_id.setEnabled(True)
            form2.spinBox_id.setEnabled(True)
            form2.label_password.setEnabled(True)
            form2.lineEdit_password.setEnabled(True)
            form2.spinBox_id.setValue(int(Service.id))
            form2.lineEdit_password.setText(Service.password)
        else:
            form2.label_id.setEnabled(False)
            form2.spinBox_id.setEnabled(False)
            form2.label_password.setEnabled(False)
            form2.lineEdit_password.setEnabled(False)
            form2.spinBox_id.setValue(int(Service.id))
            form2.lineEdit_password.setText(Service.password)

    # Показать/Скрыть поле Хелпера для ввода кол-ва мин.;
    @staticmethod
    def show_hide_service_helper() -> None:
        if form2.checkBox_helper.isChecked():
            form2.spinBox_helper_service.setEnabled(True)
        else:
            form2.spinBox_helper_service.setEnabled(False)


Tool.set_modes_button()
Tool.check_connection_type()


class Window:
    @staticmethod
    def show_settings() -> None:
        window2.show()
        Tool.set_child_window_pos(window2, window)

    @staticmethod
    def close_settings() -> None:
        window2.close()

    @staticmethod
    def show_about() -> None:
        window3.show()
        Tool.set_child_window_pos(window3, window)

    @staticmethod
    def show_abook() -> None:
        window4.show()
        Tool.set_child_window_pos(window4, window)

    @staticmethod
    def show_add_profile() -> None:
        # Очищаем от предыдущих введенных данных;
        form5.lineEdit_name.setText("")

        window5.show()
        Tool.set_child_window_pos(window5, window)

    @staticmethod
    def close_add_profile() -> None:
        window5.close()

    @staticmethod
    def show_edit_profile() -> None:
        profile_name = form.comboBox_profiles.currentText()

        form6.lineEdit_name.setText(profile_name)

        window6.show()
        Tool.set_child_window_pos(window6, window)

    @staticmethod
    def close_edit_profile() -> None:
        window6.close()


# (Окно Main) Обработка действий при нажатии кнопок;
def click_connect() -> None:
    global connect_id, connect_pw
    connect_id = form.lineEdit_id.text()
    # Удаляем пробелы перед подключением;
    connect_pw = form.lineEdit_password.text().replace(" ", "")
    Tool.set_modes_button()
    if Check.pw(connect_pw) and MvApp.run_tunnel(Tunnel.port, Tunnel.key_client, "L", connect_id, connect_id,
                                                 Tunnel.user_client, "client"):
        if Check.ip(connect_id):
            MvApp.client_on_rd()
            form.pushButton_conn_disc.setText("Отключиться")
            form.pushButton_conn_disc.setChecked(True)
            # ABook;
            form4.pushButton_connect.setChecked(True)
            # Профили ABook;
            Tool.show_hide_profiles(form4, False)


def click_disconnect() -> None:
    Tool.set_modes_button()
    MvApp.client_off_rd()
    form.pushButton_conn_disc.setText("Подключиться")
    form.pushButton_conn_disc.setChecked(False)
    # ABook;
    form4.pushButton_connect.setChecked(False)
    # Профили ABook;
    Tool.show_hide_profiles(form4, True)


def click_on() -> None:
    # Сервер;
    data1 = form.radioButton_server.isChecked()
    # Служба;
    data2 = form.radioButton_service.isChecked()
    Tool.set_modes_button()
    if data1:
        if Service.fix_id_pw == "false" or Service.password != "Encrypt":
            if Check.pw(rand_pw) and MvApp.run_tunnel(Tunnel.port, Tunnel.key_server, "R", rand_id,
                                                      RemoteDesktop.portnumber, Tunnel.user_server, "server"):
                MvApp.server_on_rd()
                form.pushButton_modes.setText("OFF")
                form.pushButton_modes.setChecked(True)
                # Профили;
                Tool.show_hide_profiles(form, False)
        else:
            logger(f"Ошибка! Необходимо изменить зафиксированный пароль или отключить фиксацию.")
    elif data2:
        if Check.id(rand_id, str(RemoteDesktop.portnumber)) and Check.pw(rand_pw):
            if MvApp.service_on_rd():
                form.pushButton_modes.setText("OFF")
                form.pushButton_modes.setChecked(True)
                # Профили;
                Tool.show_hide_profiles(form, False)


def click_off() -> None:
    # Сервер;
    data1 = form.radioButton_server.isChecked()
    # Служба;
    data2 = form.radioButton_service.isChecked()
    Tool.set_modes_button()
    if data1 and modes_server:
        MvApp.server_off_rd()
        form.pushButton_modes.setText("ON")
        form.pushButton_modes.setChecked(False)
        # Профили;
        Tool.show_hide_profiles(form, True)
    elif data2 and Modes.service == "true":
        if MvApp.service_remove_rd():
            form.pushButton_modes.setText("ON")
            form.pushButton_modes.setChecked(False)
            # Профили;
            Tool.show_hide_profiles(form, True)


def refresh_id_pw_status() -> None:
    refresh_classes_vars(mv_conf_path, "Modes")
    if not modes_server and Modes.service != "true":
        # Чтобы могли сгенерироваться новые id и pw;
        edit_config(mv_conf_path, "Server", "id", "")
        edit_config(mv_conf_path, "Server", "password", "")
        refresh_classes_vars(mv_conf_path, "Server")
        form.label_id_data.setText(gen_id())
        form.label_password_data.setText(gen_pw())
    form.label_status_server_data.setText(Check.status_server(Tunnel.host, Tunnel.port))


def gui_applay() -> None:
    refresh_classes_vars(mv_conf_path, "Modes")
    if not modes_client and not modes_server and Modes.service != "true":
        global rand_id
        # Значения из Окна Main Settings;
        current_values = {
            'mv_password_length': form.spinBox_password_length.value(),
            'rd_srv_port': form.spinBox_rd_port.value(),
            'mv_connection_type_id': form.radioButton_access_by_id.isChecked(),
            'mv_connection_type_ip': form.radioButton_access_by_ip.isChecked(),
            'mv_mode_server_autorun': str(form.checkBox_autorun.isChecked()).lower()
        }
        # Если изменилось значение, то обновляем в конфиге на новое;
        if current_values["mv_password_length"] != int(MV.password_length):
            edit_config(mv_conf_path, "MV", "password_length", str(current_values["mv_password_length"]))
            refresh_classes_vars(mv_conf_path, "MV")
            # Если изменилась длина пароля, то задаем и обновляем глобально значение;
            form.label_password_data.setText(gen_pw())
        if current_values["rd_srv_port"] != int(RemoteDesktop.portnumber):
            edit_config(rd_conf_path, "admin", "portnumber", str(current_values["rd_srv_port"]))
            refresh_uvnc(rd_conf_path, "RemoteDesktop")
        if current_values["mv_connection_type_id"]:
            if MV.connection_type != "id":
                edit_config(mv_conf_path, "MV", "connection_type", "id")
                refresh_classes_vars(mv_conf_path, "MV")
                form.label_id_data.setText(gen_id())
                form.label_status_server_data.setText(Check.status_server(Tunnel.host, Tunnel.port))
        elif current_values["mv_connection_type_ip"]:
            if MV.connection_type != "ip":
                edit_config(mv_conf_path, "MV", "connection_type", "ip")
                refresh_classes_vars(mv_conf_path, "MV")
                rand_id = "N/A"
                form.label_id_data.setText("N/A")
                form.label_status_server_data.setText("LAN")
        if current_values["mv_mode_server_autorun"] != MV.mode_server_autorun:
            edit_config(mv_conf_path, "MV", "mode_server_autorun",
                        (str(current_values["mv_mode_server_autorun"])).lower())
            refresh_classes_vars(mv_conf_path, "MV")
    else:
        QMessageBox.warning(window, "microViewer: Предупреждение!", "Настройки не применены.\nИспользуется "
                                                                    "один из режимов!")


def gui_settings_applay() -> None:
    refresh_classes_vars(mv_conf_path, "Modes")
    if not modes_client and not modes_server and Modes.service != "true":
        # Значения из Окна Settings;
        current_values = {
            'tunnel_host': form2.lineEdit_host.text(),
            'tunnel_srv_port': form2.spinBox_port.value(),
            'tunnel_user_server': form2.lineEdit_user_server.text(),
            'tunnel_key_server': form2.lineEdit_key_server.text(),
            'tunnel_user_client': form2.lineEdit_user_client.text(),
            'tunnel_key_client': form2.lineEdit_key_client.text(),
            'service_check_interval': form2.spinBox_restart_service.value(),
            'service_helper': str(form2.checkBox_helper.isChecked()).lower(),
            'service_check_interval_helper': form2.spinBox_helper_service.value(),
            'service_fix_id_pw': str(form2.checkBox_id_pass.isChecked()).lower(),
            'service_id': form2.spinBox_id.value(),
            'service_password': form2.lineEdit_password.text().replace(" ", ""),
            'quality_index': form2.comboBox_quality_preset.currentIndex()
        }
        # Если изменилось значение, то обновляем в конфиге на новое;
        if current_values["tunnel_host"] != Tunnel.host:
            edit_config(mv_conf_path, "Tunnel", "host", current_values["tunnel_host"])
        if current_values["tunnel_srv_port"] != int(Tunnel.port):
            edit_config(mv_conf_path, "Tunnel", "port", str(current_values["tunnel_srv_port"]))
        if current_values["tunnel_user_server"] != Tunnel.user_server:
            edit_config(mv_conf_path, "Tunnel", "user_server", current_values["tunnel_user_server"])
        if current_values["tunnel_key_server"] != Tunnel.key_server:
            edit_config(mv_conf_path, "Tunnel", "key_server", current_values["tunnel_key_server"])
        if current_values["tunnel_user_client"] != Tunnel.user_client:
            edit_config(mv_conf_path, "Tunnel", "user_client", current_values["tunnel_user_client"])
        if current_values["tunnel_key_client"] != Tunnel.key_client:
            edit_config(mv_conf_path, "Tunnel", "key_client", current_values["tunnel_key_client"])
        if current_values["service_check_interval"] != int(Service.check_interval):
            edit_config(mv_conf_path, "Service", "check_interval", str(current_values["service_check_interval"]))
        if current_values["service_helper"] != Service.helper:
            edit_config(mv_conf_path, "Service", "helper", (str(current_values["service_helper"])).lower())
        if current_values["service_check_interval_helper"] != int(Service.check_interval_helper):
            edit_config(mv_conf_path, "Service", "check_interval_helper", str(current_values["service"
                                                                                             "_check_interval_helper"]))
        if current_values["service_fix_id_pw"] != Service.fix_id_pw:
            edit_config(mv_conf_path, "Service", "fix_id_pw", (str(current_values["service_fix_id_pw"])).lower())
            # Если Вкл./Выкл. фиксация ID/PW, то задаем и обновляем глобально значения;
            refresh_id_pw_status()
        if current_values["service_id"] != int(Service.id):
            edit_config(mv_conf_path, "Service", "id", str(current_values["service_id"]))
            # Если изменился заданный ID, то задаем и обновляем глобально значение;
            form.label_id_data.setText(gen_id())
        if current_values["service_password"] != Service.password:
            edit_config(mv_conf_path, "Service", "password", current_values["service_password"])
            # Если изменился заданный PW, то задаем и обновляем глобально значение;
            form.label_password_data.setText(gen_pw())
        if current_values["quality_index"] != int(Viewer.quality_index):
            qi = int(current_values["quality_index"])
            qp = tuple(Viewer.quality_presets)
            pe, cb = tuple(qp[qi])
            if qi == 0:
                edit_config(viewer_conf_path, "options", "preferred_encoding", str(pe))
                edit_config(viewer_conf_path, "options", "8bit", str(cb))
            elif qi == 1:
                edit_config(viewer_conf_path, "options", "preferred_encoding", str(pe))
                edit_config(viewer_conf_path, "options", "8bit", str(cb))
            elif qi == 2:
                edit_config(viewer_conf_path, "options", "preferred_encoding", str(pe))
                edit_config(viewer_conf_path, "options", "8bit", str(cb))
            elif qi == 3:
                edit_config(viewer_conf_path, "options", "preferred_encoding", str(pe))
                edit_config(viewer_conf_path, "options", "8bit", str(cb))
            edit_config(cs_conf_path, "Viewer", "quality_index", str(current_values["quality_index"]))
        # Инициализируем переменные с обновленными значениями;
        refresh_classes_vars(mv_conf_path, "Tunnel"), refresh_classes_vars(mv_conf_path, "Service"), \
            refresh_profiles(cs_conf_path, "Viewer")
    else:
        QMessageBox.warning(window2, "microViewer: Предупреждение!", "Настройки не применены.\nИспользуется "
                                                                     "один из режимов!")


class HandlerModeButton:
    # Обработчик кнопки Подключиться/Отключиться;
    @staticmethod
    def connect_disconnect() -> None:
        if form.pushButton_conn_disc.isChecked():
            click_connect()
        else:
            click_disconnect()

    # (ABook) Обработчик кнопки Подключиться/Отключиться;
    @staticmethod
    def ab_connect_disconnect() -> None:
        if form4.pushButton_connect.isChecked():
            ab_connect_line = ab_insert_data_connect()
            form.lineEdit_id.setText(ab_connect_line[1])
            form.lineEdit_password.setText(ab_connect_line[2])
            click_connect()
        else:
            form.lineEdit_id.setText("")
            form.lineEdit_password.setText("")
            click_disconnect()

    # (ABook) Обработчик строки при двойном нажатии (Подключиться/Отключиться);
    @staticmethod
    def ab_connect_disconnect_row_doubleclick() -> None:
        if not modes_client:
            ab_connect_line = ab_insert_data_connect()
            form.lineEdit_id.setText(ab_connect_line[1])
            form.lineEdit_password.setText(ab_connect_line[2])
            click_connect()
        else:
            form.lineEdit_id.setText("")
            form.lineEdit_password.setText("")
            click_disconnect()

    # Обработчик кнопки Включения/Отключения режима;
    @staticmethod
    def on_off_mode() -> None:
        if form.pushButton_modes.isChecked():
            click_on()
        else:
            click_off()


class Profile:
    @staticmethod
    def add() -> None:
        # Удаляем пробелы перед добавлением записи;
        profile_name = (form5.lineEdit_name.text()).replace(" ", "")

        # Проверка, чтобы строка была не пустой и добавляемый элемент не находился в списке;
        if profile_name and profile_name not in ConfSets.profiles:
            ConfSets.profiles.append(profile_name)
            edit_config(cs_conf_path, "ConfSets", "profiles", str(ConfSets.profiles))
            form.comboBox_profiles.addItem(profile_name)
            window5.close()

    @staticmethod
    def delete() -> None:
        cur_index = form.comboBox_profiles.currentIndex()
        count_index = form.comboBox_profiles.count()

        # Элемент должен быть не последним в списке;
        if count_index != 1:
            ques_out = QMessageBox.question(window, "microViewer: Удалить профиль", "Действительно удалить профиль?",
                                            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if ques_out == QMessageBox.StandardButton.Ok:
                ConfSets.profiles.pop(cur_index)
                cur_text = form.comboBox_profiles.currentText()
                cur_path = f"conf/{cur_text}"

                if Path(cur_path).exists():
                    rmtree(Path(cur_path))
                edit_config(cs_conf_path, "ConfSets", "index", str(cur_index - 1))
                edit_config(cs_conf_path, "ConfSets", "profiles", str(ConfSets.profiles))

                form.comboBox_profiles.removeItem(cur_index)

    @staticmethod
    def edit() -> None:
        cur_index = form.comboBox_profiles.currentIndex()
        old_profile_name = form.comboBox_profiles.itemText(cur_index)
        # Удаляем пробелы перед обновлением записи;
        new_profile_name = (form6.lineEdit_name.text()).replace(" ", "")

        # Проверка, чтобы строка была не пустой и измененный элемент не находился в списке;
        if new_profile_name and new_profile_name not in ConfSets.profiles:
            ConfSets.profiles[cur_index] = new_profile_name
            form.comboBox_profiles.setItemText(cur_index, new_profile_name)

            edit_config(cs_conf_path, "ConfSets", "profiles", str(ConfSets.profiles))
            Path(f"conf/{old_profile_name}").rename(f"conf/{new_profile_name}")
            window6.close()

    @staticmethod
    def tracking_index() -> None:
        global mv_conf_path
        cur_index = form.comboBox_profiles.currentIndex()
        profile_name = form.comboBox_profiles.itemText(cur_index)
        cur_conf_path = Path(f"conf/{profile_name}/mv.ini")

        edit_config(cs_conf_path, "ConfSets", "index", str(cur_index))

        if not Path(cur_conf_path).exists():
            cur_conf_path.parent.mkdir(parents=False, exist_ok=True)
            createconfig_mv(cur_conf_path)

        # Профили AB. Будет 2-ое обновление, (index = -1, 0) AB -> tracking_index();
        form4.comboBox_profiles.clear()
        form4.comboBox_profiles.addItems(ABOOK.profiles)

        # Профили Main (Перед обновлением, узнаем с какого конфига брать значения);
        mv_conf_path = Path(f"conf/{ConfSets.profiles[ConfSets.index]}/mv.ini")
        refresh_classes_vars(mv_conf_path, "MV")
        refresh_classes_vars(mv_conf_path, "Tunnel")
        refresh_classes_vars(mv_conf_path, "Service")

        Tool.check_connection_type()

        set_settings_forms()
        gui_applay()
        set_advanced_settings_forms()
        gui_settings_applay()
        refresh_id_pw_status()


# (Окно Main) - Управление Профилями;
form.comboBox_profiles.addItems(ConfSets.profiles)
form.comboBox_profiles.setCurrentIndex(ConfSets.index)
form.pushButton_add_profile.clicked.connect(Window.show_add_profile)
form.pushButton_delete_profile.clicked.connect(Profile.delete)
form.pushButton_edit_profile.clicked.connect(Window.show_edit_profile)
form.comboBox_profiles.currentIndexChanged.connect(Profile.tracking_index)
# (Окно Add Profile);
form5.pushButton_ok.clicked.connect(Profile.add)
form5.pushButton_cancel.clicked.connect(Window.close_add_profile)
# (Окно Edit Profile);
form6.pushButton_ok.clicked.connect(Profile.edit)
form6.pushButton_cancel.clicked.connect(Window.close_edit_profile)

# (Окно Main) Отображение, обработка ввода и нажатия кнопкок;
form.label_id_data.setText(gen_id())
form.label_password_data.setText(gen_pw())
form.label_status_server_data.setText(Check.status_server(Tunnel.host, Tunnel.port))
form.pushButton_conn_disc.clicked.connect(HandlerModeButton.connect_disconnect)
form.pushButton_modes.clicked.connect(HandlerModeButton.on_off_mode)
form.pushButton_refresh.clicked.connect(refresh_id_pw_status)
form.pushButton_adress_book.clicked.connect(Window.show_abook)
form.pushButton_about.clicked.connect(Window.show_about)
form.lineEdit_cur_ip.setText(Check.cur_ip())


# (Main Settings) - Задаем значения;
def set_settings_forms() -> None:
    form.spinBox_password_length.setValue(int(MV.password_length))
    form.spinBox_rd_port.setValue(int(RemoteDesktop.portnumber))
    Tool.check_box(form.checkBox_autorun, MV.mode_server_autorun)


set_settings_forms()

# (Окно Main Settings) - Обработка ввода и нажатия кнопкок;
form.pushButton_settings_aplay.clicked.connect(gui_applay)
form.pushButton_settings_advanced.clicked.connect(Window.show_settings)


# (Advanced Settings) - Задаем значения;
def set_advanced_settings_forms() -> None:
    form2.lineEdit_host.setText(Tunnel.host)
    form2.spinBox_port.setValue(int(Tunnel.port))
    form2.lineEdit_user_server.setText(Tunnel.user_server)
    form2.lineEdit_key_server.setText(Tunnel.key_server)
    form2.lineEdit_user_client.setText(Tunnel.user_client)
    form2.lineEdit_key_client.setText(Tunnel.key_client)
    form2.spinBox_restart_service.setValue(int(Service.check_interval))
    Tool.check_box(form2.checkBox_helper, Service.helper)
    Tool.show_hide_service_helper()
    form2.checkBox_helper.stateChanged.connect(Tool.show_hide_service_helper)
    form2.spinBox_helper_service.setValue(int(Service.check_interval_helper))
    Tool.check_box(form2.checkBox_id_pass, Service.fix_id_pw)
    Tool.show_hide_service_fix_id_pw()
    form2.checkBox_id_pass.stateChanged.connect(Tool.show_hide_service_fix_id_pw)
    form2.comboBox_quality_preset.setCurrentIndex(int(Viewer.quality_index))


set_advanced_settings_forms()

# (Окно Advanced Settings) - Обработка ввода и нажатия кнопкок;
form2.pushButton_settings_advanced_aplay.clicked.connect(gui_settings_applay)
form2.pushButton_settings_advanced_ok.clicked.connect(Window.close_settings)

# (Окно Abook);
form4.pushButton_connect.clicked.connect(HandlerModeButton.ab_connect_disconnect)
form4.tableWidget.doubleClicked.connect(HandlerModeButton.ab_connect_disconnect_row_doubleclick)

# (Окно Main) - Информация о версии;
set_title_app_version(window)

# (Окно Abaut) - Информация о сборке;
set_components_version(form3)


def main():
    window.show()
    if ParentWindow.position_x != "none" and ParentWindow.position_y != "none":
        window.move(int(ParentWindow.position_x), int(ParentWindow.position_y))
    if MV.mode_server_autorun == "true" and Modes.service == "false":
        form.radioButton_server.toggle()
        form.pushButton_modes.setText("OFF")
        form.pushButton_modes.setChecked(True)
        # Профили;
        Tool.show_hide_profiles(form, False)
        click_on()
    app.exec()

    if window.close():
        Tool.save_parent_window_pos(window)
        Tool.set_modes_button()
        if modes_server:
            click_off()
        if modes_client:
            click_disconnect()


if __name__ == "__main__":
    main()
