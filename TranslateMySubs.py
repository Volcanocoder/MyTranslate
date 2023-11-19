import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from googletrans import Translator
from tkinter import messagebox
import srt
from datetime import datetime, timedelta

def translate_and_save(subtitle_file, target_language, output_path, progress_bar):
    try:
        translator = Translator()
        translated_subtitles = []

        with open(subtitle_file, 'r', encoding='utf-8') as f:
            subtitle_generator = srt.parse(f)

            for subtitle in subtitle_generator:
                content = subtitle.content

                translated_content = translator.translate(content, dest=target_language).text

                if translated_content is not None:
                    translated_subtitle = srt.Subtitle(subtitle.index, subtitle.start, subtitle.end, translated_content)
                    translated_subtitles.append(translated_subtitle)
                else:
                    print("ترجمه ناموفق")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(srt.compose(translated_subtitles))

        messagebox.showinfo("ترجمه موفق", "ترجمه با موفقیت انجام شد.")
    except Exception as e:
        messagebox.showerror("خطا", f"خطا: {str(e)}")
    finally:
        progress_bar.stop()
        progress_bar.destroy()


def select_subtitle_file():
    subtitle_file = filedialog.askopenfilename(title="انتخاب فایل زیرنویس")
    if subtitle_file:
        subtitle_file_entry.delete(0, tk.END)
        subtitle_file_entry.insert(0, subtitle_file)

def select_output_path():
    output_path = filedialog.asksaveasfilename(title="ذخیره فایل ترجمه", filetypes=[("SRT files", "*.srt")])
    if output_path:
        if not output_path.endswith('.srt'):
            output_path += '.srt'
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(0, output_path)

def translate_and_show_message():
    subtitle_file = subtitle_file_entry.get()
    target_language = languages[target_language_combobox.get()]
    output_path = output_path_entry.get()

    if subtitle_file and target_language and output_path:
        progress_bar = ttk.Progressbar(root, mode='indeterminate')
        progress_bar.grid(row=4, column=2, pady=10, columnspan=2)
        progress_bar.start()

        root.update()

        translate_and_save(subtitle_file, target_language, output_path, progress_bar)

def is_access_allowed():
    try:
        with open('login_time.txt', 'r') as file:
            login_time_str = file.read()
            login_time = datetime.strptime(login_time_str, "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()
            time_limit = timedelta(days=150000)
            
            if current_time - login_time <= time_limit:
                return True
            else:
                return False
    except FileNotFoundError:
        return False

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username == '1' and password == '1':
        login_time = datetime.now()
        with open('login_time.txt', 'w') as file:
            file.write(login_time.strftime("%Y-%m-%d %H:%M:%S"))
        
        messagebox.showinfo("به به!", "♥خوش آمدید")
        login_window.destroy()
        root.deiconify()
    else:
        messagebox.showerror("خطا در لاگین", "نام کاربری یا رمز عبور اشتباه است.")

root = tk.Tk()
root.title("برنامه مبدل ترجمه زیرنویس")
root.configure(bg='#232D3F')

window_width = 520
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

target_language_label = tk.Label(root, text="انتخاب زبان:")
target_language_label.grid(row=0, column=0, pady=10, columnspan=2)
target_language_label.configure(bg='#005B41', fg='white') 

languages = {
    'انگلیسی': 'en',
    'فرانسوی': 'fr',
    'آلمانی': 'de',
    'اسپانیایی': 'es',
    'فارسی': 'fa',
    'ایتالیایی': 'it',
    'عربی': 'ar',
    'روسی': 'ru',
    'چینی ساده': 'zh-CN',
    'چینی سنتی': 'zh-TW',
    'ژاپنی': 'ja',
    'ترکی': 'tr',
    'بلغاری': 'bg',
    'یونانی': 'el',
    'تایلندی': 'th',
    'لهستانی': 'pl',
    'پرتغالی': 'pt',
}

target_language_combobox = ttk.Combobox(root, values=list(languages.keys()), width=30)
target_language_combobox.grid(row=0, column=2, pady=10, columnspan=2)

subtitle_label = tk.Label(root, text="انتخاب فایل زیرنویس:")
subtitle_label.grid(row=1, column=0, pady=10, columnspan=2)

subtitle_file_entry = tk.Entry(root, width=30)
subtitle_file_entry.grid(row=1, column=2, pady=10, columnspan=2)

select_subtitle_button = tk.Button(root, text="انتخاب فایل زیرنویس", command=select_subtitle_file)
select_subtitle_button.grid(row=1, column=4, pady=10, columnspan=1)

output_path_label = tk.Label(root, text="انتخاب مسیر ذخیره ترجمه:")
output_path_label.grid(row=2, column=0, pady=10, columnspan=2)

output_path_entry = tk.Entry(root, width=30)
output_path_entry.grid(row=2, column=2, pady=10, columnspan=2)

select_output_button = tk.Button(root, text="انتخاب مسیر ذخیره", command=select_output_path)
select_output_button.grid(row=2, column=4, pady=10, columnspan=1)

translate_button = tk.Button(root, text="ترجمه", command=translate_and_show_message, width=30)
translate_button.grid(row=3, column=2, pady=20, columnspan=2)
translate_button.configure(bg='#005B41', fg='white') 

login_window = tk.Tk()
login_window.title("ورود به برنامه")
login_window_width = 320
login_window_height = 180
login_window.configure(bg='#232D3F') 

login_screen_width = login_window.winfo_screenwidth()
login_screen_height = login_window.winfo_screenheight()
x = (login_screen_width - login_window_width) // 2
y = (login_screen_height - login_window_height) // 2
login_window.geometry(f"{login_window_width}x{login_window_height}+{x}+{y}")

username_label = tk.Label(login_window, text="نام کاربری:")
username_label.grid(row=0, column=0, pady=10, columnspan=2)
username_label.configure(bg='#008170', fg='black')  

username_entry = tk.Entry(login_window, width=30)
username_entry.grid(row=0, column=2, pady=10, columnspan=2)

password_label = tk.Label(login_window, text="رمز عبور:")
password_label.grid(row=1, column=0, pady=10, columnspan=2)

password_label.configure(bg='#008170', fg='black') 

password_entry = tk.Entry(login_window, show="*", width=30)
password_entry.grid(row=1, column=2, pady=10, columnspan=2)

login_button = tk.Button(login_window, text="ورود", command=login, width=25)
login_button.grid(row=2, column=2, pady=20, columnspan=2)

root.withdraw()

login_window.mainloop()

#volcanocoder♥