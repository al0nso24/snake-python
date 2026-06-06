import tkinter as tk
import random

# Configuración del juego:
ANCHO = 600
ALTO = 400
TAM_CELDA = 20
VELOCIDAD = 125

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake 🐍")

        self.score = 0


        self.label = tk.Label(
            root,
            text=f"Puntuación: {self.score}",
            font=("Arial", 14, "bold")
        )
        self.label.pack()


        self.canvas = tk.Canvas(
            root,
            width=ANCHO,
            height=ALTO,
            bg="#1e1e1e"
        )
        self.canvas.pack()

        self.reset_game()

        # Configuración de teclas para jugar:
        self.root.bind("<Up>", lambda e: self.cambiar_direccion("Up"))
        self.root.bind("<Down>", lambda e: self.cambiar_direccion("Down"))
        self.root.bind("<Left>", lambda e: self.cambiar_direccion("Left"))
        self.root.bind("<Right>", lambda e: self.cambiar_direccion("Right"))

        self.actualizar()

    def reset_game(self):
        self.canvas.delete("all")

        self.score = 0
        self.label.config(text=f"Puntuación: {self.score}")

        self.direccion = "Right"

        self.snake = [
            (100, 100),
            (80, 100),
            (60, 100)
        ]

        self.generar_comida()

    def generar_comida(self):
        while True:
            x = random.randint(0, (ANCHO // TAM_CELDA) - 1) * TAM_CELDA
            y = random.randint(0, (ALTO // TAM_CELDA) - 1) * TAM_CELDA

            if (x, y) not in self.snake:
                self.comida = (x, y)
                break

    def cambiar_direccion(self, nueva):
        opuestas = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left"
        }

        if nueva != opuestas[self.direccion]:
            self.direccion = nueva

    def mover(self):
        cabeza_x, cabeza_y = self.snake[0]

        if self.direccion == "Up":
            cabeza_y -= TAM_CELDA
        elif self.direccion == "Down":
            cabeza_y += TAM_CELDA
        elif self.direccion == "Left":
            cabeza_x -= TAM_CELDA
        elif self.direccion == "Right":
            cabeza_x += TAM_CELDA

        nueva_cabeza = (cabeza_x, cabeza_y)

        # Cuando choca con las paredes:
        if (
            cabeza_x < 0 or
            cabeza_x >= ANCHO or
            cabeza_y < 0 or
            cabeza_y >= ALTO
        ):
            return False

        # Cuando choca consigo misma:
        if nueva_cabeza in self.snake:
            return False

        self.snake.insert(0, nueva_cabeza)

        # Comer comida:
        if nueva_cabeza == self.comida:
            self.score += 1
            self.label.config(text=f"Puntuación: {self.score}")
            self.generar_comida()
        else:
            self.snake.pop()

        return True

    def dibujar(self):
        self.canvas.delete("all")

        # Comida:
        x, y = self.comida
        self.canvas.create_rectangle(
            x, y,
            x + TAM_CELDA,
            y + TAM_CELDA,
            fill="red",
            outline=""
        )

        # Serpiente:
        for i, (x, y) in enumerate(self.snake):
            color = "#00ff66" if i == 0 else "#00cc55"

            self.canvas.create_rectangle(
                x, y,
                x + TAM_CELDA,
                y + TAM_CELDA,
                fill=color,
                outline="#1e1e1e"
            )

    # Game Over:
    def game_over(self):
        self.canvas.create_text(
            ANCHO // 2,
            ALTO // 2 - 20,
            text="GAME OVER",
            fill="white",
            font=("Arial", 24, "bold")
        )

        self.canvas.create_text(
            ANCHO // 2,
            ALTO // 2 + 20,
            text="Presiona R para reiniciar",
            fill="white",
            font=("Arial", 14)
        )

        self.root.bind("r", lambda e: self.reiniciar())


    # Reinicia el juego luego de presionar la tecla R:
    def reiniciar(self):
        self.root.unbind("r")
        self.reset_game()
        self.actualizar()


    def actualizar(self):
        if self.mover():
            self.dibujar()
            self.root.after(VELOCIDAD, self.actualizar)
        else:
            self.game_over()


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()