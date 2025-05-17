import mysql.connector
from locust import HttpUser, task, between
import random

class AirbnbUser(HttpUser):
    host = "http://localhost:8000"  # Ganti dengan host API kamu
    wait_time = between(1, 3)  # Waktu tunggu antar request (1 - 3 detik)

    def on_start(self):
        # Hubungkan ke database MySQL
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",  # ganti dengan username MySQL Anda
            password="",  # ganti dengan password MySQL Anda
            database="db_tugasmdik"
        )
        self.cursor = self.conn.cursor()

        # Ambil daftar neighbourhood dari database
        self.cursor.execute("SELECT DISTINCT neighbourhood FROM listings_albany")
        self.neighbourhoods = [row[0] for row in self.cursor.fetchall()]

    def on_stop(self):
        # Menutup koneksi ke database setelah setiap user selesai
        self.cursor.close()
        self.conn.close()

    @task(3)
    def get_listings_page_limit(self):
        page = random.randint(1, 5)
        limit = 20
        response = self.client.get(f"/listings_airnb?page={page}&limit={limit}")
        if response.status_code != 200:
            print(f"[PAGE LIMIT] Request failed with status: {response.status_code}")

    @task(2)
    def get_filtered_listings(self):
        room_type = random.choice(["Entire home/apt", "Private room"])
        price = random.choice([50, 100, 150])
        response = self.client.get(f"/listings_airnb?room_type={room_type}&price_lte={price}")
        if response.status_code != 200:
            print(f"[FILTERED] Request failed with status: {response.status_code}")

    @task(1)
    def get_listings_by_type_and_area(self):
        room_type = random.choice(["Entire home/apt", "Private room"])
        neighbourhood = random.choice(self.neighbourhoods)
        response = self.client.get(f"/listings_airnb?room_type={room_type}&neighbourhood={neighbourhood}")
        if response.status_code != 200:
            print(f"[TYPE+AREA] Request failed with status: {response.status_code}")