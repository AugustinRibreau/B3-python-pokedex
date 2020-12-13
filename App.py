import base64
import os
import requests
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk, Image


class App():
    def __init__(self):
        super().__init__()
        self.home_window = Tk()
        self.request_all_pokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=649")
        self.home_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/1.gif"
        self.init_UI()

    def init_UI(self):
        self.home()
        self.menu()
        self.default_image()
        self.list()
        self.home_window.title("Augustin Ribreau")
        self.home_window.geometry("500x400")
        self.home_window.minsize(500, 400)
        self.home_window.resizable(width=FALSE, height=FALSE)
        self.home_window.config(bg="#F2F2F2")
        self.home_window.mainloop()

    def home(self):
        home_header = Frame(self.home_window, height=50)
        self.home_info = Frame(self.home_window, bg="#F2F2F2", width=50, height=100)
        home_info_name = Frame(self.home_info, bg='red', height=5, relief="raised", borderwidth=4)
        home_info_characteristic = Frame(self.home_info, bg='red', height=5, relief="raised", borderwidth=4)
        self.home_list = Frame(self.home_window, bg="red", height=100, borderwidth=4, relief="raised")
        home_header_title = Label(home_header, text="Pokédex", bg="#b60000", fg='white', font="Roboto, 30", width=596,
                                  height=2)
        self.home_info_name_label = Label(home_info_name,
                                          text="  01" + " " + self.request_all_pokemon.json()['results'][0]['name'],
                                          bg="#F2F2F2")
        self.home_info_characteristic_label = Label(home_info_characteristic,
                                                    text="hp : 45\n" + "attack : 49\n" + "defense : 49\n" + "speed : 45",
                                                    bg="#F2F2F2")
        home_header.pack(side=TOP)
        self.home_info.pack(side=LEFT)
        home_info_name.pack(side=TOP)
        home_info_characteristic.pack(side=BOTTOM)
        self.home_list.pack(side=RIGHT)
        home_header_title.pack(side=TOP)
        self.home_info_name_label.pack(side=TOP)
        self.home_info_characteristic_label.pack(side=BOTTOM)

    def menu(self):
        menu = Menu(self.home_window)
        self.home_window['menu'] = menu
        submenu = Menu(menu)
        submenu_teams = Menu(submenu)
        menu.add_cascade(label='Option', menu=submenu)
        submenu.add_command(label='Rechercher', command=self.search)
        submenu.add_cascade(label='Equipe', menu=submenu_teams)
        submenu_teams.add_command(label='Créer', command=self.create_team_name)
        submenu_teams.add_command(label='Afficher', command=self.display_teams)

    def create_team_name(self):
        self.create_teams_window = Toplevel(self.home_window)
        self.create_teams_window.title("Création d'une équipe")
        self.create_teams_window.geometry("500x400")
        self.create_teams_window.minsize(500, 400)
        self.create_teams_window.resizable(width=FALSE, height=FALSE)
        self.create_teams_window.config(bg="#F2F2F2")
        self.create_teams_name_title = Label(self.create_teams_window, text="Quel est le nom de ton équipe : ",
                                             bg="#F2F2F2")
        self.create_teams_name_title.pack(side=TOP)
        self.create_teams_name_frame = Frame(self.create_teams_window, bg="#F2F2F2")
        self.create_teams_name_frame.pack(side=TOP)
        self.create_teams_name_input = Entry(self.create_teams_name_frame, width=20, bd="1")
        self.create_teams_name_input.pack(side=LEFT)
        self.create_teams_name_button = Button(self.create_teams_name_frame, text="Valider", width=10,
                                               command=self.create_team, bg="#F2F2F2")
        self.create_teams_name_button.pack(side=RIGHT)
        self.create_teams_name_error = Label(self.create_teams_window, bg="#F2F2F2",
                                             text="Ce nom d'équipe éxiste déjà.", fg="red")

    def reset_create_teams_frame(self):
        self._unpack(self.create_teams_name_frame)
        self._unpack(self.create_teams_name_error)
        self._unpack(self.create_teams_name_title)
        self._unpack(self.create_teams_name_input)
        self._unpack(self.create_teams_name_button)

    def create_team(self):
        self.reset_create_teams_frame()
        self.pokemon_remaining = 5
        create_team_title = Label(self.create_teams_window, text="Choisis tes 5 pokémons : ", bg="#F2F2F2")
        create_team_title.pack(side=TOP)
        create_team_container = Frame(self.create_teams_window, bg="#F2F2F2")
        create_team_container.pack(side=TOP)
        create_team_container_frame = Frame(create_team_container, bg='red', height=5, relief="raised", borderwidth=4)
        create_team_container_frame.pack(side=LEFT)
        self.create_team_input = Entry(create_team_container_frame, width=20, bd="1")
        self.create_team_input.pack()
        self.create_team_file = open("./equipe/" + self.create_teams_name_input.get() + ".txt", "w")
        self.create_team_button = Button(create_team_container, text="Ajouter (" + str(self.pokemon_remaining) + ")",
                                         width=10,
                                         command=self.create_team_push, bg="#F2F2F2")
        self.create_team_button.pack(side=RIGHT)

    def create_team_push(self):
        self.create_team_error = Label(self.create_teams_window, fg="red", text="Ce pokémon n'existe pas !",
                                       bg="#F2F2F2")
        if self.request_all_pokemon.status_code == 200:
            self._unpack(self.create_team_error)
            result = self.request_all_pokemon.json()
            iterator = 0
            for _ in result['results']:
                if result['results'][iterator]['name'] == self.create_team_input.get():
                    self.pokemon_remaining -= 1
                    if self.pokemon_remaining == 0:
                        self._unpack(self.create_team_button)
                        self.create_team_button.config(text="Ajouter (" + str(self.pokemon_remaining) + ")")
                        self.create_team_file.write(self.create_team_input.get())
                        self.create_teams_window.destroy()
                        self.home_window.destroy()
                        return
                    self.create_team_button.config(text="Ajouter (" + str(self.pokemon_remaining) + ")")
                    self.create_team_file.write(self.create_team_input.get() + "-")
                    return
                iterator += 1
            return self.create_team_error.pack(side=BOTTOM)

    def display_teams(self):
        display_teams_window = Tk()
        display_teams_window.title("Affichage des equips")
        display_teams_window.geometry("500x400")
        display_teams_window.minsize(500, 400)
        display_teams_window.resizable(width=FALSE, height=FALSE)
        display_teams_window.config(bg="#F2F2F2")
        display_teams_list_files = os.listdir("./equipe")
        display_teams_frame = Frame(display_teams_window, bg="#F2F2F2")
        display_teams_frame.pack(side=TOP, pady=50)
        for display_teams_list_file in display_teams_list_files:
            display_teams_frame_label = Frame(display_teams_frame, bg="#F2F2F2")
            display_teams_frame_label.pack(side=TOP)
            display_teams_list_file = open("./equipe/" + display_teams_list_file, "r")
            display_teams_file = display_teams_list_file.read().split('-')
            display_teams_file_name = display_teams_list_file.name.split('/')[2].split('.')[0]
            display_teams_name_label = Label(display_teams_frame_label, text=display_teams_file_name + ": ",
                                             bg="#F2F2F2", fg="red")
            display_teams_name_label.pack(side=LEFT)
            for c in display_teams_file:
                display_teams_pokemon_name = Label(display_teams_frame_label, text=c + " ", bg="#F2F2F2")
                display_teams_pokemon_name.pack(side=LEFT)

    def search(self):
        self.search_window = Toplevel(self.home_window)
        self.search_window.title("Recherche de Pokémon")
        self.search_window.geometry("500x400")
        self.search_window.minsize(500, 400)
        self.search_window.resizable(width=FALSE, height=FALSE)
        self.search_window.config(bg="#F2F2F2")
        search_frame_title = Frame(self.search_window, bg='red', height=5, relief="raised", borderwidth=4)
        search_frame_title.pack(side=TOP)
        search_label_input = Label(search_frame_title, text="Entrer un nom :", bg="#F2F2F2", font="Roboto")
        search_label_input.pack(side=TOP)
        search_frame_header = Frame(self.search_window, bg="#F2F2F2")
        search_frame_header.pack(side=TOP)
        search_frame_input = Frame(search_frame_header, bg='red', height=5, relief="raised", borderwidth=2)
        search_frame_input.pack(side=LEFT, padx=20, pady=5)
        self.search_input = Entry(search_frame_input, width=20, bd="1")
        self.search_input.pack()
        search_frame_button = Frame(search_frame_header, bg='red', height=5, width=10, relief="raised", borderwidth=2)
        search_frame_button.pack(side=RIGHT)
        search_button = Button(search_frame_button, text="Rechercher", width=10, command=self.search_pokemon)
        search_button.pack()
        self.search_frame_result = Frame(self.search_window, bg="#F2F2F2")
        search_frame_characteristic = Frame(self.search_frame_result, bg='red', relief="raised", borderwidth=2)
        search_frame_characteristic.pack(side=BOTTOM)
        self.search_label_characteristic = Label(search_frame_characteristic, bg="#F2F2F2", font="Roboto")
        self.search_label_characteristic.pack()
        self.search_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"
        self.search_image = PhotoImage(data=self.base64img(self.search_url))
        self.search_canvas = Canvas(self.search_frame_result, bg="#F2F2F2", width="200", height="200",
                                    highlightthickness=0)
        self.search_image = self.search_image.zoom(2)
        self.search_canvas.pack()
        self.search_canvas.create_image(100, 100, image=self.search_image, anchor='center')

    def search_pokemon(self):
        search_input_value = self.search_input.get()
        if self.request_all_pokemon.status_code == 200:
            result = self.request_all_pokemon.json()
            i = 0
            for _ in result['results']:
                if result['results'][i]['name'] == search_input_value:
                    self.search_frame_result.pack()
                    self.request_all_pokemon_characteristic = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(i + 1))
                    pokemon_characteristic_json = self.request_all_pokemon_characteristic.json()
                    self.search_label_characteristic.config(text="Nom : " + str(result['results'][i]['name']) + "\n" +
                                                                 "HP : " + str(
                        pokemon_characteristic_json['stats'][0]['base_stat']) + "\n" +
                                                                 "Attack : " + str(
                        pokemon_characteristic_json['stats'][1]['base_stat']) + "\n" +
                                                                 "Defense : " + str(
                        pokemon_characteristic_json['stats'][2]['base_stat']) + "\n" +
                                                                 "Speed : " + str(
                        pokemon_characteristic_json['stats'][5]['base_stat']))
                    self.search_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + str(
                        i + 1) + ".png"
                    self.search_update_photo = PhotoImage(data=self.base64img(self.search_url))
                    self.search_image = self.search_update_photo
                    self.search_update_photo = self.search_update_photo.zoom(2)
                    self.search_canvas.create_image(100, 100, image=self.search_update_photo, anchor='center')
                i += 1

    def base64img(self, url):
        image_byt = urlopen(url)
        image_byt = image_byt.read()
        image_b64 = base64.b64encode(image_byt)
        return image_b64

    def default_image(self):
        self.home_image = PhotoImage(data=self.base64img(self.home_url))
        self.home_canvas = Canvas(self.home_info, bg="#F2F2F2", width="200", height="200", highlightthickness=0)
        self.home_image = self.home_image.zoom(2)
        self.home_canvas.pack()
        self.home_canvas.create_image(100, 100, image=self.home_image, anchor='center')
        self.home_scrollbar = Scrollbar(self.home_window)
        self.home_listbox = Listbox(self.home_list, width=30, height=30, font="Roboto, 20", bd="0",
                                    bg="#F2F2F2",
                                    selectmode=SINGLE)
        self.home_listbox.pack()
        self.home_listbox.bind('<<ListboxSelect>>', self.cur_select)

    def cur_select(self, event):
        home_widget = event.widget
        home_current_selection_id = home_widget.curselection()
        home_current_selection_name = home_widget.get(home_current_selection_id[0])
        self.request_all_pokemon_stats = requests.get(
            'https://pokeapi.co/api/v2/pokemon/' + str(home_current_selection_id[0] + 1))
        home_pokemon_hp = self.request_all_pokemon_stats.json()['stats'][0]['base_stat']
        home_pokemon_attack = self.request_all_pokemon_stats.json()['stats'][1]['base_stat']
        home_pokemon_defense = self.request_all_pokemon_stats.json()['stats'][2]['base_stat']
        home_pokemon_speed = self.request_all_pokemon_stats.json()['stats'][5]['base_stat']
        self.home_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/" + str(
            home_current_selection_id[0] + 1) + ".gif"
        self.home_update_image = PhotoImage(data=self.base64img(self.home_url))
        self.home_image = self.home_update_image
        self.home_update_image = self.home_update_image.zoom(2)
        self.home_info_name_label.config(text=home_current_selection_name)
        self.home_canvas.create_image(100, 100, image=self.home_update_image, anchor='center')
        self.home_info_characteristic_label.config(text="hp : " + str(home_pokemon_hp) + "\n" +
                                                        "attack : " + str(home_pokemon_attack) + "\n" +
                                                        "defense : " + str(home_pokemon_defense) + "\n" +
                                                        "speed : " + str(home_pokemon_speed))

    def _unpack(self, object):
        object.pack_forget()

    def list(self):
        if self.request_all_pokemon.status_code == 200:
            result = self.request_all_pokemon.json()
            i = 0
            for _ in result['results']:
                if i < 9:
                    self.home_listbox.insert(END, "  0" + str(i + 1) + " " + result['results'][i]['name'])
                    i += 1
                else:
                    self.home_listbox.insert(END, "  " + str(i + 1) + " " + result['results'][i]['name'])
                    i += 1
            self.home_listbox.config(yscrollcommand=self.home_scrollbar.set)
            self.home_scrollbar.config(command=self.home_listbox.yview)


if __name__ == "__main__":
    App()
