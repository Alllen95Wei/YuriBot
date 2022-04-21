def update(pid):
    import os
    import subprocess
    from time import sleep

    os.system("cd %USERPROFILE%\\PycharmProjects\\YuriBot")
    os.system("git pull")
    sleep(5)
    subprocess.Popen("\"執行Yuri Bot.bat\"", creationflags=subprocess.CREATE_NEW_CONSOLE)
    os.system("taskkill /f /PID {0}".format(pid))
