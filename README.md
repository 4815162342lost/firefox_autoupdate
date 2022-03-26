## Main goal
On Ubuntu, since 22.04, Firefox package will be delivered by snap instead of deb. I do not want to use snap. so, i download executiable file from official mozilla site (tar.bz2 archive) and use it:
https://www.mozilla.org/ru/firefox/download/thanks/

I unpacked downloaded tar.bz2 archive to /opt/firefox:
```
sudo tar -xjvf  /tmp/firefox-98.0.1.tar.bz2 -C /opt/firefox/
```

And dow path to executiable file:
**/opt/firefox/firefox/firefox**

For security purposes, i will run firefox from my current user, but /opt/firefox/ but must be owned by root (to avoid replacment due to vulnerability and etc.)

So, autoupdate will not work, because current user can not replace files in /opt/firefox

## How to install
```
Create directory:
mkdir /opt/firefox/
```
put **firefox_update.py** to mentioned catalog

Create systemd-service:
```
/etc/systemd/firefox_update.service
```

And copy content from this repo

Run this command:
```
sudo systemctl daemon-reload
```

And edit service:
```
sudo systemctl edit firefox_update.service
```

And put this line:
```
[Service]
Environment="firefox_path=/opt/firefox/"
```

Replace firefox_path (i.e. **"/opt/firefox/"**) to your firefox dirn (in my case firefox exe file here: /opt/firefox/firefox/firefox).

After that create systemd-timer:
```
/etc/systemd/system/firefox_update.timer
```

and copy conemt from repo.

Run again:
```
sudo systemctl daemon-reload
```

And
```
systemctl enable --now firefox_update.timer
```
