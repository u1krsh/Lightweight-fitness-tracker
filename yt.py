    import os
    import tkinter as tk
    from tkinter import messagebox
    import vlc
    import yt_dlp

    class YouTubePlayer:
        def __init__(self, master):
            self.master = master
            self.master.title("YouTube Video Player")
            self.master.geometry("800x600")
            
            self.video_frame = tk.Frame(self.master)
            self.video_frame.pack(padx=10, pady=10, fill="both", expand=True)

            self.vlc_instance = vlc.Instance()
            self.player = self.vlc_instance.media_player_new()

            self.url_entry = tk.Entry(self.master, width=50)
            self.url_entry.pack(pady=10)

            self.play_button = tk.Button(self.master, text="Play Video", command=self.play_video)
            self.play_button.pack(pady=5)

        def play_video(self):
            url = self.url_entry.get()
            if not url:
                messagebox.showerror("Error", "Please enter a valid YouTube URL.")
                return

            try:
                # Use yt-dlp to get the best video stream URL
                ydl_opts = {
                    'format': 'best',
                    'noplaylist': True,
                    'quiet': True
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    video_url = info_dict['url']

                # Load the video URL into VLC
                media = self.vlc_instance.media_new(video_url)
                self.player.set_media(media)

                # Set the player to display video in the tkinter window
                self.player.set_hwnd(self.video_frame.winfo_id())

                # Play the video
                self.player.play()

            except Exception as e:
                messagebox.showerror("Error", f"Could not play video: {e}")

    if __name__ == "__main__":
        root = tk.Tk()
        app = YouTubePlayer(root)
        root.mainloop()
