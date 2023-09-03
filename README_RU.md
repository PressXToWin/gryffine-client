# Gryffine-client

Система мониторинга и аудита попыток логина в ОС Linux (клиентская часть). Данный софт отправляет на сервер информацию о попытках входа в реальном времени.

## Как это работает

Данный скрипт запускается с помощью PAM (Pluggable Authentication Modules). В окружение скрипта передаётся информация о попытке логина и детали этой попытки. Далее эта информация идёт POST-запросом на заранее установленный эндпоинт. Предполагается использование вместе с [Gryffine-server](https://github.com/PressXToWin/gryffine-server), но каких-либо искусственных технических ограничений на использование с альтернативной серверной частью не накладывается. 

## Установка
Клонируем репозиторий

```git clone https://github.com/PressXToWin/gryffine-client.git```

Копируем скрипт в директорию ```/usr/local/bin/```

```sudo cp gryffine-client/gryffine.py /usr/local/bin/gryffine.py```

Создаём бэкап конфига PAM 

```sudo cp /etc/pam.d/common-auth /etc/pam.d/common-auth.bkp```

Изменяем конфиг PAM следующим образом:
* строчку 

```auth    [success=1 default=ignore]      pam_unix.so nullok_secure```

меняем на 

```auth    [success=2 default=ignore]      pam_unix.so nullok_secure```

* следующей строчкой добавляем сценарий действий на случай неудачного логина и указываем эндпоинт

```auth    optional                        pam_exec.so /usr/local/bin/gryffine.py http://gryffine-server/api/v1/records/ fail```

* после строчки 

```auth    requisite                       pam_deny.so```

добавляем сценарий действий на случай успешного логина и указываем эндпоинт

```auth    optional                        pam_exec.so /usr/local/bin/gryffine.py http://gryffine-server/api/v1/records/ success```

В результате должно получиться что-то наподобие

```
# here are the per-package modules (the "Primary" block)
auth    [success=2 default=ignore]      pam_unix.so nullok_secure
# here's the fallback if no module succeeds
auth    optional                        pam_exec.so /usr/local/bin/gryffine.py http://gryffine-server/api/v1/records/ fail
auth    requisite                       pam_deny.so
# prime the stack with a positive return value if there isn't one already;
# this avoids us returning an error just because nothing sets a success code
# since the modules above will each just jump around
auth    optional                        pam_exec.so /usr/local/bin/gryffine.py http://gryffine-server/api/v1/records/ success
auth    required                        pam_permit.so
# and here are more per-package modules (the "Additional" block)
auth    optional                        pam_cap.so 
# end of pam-auth-update config
```
