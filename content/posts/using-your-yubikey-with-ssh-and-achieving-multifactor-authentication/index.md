---
title: "Using Your YubiKey With SSH and Achieving Multifactor Authentication"
tags: ['ssh', 'yubikey']
date: 2020-05-18T19:07:08+00:00
aliases: ["/using-your-yubikey-with-ssh-and-achieving-multifactor-authentication"]
---
In my [introductory article](/im-starting-a-blog), I teased about using SSH with a YubiKey. Here's the post that expands on the idea.

![YubiKeys](21.jpeg)
As you can see, I *like* YubiKeys.

This is part of my #100DaysToOffload series, issue No. 6.<!--more-->

I won't go into much detail as to how to set them up, other people did. [Here's the guide I followed](https://florin.myip.org/blog/easy-multifactor-authentication-ssh-using-yubikey-neo-tokens)[^guide]. Instead, I just wanted to talk about how cool it is!

[^guide]: Sadly the website seems to have been taken down 😕

First, even if you need to access your server from multiple machines, you only have one public key to authorize. No more "oh no I didn't allow this key, I have to log in with the password instead" (you should have disabled it so it's more "oh no I have to get my other computer to allow this one"). Saving time already 😊

Second, it's portable. More than a laptop. You can even plug it in on a colleague's computer and use it from there without having to compromise your private key or create another pair.

You can also generate/store your private encryption and signature keys for PGP on a YubiKey ([*Why have separate encryption subkey?*](https://security.stackexchange.com/questions/43590/pgp-why-have-separate-encryption-subkey), [*Improve the Security of Your OpenPGP Key by Using Subkeys*](http://www.connexer.com/articles/openpgp-subkeys)). That also requires you to plug in the key to decrypt/sign messages hence increasing the security of your setup.

These are features I use every day: my key is plugged pretty much all day on my computer at work since I'm using PGP to sign my commits and SSH to push them on our shared git repo. That's also what I use to log into my [Raspberry Pi](/raspberry-pi) or this blog's host.

One thing to keep in mind though is that if you lose your key and it's your only access to a remote machine, you may be screwed. Remember to always keep a backup access with an offline key[^1] or a good old keyboard & screen if you have physical access to your server!

I hope this post helps you see the coolness of these little keys! You can of course use them for 2FA on websites but hey, why not also have 2FA for SSH 😉

[^1]: "offline key" here means a key pair stored on a device disconnected from internet and that you rarely use if ever. Maybe it's a USB drive in a Swiss safe, maybe it's in your nightstand, whatever. Just keep it offline as much as possible to not defeat the purpose of additional security brought by the YubiKey. For PGP, the certification key should be kept offline as it holds the power to certify other keys to allow them to sign/decrypt.
