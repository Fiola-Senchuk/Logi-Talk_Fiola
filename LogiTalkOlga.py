import base64
import io
import os.path
import threading
from email.mime import message
from operator import truediv
from socket import socket, AF_INET, SOCK_STREAM

from customtkinter import *
from tkinter import filedialog
from PIL import Image



green_light_color=[ "#ffffff","#e0f5da","#dbdbdb", "#628a57", "#144207"]
green_dark_color=["#628a57","#7b9e54","#144207","#36591f","#122604"]

red_light_color=[ "#ffffff","#f5dbda","#dbdbdb", "#8a5757", "#420707"]
red_dark_color=["#8a5757","#9e5454","#420707","#591f1f","#260404"]

blue_light_color=[ "#ffffff","#dadbf5","#dbdbdb", "#57588a", "#0d0742"]
blue_dark_color=["#57588a","#59549e","#0d0742","#211f59","#080426"]

pink_light_color=[ "#ffffff","#f5daf3","#dbdbdb", "#8a5782", "#420735"]
pink_dark_color=["#8a5782","#9e5495","#420735","#591f50","#260421"]

yellow_light_color=[ "#ffffff","#f5f5da","#dbdbdb", "#898a57", "#424207"]
yellow_dark_color=["#898a57","#9e8954","#424207","#57591f","#262604"]

orange_light_color=[ "#ffffff","#f5e9da","#dbdbdb", "#8a7557", "#422807"]
orange_dark_color=["#8a7557","#9e7b54","#422807","#59451f","#261404"]

turquoise_light_color=[ "#ffffff","#daf5f3","#dbdbdb", "#578a88", "#074238"]
turquoise_dark_color=["#578a88","#549e92","#074238","#1f594b","#042621"]

purple_light_color=[ "#ffffff","#eadaf5","#dbdbdb", "#6d578a", "#2e0742"]
purple_dark_color=["#6d578a","#7d549e","#2e0742","#481f59","#1a0426"]

white_light_color=[ "#ffffff","#f5f5f2","#dbdbdb", "#8a8a88", "#424242"]
white_dark_color=["#8a8a88","#9e9e9e","#424242","#595959","#262626"]



plant_color=["green_plant.png","yellow_plant.png","orange_plant.png", "red_plant.png","pink_plant.png","purple_plant.png","blue_plant.png", "turquoise_plant.png","black_plant.png"]
big_plant_color=["big_green_plant.png","big_yellow_plant.png","big_orange_plant.png", "big_red_plant.png","big_pink_plant.png","big_purple_plant.png","big_blue_plant.png", "big_turquoise_plant.png","big_black_plant.png"]



big_plant=0
plant=0
teme_color=green_light_color

class MainWindow(CTk):
    def __init__(self):
        super().__init__()



        self.geometry('600x600')
        self.title("Chat")

        self.configure(fg_color=teme_color[1])


        self.username="Fiola"
        self.oldusername="Fiola"
        self.all_messages = []

        self.plant_img = CTkImage(light_image=Image.open(plant_color[plant]), size=(450, 800))
        self.big_plant_img = CTkImage(light_image=Image.open(big_plant_color[big_plant]), size=(200, 550))

        #Menu
        self.label=None
        self.menu_frame=CTkFrame(self, width=30, height=500, fg_color=teme_color[3])
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0, y=0)
        self.is_show_menu=False
        self.speed_animete_menu=-20
        self.btn= CTkButton(self, text='>', command=self.toggle_show_menu, width=20,
                            fg_color=teme_color[0], hover_color=teme_color[2],text_color=teme_color[4],
                            corner_radius=10, bg_color=teme_color[3])
        self.btn.place(x=0, y=0)

        #Chat osnova
        self.chat_field=CTkScrollableFrame(self, fg_color=teme_color[1],
                                            scrollbar_button_color = teme_color[3],
                                            scrollbar_button_hover_color = teme_color[4]
                                        )
        self.chat_field.place(x=0, y=0)




        self.plant_label = CTkLabel(self, image=self.plant_img, text="")
        self.plant_label.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=0)


        #Input and button


        self.message_entry=CTkEntry(self, placeholder_text='...', height=40,
                                    fg_color = teme_color[0], text_color = teme_color[4], border_color=teme_color[4],
                                    corner_radius = 10, bg_color = teme_color[1],placeholder_text_color=teme_color[4]
                                    )
        self.message_entry.place(x=0, y=0)


        self.send_button=CTkButton(self, text='>', width=50, height=40, command=self.send_message,
                                   fg_color=teme_color[0], hover_color=teme_color[2], text_color=teme_color[4],
                                   corner_radius=10, bg_color=teme_color[1]
                                   )
        self.send_button.place(x=0, y=0)

        self.open_img_button=CTkButton(self, text='~', width=50, height=40, command=self.open_image,
                                       fg_color=teme_color[0], hover_color=teme_color[2], text_color=teme_color[4],
                                       corner_radius=10, bg_color=teme_color[1]
                                       )
        self.open_img_button.place(x=0, y=0)

        self.adaptive_ui()

        self.add_message("Image:",
                         CTkImage(Image.open('kitty.jpg'), size=(300, 300)))

        # self.big_plant_label = CTkLabel(self, image=self.big_plant_img, text="")
        # self.big_plant_label.place(x=10, y=50)  # Координаты подбери под скриншот

        # Правая картинка
        try:
            self.sock=socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('0.0.0.0', 8080))
            hello=f"TEXT@{self.username}@[SYSTEM]{self.username} + chat!\n"
            self.sock.send(hello.encode('utf-8'))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            self.add_message(f"Connection error: {e}")

    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu=False
            self.speed_animete_menu*=-1
            self.btn.configure(text=">")
            self.menu_frame.configure(width=30)

            if self.label:
                self.label.destroy()
            if getattr(self, "entry", None):
                self.entry.destroy()
            if getattr(self, "save_button", None):
                self.save_button.destroy()
            if getattr(self, "label_theme", None):
                self.label_theme.destroy()
            if getattr(self, "big_plant_label", None):
                self.big_plant_label.destroy()
        else:
            self.is_show_menu=True
            self.speed_animete_menu*=-1
            self.btn.configure(text='<')

            self.menu_frame.configure(width=200)

            self.big_plant_label = CTkLabel(self.menu_frame, image=self.big_plant_img, text="")
            self.big_plant_label.place( x=0, y=210)
            #Choise name

            self.label=CTkLabel(self.menu_frame, text='Name', text_color = teme_color[0])
            self.label.pack(pady=15)
            self.entry=CTkEntry(self.menu_frame, placeholder_text="You name...",
                                fg_color = teme_color[0], text_color = teme_color[4], border_color = teme_color[4],
                                corner_radius = 10, bg_color = teme_color[3],placeholder_text_color=teme_color[4]
                                )
            self.entry.pack(pady=5)

            self.label_theme = CTkOptionMenu(
                self.menu_frame,
                values=["Light green", "Dark green", "Light yellow", "Dark yellow","Light orange", "Dark orange", "Light red", "Dark red", "Light pink", "Dark pink", "Light purple", "Dark purple", "Light blue", "Dark blue", "Light turquoise", "Dark turquoise", "Light", "Dark"],fg_color=teme_color[1],
                command=self.change_theme,button_hover_color=teme_color[2],text_color=teme_color[4],button_color=teme_color[0],
                dropdown_fg_color=teme_color[1],dropdown_hover_color=teme_color[3],dropdown_text_color=teme_color[4]
            )
            self.label_theme.pack(side="bottom", pady=20)



            #Button save
            self.save_button=CTkButton(self.menu_frame, text="Save", command=self.save_name,
                                       fg_color=teme_color[0], hover_color=teme_color[2], text_color=teme_color[4],
                                       corner_radius=10, bg_color=teme_color[3]
                                       )
            self.save_button.pack()




    def save_name(self):
        new_name=self.entry.get().strip()
        if new_name:
            self.username=new_name

            self.add_message(f"{self.oldusername} new name: {self.username}")
            self.oldusername = self.username

    def adaptive_ui(self):
        self.menu_frame.configure(height=self.winfo_height())
        self.chat_field.place(x=self.menu_frame.winfo_width())
        self.chat_field.configure(width=self.winfo_width()-self.menu_frame.winfo_width()-20,
                                  height=self.winfo_height()-40)
        self.send_button.place(x=self.winfo_width()-50, y=self.winfo_height()-40)
        self.message_entry.place(x=self.menu_frame.winfo_width(), y=self.send_button.winfo_y())
        self.message_entry.configure(
            width=self.winfo_width()-self.menu_frame.winfo_width()-110)
        self.open_img_button.place(x=self.winfo_width()-105, y=self.send_button.winfo_y())

        self.after(50, self.adaptive_ui)

    def add_message(self,message, img=None):
        message_frame=CTkFrame(self.chat_field, fg_color=teme_color[4])
        message_frame.pack(pady=5, anchor='w')
        self.all_messages.append(message_frame)
        wraplend_size=self.winfo_width()-self.menu_frame.winfo_width()-40
        if not img:
            CTkLabel(message_frame, text=message, wraplength=wraplend_size,
                     text_color=teme_color[0], justify='left').pack(padx=10, pady=5)
        else:
            CTkLabel(message_frame, text=message, wraplength=wraplend_size,
                     text_color=teme_color[1], image=img, compound='top',
                     justify='left').pack(padx=10, pady=5)

    def send_message(self):
        message=self.message_entry.get()
        if message:
            self.add_message(f"{self.username}: {message}")
            data= f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
        self.message_entry.delete(0, END)

    def recv_message(self):
        buffer=""
        while True:
            try:
                chunk=self.sock.recv(4096)
                if not chunk:
                    break
                buffer+=chunk.decode('utf-8', errors='ignore')

                while "\n" in buffer:
                    line, buffer=buffer.split("\n",1)
                    self.handle_line(line.strip())

            except:
                break
        self.sock.close()

    def handle_line(self, line):
        if not line:
            return
        parts=line.split("@", 3)
        nsg_type=parts[0]

        if nsg_type=="TEXT":
            if len(parts)>=3:
                author=parts[1]
                message=parts[2]
                self.add_message(f"{author}: {message}")
        elif nsg_type=="IMAGE":
            if len(parts)>=4:
                author=parts[1]
                filename=parts[2]
                b64_img=parts[3]
                try:
                    img_data=base64.b64decode(b64_img)
                    pil_img=Image.open(io.BytesIO(img_data))
                    ctk_img=CTkImage(pil_img, size=(300, 300))
                    self.add_message(f"{author} send message: {filename}", img=ctk_img)
                except Exception as e:
                    self.add_message(f"Image display error: {e}")
        else:
            self.add_message(line)

    def open_image(self):
        file_name=filedialog.askopenfilename()
        if not file_name:
            return
        try:
            with open(file_name, "rb")as f:
                raw=f.read()
            b64_data=base64.b64encode(raw).decode('utf-8')
            short_name=os.path.basename(file_name)
            data=f"IMAGE@{self.username}@{short_name}@{b64_data}\n"
            self.sock.sendall(data.encode())
            self.add_message('', CTkImage(light_image=Image.open(file_name), size=(300, 300)))
        except Exception as e:
            self.add_message(f"Image send error: {e}")

    def change_theme(self, value):
        global teme_color, plant, big_plant

        if value == "Dark green":
            plant=0
            big_plant=0
            teme_color = green_dark_color
        elif value == "Light green":
            plant = 0
            big_plant=0
            teme_color = green_light_color


        elif value == "Dark red":
            plant = 3
            big_plant = 3
            teme_color = red_dark_color
        elif value == "Light red":
            plant = 3
            big_plant = 3
            teme_color = red_light_color

        elif value == "Light pink":
            plant = 4
            big_plant = 4
            teme_color = pink_light_color
        elif value == "Dark pink":
            plant = 4
            big_plant = 4
            teme_color = pink_dark_color

        elif value == "Dark blue":
            plant = 6
            big_plant = 6
            teme_color = blue_dark_color
        elif value == "Light blue":
            plant = 6
            big_plant = 6
            teme_color = blue_light_color

        elif value == "Light yellow":
            plant = 1
            big_plant = 1
            teme_color = yellow_light_color
        elif value == "Dark yellow":
            plant = 1
            big_plant = 1
            teme_color = yellow_dark_color

        elif value == "Dark orange":
            plant = 2
            big_plant = 2
            teme_color = orange_dark_color
        elif value == "Light orange":
            plant = 2
            big_plant = 2
            teme_color = orange_light_color

        elif value == "Light turquoise":
            plant = 7
            big_plant = 7
            teme_color = turquoise_light_color
        elif value == "Dark turquoise":
            plant = 7
            big_plant = 7
            teme_color = turquoise_dark_color

        elif value == "Dark purple":
            plant = 5
            big_plant = 5
            teme_color = purple_dark_color
        elif value == "Light purple":
            plant = 5
            big_plant = 5
            teme_color = purple_light_color

        elif value == "Dark":
            plant = 8
            big_plant = 8
            teme_color = white_dark_color
        elif value == "Light":
            plant = 8
            big_plant = 8
            teme_color = white_light_color


        # 1. Обновляем само окно
        self.configure(fg_color=teme_color[1])

        # 2. Обновляем фреймы и кнопки
        self.plant_img.configure(light_image=Image.open(plant_color[plant]))
        self.plant_label.configure(image=self.plant_img)

        self.menu_frame.configure(fg_color=teme_color[3])
        self.chat_field.configure(fg_color=teme_color[1],
                                  scrollbar_button_color=teme_color[3],
                                  scrollbar_button_hover_color=teme_color[4])

        self.btn.configure(fg_color=teme_color[0], hover_color=teme_color[2], text_color=teme_color[4],
                           bg_color=teme_color[3])

        # Обновляем поле ввода и кнопки внизу
        self.message_entry.configure(fg_color=teme_color[0], text_color=teme_color[4], border_color=teme_color[4],
                                     bg_color=teme_color[1],placeholder_text_color=teme_color[4])
        self.send_button.configure(fg_color=teme_color[0], hover_color=teme_color[2], text_color=teme_color[4],
                                   bg_color=teme_color[1])
        self.open_img_button.configure(fg_color=teme_color[0], hover_color=teme_color[2], text_color=teme_color[4],
                                       bg_color=teme_color[1])

        # Обновляем элементы внутри меню, если оно открыто
        if self.is_show_menu:
            self.big_plant_img.configure(light_image=Image.open(big_plant_color[big_plant]))
            self.big_plant_label.configure(image=self.big_plant_img)

            self.label.configure(text_color=teme_color[0])
            self.entry.configure(fg_color=teme_color[0], text_color=teme_color[4], border_color=teme_color[4],
                                 bg_color=teme_color[3],placeholder_text_color=teme_color[4])
            self.save_button.configure(fg_color=teme_color[0], hover_color=teme_color[2], text_color=teme_color[4],
                                       bg_color=teme_color[3])


            # 1. Удаляем старое меню, если оно существует
            if getattr(self, "label_theme"):
                self.label_theme.destroy()

            # 2. Создаем его заново с новыми цветами темы
            self.label_theme = CTkOptionMenu(
                self.menu_frame,
                values=["Light green", "Dark green", "Light yellow", "Dark yellow", "Light orange", "Dark orange",
                        "Light red", "Dark red", "Light pink", "Dark pink", "Light purple", "Dark purple", "Light blue",
                        "Dark blue", "Light turquoise", "Dark turquoise", "Light", "Dark"], fg_color=teme_color[1],
                command=self.change_theme, button_hover_color=teme_color[2], text_color=teme_color[4],
                button_color=teme_color[0],
                dropdown_fg_color=teme_color[1], dropdown_hover_color=teme_color[3], dropdown_text_color=teme_color[4]
            )

            self.label_theme.set(value)  # Возвращаем выбранное значение на кнопку
            self.label_theme.pack(side="bottom", pady=20)


        for msg_frame in self.all_messages:
            if msg_frame.winfo_exists():  # Проверка, что виджет еще существует
                msg_frame.configure(fg_color=teme_color[4])  # Обновляем фон фрейма

                # Обновляем цвет текста внутри лейбла
                for child in msg_frame.winfo_children():
                    if isinstance(child, CTkLabel):
                        child.configure(text_color=teme_color[0])


if __name__=="__main__":

    win= MainWindow()
    win.mainloop()

