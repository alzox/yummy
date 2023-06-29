# import command line arguments
import sys

def add_food(amount):
    week = input("Week: ")
    
    with open("current food.csv", "a") as myfile:
        for i in range(int(amount)):
            item = input("Item Name: ")
            cost = input("Item Cost: ")
            calories = input("Item Calories per Serving: ")
            servings = input("Item Servings: ")
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

def cook_food(amount):
    week = input("Week: ")
    item_calories = 0
    item_cost = 0
    for i in range(int(amount)):
        with open("current food.csv", "r") as myfile:
            lines = myfile.readlines()
            for i in range(1, len(lines)):
                item_line = lines[i].split(",")
                print(str(i) + ": " + item_line[0])
            index = input("Which item would you like to cook? ")
            
            # split the line into a list
            item_line = lines[int(index)].split(",")
            
            item_line[3] = str(int(item_line[3]) - 1) # subtract one from the servings
            # add the cost and calories to the total
            item_cos = float(lines[int(index)].split(",")[5])
            item_cal = float(lines[int(index)].split(",")[2])
            # add the cost and calories to the total
            item_cost += item_cos
            item_calories += item_cal
            
            if item_line[3] <= "0":
                # write line to ate out.csv and remove from current food.csv
                with open("ate out.csv", "a") as myfile:
                    myfile.write("Finished" + "," + item_line[1] + "," + item_line[4] + "\n")
                myfile.close()
                lines.pop(int(index))
            else:
                lines[int(index)] = ",".join(item_line) # join the list back into a string


        myfile.close()
        
        # open the file again to write the new values
        with open("current food.csv", "w") as myfile:
            for line in lines:
                myfile.write(line)
                
        # write to consumption.csv
        with open("consumption.csv", "a") as myfile:
            day = input("Day: ")
            myfile.write(item_line[0] + "," + str(item_cal) + "," + week + "," + day + "\n")
    return item_calories, item_cost

def bought_food():
    with open("ate out.csv", "a") as myfile:
        item = input("Item Name: ")
        cost = input("Item Cost: ")
        week = input("Week: ")
        day = input("Day: ")
        myfile.write(item + "," + cost + "," + week + "\n")
    myfile.close()
    
    with open("consumption.csv", "a") as myfile:
        calories = input("Item Calories: ")
        myfile.write(item + "," + calories + "," + week + "," + day + "\n")
    
if __name__ == "__main__":
    args = sys.argv[1:] # arg[0] is the file name
    # args[0] is the first (1) argument  | add or remove or cook or buy
    # args[1] is the second (2) argument | amount
    if args[0] == "add":
        add_food(args[1])
    if args[0] == "remove":
        for i in range(int(args[1])):
            remove_food()
    if args[0] == "cook":
        calories, cost = cook_food(args[1])
        print("Total Calories: " + str(calories))
        print("Total Cost: " + str(cost))
    if args[0] == "bought":
        for i in range(int(args[1])):
            bought_food()
                        
# Example command line arguments:
# python foodplanner.py add 1
# python foodplanner.py remove 1
# python foodplanner.py cook 1
# python foodplanner.py bought 1