# import command line arguments
import sys

def add_food():
    with open("current food.csv", "a") as myfile:
        item = input("Item Name: ")
        cost = input("Item Cost: ")
        calories = input("Item Calories per Serving: ")
        servings = input("Item Servings: ")
        week = input("Week: ")
        cost_per_serving = float(cost) / float(servings)
        myfile.write(item + "," + cost + "," + calories + "," + servings + "," + week + "," + str(cost_per_serving) + "\n")
        
def remove_food():
    with open("current food.csv", "r") as myfile:
        lines = myfile.readlines()
        for i in range(len(lines)):
            print(str(i) + ": " + lines[i])
        index = input("Which item would you like to remove? ")
        lines.pop(int(index))
    myfile.close()
     
    with open("current food.csv", "w") as myfile:
        for line in lines:
            myfile.write(line)

def cook_food():
    with open("current food.csv", "r") as myfile:
        lines = myfile.readlines()
        for i in range(1, len(lines)):
            item_line = lines[i].split(",")
            print(str(i) + ": " + item_line[0])
        index = input("Which item would you like to cook? ")
        
        # split the line into a list
        item_line = lines[int(index)].split(",")
        item_line[3] = str(int(item_line[3]) - 1) # subtract one from the servings
        
        if item_line[3] <= "0":
            lines.pop(int(index))
        else:
            lines[int(index)] = ",".join(item_line) # join the list back into a string

        # add the cost and calories to the total
        item_cost = float(lines[int(index)].split(",")[5])
        item_calories = float(lines[int(index)].split(",")[2])
    myfile.close()
    
    # open the file again to write the new values
    with open("current food.csv", "w") as myfile:
        for line in lines:
            myfile.write(line)
            
    # write to consumption.csv
    with open("consumption.csv", "a") as myfile:
        week = input("Week: ")
        day = input("Day: ")
        myfile.write(item_line[0] + "," + str(item_calories) + "," + week + "," + day + "\n")
    return item_calories, item_cost

def bought_food():
    with open("ate out.csv", "a") as myfile:
        item = input("Item Name: ")
        cost = input("Item Cost: ")
        week = input("Week: ")
        day = input("Day: ")
        myfile.write(item + "," + cost + "," + week + "," + day + "\n")
    myfile.close()
    
    with open("consumption.csv", "a") as myfile:
        calories = input("Item Calories: ")
        myfile.write(item + "," + cost + "," + week + "," + day + "\n")
    
if __name__ == "__main__":
    args = sys.argv[1:] # arg[0] is the file name
    # args[0] is the first (1) argument  | add or remove or cook
    # args[1] is the second (2) argument | amount to add or remove
    if args[0] == "add":
        for i in range(int(args[1])):
            add_food()
    if args[0] == "remove":
        for i in range(int(args[1])):
            remove_food()
    if args[0] == "cook":
        total_calories = 0
        total_cost = 0
        for i in range(int(args[1])):
            item_calories, item_cost = cook_food() # returns the calories and cost of the item also subtracts one from the servings

            total_calories += item_calories
            total_cost += item_cost
        print("Total Calories: " + str(total_calories))
        print("Total Cost: " + str(total_cost))
    if args[0] == "bought":
        for i in range(int(args[1])):
            bought_food()
                        
# Example command line arguments:
# python foodplanner.py add 1
# python foodplanner.py remove 1
# python foodplanner.py cook 1
# python foodplanner.py bought 1