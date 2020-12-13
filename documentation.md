
<h1 align="center">Documentation du Pokédex</h1>  

## Les fonctions :
`__init__ ` : Permet d'initialiser les valeurs principales du code.

`init_UI` :  Initialise les composent principaux

`home` : Dans cette fonction est implémenter des [Frame](http://tkinter.fdex.eu/doc/frw.html) (via Tkinter) ainsi que des [Label](http://tkinter.fdex.eu/doc/labw.html) (via Tkinter) pour la fenêtre principale.

`menu` : Implémentation du [Menu](http://tkinter.fdex.eu/doc/menw.html) (via Tkinter) et des sous menu avec leur redirection respective.

`create_team_name` : Cette fonction permet de créer une équipe et plus précisément son nom.

`reset_create_teams_frame`:  Ceci est une fonction intermédiaire permettant de supprimer toutes les [Frame](http://tkinter.fdex.eu/doc/frw.html) de la fenêtre [create_team_window](https://github.com/AugustinRibreau/python_pokedex/blob/main/App.py#L64) pour laisser place à la fonction `create_team`.

`create_team` : Après avoir choisis le nom de son équipe, nous pouvons grâce à un [Entry](http://tkinter.fdex.eu/doc/entw.html) (via Tkinter) écrire le nom du Pokémon puis l'enregistrer avec un [Button](http://tkinter.fdex.eu/doc/bw.html).

`create_team_push` : Cette fonction permet d'actualiser le [Button](http://tkinter.fdex.eu/doc/bw.html) (via Tkinter) affichant le nombre de Pokémon restant à ajouter dans l'équipe, cela permet une expérience utilisateur plus poussé.

`display_teams` : Comme toutes les fonctions précédents, le nommage de la fonction parle d'elle même. Une nouvelle fenêtre s'ouvre et laisse place à un affichage des équipes. Tkinter étant très farceur par moment, je n'ai pu afficher les images des Pokémon (malgré le faite que cela fonctionne dans un fichier test).

`search` : Nouvelle fenêtre laissant place à un titre, [Label](http://tkinter.fdex.eu/doc/labw.html) (via Tkinter), un [Entry](http://tkinter.fdex.eu/doc/entw.html) (via Tkinter) et un [Button](http://tkinter.fdex.eu/doc/bw.html).

`search_pokemon` :  Cette fonction est appelé après l'appuie du bouton "recherche". Elle va effectuer une requête sur l'api [pokeapi](https://pokeapi.co/) et afficher les caractéristiques `HP, Attack, Defense, Speed`.

`base64img` : Cette fonction prend en paramètre une URL et retourne une image en base64

`default_image` : Permet de définir l'image du Pokémon d'accueil, qui sera par la suite écrasé par le Pokémon sélectionner dans la liste.

`cur_select` : Permet de récupérer la case du [listbox](http://tkinter.fdex.eu/doc/lbw.html) (via Tkinter) et afficher les informations du Pokémon sélectionner.

`_unpack` : Avec Tkinter après la création d'un composant comme un [Label](http://tkinter.fdex.eu/doc/labw.html), un [Button](http://tkinter.fdex.eu/doc/bw.html) ou encore une [Frame](http://tkinter.fdex.eu/doc/frw.html) il fait le [`pack()`](https://riptutorial.com/fr/tkinter/example/29712/pack--). Pour facilité la suppression de ce composant, la fonction `_unpack` à été ajouté.

`list` : [listbox](http://tkinter.fdex.eu/doc/lbw.html) (via Tkinter) est tout simplement une liste d'élément. Ici c'est une liste de Pokémon. La fonction `list` implémente donc cette [listbox](http://tkinter.fdex.eu/doc/lbw.html) (via Tkinter)


## Author

👤 **Augustin Ribreau**

* Website: https://augustinribreau.com/
* GitHub: [@augustinribreau](https://github.com/augustinribreau)
* LinkedIn: [@augustinribreau](https://linkedin.com/in/augustinribreau)  