import configparser
import socket
import subprocess
from os import chdir
from sys import path
from time import sleep


# Редактирование конфига;
def edit_config(conf_path: any, section: str, settings: str, value: str) -> None:
    config = configparser.ConfigParser()
    config.read(conf_path)
    config.set(section, settings, value)
    with open(conf_path, "w") as config_file:
        config.write(config_file, space_around_delimiters=False)


# Получение значений;
def get_config(conf_path: any, section: str, settings: str) -> any:
    config = configparser.ConfigParser()
    config.read(conf_path)
    return config.get(section, settings)


# Data Path VARS;
chdir(path[0])
cs_conf_path = "../../conf/confsets.ini"
confsets_index = int(get_config(cs_conf_path, "ConfSets", "index"))
confsets_profile = eval(get_config(cs_conf_path, "ConfSets", "profiles"))
mv_conf_path = f"../../conf/{confsets_profile[confsets_index]}/mv.ini"
rd_conf_path = f"../uvnc/UltraVNC.ini"
kitty_app = "../kitty.exe"


# Проверка работы режима - сервис;
enabled = get_config(mv_conf_path, "Service", "enabled")
if enabled == "false":
    exit()

# Config VARS;
service_id = get_config(mv_conf_path, "Service", "id")
service_check_interval = int(get_config(mv_conf_path, "Service", "check_interval")) * 60
tunnel_host = get_config(mv_conf_path, "Tunnel", "host")
tunnel_port = int(get_config(mv_conf_path, "Tunnel", "port"))
tunnel_user_server = get_config(mv_conf_path, "Tunnel", "user_server")
tunnel_key_server = "../" + (get_config(mv_conf_path, "Tunnel", "key_server")).lstrip('bin/')
rd_port = int(get_config(rd_conf_path, "admin", "portnumber"))
pids_k_tunnel = get_config(mv_conf_path, "Pids", "k_tunnel")


class Util:
    # Проверка, запущен ли процесс - по pid;
    @staticmethod
    def check_pid(pid: str) -> bool:
        command = ["taskkill", "/F", "/T", "/PID", pid]
        sp = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
        return sp == 0

    # Проверка доступности сервера, открыт или закрыт порт;
    @staticmethod
    def check_port(host: str, port: int) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                if s.connect_ex((host, port)) == 0:
                    return True
                else:
                    return False
        except Exception:
            return False

    # Запуск Tunnel (Если запущен, завершаем и ждем 10 сек);
    @staticmethod
    def run_tunnel() -> None:
        if Util.check_pid(pids_k_tunnel):
            sleep(10)
        # Скрываем появление окна;
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        sp = subprocess.Popen(
            f"{kitty_app} -P {tunnel_port} -i {tunnel_key_server} -T -N -R :{service_id}:127.1:{rd_port} "
            f"{tunnel_user_server}@{tunnel_host} -auto-store-sshkey", startupinfo=si
        )
        # Получаем PID процесса и записываем в config;
        popen_curpid = sp.pid
        edit_config(mv_conf_path, "Pids", "k_tunnel", str(popen_curpid))


def main():
    while True:
        if Util.check_port(tunnel_host, tunnel_port):
            Util.run_tunnel()
            break
        sleep(service_check_interval)


if __name__ == "__main__":
    main()
