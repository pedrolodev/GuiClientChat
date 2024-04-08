from PyQt6 import QtCore, uic,QtWidgets
import os,sys,threading ,socket
import logging
import time
import config

form_class = uic.loadUiType(
    os.path.join(os.path.dirname(sys.argv[0]), 'ui', 'mainWindow.ui')
)[0]

logging.basicConfig(
    filename = 'c:\\Temp\\gui.log',
    level = logging.DEBUG, 
    format = time.strftime("%I:%M:%S")+' %(levelname)-7.7s %(message)s'
)

class MyWindowClass(QtWidgets.QMainWindow, form_class):

    stop = False

    def __init__(self):
        try:
            QtWidgets.QMainWindow.__init__(self)
            self.setupUi(self)
            nombre = self.getUsuario().encode()
            """Conexiones"""
            self.btEnviar.clicked.connect(self.btenviarfn)
            """Conectar servidor"""
            self.s = socket.socket()
            self.lMensajes.append('conectando')
            self.s.connect((config.SERVER_IP, config.SERVER_PORT))
            self.lMensajes.append('conectado correctamente')
            self.s.send(nombre)
            self.r = recibido(self.s,self.lMensajes,self.stop)
            self.r.setDaemon(True)
            self.r.start()
        except Exception as e:
            self.lMensajes.append('error conectando')
            logging.info("Error conectando")
            logging.info(str(e))

    def keyPressEvent(self, event):
        key = event.key()
        """Key_return intro normal, key_enter intro numerico"""
        if key == QtCore.Qt.Key.Key_Enter or key == QtCore.Qt.Key.Key_Return:
            self.btEnviar.click()

    def closeEvent(self, evnt):
        try:
            logging.info("CERRANDO")
            self.stop = True
            self.s.close()
            sys.exit(0)
        except Exception as e:
            logging.info("Closing error")
            logging.info(e)

    def getUsuario(self):
        nusu = ['',False]
        while(nusu[1] == False or nusu[0] == ""):
            nusu = QtWidgets.QInputDialog.getText(self,
                                              "Nombre de usuario",
                                              "Nombre de usuario:"
                                              )
            logging.info(str(nusu))
        return nusu[0]

    def btenviarfn(self):
        try:
            
            msg = str(self.tbMensaje.text())
            if(msg != ""):
                logging.info("MENSAJE ENVIADO "+msg)
                self.s.send(msg.encode())
                self.tbMensaje.setText("")
        except Exception as e:
            logging.info(str(e))

class recibido(threading.Thread):
    def __init__(self,socket,contenedor,stop):
        threading.Thread.__init__(self)
        self.soc = socket
        self.contenedor = contenedor
        self.stop = stop

    def run(self):
        while True:
            try:
                r = self.soc.recv(1024)
                a = r.decode('utf-8')
                logging.info("MENSAJE RECIBIDO "+a)
                self.contenedor.append(a)
            except Exception as e:
                logging.info("RECIBED ERROR")
                logging.info(e)
                break;
                
    



