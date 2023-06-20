import configparser


# Создание конфига для ConfSets;
def createconfig_confsets(conf_path: any) -> None:
    config = configparser.ConfigParser()
    config.add_section("ConfSets")
    config.set("ConfSets", "index", "0")
    config.set("ConfSets", "profiles", "['main']")
    config.add_section("Viewer")
    config.set("Viewer", "quality_index", "2")
    config.set("Viewer", "quality_presets", "((16, 6), (16, 4), (16, 2), (16, 0))")
    with open(conf_path, "w") as config_file:
        config.write(config_file, space_around_delimiters=False)


# Создание конфига для MV;
def createconfig_mv(conf_path: any) -> None:
    config = configparser.ConfigParser()
    config.add_section("MV")
    config.set("MV", "password_length", "7")
    config.set("MV", "connection_type", "id")
    config.set("MV", "mode_server_autorun", "false")
    config.add_section("ABOOK")
    config.set("ABOOK", "index", "0")
    config.set("ABOOK", "profiles", "['abook']")
    config.add_section("Tunnel")
    config.set("Tunnel", "host", "")
    config.set("Tunnel", "port", "22")
    config.set("Tunnel", "user_server", "mv_server")
    config.set("Tunnel", "key_server", "bin/keys/mv_server.ppk")
    config.set("Tunnel", "user_client", "mv_client")
    config.set("Tunnel", "key_client", "bin/keys/mv_client.ppk")
    config.add_section("Server")
    config.set("Server", "id", "")
    config.set("Server", "password", "")
    config.add_section("Service")
    config.set("Service", "enabled", "false")
    config.set("Service", "check_interval", "5")
    config.set("Service", "helper", "false")
    config.set("Service", "check_interval_helper", "180")
    config.set("Service", "fix_id_pw", "false")
    config.set("Service", "id", "19000")
    config.set("Service", "password", "")
    config.add_section("Modes")
    config.set("Modes", "service", "false")
    config.add_section("Pids")
    config.set("Pids", "k_tunnel", "none")
    config.add_section("ParentWindow")
    config.set("ParentWindow", "position_x", "none")
    config.set("ParentWindow", "position_y", "none")
    with open(conf_path, "w") as config_file:
        config.write(config_file, space_around_delimiters=False)


# Создание конфига для RD;
def createconfig_rd(conf_path: any) -> None:
    config = configparser.ConfigParser()
    config.add_section("admin")
    config.set("admin", "PortNumber", "5900")
    config.set("admin", "HTTPConnect", "0")
    config.set("admin", "AutoPortSelect", "0")
    config.set("admin", "MaxViewers", "5")
    config.set("admin", "AllowShutdown", "0")
    config.set("admin", "AllowEditClients", "0")
    config.set("admin", "FileTransferTimeout", "60")
    config.set("admin", "noscreensaver", "1")
    config.set("admin", "rdpmode", "1")
    config.add_section("UltraVNC")
    config.set("UltraVNC", "passwd", "")
    config.set("UltraVNC", "passwd2", "")
    with open(conf_path, "w") as config_file:
        config.write(config_file, space_around_delimiters=False)


# Создание конфига для Viewer;
def createconfig_viewer(conf_path: any) -> None:
    config = configparser.ConfigParser()
    config.add_section("options")
    config.set("options", "preferred_encoding", "16")
    config.set("options", "8bit", "2")
    config.set("options", "directx", "1")
    config.set("options", "JapKeyboard", "1")
    config.set("options", "Reconnect", "12")
    config.set("options", "AutoReconnect", "10")
    config.set("options", "filetransfertimeout", "60")
    with open(conf_path, "w") as config_file:
        config.write(config_file, space_around_delimiters=False)


# Редактирование конфига;
def edit_config(conf_path: any, section: str, settings: str, value: any) -> None:
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


# Удаление значений;
def remove_config(conf_path: any, section: str, settings: str) -> None:
    config = configparser.ConfigParser()
    config.read(conf_path)
    config.remove_option(section, settings)
    with open(conf_path, "w") as config_file:
        config.write(config_file, space_around_delimiters=False)
