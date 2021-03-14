import random
import tkinter as tk
import tkinter.messagebox as mbox

SIZE = 4


class Application(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.createWidgets()
        self.new_game()


    def new_game(self):

        for_shuffling = list(range(SIZE*SIZE))
        self.positions = [[None] * SIZE for i in range(SIZE)]

        random.shuffle(for_shuffling)
        for i, num in enumerate(for_shuffling):
            self.positions[i // SIZE][i % SIZE] = num

        while self.check_bad_position():
            random.shuffle(for_shuffling)
            for i, num in enumerate(for_shuffling):
                self.positions[i // SIZE][i % SIZE] = num

        for i in range(SIZE):
            for j in range(SIZE):
                if self.positions[i][j] != 0:
                    self.tiles[self.positions[i][j] - 1].grid(row=i, column=j, sticky='NSEW')
                else:
                    self.empty_position = (i, j)


    def next_turn(self, tile):
        
        tile_info = tile.grid_info()
        row, col = tile_info['row'], tile_info['column']

        if (abs(row - self.empty_position[0]) == 1 and abs(col - self.empty_position[1]) == 0
             or abs(row - self.empty_position[0]) == 0 and abs(col - self.empty_position[1]) == 1):
                tile.grid(row=self.empty_position[0], column=self.empty_position[1], sticky='NSEW')
                self.positions[self.empty_position[0]][self.empty_position[1]], self.positions[row][col] = \
                    self.positions[row][col], self.positions[self.empty_position[0]][self.empty_position[1]]
                self.empty_position = (row, col)
                
                self.check_win()


    def check_win(self):

        win_state = [[(i*SIZE + j + 1) % (SIZE*SIZE) for j in range(SIZE)] for i in range(SIZE)]
        
        if self.positions == win_state:
            mbox.showinfo(message='You win!')
            self.new_game()

    
    def check_bad_position(self):

        flatten_position = [item for subl in self.positions for item in subl]

        check_sum = 0

        for i in range(SIZE):
            for j in range(SIZE):
                num = self.positions[i][j]
                if num:
                    check_sum += len([i for i in flatten_position[i*SIZE + j + 1:] if i < num and i != 0])
                else:
                    check_sum += i + 1

        return bool(check_sum % 2)


    def createWidgets(self):

        self.pack(expand=True, fill='both')

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.control = tk.Frame(self)
        self.control.grid(row=0, column=0)

        new_button = tk.Button(self.control, text='New', width=7, height=1, command=self.new_game)
        exit_button = tk.Button(self.control, text='Exit', width=7, height=1, command=exit)

        new_button.grid(row=0, column=0)
        exit_button.grid(row=0, column=1)

        self.field = tk.Frame(self)
        self.field.grid(row=1, column=0, sticky='NSEW')

        for i in range(SIZE):
            self.field.rowconfigure(i, weight=1)
            self.field.columnconfigure(i, weight=1)

        self.tiles = []

        for i in range(1, SIZE*SIZE):
            tile = tk.Button(self.field, text=f'{i}')
            tile.configure(command=lambda tile=tile: self.next_turn(tile))
            
            self.tiles.append(tile)


if __name__ == '__main__':

    app = Application()
    app.master.title('15 game')
    app.mainloop()
