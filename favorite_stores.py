import tkinter
import tkintermapview
import pandas as pd

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1200}x{800}")
root_tk.title("my_favorite_stores.py")
root_bg_color = root_tk.cget('bg')

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=700, height=800, corner_radius=0)
map_widget.place(relx=0.75, rely=0.5, anchor=tkinter.CENTER)

# set current widget position and zoom
map_widget.set_position(47.60615924714301, -122.33231557074055)  # Seaattle city
map_widget.set_zoom(12)

#function to pass saved store info to the mapwidget:
def upload_saved_marker(store_name, store_color, store_x, store_y):
    map_widget.set_marker(store_x, store_y, text=store_name, marker_color_circle=store_color, marker_color_outside=store_color)

#function to read the saved stores file and pass to the map_widget:
df = pd.read_csv('saved_stores.csv') #df.shape[0]
saved_store_names = (df.store_names).tolist()
saved_store_colors = (df.store_colors).tolist()
saved_store_x = (df.store_x).tolist()
saved_store_y = (df.store_y).tolist()

for i in range(df.shape[0]):
    upload_saved_marker(saved_store_names[i], saved_store_colors[i], float(saved_store_x[i]), float(saved_store_y[i]))


#empty row place holders for grid consistency:
label_empty0=tkinter.Label(root_tk, text="", font=("Arial", 16), bg=root_bg_color, borderwidth=0, relief="flat")
label_empty0.grid(row=0, padx=10, pady=10)
label_empty1=tkinter.Label(root_tk, text="", font=("Arial", 16),anchor="w", bg=root_bg_color, borderwidth=0, relief="flat")
label_empty1.grid(row=1,column=0, padx=10, pady=10)
label_empty2=tkinter.Label(root_tk, text="", font=("Arial", 16), bg=root_bg_color, borderwidth=0, relief="flat")
label_empty2.grid(row=2, padx=10, pady=10)
label_empty5=tkinter.Label(root_tk, text="", font=("Arial", 16), bg=root_bg_color, borderwidth=0, relief="flat")
label_empty5.grid(row=5, padx=10, pady=10)

    # Creating a label for greeting:

label_greeting = tkinter.Label(root_tk, text="Hi! Let's build a map of your favorite stores!",foreground="orange", font=("Arial", 20, "bold"), bg=root_bg_color)
label_greeting.place(x=110, y=50) 


    # Creating entry label fields to retrieve store input from user:

#store name instruction and input field
label_name_instructions = tkinter.Label(text = "Choose the stores you want to add to the list:", foreground="orange", font=("Arial", 16))
label_name_instructions.place(x=50, y=100)

label_store_name = tkinter.Label(root_tk,text="Store Name", foreground="orange", background="white",font=("Arial", 16),borderwidth=4, relief="solid")
label_store_name.grid(row=3, column=0, padx=10, pady=10, sticky="w") 

entry_store_name = tkinter.Entry(root_tk,foreground="orange", background="white",font=("Arial", 16),borderwidth=4, relief="solid")
entry_store_name.grid(row=3, column=1, padx=10, pady=10, sticky="w") 


#store coordinate instruction and input field
label_coordinates = tkinter.Label(text = "What are the X & Y coordinates?",foreground="orange", background="white",font=("Arial", 16),borderwidth=4, relief="solid")
label_coordinates.grid(row=4, column=0, padx=10, pady=10, sticky="w")

entry_coordinates = tkinter.Entry(root_tk,foreground="orange", background="white",font=("Arial", 16),borderwidth=4, relief="solid")
entry_coordinates.grid(row=4, column=1, padx=10, pady=10, sticky="w")

label_coordinates_note = tkinter.Label(text = "Right click on the map to copy coordinates. Please seperate x and y with a comma",foreground="orange", background="white",font=("Arial", 14, "italic"),borderwidth=0, relief="solid",bg=root_bg_color)
label_coordinates_note.place (x=10, y=240)


#marker color input field
label_marker_color = tkinter.Label(text = "Choose a color for its marker",foreground="orange", background="white",font=("Arial", 16),borderwidth=4, relief="solid")
label_marker_color.grid(row=6, column=0, padx=10, pady=10, sticky="w")

entry_marker_color = tkinter.Entry(foreground="orange", background="white",font=("Arial", 16),borderwidth=4, relief="solid")
entry_marker_color.grid(row=6, column=1, padx=10, pady=10, sticky="w")


    # Creating a button to process user input and add marker to the map:

#function to pass user input to the mapwidget:
def add_marker():
    store_name = entry_store_name.get()
    store_coord_xy = entry_coordinates.get()
    split_coord = store_coord_xy.split(',')
    store_x = float(split_coord[0])
    store_y = float(split_coord[1])
    marker_color = entry_marker_color.get()
    map_widget.set_marker(store_x, store_y, text=store_name, marker_color_circle=marker_color, marker_color_outside=marker_color)

    # appending the newly added store info to the saved stores file. 
    # this file will be read and the info within will be passed to the map_widget next time this program is run.    

    saved_store_names.append(store_name)
    saved_store_colors.append(marker_color)
    saved_store_x.append(store_x)
    saved_store_y.append(store_y)

    # dictionary of lists to populate the saved store file
    dict = {'store_names': saved_store_names, 'store_colors': saved_store_colors, 'store_x': saved_store_x, 'store_y': saved_store_y}
    df = pd.DataFrame(dict)
    # saving the dataframe to the csv file
    df.to_csv('saved_stores.csv')

    # cleaning up the fields each time the add marker button is used
def delete_entries():
    entry_store_name.delete(0, tkinter.END)
    entry_coordinates.delete(0, tkinter.END)
    entry_marker_color.delete(0, tkinter.END)

#creating the button:
button = tkinter.Button(root_tk, text="Add Marker", command=lambda: [add_marker(), delete_entries()])
button.place(x=200, y= 500)



# using .lift to make sure that the relevant widgets are visible in case they coincide with the "invisible" 
# grids that i used as place holders.
# this is a crude work around to a problem i encountered when positioning the widgets using both grid and place methods.
# it can and should be improved using frames.

label_greeting.lift()
label_name_instructions.lift()
button.lift()
map_widget.lift()
label_coordinates_note.lift()

root_tk.mainloop()