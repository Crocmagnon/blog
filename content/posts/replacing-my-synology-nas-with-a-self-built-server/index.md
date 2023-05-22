---
title: "Replacing my Synology NAS with a self-built server"
tags: ['FreeBSD', 'FreeNAS', 'NAS', 'TrueNAS', 'self-hosting', 'server']
date: 2020-11-11T12:31:38.826817+00:00
aliases: ["/replacing-my-synology-nas-with-a-self-built-server"]
canonicalURL: "/replacing-my-synology-nas-with-a-self-built-server"
---
{{< note class="info" title="👴 Old post" >}}
I don't use TrueNAS anymore but I still have this machine and I even upgraded the RAM to a more comfortable 56GB.
{{< /note >}}

A few weeks ago, I replaced my trusty [Synology DS216play]({{< ref "synology-nas-stream-and-backup/" >}}) with a more powerful station that I built myself. I hadn't built a computer in a long time and it was a lot of fun!

{{< img src="26.svg" alt="TrueNAS Logo" >}}<!--more-->

## Build time!
I chose to go team red this time because I never used an AMD processor. I picked a Ryzen 5 3400G which should be more than enough for the next few years. A quick detour on the specs:

* 4 cores / 8 threads AMD CPU
* 8GB DDR4 RAM
* 550W power supply
* a motherboard, case and a fan

Bringing us to a total of 440€. I decided to add another 8GB RAM afterwards, the final price was around 475€.

I'm not 100% happy with the case. First it's way bigger than the Synology enclosure was but it still fits in the furniture under my TV, though I had to remove the front panel. Then, it can only contain two 3.5" HDD. I only have two at this time but it may prevent me to easily expand my storage afterwards. I'll see later, for the moment it's enough.

## Backup
Before unplugging the Synology NAS, I picked an external USB HDD and backed up what I wanted to transfer. I didn't have much data on my 2x2To drives so it didn't take long.

## OS Installation & configuration

Following the recommendations of a colleague, I decided to go with [FreeNAS](https://www.truenas.com/) (which was recently renamed TrueNAS, I will use both in this article). The installation is straightforward with very few options. I used a spare USB key for the OS boot drive since TrueNAS prevented me from using the storage disks for that.

After the installation is complete, I could reboot, unplug the keyboard and the monitor, and use another computer to access the web interface through which FreeNAS is configured and managed. A few settings later, I had a working home server! I just had to dump the external drive to the newly created [ZFS](https://en.wikipedia.org/wiki/ZFS) pool which would hold my data, setup some shares and get going!

Overall the complete setup including building the PC and backing up data took me something like 3-4 hours. The data restoration was done overnight.

The day to day management is also quite easy and after setting up some automated tasks like ZFS snapshots, you pretty much don't have anything to do.

I experienced some issues with my UPS though. TrueNAS allows you to monitor the state of a USB UPS and gracefully shutdown the system when it's on battery or when it reaches low battery. This is very useful to prevent data loss. It also sends you an email when something bad happens (UPS in bad state, UPS doesn't respond, etc). The state is polled every 2 seconds by default. My UPS decided it was a bit too much and the monitoring service *in the UPS* failed in the night after running a couple of hours. I woke up with an inbox full of alert emails (*one per minute* of supposed outage). The fix was relatively easy: set the polling interval to a higher value like 15 seconds, so the UPS doesn't feel DOSed. I'm not running a datacenter and my server doesn't draw too much power compared to the UPS capacity so I'm not concerned about the UPS failing within 15 seconds in case of a power outage.

## Experimentations
{{< img src="28.png" alt="FreeBSD Logo" >}}

This server will allow me to experiment more freely. I used to rent a VPS for always on services but now I can just pop them onto this machine. One detail though: FreeNAS is based on [FreeBSD](https://en.wikipedia.org/wiki/FreeBSD). FreeBSD is *not* a GNU/Linux distribution though there are some similarities. It's a system I've never administrated before and it can be a bit confusing when popping into the command line. On the other hand, if you have a pretty standard setup, you never see FreeBSD as everything can be managed through the GUI.

You can also create a virtual machine from the GUI and install a custom OS inside to run services that FreeBSD can't run. That's exactly what I needed since I had a few services that required Docker and Docker is not available on FreeBSD. I set up a VM with Ubuntu server, which I only use for my Docker services.

Fortunately, VMs are not the only way to isolate your services. FreeBSD has an integrated containerization mechanism called *jails*. It pretty much looks like a Docker container except that you can't pick a GNU/Linux distribution. It shares the kernel of the host system leading to much small overhead compared to a full-blown VM. TrueNAS comes with a plugin mechanism that creates a jail to run a custom service, like NextCloud, Deluge, Plex, etc. You can also create jails manually.

My current setup includes:

* Some jails:
    * nginx (handles the incoming HTTP(S) traffic and dispatches to the appropriate service)
    * NextCloud
    * miniflux (moved from my Raspberry Pi)
    * postgresql
    * [cleantoots]({{< ref "cleantoots-clean-your-toot-history/" >}})
    * Deluge
    * Plex
* A VM with some Docker services:
    * This blog (migrated from the VPS)
    * Collabora Online server (provides online collaboration on LibreOffice/Microsoft Office documents in NextCloud)
    * [Plausible Analytics]({{< ref "/about#analytics" >}})

The Raspberry Pi still runs Home Assistant but I disabled InfluxDB and Grafana since I didn't use them. The VPS is shut down and I plan on deleting it by the end of the month since I don't need it anymore.

## Closing thoughts
I'm really happy with this setup! I don't know yet what I'm going to do with my new NextCloud though. I tried NextCloud talk but I couldn't get it working properly for video calls. I might replace pCloud (I have a lifetime 2To plan) and use it as a backup service, who knows! If you have suggestions, please feel free to [contact me]({{< ref "/about" >}}). 😀
