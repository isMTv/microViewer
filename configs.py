import configparser


# Создание конфига для ConfSets;
def createconfig_confsets(conf_path):
    config = configparser.ConfigParser()
    config.add_section("ConfSets")
    config.set("ConfSets", "index", "0")
    config.set("ConfSets", "profiles", "['main']")
    with open(conf_path, "w") as config_file:
        config.write(config_file, space_around_delimiters=False)


# Создание конфига для MV;
def createconfig_mv(conf_path):
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
    config.set("Service", "fix_id_pw", "false")
    config.set("Service", "id", "19000")
    config.set("Service", "password", "")
    config.set("Service", "disable_sleep_mode", "false")
    config.set("Service", "disable_hibernation_mode", "false")
    config.set("Service", "disable_lock_screen", "false")
    config.add_section("Modes")
    config.set("Modes", "service", "false")
    config.add_section("Pids")
    config.set("Pids", "tun_service", "none")
    config.add_section("ParentWindow")
    config.set("ParentWindow", "position_x", "none")
    config.set("ParentWindow", "position_y", "none")
    with open(conf_path, "w") as config_file:
        config.write(config_file, space_around_delimiters=False)


# Создание конфига для RD;
def createconfig_rd(conf_path):
    config = configparser.ConfigParser()
    config.add_section("Permissions")
    config.add_section("admin")
    config.set("admin", "FileTransferEnabled", "1")
    config.set("admin", "FTUserImpersonation", "1")
    config.set("admin", "BlankMonitorEnabled", "1")
    config.set("admin", "BlankInputsOnly", "0")
    config.set("admin", "DefaultScale", "1")
    config.set("admin", "UseDSMPlugin", "0")
    config.set("admin", "DSMPlugin", "")
    config.set("admin", "primary", "1")
    config.set("admin", "secondary", "0")
    config.set("admin", "SocketConnect", "1")
    config.set("admin", "HTTPConnect", "0")
    config.set("admin", "AutoPortSelect", "0")
    config.set("admin", "PortNumber", "5900")
    config.set("admin", "HTTPPortNumber", "5800")
    config.set("admin", "InputsEnabled", "1")
    config.set("admin", "LocalInputsDisabled", "0")
    config.set("admin", "IdleTimeout", "0")
    config.set("admin", "EnableJapInput", "0")
    config.set("admin", "EnableUnicodeInput", "0")
    config.set("admin", "EnableWin8Helper", "0")
    config.set("admin", "QuerySetting", "2")
    config.set("admin", "QueryTimeout", "10")
    config.set("admin", "QueryDisableTime", "0")
    config.set("admin", "QueryAccept", "0")
    config.set("admin", "MaxViewerSetting", "0")
    config.set("admin", "MaxViewers", "5")
    config.set("admin", "Collabo", "0")
    config.set("admin", "Frame", "0")
    config.set("admin", "Notification", "0")
    config.set("admin", "OSD", "0")
    config.set("admin", "NotificationSelection", "0")
    config.set("admin", "LockSetting", "0")
    config.set("admin", "RemoveWallpaper", "0")
    config.set("admin", "RemoveEffects", "0")
    config.set("admin", "RemoveFontSmoothing", "0")
    config.set("admin", "DebugMode", "0")
    config.set("admin", "Avilog", "0")
    config.set("admin", "path", "")
    config.set("admin", "DebugLevel", "0")
    config.set("admin", "AllowLoopback", "1")
    config.set("admin", "LoopbackOnly", "0")
    config.set("admin", "AllowShutdown", "0")
    config.set("admin", "AllowProperties", "1")
    config.set("admin", "AllowInjection", "0")
    config.set("admin", "AllowEditClients", "1")
    config.set("admin", "FileTransferTimeout", "30")
    config.set("admin", "KeepAliveInterval", "5")
    config.set("admin", "IdleInputTimeout", "0")
    config.set("admin", "DisableTrayIcon", "0")
    config.set("admin", "rdpmode", "0")
    config.set("admin", "noscreensaver", "1")
    config.set("admin", "Secure", "0")
    config.set("admin", "MSLogonRequired", "0")
    config.set("admin", "NewMSLogon", "0")
    config.set("admin", "ReverseAuthRequired", "1")
    config.set("admin", "ConnectPriority", "0")
    config.set("admin", "service_commandline", "")
    config.set("admin", "accept_reject_mesg", "")
    config.add_section("UltraVNC")
    config.set("UltraVNC", "passwd", "")
    config.set("UltraVNC", "passwd2", "")
    with open(conf_path, "w") as config_file:
        config.write(config_file, space_around_delimiters=False)


# Создание конфига для Viewer;
def createconfig_viewer(conf_path):
    config = configparser.ConfigParser()
    config.add_section("options")
    config.set("options", "JapKeyboard", "1")
    config.set("options", "Reconnect", "12")
    config.set("options", "AutoReconnect", "10")
    config.set("options", "directx", "1")
    with open(conf_path, "w") as config_file:
        config.write(config_file, space_around_delimiters=False)


# Редактирование конфига;
def edit_config(conf_path, section, settings, value):
    config = configparser.ConfigParser()
    config.read(conf_path)
    config.set(section, settings, value)
    with open(conf_path, "w") as config_file:
        config.write(config_file, space_around_delimiters=False)


# Получение значений;
def get_config(conf_path, section, settings):
    config = configparser.ConfigParser()
    config.read(conf_path)
    value = config.get(section, settings)
    return value


# Удаление значений;
def remove_config(conf_path, section, settings):
    config = configparser.ConfigParser()
    config.read(conf_path)
    config.remove_option(section, settings)
    with open(conf_path, "w") as config_file:
        config.write(config_file, space_around_delimiters=False)
