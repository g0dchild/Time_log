import os
print(f"📍 Jag sparar filer i den här mappen: {os.getcwd()}")
import tkinter as tk
from tkinter import messagebox
import time
import csv
import os
from datetime import datetime

class TimeLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enkel Tidslogg")
        self.root.geometry("400x350")
        
        # Variabler
        self.start_time = None
        self.running = False
        self.log_file = "min_tidslogg.csv"

        # --- UI Komponenter ---
        
        # Rubrik
        self.label_title = tk.Label(root, text="Vad jobbar du på?", font=("Arial", 12))
        self.label_title.pack(pady=5)

        # Inmatningsfält för uppgift
        self.task_entry = tk.Entry(root, font=("Arial", 12), width=30)
        self.task_entry.pack(pady=5)

        # Tidvisare
        self.time_display = tk.Label(root, text="00:00:00", font=("Helvetica", 36, "bold"), fg="#333")
        self.time_display.pack(pady=20)

        # Knappar (Frame för att lägga dem bredvid varandra)
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.btn_start = tk.Button(button_frame, text="Starta", command=self.start_timer, bg="#4CAF50", fg="white", width=10, font=("Arial", 10, "bold"))
        self.btn_start.pack(side=tk.LEFT, padx=10)

        self.btn_stop = tk.Button(button_frame, text="Stoppa & Spara", command=self.stop_timer, bg="#f44336", fg="white", width=15, font=("Arial", 10, "bold"))
        self.btn_stop.pack(side=tk.LEFT, padx=10)
        self.btn_stop.config(state=tk.DISABLED) # Inaktiverad tills start

        # Senaste loggar (Status)
        self.status_label = tk.Label(root, text="Senaste loggar:", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=(20, 5))
        
        self.log_display = tk.Text(root, height=5, width=45, state=tk.DISABLED, bg="#f0f0f0", font=("Consolas", 9))
        self.log_display.pack(pady=5)

        # Skapa filen om den inte finns
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Datum", "Uppgift", "Starttid", "Sluttid", "Duration"])
        
        # Uppdatera logg-fönstret vid start
        self.update_log_display()

    def update_clock(self):
        if self.running:
            elapsed = time.time() - self.start_time
            # Formatera till HH:MM:SS
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed))
            self.time_display.config(text=formatted_time)
            # Anropa denna funktion igen om 100ms
            self.root.after(100, self.update_clock)

    def start_timer(self):
        task_name = self.task_entry.get().strip()
        if not task_name:
            messagebox.showwarning("Varning", "Du måste namnge uppgiften först!")
            return

        self.start_time = time.time()
        self.running = True
        
        # UI uppdateringar
        self.task_entry.config(state=tk.DISABLED)
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        
        self.update_clock()

    def stop_timer(self):
        if not self.running:
            return

        end_time = time.time()
        self.running = False
        
        # Beräkna data för sparning
        elapsed = end_time - self.start_time
        duration_str = time.strftime("%H:%M:%S", time.gmtime(elapsed))
        
        start_dt = datetime.fromtimestamp(self.start_time).strftime("%H:%M:%S")
        end_dt = datetime.fromtimestamp(end_time).strftime("%H:%M:%S")
        date_str = datetime.now().strftime("%Y-%m-%d")
        task_name = self.task_entry.get()

        # Spara till CSV
        with open(self.log_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([date_str, task_name, start_dt, end_dt, duration_str])

        # Återställ UI
        self.time_display.config(text="00:00:00")
        self.task_entry.config(state=tk.NORMAL)
        self.task_entry.delete(0, tk.END) # Rensa fältet
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        
        self.update_log_display()
        messagebox.showinfo("Klar", f"Sparade tid för: {task_name}\nTid: {duration_str}")

    def update_log_display(self):
        """Läser de sista raderna från CSV-filen och visar dem"""
        self.log_display.config(state=tk.NORMAL)
        self.log_display.delete(1.0, tk.END)
        
        try:
            with open(self.log_file, mode='r', encoding='utf-8') as file:
                lines = file.readlines()
                # Visa bara de sista 5 raderna (exklusive header om filen är kort)
                last_lines = lines[-5:] if len(lines) > 5 else lines[1:]
                for line in last_lines:
                    self.log_display.insert(tk.END, line)
        except Exception:
            self.log_display.insert(tk.END, "Inga loggar än...")
            
        self.log_display.config(state=tk.DISABLED)

# Kör programmet
if __name__ == "__main__":
    root = tk.Tk()
    app = TimeLoggerApp(root)
    root.mainloop()