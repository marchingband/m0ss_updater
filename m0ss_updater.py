# flash_gui.py
# -*- coding:utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import serial.tools.list_ports
import subprocess
import threading

def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def burn_firmware(file_path, port, status_label):
    cmd = [
        "bflb-mcu-tool",
        "--chipname=bl616",
        f"--port={port}",
        f"--firmware={file_path}"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout + "\n" + result.stderr
    except Exception as e:
        root.after(0, lambda: (
            messagebox.showerror("Error", str(e)),
            status_label.config(text="Failed", foreground="red")
        ))
        return

    last_line = output.strip().splitlines()[-1] if output.strip() else ""
    if "All Successful" in last_line:
        root.after(0, lambda: (
            messagebox.showinfo("Success", "Firmware burned successfully!"),
            status_label.config(text="Success", foreground="green")
        ))
    else:
        root.after(0, lambda: (
            messagebox.showerror("Failure", "Firmware burning failed.\n\n" + last_line),
            status_label.config(text="Failed", foreground="red")
        ))

def start_burn(file_path, port, status_label):
    status_label.config(text="Burning...", foreground="gray")
    # run burn_firmware in a background thread
    threading.Thread(
        target=burn_firmware,
        args=(file_path, port, status_label),
        daemon=True
    ).start()

def launch_gui():
    global root
    root = tk.Tk()
    root.title("BFLB Flash Tool")
    root.geometry("460x280")

    selected_file = tk.StringVar()
    selected_port = tk.StringVar()

    def choose_file():
        path = filedialog.askopenfilename(filetypes=[("BIN files", "*.bin")])
        if path:
            selected_file.set(path)

    def refresh_ports():
        ports = get_serial_ports()
        if not ports:
            ports = ["No ports found"]
        port_combo['values'] = ports
        selected_port.set(ports[0])

    def do_burn():
        file_path = selected_file.get()
        port = selected_port.get()
        if not file_path or not port or port == "No ports found":
            messagebox.showwarning("Missing Info", "Please select a file and a valid serial port.")
            return
        start_burn(file_path, port, status_label)
    
    ttk.Label(root, text="Serial Port:").pack(pady=(10, 0))
    port_combo = ttk.Combobox(root, textvariable=selected_port, state="readonly")
    port_combo.pack(fill='x', padx=10)

    ttk.Button(root, text="Refresh Ports", command=refresh_ports).pack(pady=(5, 10))
    refresh_ports()

    ttk.Label(root, text="Firmware File:").pack(pady=(10, 0))
    file_entry = ttk.Entry(root, textvariable=selected_file)
    file_entry.pack(fill='x', padx=10)

    ttk.Button(root, text="Browse", command=choose_file).pack(pady=(0, 10))

    ttk.Button(root, text="Burn", command=do_burn).pack(pady=(0, 10))

    global status_label
    status_label = ttk.Label(root, text="Idle", foreground="gray")
    status_label.pack()

    root.mainloop()

if __name__ == "__main__":
    print("m0ss_updater")
    launch_gui()
