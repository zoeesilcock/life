from Tkinter import *
from lifegrid import LifeGrid

def test(string):
  print string

class App:

  CELL_SIZE = 10
  GRID_WIDTH = 50
  GRID_HEIGHT = 50

  running = False
  generation = 0

  def __init__(self, master):
    master.wm_title('Game of life')
    self.frame = Frame(master)
    self.frame.pack()

    self.top_frame = Frame(self.frame)
    self.grid_frame = Frame(self.frame)

    self.top_frame.pack(side="top", fill="x")
    self.grid_frame.pack(side="bottom", fill="both", expand=True)

    self.start_button = Button(self.top_frame, text="Start", command=self.toggle)
    self.start_button.grid(column=0, row=0)
    self.reset_button = Button(self.top_frame, text="Reset", command=self.reset)
    self.reset_button.grid(column=1, row=0)

    self.generation_string = StringVar()
    self.generation_counter = Label(self.top_frame, textvariable=self.generation_string)
    self.generation_counter.grid(column=2, row=0)
    self.update_generation()
    
    self.canvas = Canvas(self.grid_frame, width=App.CELL_SIZE * App.GRID_WIDTH, height=App.CELL_SIZE * App.GRID_HEIGHT)
    self.canvas.grid(column=0, row=1)
    self.canvas.bind('<Button-1>', self.on_canvas_click)

    self.grid = LifeGrid(self.GRID_WIDTH, self.GRID_HEIGHT)
    self.draw_grid()

  def draw_grid(self):
    self.canvas.delete('all')
    self.canvas.create_rectangle((1, 1, self.CELL_SIZE * self.GRID_WIDTH, self.CELL_SIZE * self.GRID_HEIGHT))    

    for y, row in enumerate(self.grid.matrix):
      for x, cell in enumerate(row):
        if self.grid.matrix[y][x] == 1:
          self.canvas.create_rectangle((x*self.CELL_SIZE, y*self.CELL_SIZE, x*self.CELL_SIZE+self.CELL_SIZE, y*self.CELL_SIZE+self.CELL_SIZE), fill="black")

  def toggle(self):
    if self.running:
      self.running = False
      self.start_button.config(text="Start")
    else:
      self.running = True
      self.start_button.config(text="Stop")
      self.do_step()

  def reset(self):
    self.grid.reset()
    self.generation = 0
    self.draw_grid()
    self.update_generation()

  def do_step(self):
    if self.running:
      self.grid.step()
      self.generation += 1
      self.draw_grid()
      self.update_generation()
      self.frame.after(1000, self.do_step)

  def on_canvas_click(self, event):
    if not self.running:
      x = event.x / self.CELL_SIZE
      y = event.y / self.CELL_SIZE

      self.grid.matrix[y][x] = not self.grid.matrix[y][x]
      self.draw_grid()

  def update_generation(self):
    self.generation_string.set("Generation: {0}".format(self.generation))

root = Tk()
app = App(root)
root.mainloop()
