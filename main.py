from flask import Flask, render_template, request, redirect
import json
import os

from team import Team
from bst import TeamBST
from sorting import merge_sort
from heap import MaxHeap


app = Flask(__name__)

team_bst = TeamBST()

DATA_FILE = "data.json"


def save_data():

    teams = team_bst.inorder()

    data = []

    for team in teams:
        data.append(team.to_dict())

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_data():

    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r") as file:
        content = file.read().strip()

    if not content:
        return

    data = json.loads(content)

    for team_data in data:

        team = Team.from_dict(team_data)

        team_bst.insert(team)


@app.route("/")
def home():

    teams = team_bst.inorder()

    leaderboard = merge_sort(teams)

    max_heap = MaxHeap()

    for team in teams:
        max_heap.insert(team)

    top_teams = []

    for i in range(3):

        team = max_heap.extract_max()

        if team is not None:
            top_teams.append(team)

    return render_template(
        "index.html",
        teams=teams,
        leaderboard=leaderboard,
        top_teams=top_teams
    )


@app.route("/add_team", methods=["POST"])
def add_team():

    team_name = request.form["team_name"].strip()

    if team_name:

        new_team = Team(team_name)

        added = team_bst.insert(new_team)

        if not added:
            return "Team already exists!"

        save_data()

    return redirect("/")


@app.route("/record_match", methods=["POST"])
def record_match():

    team_a_name = request.form["team_a"]
    team_b_name = request.form["team_b"]

    score_a = int(request.form["score_a"])
    score_b = int(request.form["score_b"])

    team_a = team_bst.search(team_a_name)
    team_b = team_bst.search(team_b_name)

    if team_a is None or team_b is None:
        return "Team not found!"

    if team_a_name.lower() == team_b_name.lower():
        return "A team cannot play against itself!"

    team_a.played += 1
    team_b.played += 1

    team_a.score_for += score_a
    team_a.score_against += score_b

    team_b.score_for += score_b
    team_b.score_against += score_a

    team_a.score_difference = (
        team_a.score_for - team_a.score_against
    )

    team_b.score_difference = (
        team_b.score_for - team_b.score_against
    )

    if score_a > score_b:

        team_a.wins += 1
        team_a.points += 3

        team_b.losses += 1

    elif score_b > score_a:

        team_b.wins += 1
        team_b.points += 3

        team_a.losses += 1

    else:

        team_a.draws += 1
        team_b.draws += 1

        team_a.points += 1
        team_b.points += 1

    save_data()

    return redirect("/")
@app.route("/search", methods=["POST"])
def search_team():

    team_name = request.form["team_name"].strip()

    team = team_bst.search(team_name)

    if team is None:
        return "Team not found!"

    return render_template(
        "search.html",
        team=team
    )
load_data()

@app.route("/reset", methods=["POST"])
def reset_tournament():

    global team_bst

    team_bst = TeamBST()

    save_data()

    return redirect("/")

if __name__ == "__main__":

    app.run(debug=True)

