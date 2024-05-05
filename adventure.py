import sys
import json
import re

with open(sys.argv[1], "r") as f:
    data = json.load(f)


def main():
    msg = "Map is invalid!\n"
    if "start" in data.keys() and "rooms" in data.keys():  # The map json should have "start" and "rooms" keys in the top-level object
        my_data = dict()

        my_data["rooms"] = dict()
        my_data["inventory"] = list()

        for item in data["rooms"]:
            # Each room should have a name, desc, and exits of appropriate type
            if "name" in item.keys() and "desc" in item.keys() and "exits" in item.keys():
                if isinstance(item["name"], str) and isinstance(item["desc"], str) and isinstance(item["exits"], dict):
                    for k, v in item["exits"].items():
                        if not isinstance(v, str):
                            err(msg + f"Direction {v} is not string!")
                    my_data["rooms"][item["name"]] = item

                else:
                    err(msg + f"name, desc or exits of {item} is not appropriate type!")
            else:
                err(msg + f"name, desc or exits of {item} is not exist!")
        valid_room = my_data["rooms"].keys()
        for item in data["rooms"]:
            for k, v in item["exits"].items():
                if not v in valid_room:
                    err(msg + f"directions in exits of {item} is not a valid room!")
        if not len(my_data["rooms"].keys()) == len(data["rooms"]):  # Check if the names of the rooms are unique
            err(msg)
        if data["start"] in my_data["rooms"].keys():  # If "start" room is in the map, set it as current rom
            room_curr = my_data["rooms"][data["start"]]
            run_game(my_data, room_curr)  # run the game
        else:
            err(msg + f"Start of the map {data['start']} is not a valid room!")
    else:
        err(msg + "'star' and 'rooms' keys are not in the top-level object!")


# If the map is invalid, set exit status to 1, stdout to empty, stderr not empty.
def err(msg):
    sys.stderr.write(msg)
    exit(1)


def run_game(my_data, room_curr):
    cmds = ["go", "look", "inventory", "quit", "help"]
    name = room_curr["name"]
    desc = room_curr["desc"]

    exit_str = " ".join([x for x in room_curr["exits"].keys()])  # get strings to display the message of the room

    if "items" in room_curr.keys() and len(room_curr["items"]) > 0:
        cmds.insert(1, "get")  # insert "get" in valid commands if there is any item in the room

        item_str = ", ".join(room_curr["items"])
        print(f'> {name}\n\n{desc}\n\nItems: {item_str}\n\nExits: {exit_str}\n')
    else:
        print(f'> {name}\n\n{desc}\n\nExits: {exit_str}\n')
    if len(my_data["inventory"]) > 0:
        cmds.insert(1, "drop")  # insert "drop" in valid commands if there is any item in the inventory
    loop(my_data, cmds, room_curr)


def loop(my_data, cmds, room_curr):
    try:
        cmd_in = input('What would you like to do? ')

        cmd_in = cmd_in.strip().lower()
        if cmd_in.lower() == 'quit':
            exit_game()
        my_cmd = cmd_in.split()
        obj = ""
        cmd_filtered = list(filter(lambda x: re.fullmatch(my_cmd[0], x), cmds))
        if len(cmd_filtered) == 0:
            pt_cmd = my_cmd[0] + '(.*)'
            cmd_filtered = list(filter(lambda x: re.match(pt_cmd, x), cmds))
            if len(cmd_filtered) == 0:
                if my_cmd[0] == "drop":
                    if (len(my_cmd) > 1):
                        print("You're not carrying anything.")
                        loop(my_data, cmds, room_curr)
                    else:
                        print("Sorry, you need to 'drop' something.")
                        loop(my_data, cmds, room_curr)
                elif my_cmd[0] == "get":
                    if (len(my_cmd) > 1):
                        obj = " ".join(my_cmd[1::])
                        print(f"There's no {obj} anywhere.")
                        loop(my_data, cmds, room_curr)
                    else:
                        print("Sorry, you need to 'get' something.")
                        loop(my_data, cmds, room_curr)

                else:
                    print("Use 'quit' to exit.")  # If the verb is invalid, maybe the user wants to quit.
                    loop(my_data, cmds, room_curr)  # Ask for command again
            elif len(cmd_filtered) > 1:
                out = "Did you want to " + cmd_filtered[0]  # If 2 or more commands are matched, ask for clarify
                if (len(cmd_filtered) > 2):
                    for i in range(1, len(cmd_filtered) - 1):
                        out += ", "
                        out += cmd_filtered[i]

                out += " or "
                out += cmd_filtered[-1]
                print(out)
                loop(my_data, cmds, room_curr)

        if (len(my_cmd) > 1):
            obj = " ".join(my_cmd[1::])  # words starts from the second are recognized as objects (items, directions)
        verb = cmd_filtered[0]

        if verb == 'go':
            if len(my_cmd) == 1:
                print("Sorry, you need to 'go' somewhere.")
                loop(my_data, cmds, room_curr)
            location_filtered = list(filter(lambda x: re.fullmatch(obj, x), room_curr["exits"].keys()))
            if len(location_filtered) == 0:
                pt_locs = "(.*)".join([x for x in obj])
                location_filtered = list(filter(lambda x: re.match(pt_locs, x), room_curr["exits"].keys()))
                if len(location_filtered) == 0:  # No directions in exits.keys() are matched, illegal direction
                    print(f"There's no way to go {obj}.")
                    loop(my_data, cmds, room_curr)

                elif len(location_filtered) > 1:
                    out = "Did you want to go "  # If 2 or more directions are matched, ask for clarify
                    out += location_filtered[0]

                    if (len(location_filtered) > 2):
                        for i in range(1, len(location_filtered) - 1):
                            out += ", "
                            out += location_filtered[i]

                    out += " or "
                    out += location_filtered[-1]
                    out += "?"
                    print(out)
                    loop(my_data, cmds, room_curr)

            my_dir = room_curr["exits"][location_filtered[0]]
            next_room = my_data["rooms"][my_dir]
            print(f"You go {location_filtered[0]}.\n")
            run_game(my_data, next_room)

        if verb == 'get':
            if not "items" in room_curr.keys() or len(room_curr["items"]) == 0:
                print(f"There's no {obj} anywhere.")
                loop(my_data, cmds, room_curr)
            if len(my_cmd) == 1:
                print("Sorry, you need to 'get' something.")
                loop(my_data, cmds, room_curr)

            items_filtered = list(filter(lambda x: re.fullmatch(obj, x), room_curr["items"]))
            if len(items_filtered) == 0:
                pt_items = obj + '(.*)'

                items_filtered = list(filter(lambda x: re.match(pt_items, x), room_curr["items"]))
                if len(items_filtered) == 0:
                    print(
                        f"There's no {obj} anywhere.")  # No items in room_curr["items"] are matched, illegal item name
                    loop(my_data, cmds, room_curr)
                elif len(items_filtered) > 1:
                    out = "Did you want to get the "  # If 2 or more items are matched, ask for clarify
                    out += items_filtered[0]

                    if (len(items_filtered) > 2):
                        for i in range(1, len(items_filtered) - 1):
                            out += ", "
                            out += items_filtered[i]

                    out += " or the "
                    out += items_filtered[-1]
                    out += "?"
                    print(out)
                    loop(my_data, cmds, room_curr)

            my_obj = items_filtered[0]
            my_data["inventory"].append(my_obj)
            room_curr["items"].remove(my_obj)
            print(f'You pick up the {my_obj}.')
            if len(room_curr["items"]) == 0:
                cmds.remove("get")
            if not "drop" in cmds:
                cmds.insert(1, "drop")
            loop(my_data, cmds, room_curr)

        if verb == 'drop':
            if len(my_data["inventory"]) == 0:
                print("You're not carrying anything.")
                loop(my_data, cmds, room_curr)
            if len(my_cmd) == 1:
                print("Sorry, you need to 'drop' something.")
                loop(my_data, cmds, room_curr)

            items_filtered = list(filter(lambda x: re.fullmatch(obj, x), my_data["inventory"]))
            if len(items_filtered) == 0:
                pt_items = obj + '(.*)'

                items_filtered = list(filter(lambda x: re.match(pt_items, x), my_data["inventory"]))
                if len(items_filtered) == 0:
                    print(
                        f"There's no {obj} in inventory.")  # No items in my_data["inventory"] are matched, illegal item name
                    loop(my_data, cmds, room_curr)
                elif len(items_filtered) > 1:
                    out = "Did you want to drop the "  # If 2 or more items are matched, ask for clarify
                    out += items_filtered[0]

                    if (len(items_filtered) > 2):
                        for i in range(1, len(items_filtered) - 1):
                            out += ", "
                            out += items_filtered[i]

                    out += " or the "
                    out += items_filtered[-1]
                    out += "?"
                    print(out)
                    loop(my_data, cmds, room_curr)

            my_obj = items_filtered[0]
            my_data["inventory"].remove(my_obj)
            if "items" in room_curr.keys():
                room_curr["items"].append(my_obj)
            else:
                room_curr["items"] = [my_obj]
            print(f'You drop the {my_obj}.')
            if len(my_data["inventory"]) == 0:
                cmds.remove("drop")
            if not "get" in cmds:
                cmds.insert(1, "get")
            loop(my_data, cmds, room_curr)

        if verb == 'inventory':
            if len(my_data["inventory"]) == 0:
                print("You're not carrying anything.")
                loop(my_data, cmds, room_curr)
            print("Inventory:")
            for item in my_data["inventory"]:
                print(f'  {item}')
            loop(my_data, cmds, room_curr)

        if verb == 'look':
            run_game(my_data, room_curr)

        if verb == 'help':
            print("You can run the following commands:")
            for item in cmds:

                if item == "go" or item == "get" or item == "drop":
                    print(f'  {item} ...')
                else:
                    print(f'  {item}')
            loop(my_data, cmds, room_curr)



    except Exception as e:
        print(e)
        print("Use 'quit' to exit.")
        loop(my_data, cmds, room_curr)


def exit_game():
    print("Goodbye!")
    exit(0)


if __name__ == "__main__":
    main()
