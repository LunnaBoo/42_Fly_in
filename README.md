_This project has been created as part
of the 42 curriculum by luccribe._

# Description
The **Fly-in** project's goal is to develop a program capable of reading data from a .txt file, build a graph based on it
and traverse with multiple 'drones' from a start to a goal node in a limited number of turns. Each drone may move once per
turn. \
It is designed to test a student's knowledge on graphs, algorithms and graphical interfaces. This is my second project that has
some form of graphical interface. Last time, I used basic terminal printing logic using ANSI Codes to serve as the visuals. \
But this time, even though I really like terminal based apps, I chose an external python library to aid me in this task.

# Instructions
In order to test the project in your machine you'll have to follow these steps:
1. Open your terminal and clone this repository.
2. Move to the project's directory (using 'cd' command)

Now, before you can actually test it you'll need a map.txt
file. This is the file the program will read in order to build the graph.
Here's a template:

    nb_drones: 5
  
    start_hub: hub 0 0 [color=green] 
    end_hub: goal 10 10 [color=yellow] 
    hub: roof1 3 4 [zone=restricted color=red] 
    hub: roof2 6 2 [zone=normal color=blue] 
    hub: corridorA 4 3 [zone=priority color=green max_drones=2] 
    hub: tunnelB 7 4 [zone=normal color=red] 
    hub: obstacleX 5 5 [zone=blocked color=gray] 
    connection: hub-roof1 
    connection: hub-corridorA 
    connection: roof1-roof2 
    connection: roof2-goal 
    connection: corridorA-tunnelB [max_link_capacity=2] 
    connection: tunnelB-goal

You have two options:
1. Create a file called 'map.txt' and copy the template's text in it.
2. Create a file called 'map.txt' and write your own map. Don't worry, the program will let you know in case the map file isn't valid.

Now, with the map file inside the project's directory, all you need is to type 'make run'. The program will open automatically right
after it finishes downloading all project dependencies.

# Path-finding Algorithm
A powerful algorithm was needed in order to achieve the performance necessary to beat all maps given by the project's subject.
In my last project, A-Maze-ing, I used Breadth-First-Search but quickly realized it wouldn't be enough for Fly-in. \
My second option
was Djikstra, which I think it was a really appropriate choice considering the graphs created by the subject's maps are undirected
and have weight. \
I also considered A*, but later realized it would be overkill for a project like Fly-in. Djikstra was just perfect for the type of
graphs I'd be dealing with and it achieved the performance needed to beat every map. \
I did tweak it a little, but barely. All I did was add a second method implementing Djikstra but taking into consideration hubs that
were full, meaning no drones could enter, so drones could find alternative routes. \
Basically all I did was tweak it a little so drones could avoid being stuck in air traffic!

# Visual Representation (with Textual)
I know I implied earlier this wouldn't be a terminal based app... but it kind of is. I really like this style of apps so
I picked a python library called Textual used to build apps with sophisticated user interfaces that run in the terminal. \
Technically it also runs in the browser, but I haven't tested this funcionality myself yet! Besides the known limitations of
terminal based apps I managed to build a graphical interface that not only looks good but is also clear and easy to understand. \
In case the user is confused about different Hub colors in the Visual Output tab they can press 'h' to open another screen explaining
each of the colors used and what they mean. And although drone movement isn't the most explicit, 
since they just disappear and reappear, the user has the Textual Output tab with text explaining each movement that happened in 
each turn up to that point. \
There is also a screen that pops up once the simulation is finished encouraging the user to check the Textual Output tab for
statistics. All of these features were though by me in order to make the user experience as intuitive as possible. \
The last thing I want is the user to be lost or confused with no idea what to do to progress. That's why I made the app as
responsive as it is and added the Textual Output tab to aid the user. It is not enough to be a pretty app, it also has to 
work properly.

# Resources
GeeksForGeeks guide about Djikstra algorithm: \
https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/ 

Color palette used: \
https://lospec.com/palette-list/inkpink 

Textual lib tutorial: \
https://textual.textualize.io/tutorial/ \
I read and re-read not only this tutorial but all of Textual's documentation. I had a really hard time getting around this library.

How I found Textual: \
https://realpython.com/python-textual/ 

Website used to generate the ASCII art used: \
https://patorjk.com/software/taag/#p=display&f=DiamFont&t=IMPOSSIBLE&x=none&v=4&h=4&w=80&we=false 

Another guide on Djikstra: \
https://towardsdev.com/dijkstras-algorithm-explained-the-heart-of-pathfinding-and-optimization-24d927b8adb5 

AI was used only to solve problems regarding the Textual lib, which was my biggest headache during development. Yet, no code was
taken from AI. All code present in this project was developed by me.
