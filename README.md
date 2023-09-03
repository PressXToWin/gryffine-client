# Gryffine-client

Linux OS Login Attempts Monitoring and Auditing System (client-side). This software sends real-time login attempt information to the server.

## How it works

This script is executed using PAM (Pluggable Authentication Module). Information about the login attempt and its details are passed to the script's environment. Then, this information is sent to a preconfigured endpoint using a POST request. It is intended to be used together with [Gryffine-server](https://github.com/PressXToWin/gryffine-server), but there are no artificial technical limitations on its use with an alternative server-side component.

## Installation
Clone the repository

```git clone https://github.com/PressXToWin/gryffine-client.git```

Copy the script to the directory ```/usr/local/bin/```

```sudo cp gryffine-client/gryffine.py /usr/local/bin/gryffine.py```

Create a backup of the PAM configuration

```sudo cp /etc/pam.d/common-auth /etc/pam.d/common-auth.bkp```

Modify the PAM configuration as follows:
* Change the line 

```auth    [success=1 default=ignore]      pam_unix.so nullok_secure```

to

```auth    [success=2 default=ignore]      pam_unix.so nullok_secure```

* Add the following line with action for case of failed login and set the endpoint

```auth    optional                        pam_exec.so /usr/local/bin/gryffine.py http://gryffine-server/api/v1/records/ fail```

* After the line

```auth    requisite                       pam_deny.so```

add action for case of successful login and set the endpoint

```auth    optional                        pam_exec.so /usr/local/bin/gryffine.py http://gryffine-server/api/v1/records/ success```

As a result, it should look something like this:

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