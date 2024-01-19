import tkinter as tk
import crawl

window=tk.Tk()
window.title('Bilibili Downloader')
window.resizable(0,0)

urlString=tk.StringVar(window)
tk.Label(window,text="輸入你想下載的影片地址：").pack()
url=tk.Entry(window,width=50,textvariable=urlString).pack()

cookieString=tk.StringVar(window)
tk.Label(window,text="輸入你的cookie(有cookie才能下載高清影片)：").pack()
cookie=tk.Entry(window,width=50,textvariable=cookieString).pack()
def execute():
    url=urlString.get()
    cookie=cookieString.get()
    
    
    result=crawl.work(url,cookie)
    tk.Label(window,text=result).pack()

tk.Button(window,command=execute,text='執行').pack()

window.mainloop()



