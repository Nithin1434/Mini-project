import tkinter as tk
from tkinter import ttk, messagebox
import openai
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
        f"Suggest only Top 3 devices based on the following preferences: with their prices \n"
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
root = tk.Tk()
root.title("Device Selection System")
root.geometry("600x550")  # Dynamically adjust based on content
root.configure(bg="#f7f7f9")

# Title Label
title_label = tk.Label(
    root, 
    text="Device Selection System", 
    font=("Helvetica", 18, "bold"), 
    fg="#4b5d67", 
    bg="#f7f7f9"
)
title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

# Input Frame
input_frame = tk.Frame(root, bg="#f7f7f9")
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
    ("Category", ["Laptop", "Smartphone", "iPad"], "category_var"),
    ("Price Range", ["₹10,000 and below", "₹10,000 - ₹15,000", "₹15,000 - ₹20,000", "₹20,000 - ₹25,000", "₹25,000 - ₹30,000", "₹30,000 - ₹40,000", "₹40,000 - ₹45,000", "₹45,000 - ₹50,000", "₹50,000 - ₹60,000", "₹60,000 - ₹70,000", "₹70,000 - ₹80,000", "₹80,000 - ₹90,000", "above ₹90,000"], "price_range_var"),
    ("Brand", ["Apple", "Samsung", "Vivo", "Oppo", "Realme", "Xiaomi", "Asus", "Lava", "Motorola", "OnePlus", "Huawei", "Sony"], "brand_var"),
    ("Speciality", ["Camera", "Gaming", "Battery Life"], "speciality_var"),
    ("Internal Storage", ["64GB", "128GB", "256GB"], "storage_var"),
    ("Battery", ["1000 to 2000", "2000 to 3000", "3000 to 4000", "4000 to 5000", "5000 to 6000"], "battery_var"), 
    ("Processor", ["Snapdragon", "MediaTek Dimensity", "MediaTek", "MediaTek Helio", "Apple A-Series", "Apple A15 Bionic", "Apple A16 Bionic", "Exynos", "Unisoc", "Airin"], "processor_var"),
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
    root, 
    text="Get Suggestions", 
    command=get_suggestions, 
    state="disabled", 
    font=("Arial", 12), 
    bg="#4CAF50", 
    fg="white", 
    padx=10
)
get_suggestions_button.grid(row=len(options) + 1, column=0, pady=20)

# Run the Application
root.mainloop()
