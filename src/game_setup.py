def input_algorithm():
    while True:
        algorithm = input("Enter the number of the algorithm you would like to play against: ")
        if algorithm == "1" or algorithm == "2" or algorithm == "3":
            print ("Only minimax is available at the moment.")
            return algorithm
        else:
            print("Invalid input. Please enter a valid number.")

def input_difficulty():
    while True:
        difficulty = input("Enter the number of the difficulty you would like to play against: ")
        if difficulty == "1" or difficulty == "2" or difficulty == "3":
            return difficulty
        else:
            print("Invalid input. Please enter a valid number.")

def input_color():
    while True:
        color = input("Enter the number of the color you would like to play as: ")
        if color == "1" or color == "2":
            return color
        else:
            print("Invalid input. Please enter a valid number.")

def create_setup(): 
    print ("Welcome to the Checkers Game! Please select the number of your coresponding choice.")
    print ("What algorithm would you like to fight against?")
    print ("1. Minimax")
    print ("2. A*")
    print ("3. Bayesian Network")
    algorithm = input_algorithm()
    print ("What difficulty would you like to play against?")
    print ("1. Easy")
    print ("2. Medium")
    print ("3. Hard")
    difficulty = input_difficulty()
    print ("What color would you like to play as?")
    print ("1. Black")
    print ("2. Red")
    color = input_color()

    return algorithm, difficulty, color
