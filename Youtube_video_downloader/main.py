
from pytube import YouTube
link = input("Enter the video link:")
print("Downloading.../")
YouTube(link).streams.first().download()
print("Download Successfull")
    
