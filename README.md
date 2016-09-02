# webbridge
A bridge between pywebview and your web application.

# installation
`pip install webbridge`

or if you don't enjoy the ease of pip, download the source and run

`python setup.py install`

# dependencies
The only hard dependency is [pywebview](https://github.com/r0x0r/pywebview) which this package is made to compliment. Without that, this package is basically nothing (in fact, it won't work at all).

# basic usage
If pywebview is your 4k TV, and your web applications is the cable box, webbridge is that nice, standardized HDMI cable that allows them to play nicely together.

Think of it as a bridge between your web app and the webview window.

## first
You need to create a proper `config.json` for the project. Check out the `example_config.json` file for the expected keys and their explanations, if you prefer. Why JSON? Because it's fairly universal and plays with Python very nicely. It was either JSON or my own custom super intuitive config file format; you can thank me later.

This config file should live in the same directory as your main file (the file that acts as your main execution point).

Keys:
* **title**: A title for the webview window
* **cmd**: The command to execute if running a server in the background for your web app (i.e. Flask, Node, etc.)
* **url**: The URL for webview to navigate its browser to

## second
Now that the config file exists, let's create our main file. Create a file called `main.py`. In that file, type the following:

```python
from webbridge import Bridge

if __name__ == "__main__":
  app = Bridge()
  
  app.run()
```

And that's it. All the specifics have already been defined by you in the config file. Sit back, relax, and enjoy your web app as a desktop application.

Unless of course it *doesn't work*, which in that case you should head on over to the issues section and let me know.

## finally
Provide some feedback if you're interested in helping out. I'm always open to criticism and contribution.

# advanced usage
*coming soon*

#  changelog
## 0.1
**9/2/2016**

Widely untested, hardly proven, and pretty wild. Webbridge has pretty much only been tested with a local Flask application and live websites. This is the project in its infancy, so there will be more testing/development to come.
