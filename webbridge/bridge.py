import os
import json
import win32gui, win32con
import platform

from webbridge.client import Client
from webbridge.server import Server

def cleanup_config(cfg):
    """
    Clean up the supplied config.
    
    Utility function for checking whether or not the config.json map supplies all
    the required config values. Using the DEFAULT_CONFIG_KEYS dictionary, this function
    checks the supplied config and verifies that each default key exists within. Any key that
    it can't find will be added to the dictionary with the default value.
    
    @param (dict) cfg: the config map supplied in config.json
    @returns (dict) clean_cfg
    """
    
    DEFAULT_CONFIG_KEYS = {
        "title": "",
        "cmd": "",
        "url": "",
        "borderless": False
    }
    
    clean_cfg = dict(cfg)
    
    for key in DEFAULT_CONFIG_KEYS:
        if key not in clean_cfg:
            clean_cfg[key] = DEFAULT_CONFIG_KEYS[key]
            print "> key {} not found in config.json, supplying default".format(key)
            
    return clean_cfg

def blow():
    """
    Blow the bridge. Get it? Guys?
    
    This function is for embedding a killswitch in the actual web application.
    Currently only supports windows.
    Also, not sure how this would be done in a non-python web app (i.e. not sure
    how a backend like Node would call this command).
    This function can be called outside of the client's process, since it sends the
    message to the window directly.
    
    Scenario:
        Your webview is borderless which means there is no "X" button obviously available
        to the user. This is not good for UX, but you love your slick border free UI. To
        allow for an easy means of exiting the window for the user, you create a button that
        triggers a function on your calling webbridge.bridge.blow(). This sends a message to
        the window to destroy it.
    """
    if platform.system() == "Windows":
        if os.path.exists(os.path.join(os.getcwd(), "config.json")):
            cfg_file = open(os.path.join(os.getcwd(), "config.json"), "r")

            try:
                title = json.loads(cfg_file.read())["title"]
            except KeyError:
                raise KeyError("no title in config, can't blow the bridge")
        else:
            raise Exception("no config file found, no window title provided, can't blow the bridge")

        def enum_windows(hwnd, window_list):
            window_list.append(hwnd)

        windows = []
        win32gui.EnumWindows(enum_windows, windows)

        bridge_window = None

        for w in windows:
            if win32gui.GetWindowText(w) == unicode(title.decode("utf-8")):
                bridge_window = w
                break

        if bridge_window is not None:
            win32gui.SendMessage(bridge_window, win32con.WM_DESTROY)
        else:
            print "bridge.blow: no window with title '{}' found, can't blow the bridge".format(title)
    else:
        raise Exception("currently only Windows blow()'s (in a sense you're lucky to see this error)")
    

class Bridge:
    """
    Bridge class that handles web app and webview.
    config.json necessary for options.
    
    .run():
        Main method to run the web app and webview together.
        First starts the web app in its own process, if 'cmd'
        exists in the config, then creates a webview client in 
        it's own process.
        
        This method fires hooks supplied by self.hooks and
        triggered by self._do_hook().
        
    .hook():
        Decorator method that appends a function to the supplied
        hook's list in self.hooks.
        
    ._do_hook():
        Method to execute all functions for the supplied hook
        in self.hooks.
    """
    def __init__(self):
        
        # config retrieval
        if os.path.exists(os.path.join(os.getcwd(), "config.json")):
            cfg_file = open(os.path.join(os.getcwd(), "config.json"), "r")

            self.config = json.loads(cfg_file.read())
        else:
            raise Exception("No config supplied; config.json needed in working directory")
            
        # Clean up config
        self.config = cleanup_config(self.config)
        
        # Create the client. Required for minimal functionality
        if self.config["title"] != "" and self.config["url"] != "":
            self.client = Client(self.config["title"], self.config["url"])
        else:
            raise Exception("'title' and 'url' required, one or the both not supplied; check your config.json")
        
        # Create the server. Not required, reliant on the 'cmd' config key.
        if self.config["cmd"] != "":
            self.server = Server(self.config["cmd"])
        else:
            self.server = None
            
        self.hooks = {
            # Server hooks
            "before_server_start": [],
            "after_server_start": [],
            "before_server_close": [],
            "after_server_close": [],
            
            # Client hooks
            "before_client_start": [],
            "after_client_start": [],
            "before_client_close": [], # TODO
            "after_client_close": []
        }
    
    def run(self):
        """
        Main method for running a Bridge. Starts by running
        the server (if it exists). Then the client is called to run.
        Hook functions are executed in their respective positions.
        """
        # Start the server, perform server_start hooks
        if self.server is not None:
            self._do_hook("before_server_start")
            
            self.server.run()
            
            self._do_hook("after_server_start")
        
        # Start the client, perform client_start hooks
        self._do_hook("before_client_start")
        self.client.run()
        
        self._do_hook("after_client_start")
        
        # Main application loop.
        # Wait until the client has closed.
        while self.client.running():
            pass
        
        self._do_hook("after_client_close")
        
        # Kill the server after the client has closed
        if self.server is not None:
            self._do_hook("before_server_close")
            self.server.kill()
            self._do_hook("after_server_close")
            
    def hook(self, hook):
        """
        Decorator for adding functions to the lists in
        self.hooks.
        
        @param (str) hook: hook to append function to
        """
        
        def hook_wrapper(func):
            try:
                self.hooks[hook].append(func)
            except KeyError:
                print "Bridge: no such hook {}, skipping".format(hook)
            
        return hook_wrapper
    
    def _do_hook(self, hook):
        """
        Method to execute all functions within function lists
        in self.hooks for the supplied hook.
        
        @param (str) hook: hook to execute
        """
        print "bridge: doing hook {}".format(hook)
        for func in self.hooks[hook]:
            func()