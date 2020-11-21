# Huawei LTE Router Quick Info

UI Overview:
![GUI overview](https://github.com/NAbdulla1/Huawei-LTE-Router-Quick-Info/blob/main/router%20controller%20ui.png?raw=true)

Create a file named `conf.json` in the root directory or  and populate it with following information (if the file is not created, a file will be created automatically with default values, then you need to edit that file):
```
{
    "router-ip": "192.168.8.1",
    "admin": {
        "username": "your username",
        "password": "your password"
    },
    "update-interval": 1, (this value in seconds)
    "color1": {
        "r": 250,
        "g": 250,
        "b": 250
    },
    "color2": {
        "r": 220,
        "g": 220,
        "b": 220
    }
}
```