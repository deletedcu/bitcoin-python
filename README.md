<h1 align="center">Bitcoin Price Application (with Python)</h1>

<p align="center">
    <a href="https://travis-ci.org/julianYaman/bitcoinPriceApp_python"><img src="https://travis-ci.org/julianYaman/bitcoinPriceApp_python.svg?branch=master"></a>
    <img src="https://img.shields.io/badge/language-python-blue.svg" />
    <a href="https://discord.gg/ccpgH3b"><img src="https://discordapp.com/api/guilds/358751806697897984/embed.png" /></a>
    <a href="https://twitter.com/intent/user?screen_name=julianYaman"><img src="https://img.shields.io/twitter/follow/julianyaman.svg?style=social&label=Follow" /></a>
    <img src="https://img.shields.io/github/languages/code-size/julianYaman/bitcoinPriceApp_python.svg" alt="Code Size" />
    <img src="https://img.shields.io/badge/master--version-2.4.2-brightgreen.svg" />
    <a href="https://github.com/julianYaman/bitcoinPriceApp_python/"><img src="https://img.shields.io/github/release/julianYaman/bitcoinPriceApp_python.svg" /></a>
</p>

<p align="center"><b>This application works with Python 2.7 and newer!</b><p>

## Installation:
To install all dependencies which are required for this project, run:

the **Bash script** (recommended, use this on Linux)

```
> install.sh
```

the **Bash script** (recommended, use this on Windows)

```
> install.cmd
```

or run the **pip** command:

```
> pip install -r requirements.txt
```

## Usage:
**To run the project type:**

```
> set FLASK_APP=getprice.py (use set on Windows)
> export FLASK_APP=getprice.py (use this if you are not on Windows)
> flask run
```

<hr>

If you are going to add new functions, add them to **testapp.py** and run 
```
> pytest testapp.py -s
``` 
for testing everything and don´t forget to **import** every function in the file.

## Description

With this python application, you can check the price of one Bitcoin (currently you get the result in a console output).

At the moment, I use the **[BitPay API](https://bitpay.com/api/rates)** for getting the current price in US Dollar.

## Planned updates:

- **Automatic price refresh every minute:** Every minute, the price should be updated.

- **Changing between exchanges:** The user should be able to switch to any exchange and set it to the main one so the user will only see his preferred exchange option.
