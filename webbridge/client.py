import multiprocessing

try:
    import webview
except:
    raise ImportError("webview not found")
    
class Client:
    
    def __init__(self, title, url, borderless=False):
        self.title = title
        self.url = url
        self.borderless = borderless #TODO: need to submit pull request to webview
        self.process = None
        self.running = False
    
    def run(self):
        self.process = multiprocessing.Process(target=self._handle_webview, args=(self._cleanup,))
        self.process.start()
        
        self.running = lambda: self.process.is_alive()
        
    def kill(self):
        
        if self.running != False:
            self.process.terminate()
            self.process.join()
        
    def _handle_webview(self, cleanup_callback):
        
        try:
            webview.create_window(self.title, self.url)
        except Exception as e:
            with open("error-log.txt", "w") as f:
                f.write(e)
        
        # After webview shuts down, cleanup
        cleanup_callback()
            
    def _cleanup(self):
        self.process.terminate()
        self.process.join()