from tkinter import *
from threading import Thread
import socketserver
import queue
import logging
import os

# logging configuration
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=os.environ.get("LOG_LEVEL", "DEBUG"))
CMDQ = queue.Queue(maxsize=0)

LISTEN_HOST = os.environ.get('LISTEN_HOST', '127.0.0.1')
LISTEN_PORT = int(os.environ.get('LISTEN_PORT', '1337'))
LISTEN_SECRET = b'UNCONTAINED'
ESCAPE_CODE = "<Escape>."
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



class Splasher(Thread):
    def __init__(self):
        super(Splasher, self).__init__(name="Splasher")

    def parse(self):
        try:
            cmd = CMDQ.get(block=False)
            logging.debug("SPL: removed (%s) from queue" % (cmd))
            if (cmd == LISTEN_SECRET):
                self.ascii_splash()
            CMDQ.task_done()
        except queue.Empty:
            pass
        self.root.after(500, self.parse)

    def run(self):
        self.root = Tk()
        self.root.withdraw()
        self.root.after(0, self.parse)
        self.root.mainloop()

    def ascii_splash(self):
        logging.debug("SPL: generating new splash window")
        splash_screen = Toplevel(self.root)

        splash_screen.attributes("-topmost", True)
        splash_screen.attributes('-fullscreen', True)
        splash_screen.bind(ESCAPE_CODE, lambda w: w.widget.destroy())  # Exit on Escape + period
        splash_screen.focus_force()
        splash_screen.lift()

        ascii_label = Label(splash_screen, text=SPLASH_MESSAGE)
        ascii_label.config(bg="red", fg="white", font=('Courier', 18))
        ascii_label.pack(side=TOP, expand=YES, fill=BOTH)

class SplashListener(socketserver.StreamRequestHandler):
    def handle(self):
        cmd = self.rfile.readline().strip()
        CMDQ.put(cmd)
        logging.debug("SRV: client %s added (%s) to queue" % (self.client_address[0], cmd))

try:
    tk_worker = Splasher()
    tk_worker.setDaemon(True)
    tk_worker.start()
except Exception as e:
    logging.error("SPL: failed to start Splash Worker thread (%s)"
                  % (e))
    raise
else:
    logging.info("SPL: successfully created Splash Worker thread")

try:
    server = socketserver.TCPServer((LISTEN_HOST, LISTEN_PORT), SplashListener)
    logging.info("SRV: starting splash server on %s:%s triggering on '%s'" % (LISTEN_HOST, LISTEN_PORT, LISTEN_SECRET))
    server.serve_forever(poll_interval=0.5)
except IOError as e:
    logging.error("SRV: IO exception encountered while starting secret splash server (%s) shutting down"
                  % (e))
    CMDQ.join()
    tk_worker.stop()
    raise
