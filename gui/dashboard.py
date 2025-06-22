import customtkinter
import mysql.connector
from db.database import connect_db
from gui.admins import afficher_admins

# --- Fonction pour compter les enregistrements d'une table ---
def count_rows(table_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        print(f"Erreur SQL ({table_name}) :", e)
        return "-"
    finally:
        conn.close()

# --- Dashboard principal ---
def afficher_dashboard(admin_actuel):
    app = customtkinter.CTk()
    app.title("Dashboard - Gestion des Concours")
    app.geometry("1100x650")
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")

    current_theme = ["light"]

    light_colors = {
        "menu": "#00bcd4",
        "header": "#f5f5f5",
        "background": "#f9f9f9",
        "card1": "#c8e6c9",
        "card2": "#fff9c4",
        "card3": "#bbdefb",
        "text": "black",
        "button": "white"
    }

    dark_colors = {
        "menu": "#004d40",
        "header": "#1a1a1a",
        "background": "#121212",
        "card1": "#2e7d32",
        "card2": "#fbc02d",
        "card3": "#1976d2",
        "text": "white",
        "button": "#333333"
    }

    menu_frame = customtkinter.CTkFrame(app, width=220)
    menu_frame.pack(side="left", fill="y")
    menu_frame.pack_propagate(False)

    header = customtkinter.CTkFrame(app, height=60)
    header.pack(side="top", fill="x")
    title_label = customtkinter.CTkLabel(header, text="Dashboard", font=("Arial", 22))
    title_label.pack(pady=15, padx=20, anchor="w")

    contenu_frame = customtkinter.CTkFrame(app)
    contenu_frame.pack(side="left", fill="both", expand=True)

    def update_theme_ui(theme_colors):
        menu_frame.configure(fg_color=theme_colors["menu"])
        header.configure(fg_color=theme_colors["header"])
        contenu_frame.configure(fg_color=theme_colors["background"])
        title_label.configure(text_color=theme_colors["text"])

    def toggle_theme():
        if current_theme[0] == "light":
            customtkinter.set_appearance_mode("dark")
            current_theme[0] = "dark"
            update_theme_ui(dark_colors)
        else:
            customtkinter.set_appearance_mode("light")
            current_theme[0] = "light"
            update_theme_ui(light_colors)

    update_theme_ui(light_colors)

    customtkinter.CTkLabel(menu_frame, text="Admin Dashboard", font=("Arial", 20, "bold"),
                           text_color="white").pack(pady=(30, 20))

    def afficher_vue(nom_vue):
        for widget in contenu_frame.winfo_children():
            widget.destroy()
        title_label.configure(text=nom_vue.capitalize())

        if nom_vue == "dashboard":
            cards_frame = customtkinter.CTkFrame(contenu_frame)
            cards_frame.pack(pady=20, padx=30)

            def create_card(parent, titre, valeur, couleur):
                c = customtkinter.CTkFrame(parent, width=200, height=100, fg_color=couleur, corner_radius=10)
                c.pack(side="left", padx=10)
                c.pack_propagate(False)
                customtkinter.CTkLabel(c, text=str(valeur), font=("Arial", 22, "bold"), text_color="black").pack(pady=(10, 2))
                customtkinter.CTkLabel(c, text=titre, font=("Arial", 14), text_color="black").pack()

            theme = dark_colors if current_theme[0] == "dark" else light_colors

            create_card(cards_frame, "Candidats", count_rows("candidat"), theme["card1"])
            create_card(cards_frame, "Salles", count_rows("salle"), theme["card2"])
            create_card(cards_frame, "Concours", count_rows("concours"), theme["card3"])

            customtkinter.CTkLabel(contenu_frame, text="Bienvenue dans le dashboard",
                                   font=("Arial", 20)).pack(pady=30)

        elif nom_vue == "admins":
            afficher_admins(contenu_frame, admin_actuel)
        else:
            customtkinter.CTkLabel(contenu_frame, text=f"Page {nom_vue.capitalize()}", font=("Arial", 18)).pack(pady=40)

    menu_buttons = [
        ("Dashboard", lambda: afficher_vue("dashboard")),
        ("Candidats", lambda: afficher_vue("candidats")),
        ("Salles", lambda: afficher_vue("salles")),
        ("Concours", lambda: afficher_vue("concours")),
        ("Affectation", lambda: afficher_vue("affectation")),
        ("Déconnexion", app.destroy)
    ]

    if admin_actuel and admin_actuel.get("root") == 1:
        menu_buttons.insert(1, ("Admins", lambda: afficher_vue("admins")))

    for label, command in menu_buttons:
        customtkinter.CTkButton(menu_frame, text=label, width=180, corner_radius=8,
                                fg_color="white", text_color="black", hover_color="#e0f7fa",
                                command=command).pack(pady=5)

    customtkinter.CTkButton(menu_frame, text="Switch Thème", command=toggle_theme,
                            width=180, fg_color="#004d40", text_color="white").pack(pady=40)

    afficher_vue("dashboard")
    app.mainloop()
