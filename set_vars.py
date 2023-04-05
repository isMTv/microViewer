import re
from secrets import choice
from random import randint
from string import ascii_letters, digits
from os import chdir
from pathlib import Path
from configs import createconfig_confsets, createconfig_mv, createconfig_rd, createconfig_viewer, get_config

# Data Path VARS;
dir_path = Path.cwd()
chdir(dir_path)

# Файл настроек ConfSets;
cs_conf_path = Path("conf/confsets.ini")
if not Path(cs_conf_path).exists():
    cs_conf_path.parent.mkdir(parents=False, exist_ok=True)
    createconfig_confsets(cs_conf_path)


class ConfSets:
    index: int = int(get_config(cs_conf_path, "ConfSets", "index"))
    profiles: list = eval(get_config(cs_conf_path, "ConfSets", "profiles"))
    all: tuple = ("index", "profiles")


class Viewer:
    quality_index: int = int(get_config(cs_conf_path, "Viewer", "quality_index"))
    quality_presets: tuple = eval(get_config(cs_conf_path, "Viewer", "quality_presets"))
    all: tuple = ("quality_index", "quality_presets")


# Файл настроек MV;
mv_conf_path = Path(f"conf/{ConfSets.profiles[ConfSets.index]}/mv.ini")
if not Path(mv_conf_path).exists():
    mv_conf_path.parent.mkdir(parents=False, exist_ok=True)
    createconfig_mv(mv_conf_path)

# Файл настроек RD;
rd_conf_path = Path("bin/uvnc/UltraVNC.ini")
if not Path(rd_conf_path).exists():
    rd_conf_path.parent.mkdir(parents=True, exist_ok=True)
    createconfig_rd(rd_conf_path)

# Файл настроек Viewer;
viewer_conf_path = Path("bin/uvnc/viewer.vnc")
if not Path(viewer_conf_path).exists():
    viewer_conf_path.parent.mkdir(parents=True, exist_ok=True)
    createconfig_viewer(viewer_conf_path)

# App's Path;
rd_app_server = Path(dir_path, "bin/uvnc/winvnc.exe")
rd_app_client = Path(dir_path, "bin/uvnc/vncviewer.exe")
k_app = "bin/kitty.exe"
k_tunnel = Path(dir_path, "bin/k_utils/k_tunnel.exe")
k_tunnel_helper = Path(dir_path, "bin/k_utils/k_tunnel_helper.exe")
k_task_tunnel = Path(dir_path, "bin/tasks/k_tunnel.xml")
k_task_tunnel_helper = Path(dir_path, "bin/tasks/k_tunnel_helper.xml")


class MV:
    password_length: int = int(get_config(mv_conf_path, "MV", "password_length"))
    connection_type: str = get_config(mv_conf_path, "MV", "connection_type")
    mode_server_autorun: str = get_config(mv_conf_path, "MV", "mode_server_autorun")
    all: tuple = ("password_length", "connection_type", "mode_server_autorun")


class ABOOK:
    index: int = int(get_config(mv_conf_path, "ABOOK", "index"))
    profiles: list = eval(get_config(mv_conf_path, "ABOOK", "profiles"))
    all: tuple = ("index", "profiles")


class Tunnel:
    host: str = get_config(mv_conf_path, "Tunnel", "host")
    port: int = int(get_config(mv_conf_path, "Tunnel", "port"))
    user_server: str = get_config(mv_conf_path, "Tunnel", "user_server")
    key_server: str = get_config(mv_conf_path, "Tunnel", "key_server")
    user_client: str = get_config(mv_conf_path, "Tunnel", "user_client")
    key_client: str = get_config(mv_conf_path, "Tunnel", "key_client")
    all: tuple = ("host", "port", "user_server", "key_server", "user_client", "key_client")


class RemoteDesktop:
    portnumber: int = get_config(rd_conf_path, "admin", "portnumber")
    all: tuple = ("portnumber",)


class Server:
    id: str = get_config(mv_conf_path, "Server", "id")
    password: str = get_config(mv_conf_path, "Server", "password")
    all: tuple = ("id", "password")


class Service:
    enabled: str = get_config(mv_conf_path, "Service", "enabled")
    check_interval: int = int(get_config(mv_conf_path, "Service", "check_interval"))
    helper: str = (get_config(mv_conf_path, "Service", "helper")).lower()
    check_interval_helper: int = int(get_config(mv_conf_path, "Service", "check_interval_helper"))
    fix_id_pw: str = (get_config(mv_conf_path, "Service", "fix_id_pw")).lower()
    id: str = get_config(mv_conf_path, "Service", "id")
    password: str = get_config(mv_conf_path, "Service", "password")
    all: tuple = ("enabled", "check_interval", "helper", "check_interval_helper", "fix_id_pw", "id", "password")


class Modes:
    service: str = get_config(mv_conf_path, "Modes", "service")
    all: tuple = ("service",)


class Pids:
    k_tunnel: str = get_config(mv_conf_path, "Pids", "k_tunnel")
    all: tuple = ("k_tunnel",)


class ParentWindow:
    position_x: int = get_config(mv_conf_path, "ParentWindow", "position_x")
    position_y: int = get_config(mv_conf_path, "ParentWindow", "position_y")
    all: tuple = ("position_x", "position_y")


# Если параметр обновился в файле конфига, то обновляем его внутри класса;
def refresh_classes_vars(conf_path: any, data_class: any) -> None:
    for index in eval(data_class).all:
        data = get_config(conf_path, data_class, index)
        command = f'{data_class}.{index} = "{data}"'
        exec(command)


# Чтобы не ломался eval(tuple and list);
def refresh_profiles(conf_path: any, data_class: any) -> None:
    for index in eval(data_class).all:
        data = get_config(conf_path, data_class, index)
        command = f'{data_class}.{index} = {data}'
        exec(command)


def refresh_uvnc(conf_path: any, data_class: any) -> None:
    for index in eval(data_class).all:
        data = get_config(conf_path, f"admin", index)
        command = f'{data_class}.{index} = {data}'
        exec(command)


class Rand_Id_Pw:
    # Генерация рандомного ID в диапазоне;
    @staticmethod
    def id() -> any:
        global mv_conf_path
        rand_id = "None"
        if MV.connection_type == "id":
            # Перед обновлением, узнаем с какого конфига брать значения;
            mv_conf_path = Path(f"conf/{ConfSets.profiles[ConfSets.index]}/mv.ini")
            refresh_classes_vars(mv_conf_path, "Service")
            if Service.enabled == "false" and Service.fix_id_pw == "false":
                # Подгружаем из конфига предыдущее значение;
                if not Server.id:
                    rand_id = str(randint(20000, 60000))
                else:
                    rand_id = Server.id
            else:
                rand_id = Service.id
        elif MV.connection_type == "ip":
            rand_id = "N/A"
        return rand_id

    # Генерация рандомного пароля;
    @staticmethod
    def pw() -> str:
        global mv_conf_path
        password_length = int(MV.password_length)
        # Перед обновлением, узнаем с какого конфига брать значения;
        mv_conf_path = Path(f"conf/{ConfSets.profiles[ConfSets.index]}/mv.ini")
        refresh_classes_vars(mv_conf_path, "Service")
        if Service.enabled == "false" and Service.fix_id_pw == "false":
            # Подгружаем из конфига предыдущее значение;
            if not Server.password:
                # Убираем похожие символы;
                let_dig = re.sub("[10IoOl]", "", ascii_letters + digits)
                while True:
                    rand_pw = ''.join(choice(let_dig) for i in range(password_length))
                    if (any(c.islower() for c in rand_pw)
                            and any(c.isupper() for c in rand_pw)
                            and sum(c.isdigit() for c in rand_pw) >= 3):
                        break
            else:
                rand_pw = Server.password
        else:
            rand_pw = Service.password
        return rand_pw
