import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Maker by Satendra Goswami")
        
        # Initialize attributes
        self.session_times = []
        self.data = None

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # File selection
        tk.Label(self.root, text="Select CSV File:").grid(row=0, column=0, padx=10, pady=10)
        self.file_path_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.file_path_var, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=10, pady=10)

        # Number of sessions
        tk.Label(self.root, text="Number of Sessions:").grid(row=1, column=0, padx=10, pady=10)
        self.num_sessions_var = tk.StringVar()
        self.num_sessions_entry = tk.Entry(self.root, textvariable=self.num_sessions_var, width=10)
        self.num_sessions_entry.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Set Sessions", command=self.set_sessions).grid(row=1, column=2, padx=10, pady=10)

        # Session times
        self.session_times_frame = tk.Frame(self.root)
        self.session_times_frame.grid(row=2, column=0, columnspan=3)

        # Required participation time
        tk.Label(self.root, text="Required Participation Time (minutes):").grid(row=3, column=0, padx=10, pady=10)
        self.required_participation_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.required_participation_var, width=10).grid(row=3, column=1, padx=10, pady=10)

        # Process button
        tk.Button(self.root, text="Process Attendance", command=self.process_attendance).grid(row=4, column=0, columnspan=3, pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
        self.file_path_var.set(file_path)
        self.load_csv(file_path)

    def load_csv(self, file_path):
        try:
            self.data = pd.read_csv(file_path, skiprows=3)
            self.data['Join Time'] = pd.to_datetime(self.data['Join Time'], format='%m/%d/%Y %I:%M:%S %p')
            self.data['Leave Time'] = pd.to_datetime(self.data['Leave Time'], format='%m/%d/%Y %I:%M:%S %p')
            messagebox.showinfo("Success", "CSV file loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")

    def set_sessions(self):
        # Clear previous session entries if they exist
        for widget in self.session_times_frame.winfo_children():
            widget.destroy()

        try:
            num_sessions = int(self.num_sessions_var.get())
            self.session_times = []

            for i in range(num_sessions):
                tk.Label(self.session_times_frame, text=f"Session {i + 1} Start:").grid(row=i, column=0, padx=10, pady=5)
                start_date_var = tk.StringVar()
                start_hour_var = tk.StringVar()
                start_minute_var = tk.StringVar()

                start_date_picker = DateEntry(self.session_times_frame, textvariable=start_date_var, date_pattern='y-mm-dd')
                start_date_picker.grid(row=i, column=1, padx=10, pady=5)
                
                start_hour_spinbox = tk.Spinbox(self.session_times_frame, from_=0, to=23, wrap=True, format='%02.0f', width=3, textvariable=start_hour_var)
                start_hour_spinbox.grid(row=i, column=2, padx=5, pady=5)
                
                start_minute_spinbox = tk.Spinbox(self.session_times_frame, from_=0, to=59, wrap=True, format='%02.0f', width=3, textvariable=start_minute_var)
                start_minute_spinbox.grid(row=i, column=3, padx=5, pady=5)

                tk.Label(self.session_times_frame, text=f"End:").grid(row=i, column=4, padx=10, pady=5)
                end_date_var = tk.StringVar()
                end_hour_var = tk.StringVar()
                end_minute_var = tk.StringVar()

                end_date_picker = DateEntry(self.session_times_frame, textvariable=end_date_var, date_pattern='y-mm-dd')
                end_date_picker.grid(row=i, column=5, padx=10, pady=5)
                
                end_hour_spinbox = tk.Spinbox(self.session_times_frame, from_=0, to=23, wrap=True, format='%02.0f', width=3, textvariable=end_hour_var)
                end_hour_spinbox.grid(row=i, column=6, padx=5, pady=5)
                
                end_minute_spinbox = tk.Spinbox(self.session_times_frame, from_=0, to=59, wrap=True, format='%02.0f', width=3, textvariable=end_minute_var)
                end_minute_spinbox.grid(row=i, column=7, padx=5, pady=5)

                start_date_picker.bind("<<DateEntrySelected>>", lambda event, end_date_var=end_date_var, start_date_var=start_date_var: end_date_var.set(start_date_var.get()))

                self.session_times.append(((start_date_var, start_hour_var, start_minute_var), (end_date_var, end_hour_var, end_minute_var)))

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of sessions.")

    def process_attendance(self):
        if self.data is None:
            messagebox.showerror("Error", "Please load a CSV file first.")
            return

        if not self.session_times:
            messagebox.showerror("Error", "Please set the session times.")
            return

        required_participation = int(self.required_participation_var.get())
        session_labels = [f'{session[0][0].get()}_session{i + 1}' for i, session in enumerate(self.session_times)]

        for label in session_labels:
            if label not in self.data.columns:
                self.data[label] = 'A'  # Default to absent

        for i, ((start_date_var, start_hour_var, start_minute_var), (end_date_var, end_hour_var, end_minute_var)) in enumerate(self.session_times):
            session_start = pd.to_datetime(f"{start_date_var.get()} {start_hour_var.get()}:{start_minute_var.get()}:00")
            session_end = pd.to_datetime(f"{end_date_var.get()} {end_hour_var.get()}:00:{end_minute_var.get()}")

            for idx, row in self.data.iterrows():
                join_time = row['Join Time']
                leave_time = row['Leave Time']

                if join_time < session_end and leave_time > session_start:
                    presence_duration = (min(leave_time, session_end) - max(join_time, session_start)).total_seconds() / 60.0

                    if presence_duration >= required_participation:
                        self.data.at[idx, session_labels[i]] = 'P'

        # Merging entries with the same name and email
        merged_data = self.data.groupby(['Name (Original Name)', 'User Email'], as_index=False).apply(self.merge_entries).reset_index(drop=True)

        # Creating attendance summary
        attendance_summary = merged_data[session_labels].apply(pd.Series.value_counts).fillna(0).sum()

        # Displaying summary
        popup = tk.Toplevel(self.root)
        popup.title("Attendance Summary")
        tk.Label(popup, text=f"Present: {int(attendance_summary.get('P', 0))}\nAbsent: {int(attendance_summary.get('A', 0))}\n\nThanks to Satendra Goswami for this application!", padx=20, pady=20).pack()
        tk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)

        # Save to CSV
        output_file_path = self.file_path_var.get().replace('.csv', '_attendance_results.csv')
        merged_data.to_csv(output_file_path, index=False)

        messagebox.showinfo("Success", f"Attendance has been successfully generated and saved to {output_file_path}.")

    def merge_entries(self, group):
        # Initialize the merged row
        merged_row = group.iloc[0].copy()
        merged_row['Join Time'] = group['Join Time'].min()
        merged_row['Leave Time'] = group['Leave Time'].max()
        merged_row['Duration (Minutes)'] = sum(group['Duration (Minutes)'].tolist())
        
        # Check if participant has satisfied the attendance criteria for each session
        for label in [col for col in group.columns if '_session' in col]:
            if (group[label] == 'P').any():
                merged_row[label] = 'P'
            else:
                merged_row[label] = 'A'
        
        return merged_row

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
