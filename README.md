# microViewer
<p align="center">
  <img width="285" height="267" src="https://github.com/isMTv/microViewer/blob/main/screens/mv_main.png">
</p>

Софт для получения удаленного доступа к ПК через собственный OpenSSH сервер. Написан на языке Python с использованием QT и сторонних программ Gungnir, Kitty, Nosleep.

### Возможности:
* Настроить под собственный OpenSSH сервер;
* Не требователен к пропускной способности сети Интеренет;
* Авторизация по ключам (OpenSSH);
* Может работать как сквозь NAT, так и внутри локальной сети;
* Доступ по ID/IP/DNS-имени ПК (выбирается в режимах);
* Адресная книга с возможностью поиска записей, может работать отдельно от основной программы;
* Создание профилей для настроек программы и записей Адресной книги;
* Автоматическое переподключение клиента к туннелю при отключении Интернета;
* Работа в режиме сервера (для временного включения доступа);
* Работа в режиме службы (получить постоянный доступ, возможно подключиться к ПК на этапе LogonScreen);
* В режиме службы, когда ID/Пароль закреплены, пароль зашифрован средствами Gungnir (Отобразится в окне MV при повторном запуске);
* Передача файлов с возможностью перетаскивания в(из) окно программы;
* Автоматическое cохранение ID/Пароля от предыдущего запуска (Сброс сохроненных данных осуществляется кнопкой обновить);
* Задать свои ID/Пароль (диапазон ID 19000-19999, не пересекается с основным 20000-60000);
* Одновременная работа Серверного/Клиентского подключения;
* Оставить серверную пару Логин/Ключ и запускать на ПК на которых будет работать только режим сервера;

### Для работы microViewer необходимы:
* Gungnir (http://blog.x-row.net/?p=17878);
* Kitty (https://github.com/cyd01/KiTTY);
* Nosleep (https://github.com/CHerSun/NoSleep);

### QT:
* x32_QT5: (Win7) - Windows 7sp1-11;
* x32_QT5: Windows 8.1-11;
* x64_QT6: Windows 10-11 (Support 4K Displays);

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
# pip install --upgrade pip
# pip install pyqt6
# pip install wheel
# pip install nuitka
# pip install zstandard ordered-set (orderedset)

# nuitka -h, --help
(--standalone) или (--onefile)
 - kitty_service.py
# nuitka bin/kitty_service.py --onefile --follow-imports --windows-disable-console --windows-icon-from-ico=bin\ui\img\MicroViewer.ico --remove-output --windows-company-name='open-networks.ru' --windows-file-description='microViewer - Kitty_Service' --windows-file-version=x.x.x.x --windows-product-name='Kitty_Service'
 - main.py
# nuitka main.py --onefile --follow-imports --plugin-enable=pyqt6 --windows-disable-console --windows-icon-from-ico=bin\ui\img\MicroViewer.ico -o microViewer.exe --remove-output --windows-company-name='open-networks.ru' --windows-file-description='microViewer - Remote Access over SSH' --windows-file-version=x.x.x.x --windows-product-name='microViewer'
 - Windows 7 (x32):
python-3.8.10 (x32) для full updates
python-3.7.6 (x32) для no updates (Win7 SP1 [21.02.2011])
 - kitty_service.py
# nuitka bin/kitty_service.py --follow-imports --standalone --windows-disable-console --windows-icon-from-ico=bin\ui\img\MicroViewer.ico --remove-output --windows-company-name="open-networks.ru" --windows-file-description="microViewer - Kitty_Service" --windows-file-version=x.x.x.x --windows-product-name="Kitty_Service"
 - main.py
# nuitka main.py --follow-imports --plugin-enable=pyqt5 --standalone --windows-disable-console --windows-icon-from-ico=bin\ui\img\MicroViewer.ico --remove-output --windows-company-name="open-networks.ru" --windows-file-description="microViewer - Remote Access over SSH" --windows-file-version=x.x.x.x --windows-product-name="microViewer"
```
