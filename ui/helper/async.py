# Copyright (c) 2011-2012, ImageCat Inc.
#
# SIDD is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# only, as published by the Free Software Foundation.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License version 3 for more details
# (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU Lesser General Public License
# version 3 along with SIDD.  If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> for a copy of the LGPLv3 License.
#
# Version: $Id: __init__.py 5 2012-08-28 23:14:35Z zh $

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
        self.layout().addWidget(self.progress_bar)

class AsyncThread(Thread):
    """ thread that run asynchronous process and saves return value """
    def __init__(self, progress=None, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return_val = None
    
    def run(self):
        if self._Thread__target is not None:
            self._return_val = self._Thread__target(*self._Thread__args,
                                                    **self._Thread__kwargs)
    def join(self):
        Thread.join(self)
        return self._return_val

def invoke_async(name, f, progress_bar=None, *args, **kw):
    """
    """
    thread = AsyncThread(target=f, *args, **kw)
    if progress_bar is None:
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
        sleep(1)
    return thread.join()