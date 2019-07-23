# Back-End install

Ubuntu 18.04

## Requirements

```bash
sudo apt-get update
sudo apt-get dist-upgrade
sudo dpkg-reconfigure tzdata

sudo apt-get install apache2

sudo apt-get install python
sudo apt-get install python-pip
pip install pipenv
```

### Docker

...

### Certbot

[Certbot](https://certbot.eff.org/) is used to generate SSL certificates.
See [Certbot documentation](https://certbot.eff.org/lets-encrypt/ubuntubionic-apache) for installation process.

## Apache configuration

We use Apache server as proxy to the backend (running on port 5005).

Enable require Apache modules:
```bash
a2enmod proxy proxy_http
systemctl restart apache2.service
```

Setup your Virtual Host configuration (see [documentation](https://httpd.apache.org/docs/2.4/en/mod/mod_proxy.html)):
```ApacheConfig
ProxyPass / http://localhost:5005/
ProxyPassReverse / http://localhost:5005/
```

## Automated deploy

**Based on [*Deploy a website to a remote server with Git push*](https://medium.com/@francoisromain/vps-deploy-with-git-fea605f1303b)** by [@francoisromain](https://github.com/francoisromain)

Command to deploy from local:
```bash
git remote add deploy ssh://<user>@<ip-address>:/srv/app/git/backend.git
git push deploy
```
