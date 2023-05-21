---
title: "CodinGame Spring Challenge 2020 - Pacman"
tags: ['challenge', 'codingame', 'programming']
date: 2020-05-21T19:13:49+00:00
aliases: ["/codingame-spring-challenge-2020-pacman"]
---
I participated in the [latest CodinGame challenge](https://www.codingame.com/multiplayer/bot-programming/spring-challenge-2020) and quickly got out of the beginner's league. In this article, I'll explain my approach.

#100DaysToOffload No. 7

{{< img src="2.jpg" alt="Cover picture for CodinGame Spring Challenge 2020. There is one yellow Pacman and one blue Pacman fighting against each other" >}}<!--more-->

CodinGame is a coding platform on which you can solve puzzles by writing a program in the language of your choice. They also often host contests in which your code fights against that of other developers. The most matches you win, the most points you get. And the most points you get, the higher you climb on the leaderboard. I like to participate in these challenges, so I signed up for the latest one: CodinGame Spring Challenge 2020.

In all CodinGame challenges, there is a league system. You start in the Wood 1 league with an easier version of the game and a subset of the rules, just to get you started. When your code is good enough, you get to Wood 2 where you have more rules and more mechanisms. After passing Wood 2, you end up in the Bronze league with the full version of the game and all the rules.

I didn't go further than Bronze league because I didn't want to spend much more time working on my bot but you can do that if you want 😊

## The rules
In this contest, each participant has a team of Pacmans and has to eat more pellets than the opponent. There are standard pellets worth 1 point and super pellets worth 10 points. At each turn, you're given the position of everything you can see (pellets, allies and enemies) and you have to give an instruction (telling your Pacs what to do). The game stops when there are no enough pellets in game to change the outcome of the game (one of the opponents ate more than half of the points available in the board) or after 200 turns.

League Wood 1:

* You control only one Pac
* You can see the whole map (everything's given to you at each turn)
* When colliding, the movement is canceled

League Wood 2 :

* You control many Pacs (2-5)

League Bronze :

* Speed boost
* Each Pac has a type and you can change it in a game turn. When colliding, the Pacs fight. Each one can be one of rock, paper or scissors and the winner is chosen according to [the game](https://en.wikipedia.org/wiki/Rock_paper_scissors).
* You can only see what's in your Pacs line of sight. Everything else is in the fog. You can see super pellets from anywhere, though.

## Start small, submit early

As you can see from the rules, there is a big gap between the woods and bronze league. The fog is the main thing preventing you from optimizing your path since you don't know what's happening outside your lines of sight.

When talking with other participants, I noticed that some people were over engineering their program right from the wood 1 league. They were talking about path-finding algorithms, path optimization and so on. This could've worked if later the ability to view the whole map weren't taken away.

My advice for this kind of challenge is to start with a **simple algorithm** that does uncomplicated things in a few lines of code. Just enough to get out of wood leagues. For example, the simplest algorithm I can think of for the first level would be : "go eat the nearest super pellet, if there aren't, go eat the nearest standard pellet". **Submit early** and **iterate** on your code. Some things won't work but it's better to see that while running your algorithm than spend two days working on it and discover later that you can't see the whole map anymore.

That's how I got out of wood 1. No optimization, no over engineering, just "go eat". Of course, this was not optimal. Since I never changed my trajectory until it disappeared (because I ate it or because the opponent did), sometimes I ended up in an infinite collision because my opponent and I were too stubborn. But that allowed me to win most of my matches and beat the boss (which is how you leave wood leagues).

## Grow later

The wood leagues are here to make you comfortable with the contest rules.

When entering the Bronze league, you unlock all the rules of the game. In our case, this means that we only see in direct line of sight (we don't see behind walls or in diagonal), and that we have abilities we can use other than just moving towards a target: speed boost and change type.

These two abilities can really change the course of a match so you'd better take them into account.

Of course, not seeing the whole map means you have to keep a state between each turn to remember the position of the pellets you've already seen. That way, you can go back to them later if you don't see anything anymore.

My code for this challenge is available on [Gitea](https://git.augendre.info/gaugendre/codingame/src/branch/master/challenges/2020-spring.py). It's written in Python, feel free to check it and drop me an [email]({{< ref "/about" >}}) or a message on [Mastodon]({{< ref "/about" >}}) if you have any question! It's not written in a very maintainable way since its expected life span was that of the contest, so 11 days. I could've spent more time refactoring stuff but *in this context* this would have likely been wasted time.

Basically, here's what I do:

* Go eat the super pellets
* Use boost nearly whenever possible
* Change to the winning type if an enemy is nearby and chase it
* Go eat the nearest pellet (actually second nearest because I want to make the most use of the boost)
* When nothing in sight, go to a remembered pellet position or go discover new areas

The core method is `get_action` ([line 221](https://git.augendre.info/gaugendre/codingame/src/branch/master/challenges/2020-spring.py#L221)). It returns the action a given Pac should take for this turn. This method is run for every Pac at every turn.

My final position was 1758th/4103 total, or 121st/2466 in the Bronze league.
There were 118 in Legend, 535 in Gold, 984 in Silver, 2466 in Bronze and 904 in the woods league at the time of writing this article (a few days after the end of the contest).

A strategy that I could have applied is to try and predict your opponent's movement. That's something you can do in a game where you see the whole map: run your own algorithm on the opponent's units and try to predict what you would do in their position. Then, use this knowledge to your advantage. This is a strategy you could easily apply in a game in which you see the whole map, I don't think that would've worked well in this case.

#programming #dev #coding #codingame #100DaysToOffload
