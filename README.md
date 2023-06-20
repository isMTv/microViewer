# microViewer
<p align="center">
  <img width="285" height="267" src="https://github.com/isMTv/microViewer/blob/main/screens/mv_main.png">
</p>

Софт для получения удаленного доступа к ПК через собственный OpenSSH сервер. Написан на языке Python с использованием QT и сторонних программ UltraVNC, KiTTY.

### Возможности:
* Настроить под собственный OpenSSH сервер;
* Не требователен к пропускной способности сети Интеренет;
* Авторизация по ключам (OpenSSH);
* Может работать как сквозь NAT, так и внутри локальной сети;
* Доступ по ID/IP/DNS-имени ПК (выбирается в режимах);
* Адресная книга с возможностью поиска записей, может работать отдельно от основной программы;
* Создание профилей для настроек программы и записей Адресной книги;
* Автоматическое переподключение к OpenSSH-туннелю при потере доступа к Интернет;
* Работа в режиме сервера (для временного включения доступа);
* Работа в режиме службы (получить постоянный доступ, возможно подключиться к ПК на этапе LogonScreen);
* В режиме службы, когда ID/Пароль закреплены, пароль будет зашифрован средствами UltraVNC (Отобразится в окне MV на вкладке "хост" при повторном запуске);
* Передача файлов, чат, возможность выбрать экран (при наличии второго монитора);
* Автоматическое cохранение ID/Пароля от предыдущего запуска (сброс сохроненной пары осуществляется кнопкой обновить);
* Задать свои ID/Пароль (диапазон ID 19000-19999, не пересекается с основным 20000-60000);
* Одновременная работа Серверного/Клиентского подключения;
* Оставить серверную пару Логин/Ключ и запускать на ПК на которых будет работать только режим сервера;

### Сторонние компоненты:
* UltraVNC (https://github.com/ultravnc/ultravnc);
* KiTTY (https://github.com/cyd01/KiTTY);

### QT:
* x32_QT5: (Win7) - Windows 7sp1-11;
* x32_QT5: Windows 8.1-11;
* x64_QT6: Windows 10-11 (Support 4K Displays);


### VNC Viewer:
```
 - Файл настроек:
# App_microViewer\conf\confsets.ini
[Viewer]
quality_index=2
quality_presets=((16, 6), (16, 4), (16, 2), (16, 0))

 - Расшифровка значений:
# Encoding:
 - ZRLE = 16
 - ZYWRLE = 17 | u2 = 10
 - XZ = 18 | XZYW = 19

# Colors:
 - 0: Full Colors
 - 1: 256 Colors
 - 2: 64 Colors
 - 3: 8 Colors
 - 4: 8 Dark Colors
 - 5: 4 Grey Colors
 - 6: Black & White
 ```

### Настройка OpenSSH сервера;
```
 - Авторизация по ключам:
# useradd -m -U -s /bin/bash mv_server
# passwd mv_server
# useradd -m -U -s /bin/bash mv_client
# passwd mv_client
# su - mv_server
# su - mv_client
---
$ mkdir .ssh
$ cat > .ssh/authorized_keys << EOF - ENTER вставляем наш публичный ключ ENTER - EOF
$ chmod 700 .ssh
$ chmod 600 .ssh/authorized_keys
---
# usermod -s /bin/false mv_server
# usermod -s /bin/false mv_client

Первые 3 параметра позволят быстрее убить сессию клиента, на стороне которого произошел разрыв соединения.
Иначе, после переподключения к SSH, RD-Клиент не сможет подключиться к RD-Cерверу.
# tee /etc/ssh/sshd_config.d/microviewer.conf >/dev/null <<EOF
TCPKeepAlive yes
ClientAliveInterval 5
ClientAliveCountMax 2

Match User mv_server
    PasswordAuthentication no
    AllowTcpForwarding remote
    AllowStreamLocalForwarding no
    AllowAgentForwarding no
    GatewayPorts no
    X11Forwarding no
    PermitTunnel no
    ForceCommand echo "You've successfully authenticated, but server does not provide shell access."

Match User mv_client
    PasswordAuthentication no
    AllowTcpForwarding local
    AllowStreamLocalForwarding no
    AllowAgentForwarding no
    GatewayPorts no
    X11Forwarding no
    PermitTunnel no
    ForceCommand echo "You've successfully authenticated, but server does not provide shell access."
EOF
# systemctl restart sshd.service
```

### Сборка с помощью Nuitka:
https://nuitka.net/doc/user-manual.html
```
 - Необходимые пакеты:
# python.exe -m pip install --upgrade pip
# pip install pyqt6 / для x32 pyqt5
# pip install wheel
# pip install nuitka
# pip install zstandard ordered-set (orderedset)
# pip install pywin32

# nuitka -h, --help
(--standalone) или (--onefile)
 - k_tunnel.py + k_tunnel_helper.py
# nuitka bin/k_utils/k_tunnel.py --follow-imports --standalone --windows-disable-console --windows-icon-from-ico=bin\ui\img\microViewer.ico --remove-output --windows-company-name='open-networks.ru' --windows-file-description='microViewer - Kitty_Tunnel' --windows-file-version=1.3.7.0 --windows-product-name='Kitty_Tunnel'
# nuitka bin/k_utils/k_tunnel_helper.py --follow-imports --standalone --windows-disable-console --windows-icon-from-ico=bin\ui\img\microViewer.ico --remove-output --windows-company-name='open-networks.ru' --windows-file-description='microViewer - Kitty_Tunnel_Helper' --windows-file-version=1.3.7.0 --windows-product-name='Kitty_Tunnel_Helper'
 - main.py
# nuitka main.py --onefile --follow-imports --plugin-enable=pyqt6 --windows-disable-console --windows-icon-from-ico=bin\ui\img\microViewer.ico -o microViewer.exe --remove-output --windows-company-name='open-networks.ru' --windows-file-description='microViewer - Remote Access over SSH' --windows-file-version=1.3.7.0 --windows-product-name='microViewer'
# nuitka main.py --standalone --follow-imports --plugin-enable=pyqt6 --windows-disable-console --windows-icon-from-ico=bin\ui\img\microViewer.ico --remove-output --windows-company-name='open-networks.ru' --windows-file-description='microViewer - Remote Access over SSH' --windows-file-version=1.3.7.0 --windows-product-name='microViewer'

 - Компиляция. Если для x64, то в переменной среды "Path": пути для x64 должны быть над x32;
- \Python310\Scripts\
- \Python310\
# x32, поднимаем вверх..
- \Python310-32\Scripts\
- \Python310-32\

 - Windows 7 (x32):
python-3.8.10 (x32) для full updates
python-3.7.6 (x32) для no updates (Win7 SP1 [21.02.2011])
 - k_tunnel.py + k_tunnel_helper.py
# nuitka bin/k_utils/k_tunnel.py --follow-imports --standalone --windows-disable-console --windows-icon-from-ico=bin\ui\img\microViewer.ico --remove-output --windows-company-name="open-networks.ru" --windows-file-description="microViewer - Kitty_Tunnel" --windows-file-version=1.3.7.0 --windows-product-name="Kitty_Tunnel"
# nuitka bin/k_utils/k_tunnel_helper.py --follow-imports --standalone --windows-disable-console --windows-icon-from-ico=bin\ui\img\microViewer.ico --remove-output --windows-company-name="open-networks.ru" --windows-file-description="microViewer - Kitty_Tunnel_Helper" --windows-file-version=1.3.7.0 --windows-product-name="Kitty_Tunnel_Helper"
 - main.py
# nuitka main.py --follow-imports --plugin-enable=pyqt5 --standalone --windows-disable-console --windows-icon-from-ico=bin\ui\img\microViewer.ico --remove-output --windows-company-name="open-networks.ru" --windows-file-description="microViewer - Remote Access over SSH" --windows-file-version=1.3.7.0 --windows-product-name="microViewer"
```
