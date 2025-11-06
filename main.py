import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

class HostelManagementSystem:
    def _init_(self, root):
        self.root = root
        self.root.title("Hostel Query Management System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0e6ff')
        
        self.current_user = None
        self.current_frame = None
        
        self.setup_database()
        self.setup_styles()
        self.show_login_frame()
    
    def setup_database(self):
        self.conn = sqlite3.connect('hostel.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                full_name TEXT,
                role TEXT,
                room_number TEXT,
                fee_receipt TEXT,
                email TEXT,
                contact TEXT,
                position TEXT,
                approved INTEGER DEFAULT 0
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                category TEXT,
                title TEXT,
                description TEXT,
                room_number TEXT,
                date_submitted TEXT,
                status TEXT DEFAULT 'Pending',
                assigned_to INTEGER,
                votes INTEGER DEFAULT 0,
                FOREIGN KEY(student_id) REFERENCES users(id),
                FOREIGN KEY(assigned_to) REFERENCES users(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id INTEGER,
                student_id INTEGER,
                comment TEXT,
                date TEXT,
                FOREIGN KEY(query_id) REFERENCES queries(id),
                FOREIGN KEY(student_id) REFERENCES users(id)
            )
        ''')
        
        self.conn.commit()
        
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE role IN ('warden', 'authority')")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
                INSERT INTO users (username, password, full_name, role, position, approved)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('admin', 'admin123', 'System Administrator', 'authority', 'Head Authority', 1))
            self.conn.commit()
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('Purple.TFrame', background='#f0e6ff')
        self.style.configure('Black.TLabel', background='#f0e6ff', foreground='black', font=('Arial', 10))
        self.style.configure('Title.TLabel', background='#f0e6ff', foreground='#4b0082', font=('Arial', 16, 'bold'))
    
    # ⭐⭐ THIS IS WHERE BUTTON COLORS ARE DEFINED ⭐⭐
        self.style.configure('Dark.TButton', background='black', foreground='white', font=('Arial', 10))
        self.style.map('Dark.TButton', background=[('active', '#333333')])
    
        self.style.configure('Header.TFrame', background='#4b0082')
    
    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_login_frame(self):
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Purple.TFrame')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        header_frame = ttk.Frame(self.current_frame, style='Header.TFrame', height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = ttk.Label(header_frame, text="Hostel Query Management System", 
                               style='Title.TLabel', background='#4b0082', foreground='white')
        title_label.pack(pady=20)
        
        content_frame = ttk.Frame(self.current_frame, style='Purple.TFrame')
        content_frame.pack(fill='both', expand=True)
        
        login_frame = ttk.Frame(content_frame, style='Purple.TFrame')
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(login_frame, text="Login", style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(login_frame, text="Username:", style='Black.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.login_username = ttk.Entry(login_frame, width=30, font=('Arial', 10))
        self.login_username.grid(row=1, column=1, pady=5, padx=10)
        
        ttk.Label(login_frame, text="Password:", style='Black.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.login_password = ttk.Entry(login_frame, show='*', width=30, font=('Arial', 10))
        self.login_password.grid(row=2, column=1, pady=5, padx=10)
        
        ttk.Label(login_frame, text="Role:", style='Black.TLabel').grid(row=3, column=0, sticky='w', pady=5)
        self.login_role = ttk.Combobox(login_frame, values=['student', 'staff', 'warden', 'authority'], 
                                      state='readonly', width=28)
        self.login_role.set('student')
        self.login_role.grid(row=3, column=1, pady=5, padx=10)
        
        button_frame = ttk.Frame(login_frame, style='Purple.TFrame')
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Login", style='Purple.TButton', 
                  command=self.login).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Register", style='Purple.TButton', 
                  command=self.show_registration_choice).pack(side='left', padx=10)
        
        register_label = ttk.Label(login_frame, text="Don't have an account? Register here!", 
                 style='Black.TLabel', cursor='hand2')
        register_label.grid(row=5, column=0, columnspan=2, pady=10)
        register_label.bind('<Button-1>', lambda e: self.show_registration_choice())
    
    def show_registration_choice(self):
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Purple.TFrame')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        header_frame = ttk.Frame(self.current_frame, style='Header.TFrame', height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = ttk.Label(header_frame, text="Select Registration Type", 
                               style='Title.TLabel', background='#4b0082', foreground='white')
        title_label.pack(pady=20)
        
        content_frame = ttk.Frame(self.current_frame, style='Purple.TFrame')
        content_frame.pack(fill='both', expand=True)
        
        choice_frame = ttk.Frame(content_frame, style='Purple.TFrame')
        choice_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Button(choice_frame, text="Student Registration", style='Purple.TButton',
                  command=self.show_student_registration, width=25).pack(pady=15)
        ttk.Button(choice_frame, text="Staff Registration", style='Purple.TButton',
                  command=self.show_staff_registration, width=25).pack(pady=15)
        ttk.Button(choice_frame, text="Warden/Authority Registration", style='Purple.TButton',
                  command=self.show_warden_registration, width=25).pack(pady=15)
        ttk.Button(choice_frame, text="Back to Login", style='Purple.TButton',
                  command=self.show_login_frame, width=25).pack(pady=15)
    
    def show_student_registration(self):
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Purple.TFrame')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        header_frame = ttk.Frame(self.current_frame, style='Header.TFrame', height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = ttk.Label(header_frame, text="Student Registration", 
                               style='Title.TLabel', background='#4b0082', foreground='white')
        title_label.pack(pady=20)
        
        content_frame = ttk.Frame(self.current_frame, style='Purple.TFrame')
        content_frame.pack(fill='both', expand=True)
        
        form_frame = ttk.Frame(content_frame, style='Purple.TFrame')
        form_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        fields = [
            ("Full Name:", "full_name"),
            ("Room Number:", "room_number"),
            ("Fee Receipt No.:", "fee_receipt"),
            ("Email:", "email"),
            ("Username:", "username"),
            ("Password:", "password")
        ]
        
        self.reg_entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(form_frame, text=label, style='Black.TLabel').grid(row=i, column=0, sticky='w', pady=8)
            entry = ttk.Entry(form_frame, width=30, font=('Arial', 10))
            if field == 'password':
                entry.config(show='*')
            entry.grid(row=i, column=1, pady=8, padx=10)
            self.reg_entries[field] = entry
        
        button_frame = ttk.Frame(form_frame, style='Purple.TFrame')
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Register", style='Purple.TButton',
                  command=self.register_student).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Back", style='Purple.TButton',
                  command=self.show_registration_choice).pack(side='left', padx=10)
    
    def show_staff_registration(self):
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Purple.TFrame')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        header_frame = ttk.Frame(self.current_frame, style='Header.TFrame', height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = ttk.Label(header_frame, text="Staff Registration", 
                               style='Title.TLabel', background='#4b0082', foreground='white')
        title_label.pack(pady=20)
        
        content_frame = ttk.Frame(self.current_frame, style='Purple.TFrame')
        content_frame.pack(fill='both', expand=True)
        
        form_frame = ttk.Frame(content_frame, style='Purple.TFrame')
        form_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        fields = [
            ("Full Name:", "full_name"),
            ("Position:", "position"),
            ("Official Contact:", "contact"),
            ("Email:", "email"),
            ("Username:", "username"),
            ("Password:", "password")
        ]
        
        self.staff_entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(form_frame, text=label, style='Black.TLabel').grid(row=i, column=0, sticky='w', pady=8)
            entry = ttk.Entry(form_frame, width=30, font=('Arial', 10))
            if field == 'password':
                entry.config(show='*')
            entry.grid(row=i, column=1, pady=8, padx=10)
            self.staff_entries[field] = entry
        
        button_frame = ttk.Frame(form_frame, style='Purple.TFrame')
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Register", style='Purple.TButton',
                  command=lambda: self.register_non_student('staff')).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Back", style='Purple.TButton',
                  command=self.show_registration_choice).pack(side='left', padx=10)
    
    def show_warden_registration(self):
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Purple.TFrame')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        header_frame = ttk.Frame(self.current_frame, style='Header.TFrame', height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = ttk.Label(header_frame, text="Warden/Authority Registration", 
                               style='Title.TLabel', background='#4b0082', foreground='white')
        title_label.pack(pady=20)
        
        content_frame = ttk.Frame(self.current_frame, style='Purple.TFrame')
        content_frame.pack(fill='both', expand=True)
        
        form_frame = ttk.Frame(content_frame, style='Purple.TFrame')
        form_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(form_frame, text="Role:", style='Black.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.warden_role = ttk.Combobox(form_frame, values=['warden', 'authority'], state='readonly', width=27)
        self.warden_role.set('warden')
        self.warden_role.grid(row=0, column=1, pady=8, padx=10)
        
        fields = [
            ("Full Name:", "full_name"),
            ("Position:", "position"),
            ("Official Contact:", "contact"),
            ("Email:", "email"),
            ("Username:", "username"),
            ("Password:", "password")
        ]
        
        self.warden_entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(form_frame, text=label, style='Black.TLabel').grid(row=i+1, column=0, sticky='w', pady=8)
            entry = ttk.Entry(form_frame, width=30, font=('Arial', 10))
            if field == 'password':
                entry.config(show='*')
            entry.grid(row=i+1, column=1, pady=8, padx=10)
            self.warden_entries[field] = entry
        
        button_frame = ttk.Frame(form_frame, style='Purple.TFrame')
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Register", style='Purple.TButton',
                  command=self.register_warden).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Back", style='Purple.TButton',
                  command=self.show_registration_choice).pack(side='left', padx=10)
    
    def register_student(self):
        data = {field: entry.get() for field, entry in self.reg_entries.items()}
        
        if not all(data.values()):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password, full_name, room_number, fee_receipt, email, role, approved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data['username'], data['password'], data['full_name'], data['room_number'], 
                  data['fee_receipt'], data['email'], 'student', 0))
            self.conn.commit()
            messagebox.showinfo("Success", "Your application has been sent for approval by the Warden.")
            self.show_login_frame()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
    
    def register_non_student(self, role):
        data = {field: entry.get() for field, entry in self.staff_entries.items()}
        
        if not all(data.values()):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password, full_name, position, contact, email, role, approved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data['username'], data['password'], data['full_name'], data['position'],
                  data['contact'], data['email'], role, 1))
            self.conn.commit()
            messagebox.showinfo("Success", f"{role.capitalize()} registration successful!")
            self.show_login_frame()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
    
    def register_warden(self):
        role = self.warden_role.get()
        data = {field: entry.get() for field, entry in self.warden_entries.items()}
        
        if not all(data.values()):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password, full_name, position, contact, email, role, approved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data['username'], data['password'], data['full_name'], data['position'],
                  data['contact'], data['email'], role, 1))
            self.conn.commit()
            messagebox.showinfo("Success", f"{role.capitalize()} registration successful!")
            self.show_login_frame()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
    
    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        role = self.login_role.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return
        
        self.cursor.execute('''
            SELECT id, username, role, full_name, approved FROM users 
            WHERE username = ? AND password = ? AND role = ?
        ''', (username, password, role))
        
        user = self.cursor.fetchone()
        
        if user:
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'role': user[2],
                'full_name': user[3],
                'approved': user[4]
            }
            
            if role == 'student' and self.current_user['approved'] == 0:
                messagebox.showinfo("Pending", "Your application is still pending approval.")
                return
            elif role == 'student' and self.current_user['approved'] == -1:
                messagebox.showerror("Rejected", "Your application has been rejected.")
                return
            
            if role == 'student':
                self.show_student_dashboard()
            elif role == 'staff':
                self.show_staff_dashboard()
            elif role in ['warden', 'authority']:
                self.show_warden_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    
    def show_student_dashboard(self):
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Purple.TFrame')
        self.current_frame.pack(fill='both', expand=True)
        
        header_frame = ttk.Frame(self.current_frame, style='Header.TFrame', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        ttk.Label(header_frame, text=f"Welcome, {self.current_user['full_name']}", 
                 style='Title.TLabel', background='#4b0082', foreground='white').pack(side='left', padx=20, pady=20)
        
        ttk.Button(header_frame, text="Logout", style='Purple.TButton',
                  command=self.logout).pack(side='right', padx=20, pady=20)
        
        nav_frame = ttk.Frame(self.current_frame, style='Purple.TFrame')
        nav_frame.pack(fill='x', pady=10)
        
        categories = ['Top 5', 'Water', 'Electricity', 'Carpenter', 'Mess', 'Other', 'My Queries']
        for i, category in enumerate(categories):
            ttk.Button(nav_frame, text=category, style='Purple.TButton',
                      command=lambda c=category: self.show_queries_by_category(c)).pack(side='left', padx=5)
        
        ttk.Button(nav_frame, text="Add Query", style='Purple.TButton',
                  command=self.show_add_query).pack(side='right', padx=5)
        
        self.content_frame = ttk.Frame(self.current_frame, style='Purple.TFrame')
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.show_queries_by_category('Top 5')
    
    def show_queries_by_category(self, category):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if category == 'My Queries':
            self.cursor.execute('''
                SELECT q.id, q.title, q.votes, q.status, q.date_submitted, u.full_name 
                FROM queries q 
                LEFT JOIN users u ON q.assigned_to = u.id 
                WHERE q.student_id = ? 
                ORDER BY q.date_submitted DESC
            ''', (self.current_user['id'],))
        elif category == 'Top 5':
            self.cursor.execute('''
                SELECT q.id, q.title, q.votes, q.status, q.date_submitted, u.full_name 
                FROM queries q 
                LEFT JOIN users u ON q.assigned_to = u.id 
                ORDER BY q.votes DESC 
                LIMIT 5
            ''')
        else:
            self.cursor.execute('''
                SELECT q.id, q.title, q.votes, q.status, q.date_submitted, u.full_name 
                FROM queries q 
                LEFT JOIN users u ON q.assigned_to = u.id 
                WHERE q.category = ? 
                ORDER BY q.votes DESC
            ''', (category,))
        
        queries = self.cursor.fetchall()
        
        if not queries:
            ttk.Label(self.content_frame, text="No queries found", style='Black.TLabel').pack(pady=20)
            return
        
        canvas = tk.Canvas(self.content_frame, bg='#f0e6ff')
        scrollbar = ttk.Scrollbar(self.content_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Purple.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, query in enumerate(queries):
            query_frame = ttk.Frame(scrollable_frame, style='Purple.TFrame', relief='raised', padding=10)
            query_frame.pack(fill='x', pady=5, padx=10)
            
            ttk.Label(query_frame, text=query[1], style='Title.TLabel').grid(row=0, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Votes: {query[2]}", style='Black.TLabel').grid(row=1, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Status: {query[3]}", style='Black.TLabel').grid(row=2, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Date: {query[4]}", style='Black.TLabel').grid(row=3, column=0, sticky='w')
            
            if query[5]:
                ttk.Label(query_frame, text=f"Assigned to: {query[5]}", style='Black.TLabel').grid(row=4, column=0, sticky='w')
            
            button_frame = ttk.Frame(query_frame, style='Purple.TFrame')
            button_frame.grid(row=0, column=1, rowspan=5, sticky='e')
            
            if category != 'My Queries':
                ttk.Button(button_frame, text="Vote", style='Purple.TButton',
                          command=lambda qid=query[0]: self.vote_query(qid)).pack(pady=2)
            
            ttk.Button(button_frame, text="View Details", style='Purple.TButton',
                      command=lambda qid=query[0]: self.show_query_details(qid)).pack(pady=2)
            
            if category == 'My Queries':
                ttk.Button(button_frame, text="Add Feedback", style='Purple.TButton',
                          command=lambda qid=query[0]: self.show_feedback_form(qid)).pack(pady=2)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def show_add_query(self):
        self.add_query_window = tk.Toplevel(self.root)
        self.add_query_window.title("Add New Query")
        self.add_query_window.geometry("500x400")
        self.add_query_window.configure(bg='#f0e6ff')
        
        ttk.Label(self.add_query_window, text="Add New Query", style='Title.TLabel').pack(pady=20)
        
        form_frame = ttk.Frame(self.add_query_window, style='Purple.TFrame')
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        ttk.Label(form_frame, text="Category:", style='Black.TLabel').grid(row=0, column=0, sticky='w', pady=8)
        self.query_category = ttk.Combobox(form_frame, values=['Water', 'Electricity', 'Carpenter', 'Mess', 'Other'], 
                                          state='readonly', width=27)
        self.query_category.set('Water')
        self.query_category.grid(row=0, column=1, pady=8, padx=10)
        
        ttk.Label(form_frame, text="Title:", style='Black.TLabel').grid(row=1, column=0, sticky='w', pady=8)
        self.query_title = ttk.Entry(form_frame, width=30, font=('Arial', 10))
        self.query_title.grid(row=1, column=1, pady=8, padx=10)
        
        ttk.Label(form_frame, text="Description:", style='Black.TLabel').grid(row=2, column=0, sticky='nw', pady=8)
        self.query_description = tk.Text(form_frame, width=30, height=8, font=('Arial', 10))
        self.query_description.grid(row=2, column=1, pady=8, padx=10)
        
        button_frame = ttk.Frame(form_frame, style='Purple.TFrame')
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Submit", style='Purple.TButton',
                  command=self.submit_query).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cancel", style='Purple.TButton',
                  command=self.add_query_window.destroy).pack(side='left', padx=10)
    
    def submit_query(self):
        category = self.query_category.get()
        title = self.query_title.get()
        description = self.query_description.get('1.0', 'end-1c')
        
        if not title or not description:
            messagebox.showerror("Error", "Title and description are required!")
            return
        
        self.cursor.execute('''
            INSERT INTO queries (student_id, category, title, description, room_number, date_submitted)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.current_user['id'], category, title, description, 
              self.get_user_room(), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        self.conn.commit()
        messagebox.showinfo("Success", "Query submitted successfully!")
        self.add_query_window.destroy()
        self.show_queries_by_category('My Queries')
    
    def get_user_room(self):
        self.cursor.execute('SELECT room_number FROM users WHERE id = ?', (self.current_user['id'],))
        result = self.cursor.fetchone()
        return result[0] if result else "N/A"
    
    def vote_query(self, query_id):
        self.cursor.execute('UPDATE queries SET votes = votes + 1 WHERE id = ?', (query_id,))
        self.conn.commit()
        messagebox.showinfo("Success", "Vote recorded!")
        self.show_queries_by_category('Top 5')
    
    def show_query_details(self, query_id):
        self.cursor.execute('''
            SELECT q.*, u.full_name as student_name, u2.full_name as assigned_staff
            FROM queries q 
            LEFT JOIN users u ON q.student_id = u.id 
            LEFT JOIN users u2 ON q.assigned_to = u2.id 
            WHERE q.id = ?
        ''', (query_id,))
        
        query = self.cursor.fetchone()
        
        if not query:
            return
        
        details_window = tk.Toplevel(self.root)
        details_window.title("Query Details")
        details_window.geometry("600x500")
        details_window.configure(bg='#f0e6ff')
        
        ttk.Label(details_window, text="Query Details", style='Title.TLabel').pack(pady=20)
        
        details_frame = ttk.Frame(details_window, style='Purple.TFrame')
        details_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        fields = [
            ("Title:", query[3]),
            ("Category:", query[2]),
            ("Description:", query[4]),
            ("Room Number:", query[5]),
            ("Date Submitted:", query[6]),
            ("Status:", query[7]),
            ("Votes:", query[9]),
            ("Submitted by:", query[10]),
            ("Assigned to:", query[11] or "Not assigned")
        ]
        
        for i, (label, value) in enumerate(fields):
            ttk.Label(details_frame, text=label, style='Black.TLabel', font=('Arial', 10, 'bold')).grid(row=i, column=0, sticky='w', pady=5)
            ttk.Label(details_frame, text=str(value), style='Black.TLabel').grid(row=i, column=1, sticky='w', pady=5, padx=10)
    
    def show_feedback_form(self, query_id):
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("Add Feedback")
        feedback_window.geometry("500x300")
        feedback_window.configure(bg='#f0e6ff')
        
        ttk.Label(feedback_window, text="Add Feedback", style='Title.TLabel').pack(pady=20)
        
        form_frame = ttk.Frame(feedback_window, style='Purple.TFrame')
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        ttk.Label(form_frame, text="Comment:", style='Black.TLabel').pack(anchor='w')
        feedback_text = tk.Text(form_frame, width=50, height=10, font=('Arial', 10))
        feedback_text.pack(pady=10, fill='both', expand=True)
        
        button_frame = ttk.Frame(form_frame, style='Purple.TFrame')
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Submit", style='Purple.TButton',
                  command=lambda: self.submit_feedback(query_id, feedback_text.get('1.0', 'end-1c'), feedback_window)).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cancel", style='Purple.TButton',
                  command=feedback_window.destroy).pack(side='left', padx=10)
    
    def submit_feedback(self, query_id, comment, window):
        if not comment:
            messagebox.showerror("Error", "Please enter a comment!")
            return
        
        self.cursor.execute('''
            INSERT INTO feedback (query_id, student_id, comment, date)
            VALUES (?, ?, ?, ?)
        ''', (query_id, self.current_user['id'], comment, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        self.conn.commit()
        messagebox.showinfo("Success", "Feedback submitted successfully!")
        window.destroy()
    
    def show_staff_dashboard(self):
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Purple.TFrame')
        self.current_frame.pack(fill='both', expand=True)
        
        header_frame = ttk.Frame(self.current_frame, style='Header.TFrame', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        ttk.Label(header_frame, text=f"Staff Dashboard - {self.current_user['full_name']}", 
                 style='Title.TLabel', background='#4b0082', foreground='white').pack(side='left', padx=20, pady=20)
        
        ttk.Button(header_frame, text="Logout", style='Purple.TButton',
                  command=self.logout).pack(side='right', padx=20, pady=20)
        
        nav_frame = ttk.Frame(self.current_frame, style='Purple.TFrame')
        nav_frame.pack(fill='x', pady=10)
        
        categories = ['All', 'Water', 'Electricity', 'Carpenter', 'Mess', 'Other', 'Assigned to Me']
        for category in categories:
            ttk.Button(nav_frame, text=category, style='Purple.TButton',
                      command=lambda c=category: self.show_staff_queries(c)).pack(side='left', padx=5)
        
        self.content_frame = ttk.Frame(self.current_frame, style='Purple.TFrame')
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.show_staff_queries('Assigned to Me')
    
    def show_staff_queries(self, category):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if category == 'Assigned to Me':
            self.cursor.execute('''
                SELECT q.id, q.title, q.description, q.room_number, q.date_submitted, q.status, q.votes, u.full_name
                FROM queries q 
                LEFT JOIN users u ON q.student_id = u.id 
                WHERE q.assigned_to = ?
                ORDER BY q.date_submitted DESC
            ''', (self.current_user['id'],))
        elif category == 'All':
            self.cursor.execute('''
                SELECT q.id, q.title, q.description, q.room_number, q.date_submitted, q.status, q.votes, u.full_name
                FROM queries q 
                LEFT JOIN users u ON q.student_id = u.id 
                ORDER BY q.date_submitted DESC
            ''')
        else:
            self.cursor.execute('''
                SELECT q.id, q.title, q.description, q.room_number, q.date_submitted, q.status, q.votes, u.full_name
                FROM queries q 
                LEFT JOIN users u ON q.student_id = u.id 
                WHERE q.category = ?
                ORDER BY q.date_submitted DESC
            ''', (category,))
        
        queries = self.cursor.fetchall()
        
        if not queries:
            ttk.Label(self.content_frame, text="No queries found", style='Black.TLabel').pack(pady=20)
            return
        
        canvas = tk.Canvas(self.content_frame, bg='#f0e6ff')
        scrollbar = ttk.Scrollbar(self.content_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Purple.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, query in enumerate(queries):
            query_frame = ttk.Frame(scrollable_frame, style='Purple.TFrame', relief='raised', padding=10)
            query_frame.pack(fill='x', pady=5, padx=10)
            
            ttk.Label(query_frame, text=query[1], style='Title.TLabel').grid(row=0, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Room: {query[3]}", style='Black.TLabel').grid(row=1, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Status: {query[5]}", style='Black.TLabel').grid(row=2, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Votes: {query[6]}", style='Black.TLabel').grid(row=3, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Submitted by: {query[7]}", style='Black.TLabel').grid(row=4, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Date: {query[4]}", style='Black.TLabel').grid(row=5, column=0, sticky='w')
            
            desc_label = ttk.Label(query_frame, text=f"Description: {query[2]}", style='Black.TLabel', wraplength=400)
            desc_label.grid(row=6, column=0, columnspan=2, sticky='w', pady=5)
            
            button_frame = ttk.Frame(query_frame, style='Purple.TFrame')
            button_frame.grid(row=0, column=1, rowspan=6, sticky='e')
            
            if category != 'Assigned to Me':
                ttk.Button(button_frame, text="Assign to Me", style='Purple.TButton',
                          command=lambda qid=query[0]: self.assign_query_to_me(qid)).pack(pady=2)
            
            ttk.Button(button_frame, text="Update Status", style='Purple.TButton',
                      command=lambda qid=query[0]: self.update_query_status(qid)).pack(pady=2)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def assign_query_to_me(self, query_id):
        self.cursor.execute('UPDATE queries SET assigned_to = ? WHERE id = ?', 
                           (self.current_user['id'], query_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Query assigned to you!")
        self.show_staff_queries('Assigned to Me')
    
    def update_query_status(self, query_id):
        status_window = tk.Toplevel(self.root)
        status_window.title("Update Query Status")
        status_window.geometry("300x200")
        status_window.configure(bg='#f0e6ff')
        
        ttk.Label(status_window, text="Update Status", style='Title.TLabel').pack(pady=20)
        
        form_frame = ttk.Frame(status_window, style='Purple.TFrame')
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        ttk.Label(form_frame, text="New Status:", style='Black.TLabel').pack(anchor='w')
        status_var = tk.StringVar(value="In Process")
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, 
                                   values=['In Process', 'Completed'], state='readonly')
        status_combo.pack(fill='x', pady=10)
        
        button_frame = ttk.Frame(form_frame, style='Purple.TFrame')
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Update", style='Purple.TButton',
                  command=lambda: self.submit_status_update(query_id, status_var.get(), status_window)).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cancel", style='Purple.TButton',
                  command=status_window.destroy).pack(side='left', padx=10)
    
    def submit_status_update(self, query_id, status, window):
        self.cursor.execute('UPDATE queries SET status = ? WHERE id = ?', (status, query_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Status updated successfully!")
        window.destroy()
        self.show_staff_queries('Assigned to Me')
    
    def show_warden_dashboard(self):
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Purple.TFrame')
        self.current_frame.pack(fill='both', expand=True)
        
        header_frame = ttk.Frame(self.current_frame, style='Header.TFrame', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        ttk.Label(header_frame, text=f"{self.current_user['role'].capitalize()} Dashboard - {self.current_user['full_name']}", 
                 style='Title.TLabel', background='#4b0082', foreground='white').pack(side='left', padx=20, pady=20)
        
        ttk.Button(header_frame, text="Logout", style='Purple.TButton',
                  command=self.logout).pack(side='right', padx=20, pady=20)
        
        nav_frame = ttk.Frame(self.current_frame, style='Purple.TFrame')
        nav_frame.pack(fill='x', pady=10)
        
        ttk.Button(nav_frame, text="Approve Applications", style='Purple.TButton',
                  command=self.show_approval_page).pack(side='left', padx=5)
        ttk.Button(nav_frame, text="Manage Queries", style='Purple.TButton',
                  command=self.show_warden_queries).pack(side='left', padx=5)
        ttk.Button(nav_frame, text="Top 5 Queries", style='Purple.TButton',
                  command=self.show_top_queries).pack(side='left', padx=5)
        
        self.content_frame = ttk.Frame(self.current_frame, style='Purple.TFrame')
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.show_approval_page()
    
    def show_approval_page(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(self.content_frame, text="Pending Student Applications", 
                 style='Title.TLabel').pack(pady=10)
        
        self.cursor.execute('''
            SELECT id, username, full_name, room_number, fee_receipt, email 
            FROM users 
            WHERE role = 'student' AND approved = 0
        ''')
        
        applications = self.cursor.fetchall()
        
        if not applications:
            ttk.Label(self.content_frame, text="No pending applications", 
                     style='Black.TLabel').pack(pady=20)
            return
        
        canvas = tk.Canvas(self.content_frame, bg='#f0e6ff')
        scrollbar = ttk.Scrollbar(self.content_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Purple.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, app in enumerate(applications):
            app_frame = ttk.Frame(scrollable_frame, style='Purple.TFrame', relief='raised', padding=10)
            app_frame.pack(fill='x', pady=5, padx=10)
            
            ttk.Label(app_frame, text=f"Name: {app[2]}", style='Black.TLabel').grid(row=0, column=0, sticky='w')
            ttk.Label(app_frame, text=f"Username: {app[1]}", style='Black.TLabel').grid(row=1, column=0, sticky='w')
            ttk.Label(app_frame, text=f"Room: {app[3]}", style='Black.TLabel').grid(row=2, column=0, sticky='w')
            ttk.Label(app_frame, text=f"Fee Receipt: {app[4]}", style='Black.TLabel').grid(row=3, column=0, sticky='w')
            ttk.Label(app_frame, text=f"Email: {app[5]}", style='Black.TLabel').grid(row=4, column=0, sticky='w')
            
            button_frame = ttk.Frame(app_frame, style='Purple.TFrame')
            button_frame.grid(row=0, column=1, rowspan=5, sticky='e')
            
            ttk.Button(button_frame, text="Approve", style='Purple.TButton',
                      command=lambda uid=app[0]: self.approve_application(uid, 1)).pack(pady=2)
            ttk.Button(button_frame, text="Reject", style='Purple.TButton',
                      command=lambda uid=app[0]: self.approve_application(uid, -1)).pack(pady=2)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def approve_application(self, user_id, status):
        self.cursor.execute('UPDATE users SET approved = ? WHERE id = ?', (status, user_id))
        self.conn.commit()
        
        action = "approved" if status == 1 else "rejected"
        messagebox.showinfo("Success", f"Application {action} successfully!")
        self.show_approval_page()
    
    def show_warden_queries(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(self.content_frame, text="All Queries", style='Title.TLabel').pack(pady=10)
        
        nav_frame = ttk.Frame(self.content_frame, style='Purple.TFrame')
        nav_frame.pack(fill='x', pady=10)
        
        categories = ['All', 'Water', 'Electricity', 'Carpenter', 'Mess', 'Other']
        for category in categories:
            ttk.Button(nav_frame, text=category, style='Purple.TButton',
                      command=lambda c=category: self.show_filtered_queries(c)).pack(side='left', padx=2)
        
        self.queries_content = ttk.Frame(self.content_frame, style='Purple.TFrame')
        self.queries_content.pack(fill='both', expand=True)
        
        self.show_filtered_queries('All')
    
    def show_filtered_queries(self, category):
        for widget in self.queries_content.winfo_children():
            widget.destroy()
        
        if category == 'All':
            self.cursor.execute('''
                SELECT q.id, q.title, q.category, q.description, q.room_number, 
                       q.date_submitted, q.status, q.votes, q.assigned_to,
                       u.full_name as student_name, u2.full_name as staff_name
                FROM queries q 
                LEFT JOIN users u ON q.student_id = u.id 
                LEFT JOIN users u2 ON q.assigned_to = u2.id 
                ORDER BY q.date_submitted DESC
            ''')
        else:
            self.cursor.execute('''
                SELECT q.id, q.title, q.category, q.description, q.room_number, 
                       q.date_submitted, q.status, q.votes, q.assigned_to,
                       u.full_name as student_name, u2.full_name as staff_name
                FROM queries q 
                LEFT JOIN users u ON q.student_id = u.id 
                LEFT JOIN users u2 ON q.assigned_to = u2.id 
                WHERE q.category = ?
                ORDER BY q.date_submitted DESC
            ''', (category,))
        
        queries = self.cursor.fetchall()
        
        if not queries:
            ttk.Label(self.queries_content, text="No queries found", style='Black.TLabel').pack(pady=20)
            return
        
        canvas = tk.Canvas(self.queries_content, bg='#f0e6ff')
        scrollbar = ttk.Scrollbar(self.queries_content, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Purple.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, query in enumerate(queries):
            query_frame = ttk.Frame(scrollable_frame, style='Purple.TFrame', relief='raised', padding=10)
            query_frame.pack(fill='x', pady=5, padx=10)
            
            ttk.Label(query_frame, text=query[1], style='Title.TLabel').grid(row=0, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Category: {query[2]}", style='Black.TLabel').grid(row=1, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Room: {query[4]}", style='Black.TLabel').grid(row=2, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Status: {query[6]}", style='Black.TLabel').grid(row=3, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Votes: {query[7]}", style='Black.TLabel').grid(row=4, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Submitted by: {query[9]}", style='Black.TLabel').grid(row=5, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Assigned to: {query[10] or 'Not assigned'}", style='Black.TLabel').grid(row=6, column=0, sticky='w')
            
            button_frame = ttk.Frame(query_frame, style='Purple.TFrame')
            button_frame.grid(row=0, column=1, rowspan=7, sticky='e')
            
            ttk.Button(button_frame, text="Assign Staff", style='Purple.TButton',
                      command=lambda qid=query[0]: self.assign_staff(qid)).pack(pady=2)
            ttk.Button(button_frame, text="Update Status", style='Purple.TButton',
                      command=lambda qid=query[0]: self.warden_update_status(qid)).pack(pady=2)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def assign_staff(self, query_id):
        self.cursor.execute('SELECT id, full_name FROM users WHERE role = "staff"')
        staff_members = self.cursor.fetchall()
        
        if not staff_members:
            messagebox.showerror("Error", "No staff members available!")
            return
        
        assign_window = tk.Toplevel(self.root)
        assign_window.title("Assign Staff")
        assign_window.geometry("300x200")
        assign_window.configure(bg='#f0e6ff')
        
        ttk.Label(assign_window, text="Select Staff Member", style='Title.TLabel').pack(pady=20)
        
        form_frame = ttk.Frame(assign_window, style='Purple.TFrame')
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        staff_var = tk.StringVar()
        staff_combo = ttk.Combobox(form_frame, textvariable=staff_var, state='readonly')
        staff_combo['values'] = [f"{staff[0]}: {staff[1]}" for staff in staff_members]
        staff_combo.set(staff_combo['values'][0] if staff_combo['values'] else "")
        staff_combo.pack(fill='x', pady=10)
        
        button_frame = ttk.Frame(form_frame, style='Purple.TFrame')
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Assign", style='Purple.TButton',
                  command=lambda: self.submit_staff_assignment(query_id, staff_var.get(), assign_window)).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cancel", style='Purple.TButton',
                  command=assign_window.destroy).pack(side='left', padx=10)
    
    def submit_staff_assignment(self, query_id, staff_selection, window):
        if not staff_selection:
            messagebox.showerror("Error", "Please select a staff member!")
            return
        
        staff_id = int(staff_selection.split(':')[0])
        self.cursor.execute('UPDATE queries SET assigned_to = ? WHERE id = ?', (staff_id, query_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Staff assigned successfully!")
        window.destroy()
        self.show_warden_queries()
    
    def warden_update_status(self, query_id):
        status_window = tk.Toplevel(self.root)
        status_window.title("Update Query Status")
        status_window.geometry("300x200")
        status_window.configure(bg='#f0e6ff')
        
        ttk.Label(status_window, text="Update Status", style='Title.TLabel').pack(pady=20)
        
        form_frame = ttk.Frame(status_window, style='Purple.TFrame')
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        ttk.Label(form_frame, text="New Status:", style='Black.TLabel').pack(anchor='w')
        status_var = tk.StringVar(value="Pending")
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, 
                                   values=['Pending', 'In Process', 'Completed', 'Rejected'], state='readonly')
        status_combo.pack(fill='x', pady=10)
        
        button_frame = ttk.Frame(form_frame, style='Purple.TFrame')
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Update", style='Purple.TButton',
                  command=lambda: self.submit_warden_status_update(query_id, status_var.get(), status_window)).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cancel", style='Purple.TButton',
                  command=status_window.destroy).pack(side='left', padx=10)
    
    def submit_warden_status_update(self, query_id, status, window):
        self.cursor.execute('UPDATE queries SET status = ? WHERE id = ?', (status, query_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Status updated successfully!")
        window.destroy()
        self.show_warden_queries()
    
    def show_top_queries(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(self.content_frame, text="Top 5 Queries by Votes", style='Title.TLabel').pack(pady=10)
        
        self.cursor.execute('''
            SELECT q.id, q.title, q.category, q.description, q.room_number, 
                   q.date_submitted, q.status, q.votes, 
                   u.full_name as student_name, u2.full_name as staff_name
            FROM queries q 
            LEFT JOIN users u ON q.student_id = u.id 
            LEFT JOIN users u2 ON q.assigned_to = u2.id 
            ORDER BY q.votes DESC 
            LIMIT 5
        ''')
        
        queries = self.cursor.fetchall()
        
        if not queries:
            ttk.Label(self.content_frame, text="No queries found", style='Black.TLabel').pack(pady=20)
            return
        
        canvas = tk.Canvas(self.content_frame, bg='#f0e6ff')
        scrollbar = ttk.Scrollbar(self.content_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Purple.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, query in enumerate(queries):
            query_frame = ttk.Frame(scrollable_frame, style='Purple.TFrame', relief='raised', padding=10)
            query_frame.pack(fill='x', pady=5, padx=10)
            
            ttk.Label(query_frame, text=f"#{i+1}: {query[1]}", style='Title.TLabel').grid(row=0, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Category: {query[2]}", style='Black.TLabel').grid(row=1, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Votes: {query[7]}", style='Black.TLabel', 
                     font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Status: {query[6]}", style='Black.TLabel').grid(row=3, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Submitted by: {query[8]}", style='Black.TLabel').grid(row=4, column=0, sticky='w')
            ttk.Label(query_frame, text=f"Assigned to: {query[9] or 'Not assigned'}", style='Black.TLabel').grid(row=5, column=0, sticky='w')
            
            desc_label = ttk.Label(query_frame, text=f"Description: {query[3]}", style='Black.TLabel', wraplength=400)
            desc_label.grid(row=6, column=0, columnspan=2, sticky='w', pady=5)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')   
    def logout(self):
        self.current_user = None
        self.show_login_frame()
def main():
    root = tk.Tk()
    app = HostelManagementSystem(root)
    root.mainloop()

if _name_ == "_main_":
    main()