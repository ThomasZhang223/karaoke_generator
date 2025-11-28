from downloader import download_audio
import sys

def main():
    # Standard video
    audio1 = download_audio("https://www.youtube.com/watch?v=npUK_dnv1VM", "downloaded_audio", audio_format="mp3", bitrate=128)
    print(f'id: {audio1.id}; duration: {audio1.duration}; filesize: {audio1.file_size}')
    # Video in playlist
    audio2 = download_audio("https://www.youtube.com/watch?v=nSDgHBxUbVQ&list=RDkjD3LoXp-Pw&index=2", "downloaded_audio", audio_format="mp3", bitrate=128)
    print(f'id: {audio2.id}; duration: {audio2.duration}; filesize: {audio2.file_size}')
    
     # Video in playlist
    audio3 = download_audio("https://www.youtube.com/watch?v=NM4e606yFJg", "downloaded_audio", audio_format="mp3", bitrate=128)
    print(f'id: {audio3.id}; duration: {audio3.duration}; filesize: {audio3.file_size}')
    return 0
    
main()