import subprocess
import configparser
from os import chdir
from sys import path
from time import sleep


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

# Проверка работы режима - сервис;
enabled = get_config(mv_conf_path, "Service", "enabled")
if enabled == "false":
    exit()

# Config VARS;
tunnel_port = int(get_config(mv_conf_path, "Tunnel", "port"))


class Util:
    # Проверка, запущен ли процесс - по имени;
    @staticmethod
    def check_proc(name: str) -> bool:
        command = ["tasklist", "/fi", f"imagename eq {name}.exe"]
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="cp866"
        )
        if name in result.stdout:
            return True
        else:
            return False

    # Проверка, существует ли подключение на указанном порту;
    @staticmethod
    def check_conn(port: int) -> bool:
        command = f'netstat -ano -p tcp | find "{port}"'
        result = subprocess.call(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True
        )
        return result == 0

    # Запуск задачи в планировщике - k_tunnel;
    @staticmethod
    def run() -> None:
        command = f'schtasks /run /tn "Microsoft\Windows\microViewer\k_tunnel"'
        subprocess.call(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True
        )


def main():
    sleep(10)
    if not Util.check_proc("k_tunnel"):
        if not Util.check_conn(tunnel_port):
            Util.run()
        else:
            exit()
    else:
        exit()


if __name__ == "__main__":
    main()
