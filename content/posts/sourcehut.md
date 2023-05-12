---
title: "Sourcehut"
tags: ['GitHub alternative', 'git', 'software forge']
date: 2020-07-01T20:26:41+00:00
---
!!! Info "🧓🏻 Old post"
    This post is quite old now. Since then, I've moved my git repositories to a self-hosted [gitea](https://gitea.io/) instance and I cancelled my subscription. I still stand behind this post though. Sourcehut is a solid git forge and keeps improving.

For a few weeks now I've been hosting my new projects at [sourcehut](https://sr.ht/~crocmagnon) instead of my usual GitHub account. So far, the experience has been very pleasant but it also has some drawbacks. Let's talk about it!

#100DaysToOffload No. 15<!--more-->

[sourcehut](https://sourcehut.org/)  is a software forge grouping several tools in a **free and open source** suite:

* git/mercurial repository hosting
* mailing lists
* ticket system
* wiki
* builds / CI

It's blazing fast (see [this comparison](https://forgeperf.org/) ; disclaimer : it's maintained by sourcehut) and very [accessible](https://en.wikipedia.org/wiki/Web_accessibility). Every page is also usable with a browser on which you disabled Javascript, which I think is a very nice feature since it allows for any kind of web browser to use your website. Not just the ones supporting the latest [ECMAScript](https://en.wikipedia.org/wiki/ECMAScript) bells and whistles.

## Collaboration
### Email
Collaboration is mainly achieved through email. After being caught in GitHub and Gitlab for years, I recently discovered that `git` has some integrated tools to collaborate, send patches, etc. You can try generating your first patch with `git send-email` with [this tutorial](https://git-send-email.io) (brought to you by the sourcehut team). I even managed to create and send a patch to sourcehut's ticketing system so that you receive your attributed issue number when you submit by email. It's been merged and published [last month](https://lists.sr.ht/~sircmpwn/sr.ht-announce/%3CC3HPI7MYB0VU.A8FD2OLYNAG6%40homura%3E)! 🎉

I still haven't made my mind up about this. I think it might discourage external contributions because I believe that more people know the "GitHub flow" (fork to your account, push your changes and make a pull request) when fewer learned the "pure" git flow. However, as Drew pointed out[^drew], one had to also learn the GitHub flow.

[^drew]: In a toot on his Mastodon server, which is now offline, sorry about that.

On the other hand, it's like going back to the basics, which I appreciate. Also, many of my projects didn't have external contributors even on GitHub, so it's not like it would change the world for my use case.

The basic contribution workflow at sourcehut looks like this:

1. Clone the project locally
2. Make changes
3. Use git send-email to send them to the right mailing list

Finding the mailing list, configuring your git client to send emails, ... All of these may be obstacles to contributors. Though I see one (big) advantage: **if you have git and an email account, you have everything you need to contribute to projects on sourcehut**.

You don't need to create an account, fork the repository or own any resource. You just need an email address to send your patches to sourcehut mailing lists and receive feedback.

Another advantage is that "issues" are not the only way to communicate around a project. If you want to start a discussion, just send an email to the project's appropriate mailing list!

### Code review
I also tried reviewing some code since it's a big part of collaboration around software projects.

At first I found it a bit hard since there's no guidance in the web UI. But once you understand that you can do that via email, then everything falls into place.

You just need to reply to the email you received when the contributor sent the patch. You can even add inline comments and they'll be shown inline in the web UI. See an example of such discussion [here](https://lists.sr.ht/~sircmpwn/email-test-drive/patches/10576). 

I found that to be very clever, though there is still room for improvement. Especially on the docs or UI to guide people.

## Documentation
The documentation is still quite Spartan and even sometimes incomplete, but that's to be expected since sourcehut is [still an alpha product](https://sourcehut.org/alpha-details/).

The team is making good progress though! They send a monthly email indicating the changes they pushed during the last month. It's always filled with good new stuff, improvements, performances upgrades, etc.

## Business model
Their business model is based on paid users. They [don't have any investors](https://man.sr.ht/billing-faq.md#why-do-i-have-to-pay-for-srht-when-github-gitlab-etc-are-free), so they're entirely driven by what their users would want. Not by how to make money fast under big companies' pressure. After the alpha, users owning resources (repositories, mailing lists, bug trackers, etc) will have to subscribe to a paid plan.

So if you just want an account to use the web UI to publish issues for example, you won't have to pay. But as I said, you don't even need an account for that: you can use email! You would need an account to get write access to any repository or read access to private repos though.

During the alpha you don't need to pay but I figured it would be a nice way to contribute to the free and open source software environment so I decided to subscribe. 

## CI / Builds
I also wanted to talk a bit about their CI system. It's as simple as writing a YAML file (called a manifest) and submitting it either through the API or using a web form.

That allows you to decouple your build jobs from your repository if you want to. Or test some changes before committing them. Too many times I've seen (and made!) commits like "try to fix CI", "fix CI 2", "this should finally fix CI" because the only way to submit jobs on GitLab CI or GitHub Actions is by committing and pushing to your repo.

The final bonus that kills every other CI system is that sourcehut automatically enables an SSH access if your job fails. You can then connect to the machine that ran your scripts and investigate what happened.

Edit (2020-07-06): sourcehut lacks Windows and macOS for their builds system, making it less suitable than some others if you need to target these platforms.

## Closing words
All of this makes sourcehut a far superior software forge than GitHub or GitLab in my opinion. I especially like their full commitment to free and open source software, unlike GitLab which only has a free core and GitHub which is entirely proprietary.

I might not migrate my existing projects (yet) but I will at least continue creating new ones on sourcehut rather than GitHub. And maybe someday I'll find the courage to migrate everything.

Thanks sourcehut, for contributing to this ecosystem with such great tools.

## Related reading

* [Why not GitHub?](https://sanctum.geek.nz/why-not-github.html)
* [Github is sinking](https://yarmo.eu/post/github-sinking)
