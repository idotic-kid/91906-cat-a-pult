import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Cat-a-pult!"

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)
        self.highscore = 0

        self.background_color = arcade.csscolor.BURLYWOOD

    def home():
        """Function for the home screen"""

        
    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()



def main():
    """Main function"""
    window = GameView()

    arcade.run()


if __name__ == "__main__":
    main()
