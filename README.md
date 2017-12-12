<h1 align="center">Bitcoin Price Application (with Python)</h1>

<p align="center">
    <a href="https://travis-ci.org/julianYaman/bitcoinPriceApp_python"><img src="https://travis-ci.org/julianYaman/bitcoinPriceApp_python.svg?branch=master"></a>
    <img src="https://img.shields.io/badge/language-python-blue.svg" />
    <a href="https://discord.gg/ccpgH3b"><img src="https://discordapp.com/api/guilds/358751806697897984/embed.png" /></a>
    <a href="https://twitter.com/intent/user?screen_name=julianYaman"><img src="https://img.shields.io/twitter/follow/julianyaman.svg?style=social&label=Follow" /></a>
    <img src="https://img.shields.io/github/languages/code-size/julianYaman/bitcoinPriceApp_python.svg" alt="Code Size" />
</p>

## Installation:
To install all dependencies which are required for this project, run:

the **Bash script**

```
> install.sh
```

or with **pip**:

```
> pip install -r requirements.txt
```

## Usage:
**To run the project type:**

```
> python getprice.py
```

<hr>

If you are going to add new functions, add them to **test_class.py** and run 
```
> pytest
``` 
for testing everything and don´t forget to **import** every function in the file.

## Description

With this python application, you can check the price of one Bitcoin (currently you get the result in a console output).

At the moment, I use the **[BitPay API](https://bitpay.com/api/rates/usd)** for getting the current price in US Dollar.

**Note from the developer of the main repository (delete it when you fork it):**

My main purpose for creating this project is to learn more about Python and its libraries.

## Planned updates:

- **Automatic price refresh every minute:** Every minute, the price should be updated.

- **Changing between exchanges:** The user should be able to switch to any exchange and set it to the main one so the user will only see his preferred exchange option.
