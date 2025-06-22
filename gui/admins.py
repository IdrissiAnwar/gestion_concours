import customtkinter
from tkinter import messagebox
from db.database import connect_db
from utils.hashing import hash_password

# --- Fonction d'ajout d'un nouvel admin ---
def ajouter_admin(username, password, grade, contenu_frame, admin_actuel):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
        if cursor.fetchone():
            messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")
            return

        hashed_pw = hash_password(password)
        is_root = 1 if grade == "admin root" else 0

        cursor.execute("INSERT INTO admin (username, password, grade, root) VALUES (%s, %s, %s, %s)",
                       (username, hashed_pw, grade, is_root))
        conn.commit()
        messagebox.showinfo("Succès", "Administrateur ajouté avec succès.")
        afficher_admins(contenu_frame, admin_actuel)
    except Exception as e:
        messagebox.showerror("Erreur SQL", str(e))
    finally:
        conn.close()

# --- Fonction de suppression ---
def supprimer_admin(id_admin, contenu_frame, admin_actuel):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Vérifier le nombre total d'admins
        cursor.execute("SELECT COUNT(*) FROM admin")
        nb_admins = cursor.fetchone()[0]
        if nb_admins <= 1:
            messagebox.showwarning("Refusé", "Vous ne pouvez pas supprimer le dernier administrateur.")
            return

        # Empêcher la suppression de soi-même
        if id_admin == admin_actuel["id"]:
            messagebox.showwarning("Refusé", "Vous ne pouvez pas vous supprimer vous-même.")
            return

        # Vérifier si le compte ciblé est root
        cursor.execute("SELECT root FROM admin WHERE id_admin = %s", (id_admin,))
        target = cursor.fetchone()
        if target and target[0] == 1:
            # Compter le nombre total de roots
            cursor.execute("SELECT COUNT(*) FROM admin WHERE root = 1")
            root_count = cursor.fetchone()[0]
            if root_count <= 1:
                messagebox.showwarning("Refusé", "Vous ne pouvez pas supprimer le dernier admin root.")
                return

            confirm = messagebox.askyesno("Confirmation", "Vous êtes sur le point de supprimer un admin root. Confirmer ?")
            if not confirm:
                return

        cursor.execute("DELETE FROM admin WHERE id_admin = %s", (id_admin,))
        conn.commit()
        messagebox.showinfo("Succès", "Administrateur supprimé.")
        afficher_admins(contenu_frame, admin_actuel)
    except Exception as e:
        messagebox.showerror("Erreur", str(e))
    finally:
        conn.close()

# --- Page interface de gestion des admins ---
def afficher_admins(contenu_frame, admin_actuel):
    for widget in contenu_frame.winfo_children():
        widget.destroy()

    customtkinter.CTkLabel(contenu_frame, text="Gestion des Administrateurs", font=("Arial", 20)).pack(pady=20)

    if admin_actuel is None or admin_actuel.get("root") != 1:
        customtkinter.CTkLabel(contenu_frame, text="Vous n'avez pas les droits pour gérer les administrateurs.",
                               font=("Arial", 14)).pack(pady=20)
        return

    # --- Formulaire d'ajout ---
    form_frame = customtkinter.CTkFrame(contenu_frame)
    form_frame.pack(pady=10)

    entry_username = customtkinter.CTkEntry(form_frame, placeholder_text="Nom d'utilisateur")
    entry_username.grid(row=0, column=0, padx=10, pady=5)

    entry_password = customtkinter.CTkEntry(form_frame, placeholder_text="Mot de passe", show="*")
    entry_password.grid(row=1, column=0, padx=10, pady=5)

    grade_menu = customtkinter.CTkOptionMenu(form_frame, values=["admin root", "admin 2ème grade", "admin 3ème grade"])
    grade_menu.set("admin 3ème grade")
    grade_menu.grid(row=2, column=0, padx=10, pady=5)

    btn_ajouter = customtkinter.CTkButton(form_frame, text="Ajouter Admin", 
        command=lambda: ajouter_admin(entry_username.get(), entry_password.get(), grade_menu.get(), contenu_frame, admin_actuel))
    btn_ajouter.grid(row=3, column=0, padx=10, pady=10)

    # --- Liste des admins existants ---
    table_frame = customtkinter.CTkFrame(contenu_frame)
    table_frame.pack(pady=20, padx=20, fill="x")

    header = customtkinter.CTkLabel(table_frame, text="ID   |   Username   |   Grade", font=("Arial", 14))
    header.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id_admin, username, grade FROM admin")
        rows = cursor.fetchall()

        for i, row in enumerate(rows):
            text = f"{row[0]}     |   {row[1]}   |   {row[2]}"
            label = customtkinter.CTkLabel(table_frame, text=text, font=("Arial", 12))
            label.grid(row=i+1, column=0, sticky="w", padx=10, pady=2)

            btn_supprimer = customtkinter.CTkButton(table_frame, text="Supprimer",
                                fg_color="#c62828", hover_color="#b71c1c", text_color="white",
                                command=lambda id=row[0]: supprimer_admin(id, contenu_frame, admin_actuel))
            btn_supprimer.grid(row=i+1, column=1, padx=5)

    except Exception as e:
        messagebox.showerror("Erreur", str(e))
    finally:
        conn.close()
