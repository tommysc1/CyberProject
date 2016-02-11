#!/usr/bin/env python

import win32con, win32api, win32gui
from ctypes import *
from threading import Thread


class KeyboardHook:
    """
    To install the hook, call the (gasp!) installHook() function.
    installHook() takes a pointer to the function that will be called
    after a keyboard event.  installHook() returns True if everything
    was successful, and False if it failed
    Note:  I've also provided a function to return a valid function pointer
    
    To make sure the hook is actually doing what you want, call the
    keepAlive() function
    Note:  keepAlive() doesn't return until kbHook is None, so it should
    be called from a separate thread
    
    To uninstall the hook, call uninstallHook()    

    """
    # Capital letters
    vkeys_list = [ 65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90 ]

    check=False;
    

    def __init__(self):
        self.user32     = windll.user32
        self.kbHook     = None
        self.word=""
    
    def installHook(self, pointer):
        self.kbHook = self.user32.SetWindowsHookExA(
                              win32con.WH_KEYBOARD_LL,
                              pointer,
                              win32api.GetModuleHandle(None),
                              0 # this specifies that the hook is pertinent to all threads
        )
        return self.kbHook != None
    
    def keepAlive(self):
        if self.kbHook is None:
            return
        msg = win32gui.GetMessage(None, 0, 0)
        while msg is not None and self.kbHook is not None:
            win32gui.TranslateMessage(byref(msg))
            win32gui.DispatchMessage(byref(msg))
            msg = win32gui.GetMessage(None, 0, 0)
    
  

    def uninstallHook(self):
        if self.kbHook is None:
            return
        self.user32.UnhookWindowsHookEx(self.kbHook)
        self.kbHook = None

    ##################################################
    # returns a function pointer to the fn paramater #
    # assumes the function takes three params:       #
    # c_int, c_int, and POINTER(c_void_p)            #
    ##################################################
    def getFunctionPointer(self, fn):
        CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
        return CMPFUNC(fn)

    #############################################
    # Sample function to handle keyboard events #
    #############################################
    def kbEvent(self, nCode, wParam, lParam):
        if wParam is not win32con.WM_KEYDOWN: # It just occured to me that I should aso be checking for WM_SYSKEYDOWN as well
            self.user32.CallNextHookEx(self.kbHook, nCode, wParam, lParam)
            return self.user32.CallNextHookEx(self.kbHook, nCode, wParam, lParam)
        if lParam[0] in self.vkeys_list:
            print chr(lParam[0])
            self.word=self.word+chr(lParam[0])
        if chr(lParam[0])==' ' or lParam[0]==0xBC or lParam[0]==0x0D: #0xBC=','  0x0D='ENTER'
            self.check=True;
        if lParam[0]==0x08: #0x08='BACKSPACE'
            print "Deleted"
            self.word=self.word[:-1]
            
        return self.user32.CallNextHookEx(self.kbHook, nCode, wParam, lParam)

    def start(self):
        pointer = self.getFunctionPointer(self.kbEvent)
        self.installHook(pointer)
        #keyboardHook.uninstallHook()
        self.keepAlive()



