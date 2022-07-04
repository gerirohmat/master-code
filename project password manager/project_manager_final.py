from cryptography.fernet import Fernet
import os.path
import sys
import pandas as pd


class PasswordManager:

    def __init__(self):
        self.kunci = None
        self.password_file = 'password.pass'
        self.password_dict = {}

    def kunci_gen(self): ## hasil value (none type is not callable)
        file_kunci =os.path.exists('kunci.key')

        if file_kunci == False:
            self.kunci = Fernet.generate_key()
            with open('kunci.key', 'wb') as f:
                        f.write(self.kunci)
            print('file berhasil dibuat')
        else:
            with open('kunci.key','rb') as f:
                self.kunci = f.read()
            print('file berhasil di akses')

    def file_password_gen(self):

        password_loc = os.path.exists('password.pass')

        if password_loc == False:
            with open(os.path.join(sys.path[0], self.password_file), 'w') as f:
                pass
            print('file berhasil dibuat')
        else:
            with open('password.pass','r') as f:
                for baris in f:
                    situs, encripted = baris.split(":")
                    self.password_dict[situs] = Fernet(self.kunci).decrypt(encripted.encode()).decode()
            print('file berhasil di akses')

    def tambah_password(self, situs, password):
        self.password_dict[situs] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.kunci).encrypt(password.encode())
                f.write(situs + ":" + encrypted.decode() + "\n")
            print ("password berhasil ditambahkan")

    def list_password(self):

        web_pass = list(self.password_dict.keys())

        list_web = {
            'List website : ' : web_pass
        }

        data_web = pd.DataFrame(data=list_web)
        data_web.index += 1
        if data_web.empty == False:
            print (data_web)
        else :
            print("Tidak ada Password yang disimpan, tolong tambahkan password ter;ebih dahulu")

    def lihat_password(self,situs):
        return self.password_dict[situs]

def main():

    password = {

    }

    pm = PasswordManager()

    pm.kunci_gen()
    pm.file_password_gen()

    print(""" Pilih opsi yang ada :
    1. Lihat list website yang disimpan.
    2. Tambahkan Password baru.
    3. Akses password yang ada.
    4. Exit.
    """)

    done = False

    while not done:
        eksekusi = input("pilih nomor : ")
        if eksekusi == "1":
            pm.list_password()
        elif eksekusi == "2":
            situs = input("nama website : ")
            password = input("Masukkan password anda : ")
            pm.tambah_password(situs, password)
        elif eksekusi == "3":
            situs = input("Nama website : ")
            print(f"Password {situs} anda adalah {pm.lihat_password(situs)}")
        elif eksekusi == "4":
            done = True
            print("Terimakasih")
        else:
            print("Pilih lainnya : ")

if __name__ == "__main__":
    main()