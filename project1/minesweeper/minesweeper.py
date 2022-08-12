import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If the number of mines are equal to number of cells, all of them are mines.
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If there are no mines nearby, all of the cells are safes. 
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Subtract cell and count from original sentence
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Subtract only cell, but not count
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """
    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
    
    def cellLoader(self,matrix,i,j):
        # Checks all the valid neighbors of a cell, then returns them if they are not already in mines or safes.
        cells = set()
        for x in range(i-1,i+2):
            for y in range(i-1,i+2):
                if(not(x==i and y==j)):
                    try:
                        if(x >= 0 and y >= 0):
                            if not((x,y) in (self.mines or self.safes)):
                                cells.add(matrix[x][y])
                    except:
                        pass
        return cells

    def eliminateSubsets(sets):
        # Eliminate subsets (Tested Function) 
        for sentence in sets:
            for subsentence in sets:
                if sentence != subsentence:
                    if subsentence.cells.issubset(sentence.cells):
                        sentence.cells -= subsentence.cells
                        sentence.count -= subsentence.count

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Record the cell as one of the moves made
        self.moves_made.add(cell)

        # Mark cell as safe
        self.mark_safe(cell)

        # Make sentence out of the cell's surrounding neighbors and mine count, add it to AI's knowledge base
        neighbors = self.cellLoader(cell)
        sentence = Sentence(neighbors,count)
        self.knowledge.append(sentence)

        # Add all sentences to rule. Execute subset elimination to create new inferences.
        sets = set()
        for sentence in self.sentences:
            sets.add(sentence)

        while(True):
            # Keep track of change
            change = 0

            # Eliminate subsets
            self.eliminateSubsets(sets)

            # Check if any tiles are confident to be a mine or a safe.
            for sentence in self.sentences:
                # If a sentence confirms that a cell is mine, then mark it as mine
                mines = sentence.known_mines()
                if (len(mines) > 0):
                    change = 1
                    for mine in mines:
                        self.mark_mine(mine)

                # If a sentence confirms that a cell is safe, then add it to knowledge base (recursive method)
                safes = sentence.known_safes()
                if (len(safes) > 0):
                    change = 1
                    for safe in safes:
                        self.add_knowledge(safe,safe.count)
            
            if (change == 0):
                break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Randomly choose from safe moves :)
        return random.choices(self.safes)

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Combine all uncertain cells in sentences into a set, then randomly chooes from them.
        uncertainty = set()
        for sentence in self.knowledge:
            uncertainty.add(sentence.cells)
        return random.choice(uncertainty)
