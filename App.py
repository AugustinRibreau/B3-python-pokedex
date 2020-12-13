import base64
import os
import requests
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk, Image

r_pokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=649")
name = ""


class App():
    def __init__(self):
        super().__init__()
        self.window = Tk()

        # Frames
        self.header = Frame(self.window, height=50)
        self.info_pokemon = Frame(self.window, bg="#F2F2F2", width=50, height=100)
        self.info_pokemon_name = Frame(self.info_pokemon, bg='red', height=5, relief="raised", borderwidth=4)
        self.info_pokemon_lvl = Frame(self.info_pokemon, bg='red', height=5, relief="raised", borderwidth=4)
        self.list = Frame(self.window, bg="red", height=100, borderwidth=4, relief="raised")
        # Labels
        self.title = Label(self.header, text="Pokédex", bg="#b60000", fg='white', font="Roboto, 30", width=596,
                           height=2)
        self.pokemon_name = r_pokemon.json()['results'][0]['name']
        self.pokemon_name_label = Label(self.info_pokemon_name, text="  01" + " " + self.pokemon_name, bg="#F2F2F2")
        self.pokemon_info = Label(self.info_pokemon_lvl,
                                  text="hp : 45\n" + "attack : 49\n" + "defense : 49\n" + "speed : 45", bg="#F2F2F2")
        # Requests
        self.url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/1.gif"
        self.header.pack(side=TOP)
        self.info_pokemon.pack(side=LEFT)
        self.info_pokemon_name.pack(side=TOP)
        self.info_pokemon_lvl.pack(side=BOTTOM)
        self.list.pack(side=RIGHT)
        self.title.pack(side=TOP)
        self.pokemon_name_label.pack(side=TOP)
        self.pokemon_info.pack(side=BOTTOM)
        self.createMenu()
        self.initImg()

    def createMenu(self):
        menuBar = Menu(self.window)
        self.window['menu'] = menuBar
        sousMenu = Menu(menuBar)
        sousMenu_equipe = Menu(sousMenu)
        menuBar.add_cascade(label='Option', menu=sousMenu)
        sousMenu.add_command(label='Rechercher', command=self.searchPokemon)
        sousMenu.add_cascade(label='Equipe', menu=sousMenu_equipe)
        sousMenu_equipe.add_command(label='Créer', command=self.equipe_create)
        sousMenu_equipe.add_command(label='Afficher', command=self.equipe_display)

    def equipe_create(self):
        self.create_equipe_window = Toplevel(self.window)
        self.create_equipe_window.title("Création d'une équipe")
        self.create_equipe_window.geometry("500x400")
        self.create_equipe_window.minsize(500, 400)
        self.create_equipe_window.resizable(width=FALSE, height=FALSE)
        self.create_equipe_window.config(bg="#F2F2F2")
        self.choose_name_equipe = Label(self.create_equipe_window, text="Quel est le nom de ton équipe : ",
                                        bg="#F2F2F2")
        self.choose_name_equipe.pack(side=TOP)
        self.choose_frame = Frame(self.create_equipe_window, bg="#F2F2F2")
        self.choose_frame.pack(side=TOP)
        self.choose_name_input = Entry(self.choose_frame, width=20, bd="1")
        self.choose_name_input.pack(side=LEFT)
        self.choose_name_btn = Button(self.choose_frame, text="Valider", width=10,
                                      command=self.manageFile, bg="#F2F2F2")
        self.choose_name_btn.pack(side=RIGHT)
        self.errorLabelCreateFolder = Label(self.create_equipe_window, bg="#F2F2F2",
                                            text="Ce nom d'équipe éxiste déjà.", fg="red")

    def manageFile(self):
        self._unpack(self.choose_frame)
        self._unpack(self.errorLabelCreateFolder)
        self._unpack(self.choose_name_equipe)
        self._unpack(self.choose_name_input)
        self._unpack(self.choose_name_btn)
        self.values = []
        title = Label(self.create_equipe_window, text="Choisis tes 5 pokémons : ", bg="#F2F2F2")
        title.pack(side=TOP)
        self.numb_in_equipe = 5
        search_equipe_area = Frame(self.create_equipe_window, bg="#F2F2F2")
        search_equipe_area.pack(side=TOP)
        search_equipe_area_input = Frame(search_equipe_area, bg='red', height=5, relief="raised", borderwidth=4)
        search_equipe_area_input.pack(side=LEFT)
        self.input_equipe = Entry(search_equipe_area_input, width=20, bd="1")
        self.input_equipe.pack()
        self.fileCurrEquipe = open("./equipe/" + self.choose_name_input.get() + ".txt", "w")
        self.btn_equipe_search = Button(search_equipe_area, text="Ajouter (" + str(self.numb_in_equipe) + ")", width=10,
                                        command=self.addInEquipe, bg="#F2F2F2")
        self.btn_equipe_search.pack(side=RIGHT)

    def addInEquipe(self):
        self.error_no_pokemon_equipe = Label(self.create_equipe_window, fg="red", text="Ce pokémon n'existe pas !",
                                             bg="#F2F2F2")
        if r_pokemon.status_code == 200:
            self._unpack(self.error_no_pokemon_equipe)
            result = r_pokemon.json()
            i = 0
            for pokemon in result['results']:
                if result['results'][i]['name'] == self.input_equipe.get():
                    self.numb_in_equipe -= 1
                    if self.numb_in_equipe == 0:
                        self._unpack(self.btn_equipe_search)
                        self.btn_equipe_search.config(text="Ajouter (" + str(self.numb_in_equipe) + ")")
                        self.fileCurrEquipe.write(self.input_equipe.get())
                        return self.create_equipe_window.destroy()
                    self.btn_equipe_search.config(text="Ajouter (" + str(self.numb_in_equipe) + ")")
                    self.fileCurrEquipe.write(self.input_equipe.get() + "-")
                    return
                i += 1
            return self.error_no_pokemon_equipe.pack(side=BOTTOM)

    def equipe_display(self):
        self.display_equipe = Tk()
        self.display_equipe.title("Affichage des équipes")
        self.display_equipe.geometry("500x400")
        self.display_equipe.minsize(500, 400)
        self.display_equipe.resizable(width=FALSE, height=FALSE)
        self.display_equipe.config(bg="#F2F2F2")
        files = os.listdir("./equipe")
        equipe = Frame(self.display_equipe, bg="#F2F2F2")
        equipe.pack(side=TOP, pady=50)
        for file in files:
            file = open("./equipe/" + file, "r")
            content = file.read().split('-')
            filename = file.name.split('/')[2].split('.')[0]
            label = Label(equipe, text=filename + ": ", bg="#F2F2F2", fg="red")
            label.pack(side=LEFT)
            for c in content:
                nom = Label(equipe, text=c + " ", bg="#F2F2F2")
                nom.pack(side=LEFT)

    def searchPokemon(self):
        self.searchWindow = Toplevel(self.window)
        self.searchWindow.title("Recherche de Pokémon")
        self.searchWindow.geometry("500x400")
        self.searchWindow.minsize(500, 400)
        self.searchWindow.resizable(width=FALSE, height=FALSE)
        self.searchWindow.config(bg="#F2F2F2")
        title_area = Frame(self.searchWindow, bg='red', height=5, relief="raised", borderwidth=4)
        title_area.pack(side=TOP)
        title_input = Label(title_area, text="Entrer un nom :", bg="#F2F2F2", font="Roboto")
        title_input.pack(side=TOP)
        top_section = Frame(self.searchWindow, bg="#F2F2F2")
        top_section.pack(side=TOP)
        input_area = Frame(top_section, bg='red', height=5, relief="raised", borderwidth=2)
        input_area.pack(side=LEFT, padx=20, pady=5)
        self.input_search = Entry(input_area, width=20, bd="1")
        self.input_search.pack()
        btn_area = Frame(top_section, bg='red', height=5, width=10, relief="raised", borderwidth=2)
        btn_area.pack(side=RIGHT)
        btn_search = Button(btn_area, text="Rechercher", width=10, command=self.takeSearchValue)
        btn_search.pack()
        self.content = Frame(self.searchWindow, bg="#F2F2F2")
        info_area = Frame(self.content, bg='red', relief="raised", borderwidth=2)
        info_area.pack(side=BOTTOM)
        self.info = Label(info_area, bg="#F2F2F2", font="Roboto")
        self.info.pack()
        self.url_info = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"
        self.photo_info = PhotoImage(data=self.base64img(self.url_info))
        self.cv_info = Canvas(self.content, bg="#F2F2F2", width="200", height="200", highlightthickness=0)
        self.photo_info = self.photo_info.zoom(2)
        self.cv_info.pack()
        self.cv_info.create_image(100, 100, image=self.photo_info, anchor='center')

    def takeSearchValue(self):
        value = self.input_search.get()
        if r_pokemon.status_code == 200:
            result = r_pokemon.json()
            i = 0
            for pokemon in result['results']:
                if result['results'][i]['name'] == value:
                    self.content.pack()
                    # info
                    r_pokemon_stats = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(i + 1))
                    pokemon_stats_json = r_pokemon_stats.json()
                    self.info.config(text="Nom : " + str(result['results'][i]['name']) + "\n" +
                                          "HP : " + str(pokemon_stats_json['stats'][0]['base_stat']) + "\n" +
                                          "Attack : " + str(pokemon_stats_json['stats'][1]['base_stat']) + "\n" +
                                          "Defense : " + str(pokemon_stats_json['stats'][2]['base_stat']) + "\n" +
                                          "Speed : " + str(pokemon_stats_json['stats'][5]['base_stat']))
                    # image
                    self.url_info = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + str(
                        i + 1) + ".png"
                    self.new_photo_info = PhotoImage(data=self.base64img(self.url_info))
                    self.photo_info = self.new_photo_info
                    self.new_photo_info = self.new_photo_info.zoom(2)
                    self.cv_info.create_image(100, 100, image=self.new_photo_info, anchor='center')
                i += 1
                # TODO Ajouter un message d'erreur si le pokémon n'existe pas
        else:
            print("non")

    def base64img(self, url):
        image_byt = urlopen(url)
        image_byt = image_byt.read()
        # PhotoImage
        image_b64 = base64.b64encode(image_byt)
        return image_b64

    # img pokemon
    def initImg(self):
        self.photo = PhotoImage(data=self.base64img(self.url))
        self.cv = Canvas(self.info_pokemon, bg="#F2F2F2", width="200", height="200", highlightthickness=0)
        self.photo = self.photo.zoom(2)
        self.cv.pack()
        self.cv.create_image(100, 100, image=self.photo, anchor='center')

        # listbox
        self.scrollbar = Scrollbar(self.window)
        self.listbox = Listbox(self.list, width=30, height=30, font="Roboto, 20", bd="0",
                               bg="#F2F2F2",
                               selectmode=SINGLE)
        self.listbox.pack()
        self.listbox.bind('<<ListboxSelect>>', self.CurSelect)

        # next
        self.initUI()
        self.window.mainloop()

    def initUI(self):
        self.window.title("Augustin Ribreau")
        self.window.geometry("500x400")
        self.window.minsize(500, 400)
        self.window.resizable(width=FALSE, height=FALSE)
        self.window.config(bg="#F2F2F2")
        self.initList()

    def CurSelect(self, event):
        widget = event.widget
        selection = widget.curselection()
        picked = widget.get(selection[0])
        r_pokemon_stats = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(selection[0] + 1))
        pokemon_info_hp = r_pokemon_stats.json()['stats'][0]['base_stat']
        pokemon_info_attack = r_pokemon_stats.json()['stats'][1]['base_stat']
        pokemon_info_defense = r_pokemon_stats.json()['stats'][2]['base_stat']
        pokemon_info_speed = r_pokemon_stats.json()['stats'][5]['base_stat']
        self.url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/" + str(
            selection[0] + 1) + ".gif"
        self.new_photo = PhotoImage(data=self.base64img(self.url))
        self.photo = self.new_photo
        self.new_photo = self.new_photo.zoom(2)
        self.pokemon_name_label.config(text=picked)
        self.cv.create_image(100, 100, image=self.new_photo, anchor='center')
        self.pokemon_info.config(text=
                                 "hp : " + str(pokemon_info_hp) + "\n" +
                                 "attack : " + str(pokemon_info_attack) + "\n" +
                                 "defense : " + str(pokemon_info_defense) + "\n" +
                                 "speed : " + str(pokemon_info_speed))

    def _unpack(self, object):
        object.pack_forget()

    def initList(self):
        if r_pokemon.status_code == 200:
            result = r_pokemon.json()
            i = 0
            for pokemon in result['results']:
                if i < 9:
                    self.listbox.insert(END, "  0" + str(i + 1) + " " + result['results'][i]['name'])
                    i += 1
                else:
                    self.listbox.insert(END, "  " + str(i + 1) + " " + result['results'][i]['name'])
                    i += 1
            self.listbox.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.listbox.yview)


if __name__ == "__main__":
    App()
