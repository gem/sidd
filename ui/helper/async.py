# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
Support for asynchronous function call
"""
from threading import Thread
from time import sleep

from PyQt4.QtGui import QDialog, QBoxLayout, QProgressBar, QApplication

class AsyncProgressDialog(QDialog):
    """ dialog with progress bar to be shown during the asynchronous process """
    def __init__(self, parent=None):
        super(AsyncProgressDialog, self).__init__(parent)        
        self.setFixedSize(300, 40)
        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom, self))
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedSize(280, 20)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(10)  
        self.progress_bar.setTextVisible(False)     
        self.layout().addWidget(self.progress_bar)

class AsyncThread(Thread):
    """ thread that run asynchronous process and saves return value """
    def __init__(self, progress=None, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return_val = None
        self.execution_error = None
    
    def run(self):
        try:
            if self._Thread__target is not None:
                self._return_val = self._Thread__target(*self._Thread__args,
                                                        **self._Thread__kwargs)
        except Exception as err:            
            self.execution_error = err
            
    def join(self):        
        Thread.join(self)
        return self._return_val

def invoke_async(name, f, *args, **kw):
    """
    """
    thread = AsyncThread(target=f, args=args, kwargs=kw)
    progress = AsyncProgressDialog()
    progress.setWindowTitle(name)
    progress.show()
    progress_bar = progress.progress_bar
    step = (progress_bar.maximum() - progress_bar.minimum()) / 10.0
    
    thread.start()    
    while thread.isAlive():
        QApplication.processEvents()
        if progress_bar.value() < progress_bar.maximum():
            progress_bar.setValue(progress_bar.value()+step)
        else:
            progress_bar.setValue(progress_bar.minimum())    
        sleep(0.1)
    
    progress_bar.close()
    del progress_bar
    QApplication.processEvents()
    
    if thread.execution_error is not None:
        error = thread.execution_error
    else:
        error = False
    ret_val = thread.join()
    del thread
    if not error:
        return ret_val
    else:
        raise error
        