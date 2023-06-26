import logging
import os
import queue
import socketserver
import threading
import tkinter
import signal


## logging configuration
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=os.environ.get("LOG_LEVEL", "DEBUG"))


## Server related configuration options
LISTEN_HOST = os.environ.get('LISTEN_HOST', '127.0.0.1')
LISTEN_PORT = int(os.environ.get('LISTEN_PORT', '1337'))
LISTEN_SECRET = os.environ.get('LISTEN_SECRET', 'UNCONTAINED')

## Splash screen related configuration
SPLASH_ESCAPE = "<Escape>."
SPLASH_BG_COLOUR = "red"
SPLASH_FG_COLOUR = "white"
SPLASH_FONT = "Courier"
SPLASH_MESSAGE = """
            $uuuu$$$$$uuuuuuu$           
             $uuuuuu$$uu$uuu$            
              $uu$$$$$$$$$$u             
               $u$u$$$$$$u$              
                u$$$$$$$u$               
                                         
                  $$$$u$                 
                 $$uuuu$$                
    $$$$u$$$u$   $$$u$u$$   $$$$uuu$$$   
    $$u$$u$$uu$    u$$$    $$$$$uuu$$u   
    $$u$$$$uuu$$          $u$$$$$uu$$$   
     $u$$u$u$u$            $u$$$u$$$u    
      $u$$$u$$              $u$u$$u$     
       $$$u$                $$$$u        
  uuu    u$$                  u$   uuu   
 u$$$$                            u$$$$  
  $$$$$uu                      uu$$$$$$  
u$$$$$$$$$$$uu             uuuu$$$$$$$$$$
$$$$'''$$$$$$$$$$uuu   uu$$$$$$$$$'''$$$'
 '''      ''$$$$$$$$$$$uu ''$'''         
           uuuu ''$$$$$$$$$$uuu          
  u$$$uuu$$$$$$$$$uu ''$$$$$$$$$$$uuu$$$ 
  $$$$$$$$$$''''           ''$$$$$$$$$$$'
   '$$$$$'    We_w1LL-n0t<b3   ''$$$$''  
     $$$'       C0NTA1N3D        $$$$'   
"""

# Creating global queue for communication between Server and Splasher
CMDQ = queue.Queue(maxsize=0)


class Worker(threading.Thread):
    def __init__(self):
        super(Worker, self).__init__(name="Worker")
        logging.info("WKR: created splash Worker thread")

    def run(self):
        while True:
            logging.debug("WKR: creating new Splasher instance")
            self.splash = Splasher()

class Splasher():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.after(0, self.parse)
        self.root.mainloop()

    def parse(self):
        try:
            cmd = CMDQ.get(block=False)
            logging.debug("SPL: removed '%s' from queue" % (cmd))
            if (cmd == LISTEN_SECRET):
                logging.debug("SPL: listen secret '%s' matched" % (cmd))
                self.splash()
            CMDQ.task_done()
        except queue.Empty:
            pass
        self.root.after(500, self.parse)

    def signal_handler(self, signum, frame):
        # Handle the signal here
        logging.debug("SPL: received signal %d ignoring..." % signum)

    def splash(self):
        logging.debug("SPL: creating new splash window")
        window = tkinter.Toplevel(self.root)

        window.attributes("-topmost", True)
        window.attributes('-fullscreen', True)
        window.bind(SPLASH_ESCAPE, lambda w: w.widget.destroy())
        window.focus_force()
        window.lift()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        label = tkinter.Label(window, text=SPLASH_MESSAGE)
        label.config(bg=SPLASH_BG_COLOUR, fg=SPLASH_FG_COLOUR,
                     font=(SPLASH_FONT, 18), cursor="none")
        label.pack(side=tkinter.TOP, expand=tkinter.YES,
                   fill=tkinter.BOTH)

class Server(socketserver.StreamRequestHandler):
    def handle(self):
        cmd = self.rfile.readline().decode().strip()
        CMDQ.put(cmd)
        logging.debug("SRV: client '%s' added '%s' to queue"
                      % (self.client_address[0], cmd))

if __name__ == "__main__":
    try:
        tk_worker = Worker()
        tk_worker.setDaemon(True)
        tk_worker.start()
    except Exception as e:
        logging.error("SPL: failed to start Splash Worker thread '%s'"
                      % (e))
        raise

    try:
        server = socketserver.TCPServer((LISTEN_HOST, LISTEN_PORT), Server)
        logging.info("SRV: starting Server on '%s:%s' triggering on secret '%s'"
                     % (LISTEN_HOST, LISTEN_PORT, LISTEN_SECRET))
        server.serve_forever(poll_interval=0.5)
    except IOError as e:
        logging.error("SRV: IO exception encountered while starting server '%s'"
                      % (e))
        raise
