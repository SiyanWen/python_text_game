Siyan Wen swen4@stevens.edu
# estimate of time I costed
two days
# bugs and issues
1. Because I cannot split command by one or more spacees, I failed to get the verbs and objects of input command at first place.


# resolved issue
1. I found I can just use split() to convert input command into a list, split by one or more spaces.

# Test
I used subprocess package to compare if my stdout is consistent with my expectation.

# my extension

### 1. abbriviation for verbs, directions and items:

All verbs can be referred with the first letter except 'go' and 'get.

You can use ```g n``` as long as there is no items in that room so that you cannot use ```get``` and there is just one of 'north','northeast', 'north west'.

However. when there is both  ```go``` and ```get``` available, you must specify ```go``` or ```get```. 
If there are both 'north' and 'northwest' you should use ```g north``` if you want to go north, ```g nw``` if you want to go northwest. If there are 'west' and 'northwest', you can use ```g w```, ```g n``` because they starts with different words.
 
for items, you can use first letter if it is unique. if it's not, you need to write until the first different letter or the end of the shorter word.

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
What would you like to do? get be
You pick up the bellows.
What would you like to do? help
You can run the following commands:
go ...
drop ...
get ...
look
inventory
quit
help
What would you like to do? drop be
You drop the bellows.
What would you like to do? help
You can run the following commands:
go ...
get ...
look
inventory
quit
help
```
If there is ```drop``` and ```get``` is depends on if you have items in inventory and if there is any item in the room.

### 3. A ```drop``` verb

As shown before you can use ```drop``` verb to drop items.

# GitHub repo
https://github.com/resemble-Dunford/python_text_game.git