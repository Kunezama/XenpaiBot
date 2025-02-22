import random
import os
import time
from datetime import datetime

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

quotes_english = [
    "Life is a journey, not a destination. - Ralph Waldo Emerson",
    "Be the change that you wish to see in the world. - Mahatma Gandhi",
    "Success is the result of preparation, hard work, and learning from failure. - Colin Powell",
]

quotes_indonesia = [
    "Hidup adalah perjalanan, bukan tujuan. - Ralph Waldo Emerson",
    "Jadilah perubahan yang ingin kamu lihat di dunia. - Mahatma Gandhi",
    "Kesuksesan adalah hasil dari persiapan, kerja keras, dan belajar dari kegagalan. - Colin Powell",
]

def generate_quote(language):
    """Menghasilkan kutipan acak berdasarkan bahasa."""
    if language == "english" and quotes_english:
        return random.choice(quotes_english)
    elif language == "indonesia" and quotes_indonesia:
        return random.choice(quotes_indonesia)
    else:
        return "\033[91mTidak ada kutipan yang tersedia untuk bahasa ini.\033[0m"

def save_quote(quote):
    """Menyimpan kutipan ke dalam file."""
    try:
        with open("quotes.txt", "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp}: {quote}\n")
        print("\033[32mKutipan telah disimpan ke quotes.txt!\033[0m") # Warna hijau
    except Exception as e:
        print(f"\033[91mTerjadi kesalahan saat menyimpan kutipan: {e}\033[0m") # Warna merah

def show_saved_quotes():
    """Menampilkan kutipan yang telah disimpan."""
    try:
        with open("quotes.txt", "r") as file:
            quotes = file.readlines()
            if quotes:
                print("\033[94mKutipan-kutipan yang disimpan:\033[0m") # Warna biru
                for quote in quotes:
                    print(quote.strip())
            else:
                print("\033[93mBelum ada kutipan yang disimpan.\033[0m") # Warna kuning
    except FileNotFoundError:
        print("\033[93mFile quotes.txt belum ada.\033[0m") # Warna kuning
    except Exception as e:
        print(f"\033[91mTerjadi kesalahan saat membaca file: {e}\033[0m") # Warna merah

def main():
    """Fungsi utama program."""
    while True:
        clear_screen()
        print("\033[92m=== QUOTE GENERATOR ===\033[0m") # Warna hijau
        print("\033[1;97mAuthor  : \033[1;93mKanezama\033[0m")
        print("\033[1;97mVersion : 1.0\033[0m")
        print("\033[1;96mXenpaiBot Is Number One Bot For Pentester\033[0m")
        print("\033[0m========================\033[0m")

        print("\033[94m\nPilih bahasa / Choose language:\033[0m") # Warna biru
        print("1. \033[93mIndonesia\033[0m") # Warna kuning
        print("2. \033[93mEnglish\033[0m") # Warna kuning
        print("3. \033[95mLihat Kutipan Tersimpan\033[0m") # Warna magenta
        print("4. \033[91mKeluar\033[0m") # Warna merah
        choice = input("\033[1;94m\nr00t@XenpaiBot~ \033[0m").strip() # Warna biru muda

        if choice == "1":
            language = "indonesia"
        elif choice == "2":
            language = "english"
        elif choice == "3":
            show_saved_quotes()
            input("\033[94mTekan Enter untuk kembali ke menu utama...\033[0m") # Warna biru
            continue
        elif choice == "4":
            print("\033[93mTerima kasih telah menggunakan Quote Generator! Selamat tinggal!\033[0m")
            break
        else:
            print("\033[91mPilihan tidak valid. Silakan coba lagi.\033[0m") # Warna merah
            time.sleep(2)
            continue

        while True:
            print("\033[92m\nBerikut adalah kutipan inspiratif untukmu hari ini:\033[0m") 
            current_quote = generate_quote(language)

            for _ in range(1):
                print(current_quote)
                time.sleep(0.5)

            save_choice = input("\033[92mApakah kamu ingin menyimpan kutipan ini? (y/n): \033[0m").strip().lower()
            if save_choice == "y":
                save_quote(current_quote)

            again = input("\033[92mApakah kamu ingin kutipan lagi? (y/n): \033[0m").strip().lower() 
            if again != "y":
                print("\033[93mTerima kasih! Semoga harimu menyenangkan!\033[0m")
                time.sleep(2)
                break

if __name__ == "__main__":
    main()
