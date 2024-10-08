# Zoomcsvtoattendance
AttendanceApp is a Python-based desktop application designed to streamline attendance tracking and management. The application allows users to process attendance data from Zoom log CSV files, calculate participation based on specified session times, and determine if participants meet required attendance thresholds.

# Features:
Load CSV Files: Import attendance data from CSV files.
Flexible Session Management: Define multiple sessions with custom start and end times.
Participation Calculation: Evaluate if participants meet the required attendance duration and mark them as Present (P) or Absent (A).
Data Merging: Combine multiple records for participants with the same name and email, and sum their total session time.
Export Results: Save the processed attendance data to a new CSV file, reflecting individual participation and session statuses.

# Usage:
1. Run the Application: Execute the application to open the GUI.
2. Select a CSV File: Load your attendance data file.
3. Set Session Times: Configure session start and end times.
4. Specify Required Time: Define the minimum participation time required.
5. Process Attendance: Click the button to process the data and generate the results.

# Installation:
1. Clone the repository: git clone https://github.com/satendravoice/Zoomcsvtoattendance.git
2. Install dependencies: pip install -r requirements.txt
3. Run the application: python src/Zoomcsvtoattendance.py

# Contribution:
Feel free to open issues or submit pull requests if you have improvements or bug fixes.

# License:
This project is licensed under the MIT License. See the LICENSE file for details.
