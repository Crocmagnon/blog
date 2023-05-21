---
title: "Pi Hole"
tags: ['DNS', 'Raspberry Pi', 'self-hosting']
date: 2020-05-28T15:54:13+00:00
aliases: ["/pi-hole"]
---
!!! info "👴 Old post"
    I don't use Pi Hole anymore but this post should still be relevant. I've switched to [AdGuard](https://adguard.com/en/welcome.html). There is an easy to install Home Assistant addon available and it allows me to easily configure local-only DNS entries.


![Pi Hole logo](11.svg)


As I was telling you [before](https://gabnotes.org/raspberry-pi), I own a Raspberry Pi on which I set up a [Pi Hole](https://pi-hole.net/).

As they advertise it, Pi Hole is "a black hole for internet advertisement". It's basically an ad blocker for your whole network.<!--more-->

Again, I won't go into details of how to setup your own Pi Hole, there are plenty of good resources for that, starting with Pi Hole's own website. Just remember to setup your DHCP server to advertise your Pi Hole IP as the preferred DNS resolver, so that every device connected to your network can automatically benefit from it.

I won't also explain how Pi Hole blocks your ads but if you'd like me to, please [let me know](/about-me).

Today's quick post is about how great Pi Hole is, in a few bullet points:

* It's easy to set up.
* It's very low maintenance. I basically check for an update every now an then but otherwise I pretty much let it live its own life.
* You can set it up in a privacy preserving way by choosing what statistics/logs you want to collect:
![Privacy options in Pi Hole. There are five options ranging from "log every request with the client and the requested domain" to "no logs, no stats".](10.png)
* Did I mention it blocks ads? That works everywhere and especially well coupled with other solutions such as [uBlock Origin](https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/), [Privacy Badger](https://addons.mozilla.org/en-US/firefox/addon/privacy-badger17/) or [Ghostery](https://addons.mozilla.org/en-US/firefox/addon/ghostery/) in your browser but it also in some of your smartphone apps 😁
* Since it caches the DNS responses, it also improves a tiny bit your browsing speed and prevents your FAI or another DNS server to spy on you too much. And it reduces your footprint by sending less data on the internet. That's not why I primarily use it but it's a little bonus.

That's about it for today! I encourage you to setup a Pi Hole on one of your computers and try it, it's quite nice! They rely on donations to help them sustain the development so if you enjoy it, [consider donating](https://docs.pi-hole.net/#pi-hole-is-free-but-powered-by-your-support).

I wrote this as part of 100DaysToOffload, this is the 9th post.

Keywords/tags:
#pihole #raspberrypi #tech #home #100DaysToOffload
