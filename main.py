from flask import Flask, render_template, request, redirect, session
import json
import os
import uuid

from team import Team
from bst import TeamBST
from sorting import merge_sort
from heap import MaxHeap


app = Flask(__name__)
app.secret_key = "tournament-ranking-secret-key"

team_bst = TeamBST()
BASE_DATA_FILE = "data.json"


def get_data_file():

    if "tournament_id" not in session:

        session["tournament_id"] = uuid.uuid4().hex

    tournament_id = session["tournament_id"]

    return f"data_{tournament_id}.json"
def save_data():

    teams = team_bst.inorder()

    data = []

    for team in teams:
        data.append(team.to_dict())

    with open(get_data_file(), "w") as file:
        json.dump(data, file, indent=4)
def load_data():

    data_file = get_data_file()

    if os.path.exists(data_file):

        with open(data_file, "r") as file:
            content = file.read().strip()

        if content:

            data = json.loads(content)

            for team_data in data:

                team = Team.from_dict(team_data)

                team_bst.insert(team)

        return
    if session.get("tournament_initialized", False):

        return
    if os.path.exists(BASE_DATA_FILE):

        with open(BASE_DATA_FILE, "r") as file:
            content = file.read().strip()

        if content:

            data = json.loads(content)

            for team_data in data:

                team = Team.from_dict(team_data)

                team_bst.insert(team)

            save_data()
@app.before_request
def prepare_tournament():

    global team_bst

    team_bst = TeamBST()

    load_data()

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
@app.route("/reset", methods=["POST"])
def reset_tournament():

    global team_bst

    team_bst = TeamBST()

    data_file = get_data_file()

    if os.path.exists(data_file):

        os.remove(data_file)

    session["tournament_initialized"] = True

    return redirect("/")
if __name__ == "__main__":

    app.run(debug=True)

