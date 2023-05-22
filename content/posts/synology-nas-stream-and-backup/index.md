---
title: "Synology NAS: Stream & Backup"
tags: ['NAS', 'Plex', 'Raspberry Pi', 'Synology', 'backup', 'self-hosting', 'streaming', 'time machine']
date: 2020-05-14T05:46:00+00:00
aliases: ["/synology-nas-stream-and-backup"]
canonicalURL: "/synology-nas-stream-and-backup"
---
This is the third issue of my #100DaysToOffload

My Synology NAS (DS 216play) has two 2 TB hard drives and serves two main purposes in my setup:

* Store media files (mainly movies and TV shows) & stream them
* Hold some backups

<!--more-->

## What I don't really use
I sporadically need to share files between devices when I don't have a USB key nearby or keep large files like some Linux images (I like to have at least one ready to use in case I have to troubleshoot a computer).

I also tried the collaborative editing features (NextCloud-like) but the lack of support for editing spreadsheets on the iPad was a deal breaker for me.

So, after having talked about what I don't use on my NAS, let's move on to the things I do with it!

## Media storage & streaming
I keep my media files in a volume that everyone could access through their computer (either from the Windows Explorer or the macOS Finder), but the preferred way of consuming these files is to use Plex.

I set up a Plex account, installed the package on the NAS and linked everything. I remember having to work a bit to allow external access but nothing too hard.

Now I can watch my content from anywhere and since I subscribed to the Plex Pass, I can also download it offline to my devices.

I also installed the Plex app on my Apple TV in order to have an easy access to my content there. Nothing more to say really: once you connect to your account, your library shows up and you can select a media and hit play.

I'm nearly at "drop a video and play it", but in some cases Plex needs to transcode the media to stream it to the Apple TV app and apparently my DS 216play's CPU [isn't powerful enough to do so on the fly](https://docs.google.com/spreadsheets/d/1MfYoJkiwSqCXg8cm5-Ac4oOLPRtCkgUxU0jdj3tmMPc/edit) ([source](https://support.plex.tv/articles/115002178853-using-hardware-accelerated-streaming/)). For these cases, I either try to convert the file beforehand with ffmpeg or I use VLC (there's also an Apple TV app).

I really like Plex: it has support for various devices, you can easily download subtitles for something you're playing, you can access your library from anywhere, it's very low maintenance. I'm a little annoyed by the "CPU not powerful enough" though, I'll work on that.

### Video files encoding, transcoding and streaming
*This part is more technical, feel free to jump to the backups if you want.*

Why wouldn't the NAS be able to play a video "in some cases"? In fact, every Plex player has a compatibility matrix of content you can play with it. The matrix has 5 dimensions:

* container file (e.g., MKV, AVI)
* video codec (e.g., mpeg4, H264)
* audio codec (e.g., mp3, aac)
* resolution
* bitrate

If your file has a combination of these that match the compatibility list of your player, then your media can be *direct played*. If everything's compatible except for the container, you can use *direct streaming*. Neither of these features require high CPU usage so I'm good to go, but if the media doesn't fall in one of these two categories, then the transcoding has to take place and the NAS is not powerful enough.[^1]

I'm no expert in transcoding and all but I understood that there are basically two types of operations: you can either "just" change the container of your media without having to re-encode every frame OR you can re-encode every frame. The first is light and can be done in a couple of seconds even on low-spec hardware (that's what Plex does by itself when it *direct streams*). The latter, though, would take hours or even days on my NAS for a single 4 GB movie; so I'm not considering it.

I will probably have a look at [HandBrake](https://handbrake.fr/) which I discovered while writing this article. It's a free and open source tool to transcode videos. That should help me cleanup my library and make everything compatible with the Apple TV.

[^1]: Plex documentation on direct play and direct stream: https://support.plex.tv/articles/200250387-streaming-media-direct-play-and-direct-stream/

## Backups
### MacBook
The other main thing I use my NAS for is keeping backups. The configuration here is also really easy too, at least for Time Machine on macOS:

1. Enable a file-sharing service like SMB
{{< img src="16.png" alt="Screenshot of the 'File Services' setting screen in Synology DSM" >}}

2. Advertise Time Machine on the protocol you enabled
{{< img src="17.png" alt="Screenshot of the 'File Services - Advanced' setting screen in Synology DSM" >}}

3. Configure your Mac to use your network drive as a Time Machine backup

This setup served me well for many months but it recently started to fail and I don't understand why yet. I just have a cryptic error on my Mac telling that the backup couldn't complete.

{{< img src="18.png" alt="Screenshot of the Time Machine error on macOS" >}}

I'll have to investigate this issue further, but I'm not too stressed either. All of my documents live in the cloud and my code projects are pushed on remote git repositories. The only thing I'll lose if my computer gets stolen is a bunch of stickers I really like and a few hours to set a new one up.

### Raspberry Pi
I also recently started to use my Raspberry Pi more, so I wanted to keep a backup to prevent loss due to SD card failure.

For this one I had to get somewhat creative. I first listed the files and folders I needed to back up. For me it was nearly everything in the Home Assistant configuration directory (except for the database, 1.5 GB no thank you) and some other files scattered around the disk for various other scripts and configuration files.

I then created two very similar scripts which would be executed periodically. The first is all about Home Assistant and the second takes care of the rest.

Since this article is already long enough, I'll stop writing here and detail the scripts in [a later post](https://blog.augendre.info/raspberry-pi). Stay tuned! 😉

Keywords/tags:
#tech #home #synology #nas #plex #backup #raspberrypi #100DaysToOffload #HundredDaysToOffload
