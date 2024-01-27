# rpi-statusscreen
daemon for my e-ink display to show awesome stats about the system


## install

```
raspi-config
```

Enable SPI, set locale to preference, keyboard


```
apt update
apt upgrade
apt install ansible
ansible-playbook configure.yaml
python -m build --wheel
```
