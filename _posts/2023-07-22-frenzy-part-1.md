---
tags: godot game-dev
project: frenzy
title: Frenzy, Part 1
---

Throughout university, I dabbled with game development. I started
out using a Java-like language called *Processing*, because it
had good tutorials and a very easy to learn API.

Using *Processing*, I made a handful of apps that showcased what
I had learned about game development. 

I made an "ecosystem" of frogs, mosquitoes and fruit trees that 
gradually evolved the frogs and mosquitoes to consume more of 
their prey before dying. This app was very object-oriented,
and was one of my first big projects after learning about objects
in Java 100.

I also created another evolutionary sort of system, this time
with procedurally generated terrain and vehicles in 2D. The app
generated cars from random polygons with wheels attached to
vertices. You could mutate a car at any time to create a slightly
modified version, to see if it fared any better on a random track.
I used Box2D for the physics.

I would go on to create other projects in *Processing*, including
procedurally generated dungeons, but I wanted to learn a proper
game engine. At the time, my poor refurbished Thinkpad was not
really capable of running Unity, so making a 3D game was out of
the question. In 2019, Godot was starting to become a proper
game engine, and I heard it handled 2D well and had a *Python*-like
syntax. I downloaded it and gave it a try. I created a few random
apps, and some more complex things like a roguelike platformer.

![uss screenshot](../../../assets/images/projects/uss/k2.png)

After graduating, I wondered what I wanted to do in my spare time.
I had always wanted to do more with game dev, and since having completed
my degree, I had a lot of ideas thanks to my game dev courses and
computer graphics especially. I finished reading Frank Herbert's *Dune*
and started thinking that it would be cool to play a game as a sandworm,
where you awaken after some long period underground to the modern world,
to a complete hostile environement, and use your cool sandworm abilities
to wreak havoc and try to find some semblance of the past.

![frenzy concept art](../../../assets/images/projects/frenzy/worm_burst.jpeg)

That's roughly how the idea for *Frenzy* came about. It was inspired by
games like *Hotline Miami* and *Nuclear Throne*. The first work on 
*Frenzy* was to get a sandworm moving around. This took a long time to
get it to both feel right and work with the physics engine. I started
with an open implementation for the node movement and adapted the physics
to my needs. The worm is pretty much a chain of `KinematicNode2D` that
follow the head. The worm's name is actually Gaia - like the Mother of
Titans.

After Gaia's movement was implemented, I created some enemies to fight.
I had never written AI before, and it ended up needing a few behaviours.
The AI pathfinds using a vector of rays to detect walls, along with
a mesh of nodes along the level that it uses the A* algorithm to navigate.
The enemies also have a state machine that modifies their movement 
behaviours. They can seek, run away, chase, patrol, and other such
behaviours.

![sandworm biting an enemy](../../../assets/images/projects/frenzy/chomp.gif)

One of my favourite parts of the development was creating the art and
assets. I had recently taken computer graphics, so I knew I wanted to
use 3D models if I could, since I wanted to play with Blender, and use
normal maps to perform lighting. Each sprite in the game is a top-rendered
3D model. All the animations are hand animated in Blender. The sprite
sheets is rendered twice, once with the normal texture and a second time
with a normal map. In game, the characters use an `AnimationPlayer` and
and `Sprite` to control their animation.

![worm rotating in ice](../../../assets/images/projects/frenzy/ice.gif)

For now, that's all I'll say about the project. I'll get more into it in 
future blog posts that link from this page.