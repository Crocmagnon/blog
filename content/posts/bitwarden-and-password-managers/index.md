---
title: "Bitwarden and Password Managers"
tags: ['free software', 'passwords', 'passwords manager']
date: 2020-06-05T15:10:47+00:00
aliases: ["/bitwarden-and-password-managers"]
canonicalURL: "/bitwarden-and-password-managers"
---
[TL;DR](https://en.wiktionary.org/wiki/tl;dr): I use a password manager and you should too. [Bitwarden](http://bitwarden.com/) is a Free Software alternative.

{{< img src="3.svg" alt="Bitwarden Logo" >}}

This is my 10th post of #100DaysToOffload.<!--more-->

## Password managers
We all have a *lot* of online accounts now, between banks, emails, marketplaces, public institutions, games, transport, storage, food delivery, … The list goes on.

And the vast majority of these accounts should all have different passwords. And by different I mean very different.
For example, these two passwords are not different enough:

| Service | Password             |
|---------|----------------------|
| Dropbox | `!B2F#czqpnKB:dropbox` |
| GitHub  | `!B2F#czqpnKB:github`  |

They are based on the same root and just use the service name as a suffix. That's what I used to do before using a password manager because it was easy to remember: once you memorised the root, you just had to know where you wanted to log in.

I had a complex root composed of random letters, digits and special characters. But if any of the services were compromised, my root was compromised too and the attacker could gain access to my other accounts with very little effort.

A password manager abstracts everything for you and makes it **very easy** to generate unique, long and complex passwords **without the need to remember them all**. You just have to remember the password to your password manager and let it handle the rest for you.

Most password managers also allow you to store other items such as notes, credit cards or identities to help you fill forms.

## Bitwarden
Bitwarden is my password manager of choice because it's a **free and open source software**. The clients are under the GPL and the server code is under AGPL, both guarantee you an access to the source code and the freedom to modify it yourself for your own use or redistribute your modified version.

It offers a **free plan** that is very convenient and in no way limited like others (looking at you Dashlane, making us pay $40/year to sync passwords). With the free version of Bitwarden, you can store as many passwords as you want, you can sync them between as many devices as you want (smartphone, laptop, desktop, tablet, …). It also generates random passwords for you so you don't have to roll your face over your keyboard when creating an account.

Finally, you can host it yourself, meaning that if you don't trust the online Bitwarden service to store your passwords, you can run it on your own server or at home. I see this more useful for **enterprises** that will want to store their passwords on-premise but technical individuals can also take advantage of this and not be dependent on a third-party service for their password management.

Oh, I mentioned a free plan but to support Bitwarden you can subscribe to a Premium offer. It costs **less than a dollar per month** ($10/year) and it offers:

* reports on the content of your vault (e.g.: exposed or weak passwords)
* 1GB of encrypted file storage
* TOTP code generation

You also get the nice feeling of supporting a free software project 🎉

## Get involved
Since Bitwarden is an open source project, it's quite easy to get involved. You can contribute code on [GitHub](https://github.com/bitwarden) or translations on [Crowdin](https://crowdin.com/profile/kspearrin). From my experience, contributing code was very pleasant. Kyle (the main developer) was helpful in its feedback and I could improve credit card filling on some of the sites I use regularly.

I'm also involved as a proofreader of the French translation on [Crowdin](https://crowdin.com/profile/kspearrin), meaning that I have the final say on what will be included in the French translation of the apps. It's a responsibility I take seriously and we welcome all participation from fellow translators 😊
