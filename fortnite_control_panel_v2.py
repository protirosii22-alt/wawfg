import os
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

APP_TITLE = "FORTNITE CONTROL PANEL"
FORTNITE_URI = "com.epicgames.launcher://apps/Fortnite?action=launch&silent=true"
EPIC_URI = "com.epicgames.launcher://"


class FortniteControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("560x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#0d1320")

        self.status_var = tk.StringVar(value="READY")
        self.detail_var = tk.StringVar(value="Waiting for your command")
        self._build()

    def _button(self, parent, text, command, color="#168fe5"):
        return tk.Button(
            parent, text=text, command=command,
            bg=color, fg="white", activebackground=color,
            activeforeground="white", relief="flat", bd=0,
            font=("Segoe UI", 10, "bold"), cursor="hand2",
            padx=12, pady=12
        )

    def _build(self):
        header = tk.Frame(self.root, bg="#0d1320")
        header.pack(fill="x", padx=28, pady=(24, 14))

        tk.Label(
            header, text="FORTNITE", bg="#0d1320", fg="#38bdf8",
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w")

        tk.Label(
            header, text="CONTROL PANEL  •  WINDOWS",
            bg="#0d1320", fg="#a9b8cc",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(2, 0))

        status_card = tk.Frame(self.root, bg="#192438", padx=18, pady=16)
        status_card.pack(fill="x", padx=28, pady=8)

        top = tk.Frame(status_card, bg="#192438")
        top.pack(fill="x")

        tk.Label(
            top, text="GAME STATUS", bg="#192438", fg="#9fb0c8",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        tk.Label(
            top, textvariable=self.status_var, bg="#192438", fg="#5ee0a0",
            font=("Segoe UI", 12, "bold")
        ).pack(side="right")

        tk.Label(
            status_card, textvariable=self.detail_var,
            bg="#192438", fg="white", font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(8, 0))

        actions = tk.Frame(self.root, bg="#0d1320")
        actions.pack(fill="x", padx=28, pady=(12, 8))

        tk.Label(
            actions, text="GAME ACTIONS", bg="#0d1320", fg="#9fb0c8",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self._button(
            actions, "▶  LAUNCH FORTNITE", self.launch_fortnite
        ).pack(fill="x", pady=4)

        self._button(
            actions, "OPEN EPIC GAMES LAUNCHER",
            self.open_epic, "#33445f"
        ).pack(fill="x", pady=4)

        self._button(
            actions, "↻  REFRESH GAME STATUS",
            self.refresh_status, "#26364d"
        ).pack(fill="x", pady=4)

        note = tk.Frame(self.root, bg="#192438", padx=14, pady=12)
        note.pack(fill="x", padx=28, pady=(12, 6))

        tk.Label(
            note,
            text=("This version launches Fortnite and checks whether it is running.\n"
                  "It does not automate matches, movement, AFK activity,\n"
                  "resource farming, or item opening."),
            bg="#192438", fg="#b7c4d6",
            font=("Segoe UI", 9), justify="left"
        ).pack(anchor="w")

        footer = tk.Frame(self.root, bg="#0d1320")
        footer.pack(fill="x", padx=28, pady=(8, 16))

        tk.Label(
            footer, text="Local time:", bg="#0d1320", fg="#64748b",
            font=("Segoe UI", 8)
        ).pack(side="left")

        self.time_label = tk.Label(
            footer, text="", bg="#0d1320", fg="#64748b",
            font=("Segoe UI", 8)
        )
        self.time_label.pack(side="left", padx=(5, 0))
        self._update_clock()

    def _update_clock(self):
        self.time_label.config(text=datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self._update_clock)

    def _windows_only(self):
        if platform.system() != "Windows":
            messagebox.showinfo(
                "Windows required",
                "The Epic Games launch shortcuts in this program are for Windows."
            )
            return False
        return True

    def launch_fortnite(self):
        if not self._windows_only():
            return
        try:
            os.startfile(FORTNITE_URI)
            self.status_var.set("LAUNCH REQUEST SENT")
            self.detail_var.set("Epic Games was asked to start Fortnite.")
            self.root.after(5000, self.refresh_status)
        except OSError as exc:
            self.status_var.set("LAUNCH ERROR")
            self.detail_var.set("Could not open the Fortnite launch link.")
            messagebox.showerror(
                "Launch failed",
                "Check that Epic Games Launcher is installed and signed in.\n\n"
                + str(exc)
            )

    def open_epic(self):
        if not self._windows_only():
            return
        try:
            os.startfile(EPIC_URI)
            self.status_var.set("EPIC OPEN REQUESTED")
            self.detail_var.set("Epic Games Launcher should open.")
        except OSError as exc:
            self.status_var.set("OPEN ERROR")
            self.detail_var.set("Could not open Epic Games Launcher.")
            messagebox.showerror("Could not open Epic Games", str(exc))

    def refresh_status(self):
        if platform.system() != "Windows":
            self.status_var.set("UNSUPPORTED OS")
            self.detail_var.set("Game status detection is configured for Windows.")
            return
        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq FortniteClient-Win64-Shipping.exe"],
                capture_output=True, text=True, timeout=5,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
            if "FortniteClient-Win64-Shipping.exe" in result.stdout:
                self.status_var.set("RUNNING")
                self.detail_var.set("Fortnite process detected.")
            else:
                self.status_var.set("NOT RUNNING")
                self.detail_var.set("Fortnite process was not detected.")
        except (OSError, subprocess.SubprocessError) as exc:
            self.status_var.set("STATUS UNKNOWN")
            self.detail_var.set("Could not check the Fortnite process.")
            messagebox.showerror("Status check failed", str(exc))


if __name__ == "__main__":
    root = tk.Tk()
    app = FortniteControlPanel(root)
    root.mainloop()
