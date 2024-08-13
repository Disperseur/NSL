import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import time

class RealTimeMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carte satellite en temps réel du bateau")

        # Charger l'image satellite
        self.bg_image = Image.open("bassin_arcachon_satellite.jpg")  # Assurez-vous que le fichier image est dans le bon répertoire
        self.bg_image = self.bg_image.convert("RGB")
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        # Créer un canvas Tkinter pour afficher l'image
        self.canvas = tk.Canvas(self.root, width=self.bg_image.width, height=self.bg_image.height)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image_tk)

        # Configuration initiale de la carte
        self.fig = Figure(figsize=(10, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Ajouter l'image de fond au subplot
        self.ax.imshow(self.bg_image, extent=[-1.4, -0.8, 44.6, 44.9])  # Ajustez les limites en fonction de l'image et de votre zone d'intérêt

        # Premier tracé de la position du bateau
        self.boat_position = {'lat': 44.65, 'lon': -1.17}  # Coordonnées initiales
        self.boat_plot, = self.ax.plot(self.boat_position['lon'], self.boat_position['lat'], 'bo', markersize=10)

        # Créer le canvas matplotlib et ajouter le graphique Tkinter
        self.fig_canvas = tkagg.FigureCanvasTkAgg(self.fig, master=self.root)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Mettre à jour la carte toutes les secondes
        self.update_map()

    def update_map(self):
        # Simuler un changement de position
        self.boat_position['lat'] += 0.005
        self.boat_position['lon'] += 0.005

        # Mettre à jour le tracé de la position du bateau
        self.boat_plot.set_data(self.boat_position['lon'], self.boat_position['lat'])
        
        # Redessiner la carte
        self.fig_canvas.draw()
        
        # Appeler cette méthode de nouveau après 1 seconde
        self.root.after(1000, self.update_map)

if __name__ == '__main__':
    root = tk.Tk()
    app = RealTimeMapApp(root)
    root.mainloop()
