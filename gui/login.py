import customtkinter
from tkinter import messagebox
from db.database import get_admin_by_username
from utils.hashing import check_password
from gui.dashboard import afficher_dashboard

# --- Page de connexion ---
def afficher_login():
    global login_win, entry_user, entry_pass
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")

    login_win = customtkinter.CTk()
    login_win.title("Connexion - Gestion Concours")
    login_win.geometry("400x350")

    frame = customtkinter.CTkFrame(login_win, width=350, height=250, corner_radius=10)
    frame.pack(pady=40)
    frame.pack_propagate(False)

    customtkinter.CTkLabel(frame, text="Connexion Admin", font=("Arial", 20)).pack(pady=15)

    entry_user = customtkinter.CTkEntry(frame, placeholder_text="Nom d'utilisateur")
    entry_user.pack(pady=10)

    entry_pass = customtkinter.CTkEntry(frame, placeholder_text="Mot de passe", show="*")
    entry_pass.pack(pady=10)

    btn = customtkinter.CTkButton(frame, text="Se connecter", command=verifier_login)
    btn.pack(pady=10)

    login_win.mainloop()

# --- Vérification des identifiants ---
def verifier_login():
    username = entry_user.get()
    password = entry_pass.get()

    try:
        admin = get_admin_by_username(username)
    except Exception as err:
        messagebox.showerror("Erreur MySQL", f"Connexion impossible à la base de données :\n{err}")
        return

    if admin and check_password(password, admin["password"]):
        admin_data = {
            "id": admin["id_admin"],
            "username": admin["username"],
            "root": admin["root"],
            "grade": admin.get("grade", "")
        }
        messagebox.showinfo("Succès", f"Bienvenue {username}")
        login_win.destroy()
        afficher_dashboard(admin_data)
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")
