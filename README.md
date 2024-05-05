Siyan Wen swen4@stevens.edu
# estimate of time I costed
two days
# bugs and issues
1. Because I cannot split command by one or more spaces, I failed to get the verbs and objects of input command at first place.


# resolved issue
1. I found I can just use split() to convert input command into a list, split by one or more spaces.

# Test
I used subprocess package to compare if my stdout is consistent with my expectation.

# my extensions

### 1. abbreviation for verbs, directions and items:

All verbs can be referred with the first letter except 'go' and 'get'.

You can use ```g n``` as long as there is no items in that room and there is just one of 'north','northeast', 'northwest'. Because if there is anything in the room you can use both ```go``` and ```get```, then there would be a confusion. Same with the confusion between directions, items with same beginning letters.

For this reason when there is both  ```go``` and ```get``` available, you must specify ```go``` or ```get```. 
If there are both 'north' and 'northwest' you should use ```g north``` if you want to go north, ```g nw``` if you want to go northwest. If there are 'west' and 'northwest', you can use ```g w```, ```g n``` because they start with different words.
 
for items, you can use first letter if it is unique. if it's not, you need to write until the first different letter or the end of the shorter word.
For ```go``` verb only you can use any disconnected letters to refer to the direction, as long as they are in right order. That means  ```northwest```, ```upper-right``` can be abbreviated to ```nw``` and ```uri```.
```angular2html
> Center room

You are in the center of the World!!

Items: center card

Exits: up down left right upper-left upper-right bottom-left bottom-right

What would you like to do? go u
Did you want to go up, upper-left or upper-right?
What would you like to do? go up
You go up.
```
```angular2html
> Bottom room

This is the lower town, enjoy!

Items: bottom card

Exits: up left right upper-left upper-right

What would you like to do? go ur
Did you want to go upper-left or upper-right?
What would you like to do? go uri
You go upper-right.
```
### 2. a ```help``` verb

If you input ```help```, it would display all available commands like
```angular2html
What would you like to do? help
You can run the following commands:
  go ...
  get ...
  look
  inventory
  quit
  help
What would you like to do?
```
Whether there is ```drop``` or ```get``` is depending on if you have items in inventory and if there is any item in the room.

### 3. A ```drop``` verb
You can use ```drop``` verb to drop items.
For verb drop and its objects abbreviation is also applicable.
```angular2html
What would you like to do? i
Inventory:
  center card
  top card
  left card
  upper left card
  bottom left card
  bottom card
  bottom right card
  right card
  upper right card
What would you like to do? d c
You drop the center card.
What would you like to do? dt
Use 'quit' to exit.
What would you like to do? D t
You drop the top card.
What would you like to do? d bottom card
You drop the bottom card.
What would you like to do? d l
You drop the left card.
What would you like to do? d r
You drop the right card.
What would you like to do? d b
Did you want to drop the bottom left card or the bottom right card?
What would you like to do? d br
There's no br in inventory.
What would you like to do? d bottom r
You drop the bottom right card.
```

# GitHub repo
https://github.com/resemble-Dunford/python_text_game.git