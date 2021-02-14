import pythoncom, pyHook

def OnKeyboardEvent(event):
    print('++ Key : ', event.Key, end ='')
    print('    KeyID : ', event.KeyID)
    return True

def run():
    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()
    
def main():
    run()
    
if __name__=='__main__':
    main()