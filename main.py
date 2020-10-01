import threading
from tkinter.filedialog import *
from pytube import YouTube, request
from general import append_to_file


# dark mode :
def darkmode():
    global btnState
    if btnState:
        btn.config(image=offImg, bg="#CECCBE", activebackground="#CECCBE")
        root.config(bg="#CECCBE")
        txt.config(text="Dark Mode: OFF", bg="#CECCBE")
        btnState = False
    else:
        btn.config(image=onImg, bg="#2B2B2B", activebackground="#2B2B2B")
        root.config(bg="#2B2B2B")
        txt.config(text="Dark Mode: ON", bg="#2B2B2B")
        btnState = True


is_paused = is_cancelled = False


def download_video(url):
    global is_paused, is_cancelled
    download_button['state'] = 'disabled'
    pause_button['state'] = 'normal'
    cancel_button['state'] = 'normal'
    try:
        progress['text'] = 'Connecting ...'
        yt = YouTube(url)
        stream = yt.streams.first()
        filesize = stream.filesize
        with open('sample.mp4', 'wb') as f:
            is_paused = is_cancelled = False
            stream = request.stream(stream.url)
            downloaded = 0
            while True:
                if is_cancelled:
                    progress['text'] = 'Download cancelled'
                    break
                if is_paused:
                    continue
                chunk = next(stream, None)
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress['text'] = f'Downloaded {downloaded} / {filesize}'
                else:
                    # no more data
                    progress['text'] = 'Download completed'
                    break
        print('done')
    except Exception as e:
        print(e)
    download_button['state'] = 'normal'
    pause_button['state'] = 'disabled'
    cancel_button['state'] = 'disabled'

    def downloader(video_link, down_dir=None):
    try:
        tube = YouTube(video_link)
        title = tube.title
        print("Now downloading,  " + str(title))
        video = tube.streams.filter(progressive=True, file_extension='mp4').first()
        print('FileSize : ' + str(round(video.filesize/(1024*1024))) + 'MB')
        # print(tube.streams.filter(progressive=True, file_extension='mp4').first())
        # Stream(video).on_progress()
        if down_dir is not None:
            video.download(down_dir)
        else:
            video.download()
        print("Download complete, " + str(title))
        caption = tube.captions.get_by_language_code('en')
        if caption is not None:
            subtitle = caption.generate_srt_captions()
            open(title + '.srt', 'w').write(subtitle)
    except Exception as e:
        print("ErrorDownloadVideo  |  " + str(video_link))
        append_to_file('debug', format(e))
    # FILESIZE print(tube.streams.filter(progressive=True, file_extension='mp4').first().filesize/(1024*1024))

def start_download():
    threading.Thread(target=download_video, args=(url_entry.get(),), daemon=True).start()


def toggle_download():
    global is_paused
    is_paused = not is_paused
    pause_button['text'] = 'Resume' if is_paused else 'Pause'


def cancel_download():
    global is_cancelled
    is_cancelled = True


# gui
root = Tk()
root.title("Youtube Downloader")
root.iconbitmap("main img/icon.ico")
root.geometry("500x650")

# switch toggle:
btnState = False

# switch images:
onImg = PhotoImage(file="dark img/switch-on.png")
offImg = PhotoImage(file="dark img/switch-off.png")

# Copyright
originalBtn = Button(root, text="Made by Swapnil", font="Rockwell", relief="flat")
originalBtn.pack(side=BOTTOM)

# Night Mode:
txt = Label(root, text="Dark Mode: OFF", font="FixedSys 17", bg="#CECCBE", fg="green")
txt.pack(side='bottom')

# switch widget:
btn = Button(root, text="OFF", borderwidth=0, command=darkmode, bg="#CECCBE", activebackground="#CECCBE", pady=1)
btn.pack(side=BOTTOM, padx=10, pady=10)
btn.config(image=offImg)

# main icon section
file = PhotoImage(file="main img/youtube.png")
headingIcon = Label(root, image=file)
headingIcon.pack(side=TOP, pady=3)

# Url Field
url_entry = Entry(root, justify=CENTER, bd=5, fg='green')
url_entry.pack(side=TOP, fill=X, padx=10)
url_entry.focus()

# Download Button
download_button = Button(root, text='Download', width=10, command=start_download, font='verdana', relief='ridge', bd=5, bg='#f5f5f5', fg='black')
download_button.pack(side=TOP, pady=20)

# Progress
progress = Label(root)
progress.pack(side=TOP)

# Pause Button
pause_button = Button(root, text='Pause', width=10, command=toggle_download, state='disabled', font='verdana', relief='ridge', bd=5, bg='#f5f5f5', fg='black')
pause_button.pack(side=TOP, pady=20)

# Cancel Button
cancel_button = Button(root, text='Cancel', width=10, command=cancel_download, state='disabled', font='verdana', relief='ridge', bd=5, bg='#f5f5f5', fg='black')
cancel_button.pack(side=TOP, pady=20)

root.mainloop()
