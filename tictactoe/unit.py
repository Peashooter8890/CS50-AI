matrix = [[0, 2, 0],
          [0, 1, 1],
          [0, 0, 1],
          [1, 0, 0]]

conditionX = True
conditionO = True
counter = 0
for m in matrix:
        for num in m:
            if (counter < 2):
                if (num == 0):
                    conditionX = False
            else:
                if(num == 0):
                    conditionO = False
        counter += 1

print(conditionX,conditionO)