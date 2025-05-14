import tkinter as tk
from tkinter import filedialog, messagebox

class LineCounter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.line = []
        self.ip_add = []

    def read(self):
        try:
            with open(self.file_name, 'r') as f:
                self.line = f.readlines()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found")

    def fetch_ip_add(self):
        self.ip_add = [line.split(" ")[0] for line in self.line if line.strip()]
        return self.ip_add

    def filter_ips(self, prefix):
        return [ip for ip in self.ip_add if ip.startswith(prefix)]

    def ratio(self, prefix):
        total = len(self.ip_add)
        filtered = len(self.filter_ips(prefix))
        return filtered / total if total > 0 else 0

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Log File IP Analyzer")
        self.root.geometry("700x700")

        # Upload Button
        self.upload_button = tk.Button(root, text="Upload Log File", command=self.upload_file)
        self.upload_button.pack(pady=10)

        # All IPs Label and Listbox
        tk.Label(root, text="All IP Addresses:").pack()
        self.all_ip_listbox = tk.Listbox(root, width=80, height=10)
        self.all_ip_listbox.pack(pady=5)

        # Filter Input Field
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=10)
        tk.Label(filter_frame, text="Filter IPs starting with:").pack(side=tk.LEFT)
        self.prefix_entry = tk.Entry(filter_frame, width=20)
        self.prefix_entry.pack(side=tk.LEFT, padx=5)
        self.filter_button = tk.Button(filter_frame, text="Apply Filter", command=self.update_display)
        self.filter_button.pack(side=tk.LEFT)

        # Filtered IPs Label and Listbox
        tk.Label(root, text="Filtered IP Addresses:").pack()
        self.filtered_ip_listbox = tk.Listbox(root, width=80, height=10)
        self.filtered_ip_listbox.pack(pady=5)

        # Ratio label
        self.ratio_label = tk.Label(root, text="Ratio of filtered IPs: N/A")
        self.ratio_label.pack(pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.line_counter = LineCounter(file_path)
            self.line_counter.read()
            self.line_counter.fetch_ip_add()
            self.update_all_ips()

    def update_all_ips(self):
        self.all_ip_listbox.delete(0, tk.END)
        for ip in self.line_counter.ip_add:
            self.all_ip_listbox.insert(tk.END, ip)

    def update_display(self):
        if not hasattr(self, 'line_counter'):
            messagebox.showwarning("Warning", "Please upload a log file first.")
            return

        prefix = self.prefix_entry.get().strip()
        if not prefix:
            messagebox.showwarning("Warning", "Please enter a prefix to filter.")
            return

        filtered_ips = self.line_counter.filter_ips(prefix)
        ratio = self.line_counter.ratio(prefix)

        self.filtered_ip_listbox.delete(0, tk.END)
        for ip in filtered_ips:
            self.filtered_ip_listbox.insert(tk.END, ip)

        self.ratio_label.config(text=f"Ratio of filtered IPs: {ratio:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
