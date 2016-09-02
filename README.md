# webbridge
A bridge between pywebview and your web application.

# installation
`pip install webbridge`

or if you don't enjoy the ease of pip, download the source and run

`python setup.py install`

# dependencies
The only hard dependency is [pywebview](https://github.com/r0x0r/pywebview) which this package is made to compliment. Without that, this package is basically nothing (in fact, it won't work at all).

# usage
If pywebview is your 4k TV, and your web applications is the cable box, webbridge is that nice, standardized HDMI cable that allows them to play nicely together.

Think of it as a bridge between your web app and the webview window.

## First
You need to create a proper `config.json` for the project. Check out the `example_config.json` file for the expected keys and their explanations. Why JSON? Because it's fairly universal and plays with Python very nicely. It was either JSON or my own custom super intuitive config file format; you can thank me later.

This config file should live in the same directory as your main file (the file that acts as your main execution point).

## Second
*coming soon, i promise*

#  changelog
## 0.1
**9/2/2016**

Widely untested, hardly proven, and pretty wild
