from flask import Flask, render_template, request
import random

app = Flask(__name__)

choices = {1: "Snake", 0: "Gun", -1: "Water"}

# Global score counters
player_score = 0
computer_score = 0

def decide_winner(player, computer):
    if player == computer:
        return "Draw"
    elif (player == 1 and computer == -1) or \
         (player == 0 and computer == 1) or \
         (player == -1 and computer == 0):
        return "You Win!"
    else:
        return "Computer Wins!"

@app.route("/", methods=["GET", "POST"])
def home():
    global player_score, computer_score

    result = None
    comp_choice = None
    player_choice = None

    if request.method == "POST":
        player_choice = int(request.form["choice"])
        comp_choice = random.choice(list(choices.keys()))
        result = decide_winner(player_choice, comp_choice)

        # Update scores
        if result == "You Win!":
            player_score += 1
        elif result == "Computer Wins!":
            computer_score += 1

    return render_template(
        "index.html",
        choices=choices,
        player_choice=player_choice,
        comp_choice=comp_choice,
        result=result,
        player_score=player_score,
        computer_score=computer_score
    )

if __name__ == "__main__":
    app.run(debug=True)
