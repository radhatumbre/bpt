import tkinter as tk
from bplustree import BPlusTree

class BPlusTreeGUI:
    def __init__(self):
        self.b_plus_tree = None
        self.window = tk.Tk()
        self.window.title("B+ Tree Insertion")
        self.label_degree = tk.Label(self.window, text="Enter the degree of B+ tree:")
        self.label_degree.pack()
        self.entry_degree = tk.Entry(self.window)
        self.entry_degree.pack()
        self.label_insert = tk.Label(self.window, text="Enter elements to be inserted (comma separated):")
        self.label_insert.pack()
        self.entry_insert = tk.Entry(self.window)
        self.entry_insert.pack()
        self.button_insert = tk.Button(self.window, text="Insert", command=self.insert_elements)
        self.button_insert.pack()
        self.canvas = tk.Canvas(self.window, width=800, height=600)
        self.canvas.pack()

    def insert_elements(self):
        # Get user input for degree and elements to be inserted
        degree = int(self.entry_degree.get())
        elements = list(map(int, self.entry_insert.get().split(',')))

        if not self.b_plus_tree:
            # If B+ tree is not created, create a new one
            self.b_plus_tree = BPlusTree(degree)
        for element in elements:
            # Insert elements into the B+ tree
            self.b_plus_tree.insert([element])  # Pass the element as a list of keys
            # Clear the canvas
            self.canvas.delete("all")
            # Draw the updated B+ tree
            self.draw_tree(self.b_plus_tree.root, 400, 50, 100)
            # Update the window to display the updated B+ tree
            self.window.update()

    def draw_tree(self, node, x, y, spacing):
        # Draw node
        self.canvas.create_rectangle(x - 30, y - 15, x + 30, y + 15, fill="lightblue")
        self.canvas.create_text(x, y, text=", ".join(str(key) for key in node.keys))

        if not node.leaf:
            # Draw child nodes recursively
            for i, child in enumerate(node.child):
                child_x = x - spacing + (i * spacing * 2) - 50
                child_y = y + 50
                self.canvas.create_line(x, y + 15, child_x, child_y - 15, width=2)
                self.draw_tree(child, child_x, child_y, spacing // 2)


if __name__ == '__main__':
    b_plus_tree_gui = BPlusTreeGUI()
    b_plus_tree_gui.window.mainloop()
