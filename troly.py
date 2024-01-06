import tkinter as tk
from tkinter import scrolledtext
from bs4 import BeautifulSoup
import speech_recognition as sr
import threading
import os
import playsound
import time
import wikipedia
import datetime
import re
import webbrowser
import requests
from gtts import gTTS
from PIL import Image, ImageTk
import json
wikipedia.set_lang("vi")
language = "vi"
name=""

class VirtualAssistantGUI:
    def __init__(self, master):
        global name
        self.master = master
        master.title("Assistant")
        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=30)
        self.text_area.pack(padx=10, pady=10)
        image = Image.open("mic.png")
        image = image.resize((50, 50))  # Thay thế 'ANTIALIAS' bằng 'ANTIALIAS'
        self.button_image = ImageTk.PhotoImage(image)
        self.microphone_button = tk.Button(master,image=self.button_image, command=self.start_listening)
        self.microphone_button.pack(pady=30)
        self.knowledge_file = "knowledge_base.json"
        self.knowledge = self.load_knowledge()
    def load_knowledge(self):
        try:
            with open(self.knowledge_file, "r" , encoding='utf-8') as file:
                knowledge = json.load(file)
            return knowledge
        except (FileNotFoundError, json.JSONDecodeError):
            # Nếu tệp không tồn tại hoặc có lỗi khi phân tích cú pháp JSON, trả về một tri thức rỗng
            return {}

    def save_knowledge(self):
        with open(self.knowledge_file, "w", encoding="utf-8" ) as file:
            json.dump(self.knowledge, file ,ensure_ascii=False, indent=2)

    def learn_new_fact(self, fact, category):
        if category not in self.knowledge:
            self.knowledge[category] = []

        if fact not in self.knowledge[category]:
            self.knowledge[category].append(fact)
            self.save_knowledge()
            self.hien(f"Đã học thêm: {fact} vào danh mục {category}")
            self.speak(f"Đã học thêm: {fact} vào danh mục {category}")
            # self.speak("Bạn muốn tôi nói lại điều này không?")
            # self.hien("Bạn muốn tôi nói lại điều này không?")
            # self.hien("Đang nghe")
            # repeat = self.get_text()
            # if "có" in repeat:
            #     self.speak(f"{fact} là gì?")
            #     self.hien(f"{fact} là gì?")
        else:
            print(f"{fact} đã có trong danh mục {category}")

    def query_knowledge(self, category):
        if category in self.knowledge:
            self.hien(f"{category}: {', '.join(self.knowledge[category])}")
            self.speak(f"{', '.join(self.knowledge[category])}")
        else:
            self.hien(f"{category} không có thông tin.")
            self.speak(f"{category} không có thông tin.")
            self.speak("bạn muốn trợ lý học thêm dữ liệu này không")
            self.hien("bạn muốn trợ lý học thêm dữ liệu này không")
            hoc= self.get_text()
            if "có" in hoc:
                self.speak(f"{category} là gì ")
                self.hien(f"{category} là gì ?")
                kienthuc = self.get_text()
                self.learn_new_fact(kienthuc,category)
            if "không" in hoc:
                self.speak(f"oke bạn")
                self.hien(f"oke bạn")

    def hien(self,text):
        self.text_area.insert(tk.END, "bot: "+text+"\n")
    def recognize_speech(self):
        self.text_area.insert(tk.END, "Đang lắng nghe...\n")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, phrase_time_limit=6)
            try:
                text = r.recognize_google(audio, language="vi-VN")
                self.text_area.insert(tk.END, "Bạn : " + text + "\n")
                return text.lower()
            except sr.UnknownValueError:
                self.text_area.insert(tk.END, "Không nhận diện được giọng nói\n")
                return 0
            except sr.RequestError as e:
                self.text_area.insert(tk.END, "Lỗi kết nối: {0}\n".format(e))
                return 0
        
    def speak(self, text):
        try:
            print("Bot: {}".format(text))
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save("sound.mp3")
            playsound.playsound("sound.mp3", block=True)
            os.remove("sound.mp3")
            self.text_area.see(tk.END)
        except Exception as e:
            print("Lỗi:", e)
        

    def stop(self):
        self.speak("hẹn gặp lại bạn sau!")
        self.hien("Hẹn gặp lại bạn sau!")
        

    def get_text(self): 
        for i in range(3):
            text = self.recognize_speech()
            
            if text:
                return text
            elif i < 2:
                self.speak("bot không nghe rõ. Bạn nói lại được không!")
                self.hien("Bot không nghe rõ. Bạn nói lại được không!")
        self.text_area.see(tk.END)
        
        time.sleep(1)
        return "dừng"
    def ten_la_gi (self):
        global name
        self.speak("chào bạn, bạn tên là gì ")
        self.hien("chào bạn, bạn tên là gì")
        name= self.get_text()
    def hello(self):
        if name=="":
            self.ten_la_gi()
        day_time = int(datetime.datetime.now().strftime("%H"))
        if day_time < 12:
            self.speak("chào buổi sáng bạn {}. Chúc bạn một ngày tốt lành.".format(name))
            self.hien("Chào buổi sáng bạn {}. Chúc bạn một ngày tốt lành.".format(name))
        elif 12 <= day_time < 18:
            self.speak("chào buổi chiều bạn {}. Bạn đã dự định gì cho chiều nay chưa.".format(name))
            self.hien("Chào buổi chiều bạn {}. Bạn đã dự định gì cho chiều nay chưa.".format(name))
        else:
            self.speak("chào buổi tối bạn {}. Bạn đã ăn tối chưa nhỉ.".format(name))
            self.hien("Chào buổi tối bạn {}. Bạn đã ăn tối chưa nhỉ.".format(name))
        self.speak("bạn cần Bot giúp gì ạ?")
        self.text_area.insert(tk.END, "Bạn cần Bot giúp gì ạ?\n")
    def get_time(self, text):
        now = datetime.datetime.now()
        if "giờ" in text:
            self.speak("bây giờ là %d giờ %d phút" % (now.hour, now.minute))
            self.hien("Bây giờ là %d giờ %d phút" % (now.hour, now.minute))
        elif "ngày" in text:
            self.speak("hôm nay là ngày %d tháng %d năm %d" % (now.day, now.month, now.year))
            self.hien("Hôm nay là ngày %d tháng %d năm %d" % (now.day, now.month, now.year))
        else:
            self.speak("bot chưa hiểu ý của bạn. Bạn nói lại được không?")
            self.hien("Bot chưa hiểu ý của bạn. Bạn nói lại được không?")

    def open_application(self, text):
        if "google" in text:
            self.speak("mở Google Chrome")
            self.hien("Mở Google Chrome")
            webbrowser.get().open("https://www.google.com")
            
        elif "word" in text:
            self.speak("mở Microsoft Word")
            self.hien("Mở Microsoft Word")
            os.system("start winword")
            
        elif "excel" in text:
            self.speak("mở Microsoft Excel")
            self.hien("Mở Microsoft Excel")
            os.system("start excel")
        elif "powerpoint" in text:
            self.speak("mở Microsoft PowerPoint")
            self.hien("Mở Microsoft PowerPoint")
            os.system("start powerpnt")
        elif "spotify" in text:
            self.speak("mở spotifyt")
            self.hien("Mở spotify")
            os.system("start C:\\Users\\Admin\\AppData\\Roaming\\Spotify\\Spotify.exe")
        elif "nhạc" in text:
            self.speak("bạn muốn mở bài nhạc gì")
            self.hien("bạn muốn mở bài nhạc gì")
            nhac = self.get_text()
            youtube_search_url = f"https://www.youtube.com/results?search_query={nhac}"
    
            webbrowser.open(youtube_search_url)
            
        else:
            self.speak("ứng dụng chưa được cài đặt. Bạn hãy thử lại!")
            self.hien("Ứng dụng chưa được cài đặt. Bạn hãy thử lại!")

    def open_website(self, text):
        reg_ex = re.search("mở (.+)", text)
        if reg_ex:
            domain = reg_ex.group(1)
            url = "https://www." + domain
            webbrowser.open(url)
            self.speak("trang web bạn yêu cầu đã được mở.")
            return True
        else:
            return False

    def open_google_and_search(self, text):
        try:
            search_for = text.split("kiếm", 1)[1]
            self.speak("okay!")
            self.hien("Okay!")
            search_url = "https://www.google.com/search?q=" + search_for
            webbrowser.open(search_url)
        except Exception as e:
            print(f"An error occurred: {e}")

    def current_weather(self):
        self.speak("bạn muốn xem thời tiết ở đâu ạ.")
        self.hien("bạn muốn xem thời tiết ở đâu ạ.")
        city = self.get_text()
        if not city:
            return
        ow_url = "http://api.openweathermap.org/data/2.5/weather?"
        api_key = "fe8d8c65cf345889139d8e545f57819a"
        call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
        response = requests.get(call_url)
        data = response.json()
        if data["cod"] != "404":
            city_res = data["main"]
            current_temperature = city_res["temp"]
            current_pressure = city_res["pressure"]
            current_humidity = city_res["humidity"]
            suntime = data["sys"]
            sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
            sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
            wthr = data["weather"]
            weather_description = wthr[0]["description"]
            now = datetime.datetime.now()
            content = f"""
            hôm nay là ngày {now.day} tháng {now.month} năm {now.year}
            mặt trời mọc vào {sunrise.hour} giờ {sunrise.minute} phút
            mặt trời lặn vào {sunset.hour} giờ {sunset.minute} phút
            nhiệt độ trung bình là {current_temperature} độ C
            áp suất không khí là {current_pressure} héc tơ pascal
            độ ẩm là {current_humidity}%
            trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi."""
            self.speak(content)
            self.hien(content)
        else:
            self.speak("không tìm thấy địa chỉ của bạn")

    def play_song(self):
        self.speak("xin mời bạn chọn tên bài hát")
        mysong = self.get_text()
        search_url = "https://www.youtube.com/results?search_query=" + mysong
        webbrowser.open(search_url)

    def tell_me_about(self):
        try:
            self.speak("bạn muốn nghe về gì ạ")
            self.hien("Bạn muốn nghe về gì ạ")
            text = self.get_text()
            contents = wikipedia.summary(text).split("\n")
            self.speak(contents[0])
            for content in contents[1:]:
                self.speak("bạn muốn nghe thêm không")
                ans = self.get_text()
                if "có" not in ans:
                    break
                self.speak(content)
            self.speak("cảm ơn bạn đã lắng nghe!!!")
            self.hien("cảm ơn bạn đã lắng nghe!!!")
        except:
            self.speak("bot không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")
            self.hien("bot không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")

    def help_me(self):
        self.hien("Bot có thể giúp bạn thực hiện các câu lệnh sau đây:\n1. Chào hỏi\n2. Hiển thị giờ\n3. Mở website, application\n4. Tìm kiếm trên Google\n5. Dự báo thời tiết\n6. tìm kiếm video youtube\n7. tìm hiểu về thứ gì đó\n8. kể chuyện\n9. tính toán")

        self.speak(
            """Bot có thể giúp bạn thực hiện các câu lệnh sau đây:
        1. chào hỏi
        2. hiển thị giờ
        3. mở website, application
        4. tìm kiếm trên Google
        5. dự báo thời tiết
        6. tìm kiếm video youtube
        7. tìm hiểu về thứ gì đó
        8. kể chuyện
        9. tính toán
        """
        )
        
    def kechuyen(self):
        self.speak("""
                    một ngày nọ, ông Nguyễn, một ông lão nông dân, quyết định thử nghiệm một loại thức ăn mới cho gà của mình. Ông ta đi đến cửa hàng thức ăn cho gia súc và hỏi nhân viên:

Ông Nguyễn: "Cho tôi một túi thức ăn mới nhất dành cho gà, bạn ạ."

Nhân viên: "Dĩ nhiên, ông! Đây là một túi thức ăn đặc biệt được làm từ các thành phần tự nhiên, đảm bảo giúp gà của ông khỏe mạnh và nhanh chóng phát triển."

Ông Nguyễn vui vẻ mua túi thức ăn và về nhà đưa cho gà ăn. Tuy nhiên, sau vài ngày, ông ta nhận ra rằng không có sự thay đổi gì đáng kể ở gà. Ông ta quay lại cửa hàng và nói với nhân viên:

Ông Nguyễn: "Tôi đã thử thức ăn mới đó, nhưng gà của tôi vẫn giống như trước, không có gì khác cả."

Nhân viên: "Ông cứ yên tâm, có thể ông đã cho gà ăn đúng cách chưa."

Ông Nguyễn: "Tôi thấy tôi đã làm đúng mọi thứ mà. Tôi đã đọc kỹ hướng dẫn sử dụng trên túi thức ăn."

Nhân viên: "Vậy ông có chắc là ông đã làm đúng theo hướng dẫn không?"

Ông Nguyễn nghiêm túc: "Ừ, đúng 100%, tôi làm theo đúng hướng dẫn: 'Mở túi, đổ vào bát, rồi đặt trước mặt gà.'"

Cả hai cười sảng khoái với tình huống hài hước. Ông Nguyễn nhận ra mình đã hiểu lầm và cả hai bắt đầu tìm cách giúp gà ăn đúng cách.
        hy vọng câu chuyện đã mang lại tiếng cười cho bạn!
""")

    def tinhtoan(self):
        kq = 0
        self.speak('biểu thức của bạn là gì')
        self.hien('biểu thức của bạn là gì')
        text = self.get_text()
        
        words_to_numbers_dict = {
            'một': 1,
            'hai': 2,
            'ba': 3,
            'bốn': 4,
            'năm': 5,
            'sáu': 6,
            'bảy': 7,
            'tám': 8,
            'chín': 9,
            'mười': 10,
            
        }

        words = text.split()
        numeric_values = [words_to_numbers_dict.get(word.lower(), word) for word in words]

        if 'cộng' in text or '+' in text:
            kq = int(numeric_values[0]) + int(numeric_values[2])
            self.speak(f'kết quả là {kq}')
        elif 'trừ' in text or '-' in text:
            kq = int(numeric_values[0]) - int(numeric_values[2])
            self.speak(f'kết quả là {kq}')
        elif 'nhân' in text or 'x' in text:
            kq = int(numeric_values[0]) * int(numeric_values[2])
            self.speak(f'kết quả là {kq}')
        elif 'chia' in text:
            divisor = int(numeric_values[2])
            if divisor != 0:
                kq = int(numeric_values[0]) / divisor
                self.speak(f'kết quả là {kq}')
            else:
                self.speak("phép chia cho 0, không hợp lệ.")

    def assistant(self, text):
        
        if "dừng" in text or "tạm biệt" in text or "chào robot" in text or "ngủ thôi" in text :
            self.stop()
        elif "có thể làm gì" in text:
            self.help_me()
        elif "chào trợ lý ảo" in text or "chào" in text or "hello" in text:
            self.hello()
        elif "hiện tại" in text:
            self.get_time(text)
        elif "tìm kiếm" in text:
            self. open_google_and_search(text)
        elif "mở" in text:
            if "." in text:
              self.  open_website(text)
            else:
              self.  open_application(text)
        
        elif "thời tiết" in text:
            self.current_weather()
        elif "nhạc" in text:
           self.play_song()
           self.hien('play song')
        elif "tính toán" in text:
            self.tinhtoan()
        elif "tìm hiểu" in text:
            self.tell_me_about()
        elif "kể chuyện" in text:
            self.speak(' kể chuyện nhé')
            self.hien('kể chuyện nhé')
            self.kechuyen()
        elif "nếu" in text or "tôi" in text:
            text = text.replace("nếu", "")
            self.query_knowledge(text)
        else:
            self.speak("bạn cần Bot giúp gì ạ?")
            self.hien("bạn cần Bot giúp gì ạ?")
    def start_listening(self):
        threading.Thread(target=self.assistant, args=(self.get_text(),)).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualAssistantGUI(root)
    root.mainloop()

