from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root = Tk()

root.title("Dwayne's MP3 Player")
root.geometry("500x450")

# Initialize Pygame
pygame.mixer.init()

#Create Function To Deal with Time
def play_time():
	# Check to see if song is Stopped
	if stopped:
		return


	# Grab current song time 
	current_time = pygame.mixer.music.get_pos() / 1000
	# Convert song time to time format 
	converted_current_time= time.strftime('%M:%S', time.gmtime(current_time))

	#Reconstruct song with directory name
	song = playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'

	#Find the Current Song Length
	song_mut = MP3(song)
	global song_length
	song_length = song_mut.info.length
	# Convert to time format
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

	if int(song_slider.get()) == int(song_length):
		stop()

	elif paused:
		pass
	else:
		# Move slider along 1 second at a time 
		next_time = int(song_slider.get()) + 1
		#Output new time value to the slider 
		song_slider.config(to=song_length,value=next_time)

		# Convert slider position to the time format
		converted_current_time= time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

		# Output slider
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')


	# Add current Time to Status Bar
	if current_time >= 1:
	 status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')


	# Create Loop to check the time every second
	my_label.after(1000, play_time) 


#Create function to add one song 
def add_song():
	song = filedialog.askopenfilename(initialdir='C:/mp3/audio', title = "Choose a Song", filetypes=(("mp3 Files","*.mp3"),))
	# Strip out directory structure and .mp3
	song = song.replace("C:/mp3/audio/","")
	song = song.replace(".mp3","")

	
	playlist_box.insert(END, song)

#create function to add mnay songs 
def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='C:/mp3/audio', title = "Choose a Song", filetypes=(("mp3 Files","*.mp3"),))
	
	# Loop though songs and replace directory structure 
	for song in songs:
		song = song.replace("C:/mp3/audio/","")
		song = song.replace(".mp3","")
        # Puts the song at the end
		playlist_box.insert(END, song)

# Create Function to Delete a song 
def delete_song():
	playlist_box.delete(ANCHOR)

#Create function to delte all songs
def delete_all_songs():
	playlist_box.delete(0,END)

# Create Play Function 
def play():
	# Set Stopped to false since a song is playing
	global stopped
	stopped = False

	#Reconstruct song with directory name
	song = playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'
	#Load the song with pygame mixer
	pygame.mixer.music.load(song)
	#play the song with pygame mixer
	pygame.mixer.music.play(loops=0)
	# Get play time
	play_time()

# Create stopped Variable 
global stooped 
stooped = False

def stop():
	pygame.mixer.music.stop()
	# clear playlist Bar
	playlist_box.selection_clear(ACTIVE)

	status_bar.config(text=f' ')

	# Set the song slider to zero 
	song_slider.config(value=0)

	# set the stop variable to true
	global stooped
	stopped = True


# Create Function to Play the next song number
def next_song():
	# Reset Slider position and status bar 
	status_bar.config(text='')
	song_slider.config(value=0)



	#Get current song number
	next_one = playlist_box.curselection()
	# Add one to the current song number tuple
	next_one = next_one[0] + 1
	my_label.config(text=next_one)

	# Grab the song title from the playlist
	song = playlist_box.get(next_one)
	# Add directory structure stuff to the song 
	song = f'C:/mp3/audio/{song}.mp3'

	#Load the song with pygame mixer
	pygame.mixer.music.load(song)
	#play the song with pygame mixer
	pygame.mixer.music.play(loops=0)

	#clear active bar in playlist
	playlist_box.selection_clear(0,END)
	
	#Move active bar to next song 
	playlist_box.activate(next_one)

	#set Active bar to next bar
	playlist_box.selection_set(next_one, last=None)


def previous_song():
	# Reset Slider position and status bar 
	status_bar.config(text='')
	song_slider.config(value=0)

	#Get current song number
	next_one = playlist_box.curselection()
	# Add one to the current song number tuple
	next_one = next_one[0] - 1
	my_label.config(text=next_one)

	# Grab the song title from the playlist
	song = playlist_box.get(next_one)
	# Add directory structure stuff to the song 
	song = f'C:/mp3/audio/{song}.mp3'

	#Load the song with pygame mixer
	pygame.mixer.music.load(song)
	#play the song with pygame mixer
	pygame.mixer.music.play(loops=0)

	#clear active bar in playlist
	playlist_box.selection_clear(0,END)
	
	#Move active bar to next song 
	playlist_box.activate(next_one)

	#set Active bar to next bar
	playlist_box.selection_set(next_one, last=None)

# Create paused variable which is global 
global paused
paused = False


# Create Pause Function 
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		#unpause
		pygame.mixer.music.unpause()
		paused = False

	else:
		#pause
		pygame.mixer.music.pause()
		paused = True


# Create Volume Function
def volume(x):

	pygame.mixer.music.set_volume(volume_slider.get())

# Create slide function for song positioning 
def slide(x):

	#Reconstruct song with directory name
	song = playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'
	#Load the song with pygame mixer
	pygame.mixer.music.load(song)
	#play the song with pygame mixer
	pygame.mixer.music.play(loops=0, start=song_slider.get())
	


# Create main frame 
main_frame = Frame(root)
main_frame.pack(pady=20)

# Create Playlist Box
playlist_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
playlist_box.grid(row=0,column=0)

# Volume slider frame 
volume_frame = LabelFrame(main_frame,text="volume")
volume_frame.grid(row=0, column=1,padx=10)

volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, length=120, value=1, command= volume)
volume_slider.pack(pady=10)

# Create Song slider 
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient= HORIZONTAL, length=360,value=0, command=slide)
song_slider.grid(row=2,column=0,pady=20)

#Define Butoon Images
back_button_img = PhotoImage(file='C:/mp3/images/back50.png')
forward_button_img = PhotoImage(file='C:/mp3/images/forward50.png')
play_button_img = PhotoImage(file='C:/mp3/images/play50.png')
pause_button_img = PhotoImage(file='C:/mp3/images/pause50.png')
stop_button_img = PhotoImage(file='C:/mp3/images/stop50.png')

# Create Button Frame 
control_frame = Frame(main_frame)
control_frame.grid(row=1,column=0, pady=20)

#Create Play/Stop Buttons
back_button = Button(control_frame, image=back_button_img, borderwidth=0,command=previous_song)
forward_button = Button(control_frame, image=forward_button_img,borderwidth=0,command=next_song)
play_button = Button(control_frame, image=play_button_img,borderwidth=0,command=play)
pause_button = Button(control_frame, image=pause_button_img,borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_button_img,borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)

play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create Add song menu Dropdowns
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
#Add one song to playlist 
add_song_menu.add_command(label="Add One Song to Playlist", command = add_song)
# Add many songs to playlist
add_song_menu.add_command(label="Add many songs to playlist", command = add_many_songs)

remove_song_menu = Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu = remove_song_menu)
remove_song_menu.add_command(label="Delete a song from the playlist", command = delete_song)
remove_song_menu.add_command(label="Delete all songs from the playlist", command = delete_all_songs)


#Create status bar 
status_bar = Label(root, text='Nothing', borderwidth=1, relief= GROOVE, anchor= E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Temporary Label
my_label = Label(root, text='')
my_label.pack(pady=20)

root.mainloop()
