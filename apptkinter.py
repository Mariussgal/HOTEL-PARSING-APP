import tkinter as tk
from tkinter import ttk
from hotelparser import file_path, load_and_process_data, selection_sort, insertion_sort
from PIL import Image, ImageTk
import customtkinter
import time

dark_bg = "#000000"
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.title("Hotel Parser App")
root.geometry("1920x1080")
style = ttk.Style(root)
style.theme_use("clam")

common_font = ("Helvetica", 12)
dark_bg = "#333333"  
light_fg= "#ffffff"  
accent_color = "#4CAF50" 

original_image = Image.open("wallpaper.png")
resized_image = original_image.resize((1920, 1080), Image.Resampling.LANCZOS)
background_image = ImageTk.PhotoImage(resized_image)
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

top_frame = customtkinter.CTkFrame(root)
top_frame.pack(side='top', fill='x', padx=10, pady=10)
tree_frame = customtkinter.CTkFrame(root, corner_radius=10)
tree_frame.pack(pady=200, padx=300, expand=True)
tree = ttk.Treeview(tree_frame, columns=("Hotel Name", "Price", "Experience", "Rating"), show="headings", height=20)

hotels = load_and_process_data(file_path)
hotel_experience_var = tk.StringVar(value = 'bad')
hotel_price_var = tk.DoubleVar(value=300)
hotel_rating_var = tk.DoubleVar(value=0)
wifi_var = tk.BooleanVar(value=False)

sort_method_var = tk.StringVar(value="selection_sort")

tri_method_label = customtkinter.CTkLabel(top_frame, text="Sorting method:", font=common_font)
tri_method_label.pack(side='left', padx=10, pady=10)

tri_method_combobox = customtkinter.CTkComboBox(top_frame, values=["selection_sort", "insertion_sort"], command=lambda value: sort_method_var.set(value))
tri_method_combobox.pack(side='left', padx=10, pady=10)
tri_method_combobox.set("selection_sort")

btn_filtrer = customtkinter.CTkButton(top_frame, text="Sort and display", command=lambda: sort_display(sort_method_var.get()), font=common_font)
btn_filtrer.pack(side='right', padx=10, pady=10)

def sort_display(sort_method):
    try:
        start_time = time.time()

        max_price = hotel_price_var.get()
        selected_experience = hotel_experience_var.get()
        wifi_filter = wifi_var.get()
        rating_filter = hotel_rating_var.get()  

        
        filtered_hotels = [hotel for hotel in hotels if hotel['hotel_price'] <= max_price 
                          and hotel['hotel_experience'] == selected_experience
                          and hotel['hotel_rating'] >= rating_filter
                          and (not wifi_filter or hotel['has_wifi'])]  

        if sort_method == "selection_sort":
            selection_sort(filtered_hotels)
        elif sort_method == "insertion_sort":
            insertion_sort(filtered_hotels)

        for item in tree.get_children():
            tree.delete(item)

        for hotel in filtered_hotels:
            tree.insert("", "end", values=(hotel['hotel_name'], f"{hotel['hotel_price']}€", hotel['hotel_experience'], hotel['hotel_rating']))

        end_time = time.time()
        execution_time = end_time - start_time
        execution_time_label.configure(text=f"Execution time ({sort_method.replace('_', ' ')}): {execution_time:.4f} seconds")

    except Exception as e:
        print(e)

experience_label = customtkinter.CTkLabel(top_frame, text="Hotel experience :", font=common_font)
experience_label.pack(side='left', padx=10, pady=10)

experience_combobox = customtkinter.CTkComboBox(top_frame, values=[ "Poor","Bad", "Average", "Very good","Excellent",], command=lambda value: hotel_experience_var.set(value))
experience_combobox.pack(side='left', padx=10, pady=10)
experience_combobox.set("Poor")

hotel_rating_label = customtkinter.CTkLabel(top_frame, text="Minimum hotel rating :", font=common_font)
hotel_rating_label.pack(side='left', padx=10, pady=10)

hotel_rating_combobox = customtkinter.CTkComboBox(top_frame, values=["0", "0.5","1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"], command=lambda value: hotel_rating_var.set(value))
hotel_rating_combobox.pack(side='left', padx=10, pady=10)
hotel_rating_combobox.set("0")

max_price_label = customtkinter.CTkLabel(top_frame, text="Maximum price :", font=common_font)
max_price_label.pack(side='left', padx=10, pady=10)

max_price_combobox = customtkinter.CTkComboBox(top_frame, values=["100", "200", "300"], command=lambda value: hotel_price_var.set(value))
max_price_combobox.pack(side='left', padx=10, pady=10)
max_price_combobox.set("0")

def checkbox_wifi_event():
    sort_display(sort_method_var.get()) 

wifi_checkbutton = customtkinter.CTkCheckBox(
    master=top_frame,
    text='Free High Speed Internet (WiFi)',
    command=checkbox_wifi_event,  
    variable= wifi_var,  
    onvalue=True,  
    offvalue=False,  
    hover_color="gray",  
    font=common_font,  
    width=120,  
    height=25,  
    corner_radius=10 
)
wifi_checkbutton.pack(side='left', padx=10, pady=10)

execution_time_label = customtkinter.CTkLabel(root, text="Execution time (Selection sort): 0.0000 seconds", font=common_font)
execution_time_label.pack(pady=10)

tree.column("Hotel Name", anchor="center", width=300)
tree.column("Price", anchor="center", width=100)
tree.column("Experience", anchor="center", width=100)
tree.column("Rating", anchor="center", width=100)

tree.heading("Hotel Name", text="Hotel Name")
tree.heading("Price", text="Price (€)")
tree.heading("Experience", text="Experience")
tree.heading("Rating", text="Rating")

tree.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

root.mainloop()
