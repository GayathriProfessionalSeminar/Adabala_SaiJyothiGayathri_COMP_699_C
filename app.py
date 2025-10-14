import streamlit as st
import chess
import chess.svg
import pandas as pd
import sqlite3
from datetime import datetime
from io import BytesIO
import base64

st.set_page_config(page_title="ChessMind Mirror", layout="wide")

# Database setup
conn = sqlite3.connect("chessmind.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, age TEXT, language TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS games
             (username TEXT, moves TEXT, result TEXT, timestamp TEXT)''')
conn.commit()

# Session state for game
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "move_history" not in st.session_state:
    st.session_state.move_history = []
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "game_active" not in st.session_state:
    st.session_state.game_active = False

# Profile management
st.sidebar.header("Player Profile")

def create_profile(username, age, language):
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, age, language))
        conn.commit()
        st.success("Profile created successfully.")
    except sqlite3.IntegrityError:
        st.error("Username already exists.")

def login(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    if user:
        st.session_state.current_user = username
        st.success(f"Logged in as {username}")
    else:
        st.error("Username does not exist.")

def logout():
    st.session_state.current_user = None
    st.session_state.game_active = False
    st.success("Logged out successfully.")

def delete_profile(username):
    c.execute("DELETE FROM users WHERE username=?", (username,))
    c.execute("DELETE FROM games WHERE username=?", (username,))
    conn.commit()
    if st.session_state.current_user == username:
        st.session_state.current_user = None
    st.success("Profile and game history deleted.")

def update_profile(old_username, new_username, age, language):
    try:
        c.execute("UPDATE users SET username=?, age=?, language=? WHERE username=?", 
                  (new_username, age, language, old_username))
        c.execute("UPDATE games SET username=? WHERE username=?", (new_username, old_username))
        conn.commit()
        st.session_state.current_user = new_username
        st.success("Profile updated successfully.")
    except sqlite3.IntegrityError:
        st.error("New username already exists.")

if st.session_state.current_user is None:
    st.sidebar.text_input("Username", key="new_user")
    st.sidebar.text_input("Age", key="new_age")
    st.sidebar.text_input("Language", key="new_lang")
    if st.sidebar.button("Create Profile"):
        create_profile(st.session_state.new_user, st.session_state.new_age, st.session_state.new_lang)

    st.sidebar.text_input("Login Username", key="login_user")
    if st.sidebar.button("Login"):
        login(st.session_state.login_user)
else:
    st.sidebar.write(f"Logged in as {st.session_state.current_user}")
    st.sidebar.button("Logout", on_click=logout)
    st.sidebar.text_input("New Username", key="update_user")
    st.sidebar.text_input("Age", key="update_age")
    st.sidebar.text_input("Language", key="update_lang")
    if st.sidebar.button("Update Profile"):
        update_profile(st.session_state.current_user, st.session_state.update_user,
                       st.session_state.update_age, st.session_state.update_lang)
    if st.sidebar.button("Delete Profile"):
        delete_profile(st.session_state.current_user)

# Game management
if st.session_state.current_user:
    st.header("ChessMind Mirror")

    def start_game():
        st.session_state.board = chess.Board()
        st.session_state.move_history = []
        st.session_state.game_active = True

    if st.button("Start New Game"):
        start_game()

    if st.session_state.game_active:
        move_input = st.text_input("Enter your move (UCI format, e.g., e2e4):", key="move")
        if st.button("Make Move"):
            try:
                move = chess.Move.from_uci(move_input)
                if move in st.session_state.board.legal_moves:
                    st.session_state.board.push(move)
                    st.session_state.move_history.append(move_input)
                else:
                    st.error("Illegal move.")
            except:
                st.error("Invalid move format.")

        if st.button("Undo Last Move") and st.session_state.move_history:
            st.session_state.board.pop()
            st.session_state.move_history.pop()

        if st.button("Resign"):
            c.execute("INSERT INTO games VALUES (?, ?, ?, ?)",
                      (st.session_state.current_user, ",".join(st.session_state.move_history), "Resigned",
                       datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            st.session_state.game_active = False
            st.success("Game resigned and saved.")

        st.write("Current Board")
        st.write(st.session_state.board)

        if st.button("Finish Game and Save"):
            result = "Win/Loss/Draw"  # Placeholder
            c.execute("INSERT INTO games VALUES (?, ?, ?, ?)",
                      (st.session_state.current_user, ",".join(st.session_state.move_history), result,
                       datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            st.session_state.game_active = False
            st.success("Game saved.")

    # Completed games
    st.subheader("Completed Games")
    c.execute("SELECT * FROM games WHERE username=?", (st.session_state.current_user,))
    games = c.fetchall()
    if games:
        df = pd.DataFrame(games, columns=["Username", "Moves", "Result", "Timestamp"])
        st.table(df)
    else:
        st.info("No games found.")
