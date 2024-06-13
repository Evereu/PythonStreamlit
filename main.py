import json
import os
from calendar import monthrange
from datetime import timedelta, datetime
import streamlit as st
import pandas as pd
from Models.Movie import Movie
from Models.Reservation import Reservation
from Models.User import User

st.title('Wypożyczalnia filmów')

movies = [
    Movie('Movie1', 15.00, 2010),
    Movie('Movie2', 15.00, 2001),
    Movie('Movie3', 13.00, 2018),
    Movie('Movie4', 11.00, 1993)
]

users = [
    User(1, "Jan", "Kowalski"),
    User(2, "Piotr", "Nowak"),
    User(3, "Kapitan", "Bomba")
]

reservations = []


def save_reservations(reservat):
    if os.path.exists('Reservations.json') and os.path.getsize('Reservations.json') > 0:
        with open('Reservations.json', 'r') as file:
            datas = json.load(file)

    else:
        datas = []

    new_reservation_dict = {
        "user": {
            "id": reservat.user.id,
            "first_name": reservat.user.first_name,
            "last_name": reservat.user.last_name
        },
        "movie": {
            "title": reservat.movie.title,
            "price": reservat.movie.price,
            "year": reservat.movie.year
        },
        "date_from": reservat.date_from.isoformat(),
        "date_to": reservat.date_to.isoformat(),
        "cost": reservat.cost
    }

    datas.append(new_reservation_dict)
    with open('Reservations.json', 'w') as file:
        json.dump(datas, file, indent=4)


def read_reservations():
    if os.path.exists('Reservations.json'):
        if os.path.getsize('Reservations.json') > 0:
            with open('Reservations.json', 'r') as f:
                data = json.load(f)
                for item in data:
                    user_data = item['user']
                    user = User(user_data['id'], user_data['first_name'], user_data['last_name'])

                    movie_data = item['movie']
                    movie = Movie(movie_data['title'], movie_data['price'], movie_data['year'])

                    reservation = Reservation(user, movie, item['date_from'], item['date_to'], item['cost'])
                    reservations.append(reservation)


tab1, tab2, tab3, tab4 = st.tabs(["Dostępne filmy", "Panel wypożyczenia", "Aktualnie wypożyczone", "Wykres wypożyczeń"])
with tab1:
    movies_data = [{'Title': movie.title, 'Price': movie.price, 'Year': movie.year} for movie in movies]

    movies_df = pd.DataFrame(movies_data)

    st.title("Lista dostępnych filmów")

    st.table(movies_df)

with tab2:
    st.title("Wypożycz film")

    names = [user for user in users]
    select_user = st.selectbox("Kim jesteś?", names)

    movies_title = [movie.title for movie in movies]
    select_movie_title = st.selectbox("Wybierz film", movies_title)

    selected_movie = next((movie for movie in movies if movie.title == select_movie_title), None)

    date_from = st.date_input("Data wypożyczenia")
    days = st.number_input("Ilość dni wypożyczenia", min_value=1, step=1)

    date_to = date_from + timedelta(days=days)
    cost = selected_movie.price * days

    st.title("Podsumowanie")
    if selected_movie:
        st.write(f"Użytkownik: {select_user}")
        st.write(f"Film: {selected_movie.title}")
        st.write(f"Data wypożyczenia: {date_from}")
        st.write(f"Data zwrotu: {date_to}")
        st.write(f"Koszt: {cost} PLN")

    if st.button("Zapisz rezerwację"):
        reservat = Reservation(select_user, selected_movie, date_from, date_to, cost)

        save_reservations(reservat)

    read_reservations()

    reservation_data = [{
        'Tytuł': reservation.movie.title,
        'Data od': reservation.date_from,
        'Data do': reservation.date_to,
        'Koszt': f"{reservation.cost} PLN"
    } for reservation in reservations]


with tab3:
    read_reservations()

    options = [(f"{user.first_name} {user.last_name}", user.id) for user in users]

    selected_user_id = st.selectbox("Wybierz użytkownika", options)

    selected_user = next((user for user in users if user.id == selected_user_id[1]), None)

    if selected_user:
        user_reservations = [reservation for reservation in reservations if reservation.user.id == selected_user.id]


        reservation_data = [{
            'Tytuł': reservation.movie.title,
            'Data od': reservation.date_from,
            'Data do': reservation.date_to,
            'Koszt': f"{reservation.cost}"
        } for reservation in user_reservations]

        reservation_df = pd.DataFrame(reservation_data)

        st.title("Lista wypożyczeń użytkownika")

        st.table(reservation_df)

with tab4:
    st.title("Wypożyczenia w tym miesiącu")

    read_reservations()

    year = datetime.now().year
    month = datetime.now().month

    days = monthrange(year, month)[1]

    reservations_per_day = [0] * days

    for reservation in reservations:
        if datetime.strptime(reservation.date_from, "%Y-%m-%d").month == month:
            day = datetime.strptime(reservation.date_from, "%Y-%m-%d").day
            reservations_per_day[day - 1] += 1

    st.line_chart(reservations_per_day)
