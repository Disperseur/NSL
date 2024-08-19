import tkinter as tk

# Créer la fenêtre principale
fenetre = tk.Tk()

# Charger l'image
minimap = tk.PhotoImage(file='arcachon.png')

# Vérifier l'image
print(minimap)

# Créer un Canvas
canvas_minimap = tk.Canvas(fenetre, width=1000, height=1000)
canvas_minimap.pack()

# Ajouter l'image au Canvas
canvas_minimap.create_image(0, 0, image=minimap, anchor="nw")

# Garder la référence à l'image
canvas_minimap.image = minimap

# Démarrer la boucle principale de la fenêtre
fenetre.mainloop()
