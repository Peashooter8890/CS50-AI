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
        self.knowledge = set()

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
    
    def cellLoader(self,cell):
        # Stores i and j as row and column. Initiate set cells to store all valid neighbor cells.
        i = cell[0]
        j = cell[1]
        cells = set()
        # For each tile in the 9x9 area:
        for x in range(i-1,i+2):
            for y in range(j-1,j+2):
                # If tile is a neighbor and not itself:
                if (not(x==i and y==j)):
                    # If a tile's indices are not out of bounds:
                    if (x >= 0 and y >= 0):
                        if (x <= 7 and y <= 7):
                            # If a tile is not already a mine or a safe:
                            if not((x,y) in (self.mines or self.safes)):
                                # Store cell in the set cells.
                                cells.add((x,y))
        return cells

    def eliminateSubsets(self):
        # For each sentence in knowledge, repeat for each sentence in knowledge (iteration = knowledge^2)
        if (len(self.knowledge) > 1):
            for sentence in self.knowledge:
                for subsentence in self.knowledge:
                    # If sentence is not itself:
                    if (sentence.cells != subsentence.cells):
                        # if sentence is not empty (we have to stop program from thinking empty set is a subset)
                        if (len(sentence.cells) != 0 and len(subsentence.cells) != 0):
                            # If a sentence is a subset of our sentence:
                            if (subsentence.cells.issubset(sentence.cells)):
                                print(f"Because {subsentence} is a subset of {sentence}, I will execute set elimination :D")
                                sentence.cells -= subsentence.cells
                                temp = sentence.count - subsentence.count
                                sentence.count = temp
                                print(f"Now the two sets are: {subsentence} and {sentence}")

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
        sentence = Sentence(neighbors,int(count))
        #print(f"Our new sentence is: {sentence}")
        self.knowledge.add(sentence)

        while True:
            change = 0

            # Eliminate subsets
            self.eliminateSubsets()

            # Check if any tiles are confident to be a mine or a safe.
            for sentence in self.knowledge:
                # If a sentence confirms that a cell is mine, then mark it as mine
                mines = sentence.known_mines().copy()
                if (len(mines) > 0):
                    change = 1
                    for mine in mines:
                        self.mark_mine(mine)

                # If a sentence confirms that a cell is safe, then add it to knowledge base (recursive method)
                safes = sentence.known_safes().copy()
                if (len(safes) > 0):
                    change = 1
                    for safe in safes:
                        #print(f"Marking {safe} as safe :)")
                        self.mark_safe(safe)
            if (change == 0):
                break
        #print(f"Availiable moves are now: {self.safes - self.moves_made}")
        print("BELOW IS THE LIST OF SENTENCES AVAILIABLE NOW")
        for sentence in self.knowledge:
            print(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Load all safe moves to set that is not an already executed move :)
        certainty = set()
        for cell in self.safes:
            if (cell not in self.moves_made):
                certainty.add(cell)
        
        # If there are no newly availiable safe moves, return nothing.
        if (len(certainty) == 0):
            return None
        else:
            move = random.choice(tuple(certainty))
            print(f"Executing safe move: {move}")
            return move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Load all uncertain moves to set that is not an already executed move :)
        uncertainty = set()
        for sentence in self.knowledge:
            for cell in sentence.cells:
                if (cell not in self.moves_made):
                    uncertainty.add(cell)
        
        # If there are no newly availiable random moves, return nothing.
        if (len(uncertainty) == 0):
            return None
        else:
            move = random.choice(tuple(uncertainty))
            return move