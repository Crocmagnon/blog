---
title: "Cleantoots - Clean Your Toot History"
tags: ['cleanup', 'history', 'mastodon', 'toots']
date: 2020-05-25T17:08:28+00:00
---
Since I consider my messages on social media to be valid at the moment they're posted, I like to have them deleted after some time. When I still used Twitter, I also used a CLI tool called [cleantweets](https://github.com/magnusnissel/cleantweets) that helped with this.

A few months ago, after having created an account on [Fosstodon](https://fosstodon.org), I wrote a simple command line utility to help you achieve the same thing but with toots: [cleantoots](https://git.augendre.info/gaugendre/cleantoots) (notice how much effort I put into naming it).<!--more-->

As with most of my side-projects, the code source is released under a free software and open source license, here I used the GPL-3.0.

Since it's written in Python, I also released a [Python package](https://pypi.org/project/cleantoots/) to help with the installation process, so a simple `python -m pip install cleantoots` should do the trick. The rest of the configuration and setup process can be found in the project's [README](https://git.augendre.info/gaugendre/cleantoots/src/branch/master/README.md).

You can easily configure the tool to:

* Delete old toots
* Keep popular toots (with a minimum number of favorites/boosts)
* Keep toots given their ID
* Keep toots containing a hashtag (recent addition)

And as Mastodon is a federated social network and you may have multiple accounts on multiple instances, the configuration file allows that too.

I think the project is usable but it may be improved at least in two ways:

* Increase the test coverage
* Refactor the code to make it clearer and add some comments to help contributors

Please don't hesitate to open an [issue on the repository](https://git.augendre.info/gaugendre/cleantoots/issues) if you have any question, need help using it, find a bug or request a feature! 😀

I wrote this as part of [100DaysToOffload](https://100daystooffload.com/), this is the 8th post.

Keywords/tags:
#100DaysToOffload #cleantoots #
