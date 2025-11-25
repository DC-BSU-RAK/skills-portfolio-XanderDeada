import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

DATA_FILE = os.path.join("studentMarks.txt")

class Student:
    def __init__(self, code, name, course1, course2, course3, exam):
        self.code = int(code)
        self.name = name
        self.course_marks = [int(course1), int(course2), int(course3)]
        self.exam = int(exam)

    def coursework_total(self):
        return sum(self.course_marks)

    def total_mark(self):
        return self.coursework_total() + self.exam

    def percentage(self):
        return round(((self.total_mark()) / 160) * 100, 2)

    def grade(self):
        p = self.percentage()
        if p >= 70:
            return "A"
        elif p >= 60:
            return "B"
        elif p >= 50:
            return "C"
        elif p >= 40:
            return "D"
        else:
            return "F"

    def as_tuple(self):
        return (self.name, str(self.code), str(self.coursework_total()), str(self.exam),
                str(self.percentage()), self.grade())

    def as_line(self):
        return f"{self.code},{self.name},{self.course_marks[0]},{self.course_marks[1]},{self.course_marks[2]},{self.exam}"

def read_students():
    students = []
    try:
        with open(DATA_FILE, 'r') as f:
            lines = f.readlines()
            n = int(lines[0].strip())
            for line in lines[1:]:
                parts = [part.strip() for part in line.strip().split(',')]
                if len(parts) == 6:
                    code, name, c1, c2, c3, exam = parts
                    students.append(Student(code, name, c1, c2, c3, exam))
        return students
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load student data: {e}")
        return []

def write_students(students):
    with open(DATA_FILE, 'w') as f:
        f.write(str(len(students)) + "\n")
        for s in students:
            f.write(s.as_line() + "\n")

#This function sets the Theme of the app(Student Manager)
def set_futuristic_style(root):
    #This is the global backgrounfd
    root.configure(bg="#191c24")

    #This is the tree view style with custum colors
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
        background="#23263a",
        foreground="#b1e3fd",
        fieldbackground="#23263a",
        rowheight=32,
        borderwidth=0,
        font=('Segoe UI', 11, 'bold')
    )
    style.map("Treeview", background=[("selected", "#39e9fa")], foreground=[("selected", "#1a232e")])
    #Heading
    style.configure("Treeview.Heading",
        background="#1a212f",
        foreground="#e7f7fd",
        font=('Segoe UI Semibold', 12, 'bold'),
        relief="flat"
    )
    #Different Button styles,Label,Etc.
    style.configure("TButton", font=('Orbitron', 11, 'bold'), background="#282f47", foreground="#67fff6",
                    borderwidth=0, focuscolor="#83f3f3")
    style.configure("TLabel", font=('Share Tech Mono', 11), background="#191c24", foreground="#67fff6")
    style.configure("TEntry", background="#23263a", fieldbackground="#23263a", foreground="#f8e9ff", bordercolor="#39e9fa")

class FuturisticLabel(tk.Label):
    def __init__(self, master=None, **kw):
        kw["bg"] = "#191c24"
        kw["fg"] = "#39e9fa"
        kw["font"] = ("Share Tech Mono", 11, "bold")
        super().__init__(master, **kw)

class FuturisticButton(tk.Button):
    def __init__(self, master=None, **kw):
        kw["bg"] = "#14203e"
        kw["fg"] = "#67fff6"
        kw["activebackground"] = "#2ee2ec"
        kw["activeforeground"] = "#1d2236"
        kw["relief"] = "flat"
        kw["font"] = ("Orbitron", 11, "bold")
        super().__init__(master, **kw)

class FuturisticEntry(tk.Entry):
    def __init__(self, master=None, **kw):
        kw["bg"] = "#29304a"
        kw["fg"] = "#f7fdfc"
        kw["insertbackground"] = "#67fff6"
        kw["highlightbackground"] = "#39e9fa"
        kw["highlightcolor"] = "#39e9fa"
        kw["highlightthickness"] = 2
        kw["font"] = ("Share Tech Mono", 11)
        super().__init__(master, **kw)

class FuturisticFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        kw["bg"] = "#14171e"
        super().__init__(master, **kw)

class StudentManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap("Student.ico")
        self.title("Student Manager")
        self.geometry("900x560")
        self.configure(bg="#191c24")

        set_futuristic_style(self)

        self.students = read_students()

        self.create_widgets()

    def create_widgets(self):
    #Neon App Heading Title
        title = tk.Label(self, text="STUDENT MANAGER",
                         font=("Orbitron", 22, "bold"),
                         bg="#191c24", fg="#67fff6")
        title.pack(pady=(16,0))

        #Menu Bar
        menubar = tk.Menu(self, bg="#23263a", fg="#67fff6",
                          activebackground="#36e2ff", activeforeground="#19243a",
                          tearoff=0, borderwidth=0, relief="flat", font=("Segoe UI", 10, "bold"))
        recordmenu = tk.Menu(menubar, tearoff=0, bg="#23263a", fg="#67fff6",
                             activebackground="#36e2ff", activeforeground="#19243a", font=("Segoe UI", 10, "bold"))
        recordmenu.add_command(label="View all student records", command=self.show_all_records)
        recordmenu.add_command(label="View individual student record", command=self.show_individual_record)
        recordmenu.add_separator()
        recordmenu.add_command(label="Show student with highest total score", command=self.show_highest_record)
        recordmenu.add_command(label="Show student with lowest total score", command=self.show_lowest_record)
        recordmenu.add_separator()
        recordmenu.add_command(label="Sort student records", command=self.sort_records)
        recordmenu.add_separator()
        recordmenu.add_command(label="Add a student record", command=self.add_record)
        recordmenu.add_command(label="Delete a student record", command=self.delete_record)
        recordmenu.add_command(label="Update a student's record", command=self.update_record)
        menubar.add_cascade(label="☰ Menu", menu=recordmenu)
        self.config(menu=menubar)

        #Futuristic Fame Table
        table_outer = FuturisticFrame(self, bg="#191c24", highlightbackground="#2ee2ec", highlightcolor="#67fff6", highlightthickness=4)
        table_outer.pack(fill='both', expand=True, padx=28, pady=(20,10))

        #The Table's Output
        self.tree = ttk.Treeview(table_outer, columns=("Name", "Code", "Coursework", "Exam", "Percent", "Grade"), show='headings', height=12)
        self.tree.heading("Name", text="Student Name")
        self.tree.heading("Code", text="Student Number")
        self.tree.heading("Coursework", text="Coursework Total")
        self.tree.heading("Exam", text="Exam Mark")
        self.tree.heading("Percent", text="Overall %")
        self.tree.heading("Grade", text="Grade")
        for col in self.tree["columns"]:
            self.tree.column(col, width=138, anchor="center")
        self.tree.pack(fill='both', expand=True, padx=12, pady=10)

        #Futuristic Status Bar
        self.status_var = tk.StringVar(value="Ready")
        self.status = tk.Label(self, textvariable=self.status_var, bd=1, relief=tk.FLAT, anchor=tk.W, font=("Orbitron", 10, "bold"),
                               bg="#181929", fg="#45eaff")
        self.status.pack(fill=tk.X, side=tk.BOTTOM, pady=(2,0), padx=(2,2))

        self.show_all_records()

    def refresh_tree(self, student_list=None, show_summary=False):
        #This Removes all the rows
        for i in self.tree.get_children():
            self.tree.delete(i)
        student_list = student_list if student_list is not None else self.students
        total_p = 0
        for stu in student_list:
            self.tree.insert("", "end", values=stu.as_tuple())
            total_p += stu.percentage()
        if show_summary and student_list:
            avg_p = round(total_p / len(student_list), 2)
            self.status_var.set(f"✦ Students in class: {len(student_list)} | Average %: {avg_p}")
        else:
            self.status_var.set("Ready")

    def show_all_records(self):
        self.refresh_tree(show_summary=True)

    def show_individual_record(self):
        #You can find a student by using their id or name
        prompt = tk.simpledialog.askstring("Find Student", "Enter student's name or student number:")
        if prompt is None:
            return
        students = []
        if prompt.isdigit():
            students = [s for s in self.students if s.code == int(prompt)]
        else:
            students = [s for s in self.students if s.name.lower() == prompt.lower()]
        if students:
            self.refresh_tree(students)
            self.status_var.set(f"⧫ Record(s) found: {len(students)}")
        else:
            messagebox.showinfo("No Match", "No student found matching that name or number.")
            self.status_var.set("No student found.")

    def show_highest_record(self):
        if not self.students:
            return
        top = max(self.students, key=lambda s: s.total_mark())
        self.refresh_tree([top])
        self.status_var.set("⇧ Student with highest overall mark.")

    def show_lowest_record(self):
        if not self.students:
            return
        bottom = min(self.students, key=lambda s: s.total_mark())
        self.refresh_tree([bottom])
        self.status_var.set("⇩ Student with lowest overall mark.")

    def sort_records(self):
        if not self.students:
            return
        option = tk.simpledialog.askstring("Sort", "Enter 'asc' for ascending or 'desc' for descending sort by overall mark:")
        if option and option.lower() == "asc":
            sorted_students = sorted(self.students, key=lambda s: s.total_mark())
            self.refresh_tree(sorted_students, show_summary=True)
        elif option and option.lower() == "desc":
            sorted_students = sorted(self.students, key=lambda s: s.total_mark(), reverse=True)
            self.refresh_tree(sorted_students, show_summary=True)
        else:
            messagebox.showinfo("Sort", "Sort cancelled or invalid input.")

    def add_record(self):
        win = tk.Toplevel(self)
        win.title("Add Student Record")
        win.configure(bg="#23263a")
        labels = [
            "Student Number (1000-9999)",
            "Student Name",
            "Course 1 Mark (0-20)",
            "Course 2 Mark (0-20)",
            "Course 3 Mark (0-20)",
            "Exam Mark (0-100)"
        ]
        entries = []
        for i, text in enumerate(labels):
            FuturisticLabel(win, text=text).grid(row=i, column=0, sticky="e", pady=5, padx=10)
            e = FuturisticEntry(win)
            e.grid(row=i, column=1, pady=5, padx=2)
            entries.append(e)

        def save():
            try:
                code = int(entries[0].get())
                name = entries[1].get().strip()
                c1 = int(entries[2].get())
                c2 = int(entries[3].get())
                c3 = int(entries[4].get())
                exam = int(entries[5].get())
                if not (1000 <= code <= 9999):
                    raise ValueError
                if any(mark < 0 for mark in [c1, c2, c3, exam]) or c1 > 20 or c2 > 20 or c3 > 20 or exam > 100:
                    raise ValueError
                if any(s.code == code for s in self.students):
                    messagebox.showerror("Error", "Student number already exists!")
                    return
                new_student = Student(code, name, c1, c2, c3, exam)
                self.students.append(new_student)
                write_students(self.students)
                win.destroy()
                self.refresh_tree(show_summary=True)
                self.status_var.set("Student added.")
            except Exception:
                messagebox.showerror("Invalid Input", "Please enter valid data for all fields.")

        FuturisticButton(win, text="Add", command=save).grid(row=6, column=0, columnspan=2, pady=14, padx=10)

    def delete_record(self):
        prompt = tk.simpledialog.askstring("Delete Student", "Enter student name or student number to delete:")
        if prompt is None:
            return
        students = []
        if prompt.isdigit():
            students = [s for s in self.students if s.code == int(prompt)]
        else:
            students = [s for s in self.students if s.name.lower() == prompt.lower()]
        if students:
            # Confirm delete
            if messagebox.askyesno("Confirm Delete", f"Delete {len(students)} found record(s)?"):
                for s in students:
                    self.students.remove(s)
                write_students(self.students)
                self.refresh_tree(show_summary=True)
                self.status_var.set(f"{len(students)} student(s) deleted.")
        else:
            messagebox.showinfo("No Match", "No student found to delete.")
            self.status_var.set("No student deleted.")

    def update_record(self):
        prompt = tk.simpledialog.askstring("Update Student", "Enter student name or student number to update:")
        if prompt is None:
            return
        student = None
        if prompt.isdigit():
            res = [s for s in self.students if s.code == int(prompt)]
            student = res[0] if res else None
        else:
            res = [s for s in self.students if s.name.lower() == prompt.lower()]
            student = res[0] if res else None
        if not student:
            messagebox.showinfo("No Match", "No student found matching that name or number.")
            return

        win = tk.Toplevel(self)
        win.title("Update Student Record")
        win.configure(bg="#23263a")
        FuturisticLabel(win,
            text=f"Updating record for: {student.name} ({student.code})"
        ).grid(row=0, column=0, columnspan=2, pady=6, padx=10)

        labels = ["Course 1 Mark", "Course 2 Mark", "Course 3 Mark", "Exam Mark"]
        values = student.course_marks + [student.exam]
        entries = []

        for i, text in enumerate(labels):
            FuturisticLabel(win, text=text).grid(row=i+1, column=0, sticky="e", pady=4, padx=10)
            e = FuturisticEntry(win)
            e.insert(0, str(values[i]))
            e.grid(row=i+1, column=1, pady=4, padx=2)
            entries.append(e)

        def save_update():
            try:
                c1 = int(entries[0].get())
                c2 = int(entries[1].get())
                c3 = int(entries[2].get())
                exam = int(entries[3].get())
                if any(mark < 0 for mark in [c1, c2, c3, exam]) or c1 > 20 or c2 > 20 or c3 > 20 or exam > 100:
                    raise ValueError
                student.course_marks = [c1, c2, c3]
                student.exam = exam
                write_students(self.students)
                win.destroy()
                self.refresh_tree(show_summary=True)
                self.status_var.set("Student updated.")
            except Exception:
                messagebox.showerror("Invalid Input", "Please enter valid marks.")

        FuturisticButton(win, text="Update", command=save_update).grid(row=5, column=0, columnspan=2, pady=14, padx=10)


if __name__ == "__main__":
    app = StudentManagerApp()
    app.mainloop()