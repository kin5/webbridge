# webbridge
A bridge between pywebview and your web application.

# installation
`pip install webbridge`

or if you don't enjoy the ease of pip, download the source and run

`python setup.py install`

# dependencies
The only hard dependency is [pywebview](https://github.com/r0x0r/pywebview) which this package is made to *compliment* (not replace).

# basic usage
If pywebview is your 4k TV, and the web application is your cable box, webbridge is that nice, standardized HDMI cable that allows them to play nicely together. It could also be considered your nice, oak entertainment center that keeps your expensive TV from crushing your cable box, but I digress.

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

app = Bridge()

if __name__ == "__main__":
  
  app.run()
```

And that's it. All the specifics have already been defined by you in the config file. Sit back, relax, and enjoy your web app as a desktop application.

Unless of course it *doesn't work*, which in that case you should head on over to the issues section and let me know.

# advanced usage

Despite this applicaton not being very advanced, it has some nifty features for you to take advantage of.

## hooks
For extra special functionality, functions can be assigned to one of 7 *hooks*:
* before_server_start
* after_server_start
* before_server_close
* after_server_close
* before_client_start
* after_client_start
* after_client_close

There is one hook still under construction (and by that I mean I'm waiting until I'm smart enough to implement it):
* before_client_close

Assigning a function to a hook requires you to use the `hook` decorator method found within your `Bridge` instance.

For a simple example, let's say we want to print a message before and after the server starts. This recipe calls for two decorated functions. We can expand on our above example, easily extending it to perform these actions:

```python
from webbridge import Bridge

app = Bridge()

@app.hook("before_server_start")
def before_message():
  print "> Before server"

@app.hook("after_server_start")
def after_message():
  print "> After server"

if __name__ == "__main__":
  
  app.run()
```

And just like that we have functions executing all over the place.

## blow
This function is a bit of a doozy, and currently only works on Windows. It will literally blow the Bridge (Get it? Guys?).

Bad jokes aside, this function is a remnant of my attempt at forking pywebview to implement borderless window functionality (speaking specifically for Windows). The function posts a quit message (WM_DESTROY) to the window boasting the title supplied in your config.json. It's not bullet proof, so I'll be working on improving it down the road. Currently, pywebview doesn't support borderless application windows. This function came in handy when the application had no border as it also had no exit button. I *desperately* want this borderless functionality to exist down the road, as the possibility for beatuiful, border-free applications is just too great to pass up (Yes, I'm drooling). Since I'm holding out for its existence, I'm leaving this function in for that wonderful day.

This function may come in handy even with bordered applications, but a realistic use case has yet to be proven on my end. I haven't tested it with other web architectures (basically anything != Python), but I would love to know if its use is available/helpful in them.

It's usage is simple:

```python
# Within your Python web application (not your main entry point file), you can blow the Bridge application
# by simply calling the blow() function.

from flask import Flask
from webbridge import blow

app = Flask(__name__)

@app.route("/")
def index():
  # A link to the '/blow' route.
  # This could be styled as an 'X' button or something similar.
  return "<a href='/blow'>Blow this bridge</a>"

@app.route("/blow")
def blow_it():
  # This route immediately calls the blow function which sends
  # a quit message to our application.
  blow()

if __name__ == "__main__":
  app.run()
```

I'd wager that tearing down your win32gui application has never been simpler.

# finally
Provide some feedback if you're interested in helping out. I'm always open to criticism and contribution.

#  changelog
## 0.1
**9/2/2016**

Widely untested, hardly proven, and pretty wild. Webbridge has pretty much only been tested with a local Flask application and live websites. This is the project in its infancy, so there will be more testing/development to come.
