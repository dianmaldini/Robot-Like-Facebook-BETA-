import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import os

# --- Library Selenium ---
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as sel_ex

# Event untuk sinyal
stop_event = threading.Event()
login_event = threading.Event()

class BoomLikeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Robot Liker (Beta)")
        self.root.geometry("650x700")
        self.root.configure(bg="#f0f2f5") # Warna background khas FB (abu-abu sangat muda)
        
        # --- STYLE CONFIGURATION ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", padding=5)
        
        # --- HEADER SECTION ---
        self.header_frame = tk.Frame(root, bg="#1877F2", height=80)
        self.header_frame.pack(fill="x", side="top")
        
        tk.Label(self.header_frame, text="FACEBOOK ROBOT LIKER", 
                 font=("Segoe UI", 18, "bold"), bg="#1877F2", fg="white").pack(pady=(20, 5))
        
        tk.Label(self.header_frame, text="Beta Version | Auto-Scroll & Anti-Spam", 
                 font=("Segoe UI", 9), bg="#1877F2", fg="#e4e6eb").pack(pady=(0, 15))

        # --- MAIN CONTENT FRAME ---
        self.main_frame = tk.Frame(root, bg="white", padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 1. Input URL
        tk.Label(self.main_frame, text="Target URL (Beranda / Profil / Grup):", 
                 bg="white", font=("Segoe UI", 10, "bold"), fg="#050505").pack(anchor="w")
        
        self.entry_url = tk.Entry(self.main_frame, width=60, font=("Segoe UI", 10), bd=2, relief="groove")
        self.entry_url.pack(fill="x", pady=(5, 15), ipady=3)
        self.entry_url.insert(0, "https://www.facebook.com/") 
        
        # 2. Input Jumlah (Dropdown)
        tk.Label(self.main_frame, text="Target Jumlah Like:", 
                 bg="white", font=("Segoe UI", 10, "bold"), fg="#050505").pack(anchor="w")
        
        self.combo_jumlah = ttk.Combobox(self.main_frame, values=[20, 40, 60, 80, 100, 120, 140], state="readonly", font=("Segoe UI", 10))
        self.combo_jumlah.current(0) 
        self.combo_jumlah.pack(fill="x", pady=(5, 15), ipady=3)
        
        # Info Login
        info_frame = tk.Frame(self.main_frame, bg="#e7f3ff", padx=10, pady=5)
        info_frame.pack(fill="x", pady=(0, 15))
        tk.Label(info_frame, text="ℹ️ Info: Sesi login disimpan otomatis di folder 'profile_fb'.", 
                 bg="#e7f3ff", fg="#1877F2", font=("Segoe UI", 9)).pack(anchor="w")
        
        # 3. Tombol Aksi (Grid Layout biar rapi)
        self.btn_frame = tk.Frame(self.main_frame, bg="white")
        self.btn_frame.pack(fill="x", pady=10)
        
        self.btn_start = tk.Button(self.btn_frame, text="▶ MULAI PROSES", 
                                   command=self.start_thread, 
                                   bg="#42b72a", fg="white", font=("Segoe UI", 10, "bold"), 
                                   relief="flat", cursor="hand2")
        self.btn_start.pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=8)
        
        self.btn_login = tk.Button(self.btn_frame, text="✔ SAYA SUDAH LOGIN", 
                                   command=self.tandai_login, state="disabled", 
                                   bg="#f7b928", fg="white", font=("Segoe UI", 10, "bold"), 
                                   relief="flat", cursor="hand2")
        self.btn_login.pack(side="left", expand=True, fill="x", padx=5, ipady=8)

        self.btn_stop = tk.Button(self.btn_frame, text="⏹ STOP", 
                                  command=self.stop_process, 
                                  bg="#fa383e", fg="white", font=("Segoe UI", 10, "bold"), 
                                  relief="flat", cursor="hand2")
        self.btn_stop.pack(side="left", expand=True, fill="x", padx=(5, 0), ipady=8)

        # 4. Log Area
        tk.Label(self.main_frame, text="Log Aktivitas Robot:", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 5))
        self.log_area = scrolledtext.ScrolledText(self.main_frame, height=10, state='disabled', font=("Consolas", 9), bg="#f0f2f5", bd=0)
        self.log_area.pack(fill="both", expand=True)

        # --- FOOTER SECTION ---
        self.footer_frame = tk.Frame(root, bg="#f0f2f5", height=30)
        self.footer_frame.pack(fill="x", side="bottom", pady=5)
        tk.Label(self.footer_frame, text="All Right Reserved - Albani Computer", 
                 bg="#f0f2f5", fg="#65676b", font=("Segoe UI", 8)).pack()

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def stop_process(self):
        stop_event.set()
        self.log("✋ Tombol STOP ditekan. Robot akan berhenti sejenak lagi...")

    def tandai_login(self):
        login_event.set()
        self.btn_login.config(state="disabled", bg="#cccccc") # Ubah warna jadi abu saat disabled

    def start_thread(self):
        url = self.entry_url.get()
        try:
            jumlah = int(self.combo_jumlah.get())
        except:
            jumlah = 20
        
        if not url: return  
        stop_event.clear()
        login_event.clear()
        
        # Update status tombol
        self.btn_start.config(state="disabled", bg="#cccccc")
        self.btn_login.config(state="normal", bg="#f7b928")
        
        threading.Thread(target=self.run_boom_like, args=(url, jumlah), daemon=True).start()

    def tutup_popup_mengganggu(self, driver):
        try:
            dialogs = driver.find_elements(By.XPATH, "//div[@role='dialog']")
            if len(dialogs) > 0:
                self.log("⚠️ Popup terdeteksi. Mencoba menutup...")
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(1)
        except: pass

    def run_boom_like(self, url, target_jumlah):
        driver = None
        try:
            current_dir = os.getcwd()
            profile_dir = os.path.join(current_dir, "profile_fb")
            
            opts = webdriver.ChromeOptions()
            opts.add_argument("--disable-notifications")
            opts.add_argument(f"user-data-dir={profile_dir}") 
            
            # Menambahkan argument agar window tidak muncul text "Chrome is being controlled..."
            opts.add_experimental_option("excludeSwitches", ["enable-automation"])
            opts.add_experimental_option('useAutomationExtension', False)
            
            driver = webdriver.Chrome(options=opts)
            driver.get("https://www.facebook.com")
            
            self.log("Menunggu verifikasi login...")
            while not login_event.is_set():
                if stop_event.is_set(): return
                time.sleep(1)
            
            self.log("Login Terkonfirmasi. Membuka Target...")
            driver.get(url)
            time.sleep(5)
            
            liked_count = 0
            processed_ids = set()

            while liked_count < target_jumlah:
                if stop_event.is_set(): break
                
                self.tutup_popup_mengganggu(driver)

                try:
                    # XPATH KETAT (Anti-Unlike)
                    buttons = driver.find_elements(By.XPATH, 
                        "//div[@role='button' and (contains(@aria-label, 'Suka') or contains(@aria-label, 'Like')) and not(contains(@aria-label, 'Hapus')) and not(contains(@aria-label, 'Batal')) and not(contains(@aria-label, 'Remove'))]")
                    
                    found_in_this_scroll = False
                    
                    for btn in buttons:
                        if stop_event.is_set() or liked_count >= target_jumlah: break
                        
                        if btn.id in processed_ids: continue

                        try:
                            if btn.is_displayed():
                                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
                                time.sleep(1)
                                
                                driver.execute_script("arguments[0].click();", btn)
                                
                                processed_ids.add(btn.id)
                                liked_count += 1
                                found_in_this_scroll = True
                                
                                self.log(f"👍 Berhasil Like ke-{liked_count}")
                                
                                time.sleep(2) # Jeda 2 Detik
                                
                                # Scroll Agresif
                                driver.execute_script("window.scrollBy(0, 500);")
                                time.sleep(1)
                                
                        except Exception: pass 

                    if not found_in_this_scroll:
                        self.log("Memuat postingan baru (Scrolling)...")
                        driver.execute_script("window.scrollBy(0, 800);")
                        time.sleep(3)
                
                except Exception as e:
                    self.log(f"Error loop: {e}")
                    time.sleep(2)

            self.log(f"🏁 SELESAI! Total Like Terkirim: {liked_count}")
            messagebox.showinfo("Selesai", f"Robot Berhasil Memberikan {liked_count} Like.")

        except Exception as e:
            self.log(f"Error Fatal: {e}")
        finally:
            if driver: driver.quit()
            self.btn_start.config(state="normal", bg="#42b72a")
            self.btn_login.config(state="disabled", bg="#cccccc")

if __name__ == "__main__":
    root = tk.Tk()
    app = BoomLikeApp(root)
    root.mainloop()