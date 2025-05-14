import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

class LineCounter:
    def __init__(self, file_name): 
        self.file_name = file_name 
        self.line = [] 
        self.ip_add = []

    def read(self): 
        with open(self.file_name, 'r') as f:
            self.line = f.readlines()

    def fetch_ip_add(self):
        self.ip_add = list(map(lambda x: x.split(" ")[0], self.line))
        return self.ip_add

    def ip_add_filtered(self, threshold): 
        return list(filter(lambda x: x.split(".")[0].isdigit() and int(x.split(".")[0]) < threshold, self.ip_add))

    def ratio(self, threshold): 
        total = len(self.fetch_ip_add())
        lt_threshold = len(self.ip_add_filtered(threshold))
        return lt_threshold / total if total != 0 else 0

# GUI App
class LogFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Log File IP Filter")
        self.counter = None

        self.file_btn = tk.Button(root, text="Select Log File", command=self.load_file)
        self.file_btn.pack(pady=5)

        # Entry for filter threshold
        self.filter_frame = tk.Frame(root)
        self.filter_frame.pack(pady=5)

        tk.Label(self.filter_frame, text="Filter IPs with first octet less than: ").pack(side=tk.LEFT)
        self.threshold_entry = tk.Entry(self.filter_frame, width=5)
        self.threshold_entry.pack(side=tk.LEFT)
        self.threshold_entry.insert(0, "20")

        self.show_ips_btn = tk.Button(root, text="Show All IPs", command=self.show_ips, state='disabled')
        self.show_ips_btn.pack(pady=5)

        self.show_filtered_btn = tk.Button(root, text="Filter IPs", command=self.show_filtered, state='disabled')
        self.show_filtered_btn.pack(pady=5)

        self.ratio_btn = tk.Button(root, text="Show Ratio", command=self.show_ratio, state='disabled')
        self.ratio_btn.pack(pady=5)

        self.output = ScrolledText(root, width=60, height=20)
        self.output.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Log files", "*.log *.txt")])
        if file_path:
            self.counter = LineCounter(file_path)
            self.counter.read()
            self.show_ips_btn.config(state='normal')
            self.show_filtered_btn.config(state='normal')
            self.ratio_btn.config(state='normal')
            messagebox.showinfo("File Loaded", f"Loaded {file_path}")

    def get_threshold(self):
        try:
            return int(self.threshold_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for the filter threshold.")
            return None

    def show_ips(self):
        if self.counter:
            self.output.delete('1.0', tk.END)
            ips = self.counter.fetch_ip_add()
            self.output.insert(tk.END, "\n".join(set(ips)))

    def show_filtered(self):
        if self.counter:
            threshold = self.get_threshold()
            if threshold is not None:
                self.output.delete('1.0', tk.END)
                filtered = self.counter.ip_add_filtered(threshold)
                self.output.insert(tk.END, "\n".join(set(filtered)))

    def show_ratio(self):
        if self.counter:
            threshold = self.get_threshold()
            if threshold is not None:
                ratio = self.counter.ratio(threshold)
                self.output.delete('1.0', tk.END)
                self.output.insert(tk.END, f"Ratio (IPs with first octet < {threshold}): {ratio:.4f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LogFilterApp(root)
    root.mainloop()
