import json

def load_highscores():
    
    try:
        with open("highscore.json", "r") as file:
            return json.load(file)
    
    except FileNotFoundError:
        return {
            "CLASSIC": {
                "EASY": 0,
                "NORMAL": 0,
                "HARD": 0,
                "ULTRA_HARD": 0
            },
            "EXTRA": {
                "EASY": 0,
                "NORMAL": 0,
                "HARD": 0,
                "ULTRA_HARD": 0
            }
        }
        
def save_highscores(highscores):
    
    with open("highscore.json", "w") as file:
        json.dump(highscores, file, indent=4)
        
