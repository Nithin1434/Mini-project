from tkinter import *
from tkinter import messagebox
import ast
import os

root = Tk()
root.title('Login')
root.geometry('925x500+200+100')
root.configure(bg="#fff")
root.resizable(False, False)

def signin():
    username = user.get()
    password = code.get()

    try:
        with open('datasheet.txt', 'r') as file:
            d = file.read()
            r = ast.literal_eval(d)
    except (FileNotFoundError, SyntaxError):
        messagebox.showerror("Error", "User data file not found or corrupted.")
        return

    if username in r.keys() and password == r[username]:
        # Close the main login window
        root.withdraw()

        # Open the device suggestion interface
        def device_suggestion_system():
            import tkinter as tk
            from tkinter import ttk, messagebox
            import openai

            # OpenAI API configuration
            openai.api_type = "open_ai"
            openai.api_base = "http://127.0.0.1:1234/v1"
            openai.api_key = "NULL"

            def update_button_state():
                """Enable the 'Get Suggestions' button if all fields are selected."""
                if all([category_var.get(), price_range_var.get(), brand_var.get(), storage_var.get(),
                        processor_var.get(), speciality_var.get(), battery_var.get()]):
                    get_suggestions_button.config(state="normal")
                else:
                    get_suggestions_button.config(state="disabled")

            def get_suggestions():
                """Fetch user inputs, store in a dictionary, and prepare API prompt."""
                # Collect user inputs
                user_choices = {
                    "Category": category_var.get(),
                    "Price Range": price_range_var.get(),
                    "Brand": brand_var.get(),
                    "Speciality": speciality_var.get(),
                    "Internal Storage": storage_var.get(),
                    "Battery": battery_var.get(),
                    "Processor": processor_var.get(),
                }
                prompt = (
                    f"Suggest only Top 3 devices based on the following preferences: give correct matched devices \n"
                    f"Category: {user_choices['Category']}\n"
                    f"Price Range: {user_choices['Price Range']}\n"
                    f"Brand: {user_choices['Brand']}\n"
                    f"Speciality: {user_choices['Speciality']}\n"
                    f"Internal Storage: {user_choices['Internal Storage']}\n"
                    f"Battery: {user_choices['Battery']}\n"
                    f"Processor: {user_choices['Processor']}\n"
                )
                response = openai.ChatCompletion.create(
                    model="gpt-4-0613",
                    messages=[{
                        "role": "user",
                        "content": prompt}]
                )
                response_text = response['choices'][0]['message']['content'].strip()

                # Display the dictionary and prompt in a messagebox
                result_str = "\n".join([f"{key}: {value}" for key, value in user_choices.items()])
                messagebox.showinfo("User Choices", f"Choices:\n\n{result_str}\n\n{response_text}")

            # GUI setup
            screen = tk.Toplevel(root)
            screen.title("Device Selection System")
            screen.geometry("600x550")
            screen.configure(bg="#f7f7f9")

            # Title Label
            title_label = tk.Label(
                screen,
                text="Device Selection System",
                font=("Helvetica", 18, "bold"),
                fg="#4b5d67",
                bg="#f7f7f9"
            )
            title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

            # Input Frame
            input_frame = tk.Frame(screen, bg="#f7f7f9")
            input_frame.grid(row=1, column=0, sticky="w", padx=20, pady=10)

            # Initialize StringVar for each option
            category_var = tk.StringVar()
            price_range_var = tk.StringVar()
            brand_var = tk.StringVar()
            speciality_var = tk.StringVar()
            storage_var = tk.StringVar()
            battery_var = tk.StringVar()
            processor_var = tk.StringVar()

            # Dictionary for variables
            vars_dict = {
                "category_var": category_var,
                "price_range_var": price_range_var,
                "brand_var": brand_var,
                "speciality_var": speciality_var,
                "storage_var": storage_var,
                "battery_var": battery_var,
                "processor_var": processor_var,
            }

            # Dropdown Options
            options = [
                ("Category", ["Smartphone", "iPad","tab"], "category_var"),
                ("Price Range", ["₹10,000 and below", "₹10,000 - ₹15,000", "₹15,000 - ₹20,000", "₹20,000 - ₹25,000", "₹25,000 - ₹30,000", "₹30,000 - ₹40,000", "₹40,000 - ₹45,000", "₹45,000 - ₹50,000", "₹50,000 - ₹60,000", "₹60,000 - ₹70,000", "₹70,000 - ₹80,000", "₹80,000 - ₹90,000", "above ₹90,000"], "price_range_var"),
                ("Brand", ["Apple", "Samsung", "Vivo", "Oppo", "Realme","iQOO","Nothing","Pixel","Xiaomi", "Asus", "Lava", "Motorola", "OnePlus", "Huawei", "Sony"], "brand_var"),
                ("Speciality", ["Camera", "Gaming", "Battery Life","Curved Display", "Display"], "speciality_var"),
                ("Internal Storage", ["64GB", "128GB", "256GB"], "storage_var"),
                ("Battery", ["1000mAh to 2000mAh", "2000mAh to 3000mAh", "3000mAh to 4000mAh", "4000mAh to 5000mAh", "5000mAh to 6000mAh"], "battery_var"),
                ("Processor", ["Snapdragon", "MediaTek Dimensity","Ryzen","AMD" ,"MediaTek", "MediaTek Helio", "Apple A-Series", "Bionic chipset", "Exynos", "Unisoc", "Airin"], "processor_var"),
            ]

            # Populate Comboboxes
            for i, (label_text, values, var_name) in enumerate(options):
                tk.Label(
                    input_frame,
                    text=label_text,
                    font=("Arial", 10),
                    bg="#f7f7f9"
                ).grid(row=i, column=0, padx=10, pady=5, sticky="w")

                entry = ttk.Combobox(
                    input_frame,
                    textvariable=vars_dict[var_name],
                    values=values,
                    state="readonly",
                    font=("Arial", 10)
                )
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                entry.bind("<<ComboboxSelected>>", lambda e: update_button_state())

            # Get Suggestions Button
            get_suggestions_button = tk.Button(
                screen,
                text="Get Suggestions",
                command=get_suggestions,
                state="disabled",
                font=("Arial", 12),
                bg="#4CAF50",
                fg="white",
                padx=10
            )
            get_suggestions_button.grid(row=len(options) + 1, column=0, pady=20)

        device_suggestion_system()
    else:
        messagebox.showerror('Invalid', 'Invalid username or password. Please create an account.')

def signup_command():
    
    signup_window = Toplevel(root)
    signup_window.title("Sign Up")
    signup_window.geometry('925x500+300+200')
    signup_window.configure(bg='#fff')
    signup_window.resizable(False, False)

    def signup():
        username = user_signup.get()
        password = code_signup.get()
        conform_password = conform_code.get()

        if password == conform_password:
            try:
                if os.path.exists('datasheet.txt') and os.path.getsize('datasheet.txt') > 0:
                    with open('datasheet.txt', 'r+') as file:
                        d = file.read()
                        r = ast.literal_eval(d)
                else:
                    r = {}

                if username in r:
                    messagebox.showerror("Error", "Username already exists.")
                else:
                    r[username] = password
                    with open('datasheet.txt', 'w') as file:
                        file.write(str(r))

                    messagebox.showinfo('Signup', 'Successfully signed up')
                    signup_window.destroy()

            except Exception as e:
                messagebox.showerror('Error', f"An error occurred: {e}")
        else:
            messagebox.showerror('Invalid', "Both passwords should match")

    
    frame_signup = Frame(signup_window, width=350, height=390, bg='#fff')
    frame_signup.place(x=288, y=70)

    heading_signup = Label(frame_signup, text='Sign up', fg='#57a1f8', bg='white', font=('Microsoft Yahei UI Light', 23, 'bold'))
    heading_signup.place(x=100, y=5)

    
    user_signup = Entry(frame_signup, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
    user_signup.place(x=30, y=80)
    user_signup.insert(0, 'Username')
    user_signup.bind("<FocusIn>", lambda e: user_signup.delete(0, 'end'))
    user_signup.bind("<FocusOut>", lambda e: user_signup.insert(0, 'Username') if user_signup.get() == '' else None)
    Frame(frame_signup, width=295, height=2, bg='black').place(x=25, y=107)

    # Password Field (Signup)
    def on_focus_in_password_signup(e):
        if code_signup.get() == 'Password':
            code_signup.delete(0, 'end')
            code_signup.config(show='*')  # Mask input when focused

    def on_focus_out_password_signup(e):
        if code_signup.get() == '':
            code_signup.config(show='')  # Show placeholder without masking
            code_signup.insert(0, 'Password')

    code_signup = Entry(frame_signup, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
    code_signup.place(x=30, y=150)
    code_signup.insert(0, 'Password')  # Add placeholder
    code_signup.bind("<FocusIn>", on_focus_in_password_signup)
    code_signup.bind("<FocusOut>", on_focus_out_password_signup)
    Frame(frame_signup, width=295, height=2, bg='black').place(x=25, y=177)

    # Confirm Password Field (Signup)
    def on_focus_in_conform_password_signup(e):
        if conform_code.get() == 'Confirm Password':
            conform_code.delete(0, 'end')
            conform_code.config(show='*')  # Mask input when focused

    def on_focus_out_conform_password_signup(e):
        if conform_code.get() == '':
            conform_code.config(show='')  # Show placeholder without masking
            conform_code.insert(0, 'Confirm Password')

    conform_code = Entry(frame_signup, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
    conform_code.place(x=30, y=220)
    conform_code.insert(0, 'Confirm Password')
    conform_code.bind("<FocusIn>", on_focus_in_conform_password_signup)
    conform_code.bind("<FocusOut>", on_focus_out_conform_password_signup)
    Frame(frame_signup, width=295, height=2, bg='black').place(x=25, y=247)

    
    Button(frame_signup, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white', border=0, command=signup).place(x=35, y=280)

    
    label = Label(frame_signup, text='I have an account', fg='black', bg='white', font=('Microsoft Yahei UI Light', 9))
    label.place(x=90, y=340)

    signin_button = Button(frame_signup, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=lambda: signup_window.destroy())
    signin_button.place(x=200, y=340)


img = PhotoImage(file='logp.png')  
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)


user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', lambda e: user.delete(0, 'end'))
user.bind('<FocusOut>', lambda e: user.insert(0, 'Username') if user.get() == '' else None)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)


# Password Field (Signin)
def on_focus_in_password(e):
    if code.get() == 'Password':
        code.delete(0, 'end')
        code.config(show='*')  # Mask input when focused

def on_focus_out_password(e):
    if code.get() == '':
        code.config(show='')  # Show placeholder without masking
        code.insert(0, 'Password')

code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')  # Add placeholder
code.bind('<FocusIn>', on_focus_in_password)
code.bind('<FocusOut>', on_focus_out_password)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=200)

signup_label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
signup_label.place(x=90, y=260)

signup_button = Button(frame, text="Sign up", width=6, border=0, bg='white', cursor="hand2", fg='#57a1f8', command=signup_command)
signup_button.place(x=220, y=260)

root.mainloop()
