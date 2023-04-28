
import time

# Create a node
class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []


# Tree
class BPlusTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t


    # Insert node
    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.child.insert(0, root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)


    # Insert nonfull
    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            # Handle leaf node
            x.keys.append((None, None))
            while i >= 0 and k[0] < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k[0] < x.keys[i][0]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                # Check if the child node is full before descending
                self.split_child(x, i)
                if k[0] > x.keys[i][0]:
                    i += 1
            if x.child[i].leaf:
                self.insert_non_full(x.child[i], k)
            else:
                self.insert_non_full(x.child[i], k)

    # Split the child
    def split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BTreeNode(y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.child = y.child[t: 2 * t]
        y.child = y.child[0: t - 1]


    # Print the tree
    def print_tree(self, x, l=0):
        print("Level ", l, " ", len(x.keys), end=":")
        for i in x.keys:
            print(i, end=" ")
        print()
        l += 1
        if len(x.child) > 0:
            for i in x.child:
                self.print_tree(i, l)

    # Search key in the tree

    def search(self, k):
        return self.search_key(k, self.root)

    # Search key in the tree
    def search_key(self, k, x=None):
        if x is not None:
            i = 0
            while i < len(x.keys) and k > x.keys[i][0]:
                i += 1
            if i < len(x.keys) and k == x.keys[i][0]:
                return (x, i)
            elif x.leaf:
                return None
            else:
                return self.search_key(k, x.child[i])

        else:
            return self.search_key(k, self.root)





import tkinter as tk
from tkinter import messagebox


class BPlusTreeGUI:
    def __init__(self):
        self.b_plus_tree = None
        self.window = tk.Tk()
        self.window.title("B+ Tree Insertion")
        self.Canvasnav = tk.Canvas(self.window, bg="#027373", height=50, width=self.window.winfo_screenwidth())
        self.Canvasnav.pack()
        self.Canvasnav.create_text(self.window.winfo_screenwidth() / 2, 25, text="B+ Tree", fill="white",
                                   font=('Helvetica 30 bold'))
        self.Canvasnav.pack()
        self.Canvasop = tk.Canvas(self.window, bg="#A9D9D0", height=75, width=self.window.winfo_screenwidth())

        self.entry_degree = tk.Entry(self.window, width=5)
        self.Canvasop.create_window(50, 35, window=self.entry_degree)
        self.Canvasop.pack()
        self.Canvasop.create_text(120, 35, text="Degree:", fill="black",
                                  font=('Helvetica 15 bold'))

        self.entry_insert = tk.Entry(self.window, width=25)
        self.Canvasop.create_window(320, 35, window=self.entry_insert)
        self.Canvasop.pack()
        self.button_widget = tk.Button(text='Insert', command=self.insert_elements)
        self.Canvasop.create_window(500, 35, window=self.button_widget)

        self.entry_search = tk.Entry(self.window, width=15)
        self.Canvasop.create_window(650, 35, window=self.entry_search)
        self.button_widget = tk.Button(text='Search', command=self.search_key)
        self.Canvasop.create_window(780, 35, window=self.button_widget)

        """
        self.Canvasop.create_text(270, 35, text="Insert:", fill="black",
                                  font=('Helvetica 15 bold'))

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
        """

        self.canvas = tk.Canvas(self.window, width=self.window.winfo_screenwidth(),
                                height=self.window.winfo_screenheight() - 250)
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
                self.window.update()
                time.sleep(0.5)

    def search_key(self):
        if self.b_plus_tree is None:
            tk.messagebox.showerror("Error", "B+ Tree not initialized")
        else:
            val = int(self.entry_search.get())

            result = self.b_plus_tree.search(val)
            if result is None:
                tk.messagebox.showinfo("Search Result", f"No match found for key '{val}'")
            else:
                node, index = result
                tk.messagebox.showinfo("Search Result", f"Key '{val}' found in node: {node.keys}, at index: {index}")


if __name__ == '__main__':
    b_plus_tree_gui = BPlusTreeGUI()
    b_plus_tree_gui.window.mainloop()
