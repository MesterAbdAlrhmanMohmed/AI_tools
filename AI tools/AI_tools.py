from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
from PIL import Image
from io import BytesIO
import speech_recognition as sr
import google.generativeai as genai
import gtts,os,langdetect,pyperclip,PIL.Image,about,dic,winsound,time,webbrowser,requests
genai.configure(api_key="")
model=genai.GenerativeModel('gemini-pro')
response=model.start_chat()
if not os.path.exists("data"):
    os.makedirs("data")
class Thread1(qt2.QThread):
    finished=qt2.pyqtSignal(str)
    download_finished=qt2.pyqtSignal(list)
    def __init__(self, chat, ask):
        super().__init__()
        self.chat=chat
        self.ask=ask
    def run(self):
        try:
            response=self.chat.send_message(self.ask)
            النتيجة=response.text.split("\n")
            self.نص_الرسالة = response.text
            self.download_finished.emit(النتيجة)            
        except Exception as e:
            self.finished.emit("يرجى إدخال نص، إذا تم هذا، تأكد من عدم وجود ألفاظ خارجة، أو تأكد من إتصالك بالإنترنت")        
class tab1(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.chat=model.start_chat()
        self.m=QMediaPlayer()
        self.w=QAudioOutput()
        self.m.setAudioOutput(self.w)
        self.إظهار=qt.QLabel("إسأل سؤالا")
        self.الكتابة=qt.QLineEdit()
        self.الكتابة.setAccessibleName("إسأل سؤالا")
        self.إرسال=qt.QPushButton("إرسال")
        self.إرسال.setDefault(True)
        self.إرسال.clicked.connect(self.main)
        self.الردود=qt.QComboBox()
        self.نسخ_الرد=qt.QPushButton("نسخ تلك الفقرة")
        self.نسخ_الرد.setDefault(True)
        self.نسخ_الرد.clicked.connect(self.copy)
        self.نسخ_الكل=qt.QPushButton("نسخ كل الرسالة")
        self.نسخ_الكل.setDefault(True)
        self.نسخ_الكل.clicked.connect(self.copyAll)
        self.نص_الرسالة=""
        self.إستماع=qt.QPushButton("الإستماع إلى الرسالة")
        self.إستماع.setDefault(True)
        self.إستماع.clicked.connect(self.listen)
        l=qt.QVBoxLayout()
        l.addWidget(self.إظهار)
        l.addWidget(self.الكتابة)
        l.addWidget(self.إرسال)
        l.addWidget(self.الردود)
        l.addWidget(self.نسخ_الرد)
        l.addWidget(self.نسخ_الكل)
        l.addWidget(self.إستماع)
        self.setLayout(l)
    def main(self):
        ask=self.الكتابة.text()
        self.thread=Thread1(self.chat, ask)
        self.thread.finished.connect(self.show_warning)
        self.thread.download_finished.connect(self.update_responses)
        self.thread.start()
    def show_warning(self, message):
        qt.QMessageBox.warning(self, "عفوا", message)
    def update_responses(self, النتيجة):
        self.الردود.clear()
        self.الردود.addItems(النتيجة)
        self.نص_الرسالة = "\n".join(النتيجة)
        self.الردود.setFocus()
    def copy(self):
        pyperclip.copy(self.الردود.currentText())
    def copyAll(self):
        pyperclip.copy(self.نص_الرسالة)
    def listen(self):
        try:
            lang=langdetect.detect(self.نص_الرسالة)
            result=gtts.gTTS(self.نص_الرسالة, lang=lang)
            result.save("data/message.mp3")
            if self.m.isPlaying():
                self.إستماع.setText("الاستماع إلى الرسالة")
                self.m.stop()
            else:
                self.إستماع.setText("إيقاف")
                self.m.setSource(qt2.QUrl.fromLocalFile("data/message.mp3"))
                self.m.play()
        except:
            qt.QMessageBox.information(self, "عفوا", "لم يتم العثور على نص، إذا كان هناك نص قم بالتأكد من الإتصال بالإنترنت")
class Thread2(qt2.QThread):
    finished=qt2.pyqtSignal(str)
    download_finished=qt2.pyqtSignal(list)
    def __init__(self, model, ask1, image_path):
        super().__init__()
        self.model=model
        self.ask1=ask1
        self.image_path=image_path
    def run(self):
        model=genai.GenerativeModel('gemini-pro-vision')        
        try:
            ask=PIL.Image.open(self.image_path)
            response=self.model.generate_content([self.ask1, ask])
            النتيجة=response.text.split("\n")
            self.نص_الرسالة = response.text
            self.download_finished.emit(النتيجة)
        except Exception as e:
            self.finished.emit("يرجى إرفاق سورة، أو التأكد من إتصالك بالإنترنت")
class tab2(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.model=genai.GenerativeModel('gemini-pro-vision')
        self.m=QMediaPlayer()
        self.w=QAudioOutput()
        self.m.setAudioOutput(self.w)
        self.فتح=qt.QPushButton("إختيار سورة")
        self.إظهار=qt.QLabel("إسأل سؤالا")
        self.السؤال=qt.QLineEdit()
        self.السؤال.setAccessibleName("إسأل عن السورة")
        self.فتح.setDefault(True)
        self.فتح.clicked.connect(self.opinFile)
        self.إرسال=qt.QPushButton("إرسال")
        self.إرسال.setDefault(True)
        self.إرسال.clicked.connect(self.main)
        self.الردود=qt.QComboBox()
        self.نسخ_الرد=qt.QPushButton("نسخ تلك الفقرة")
        self.نسخ_الرد.setDefault(True)
        self.نسخ_الرد.clicked.connect(self.copy)
        self.نسخ_الكل=qt.QPushButton("نسخ كل الرسالة")
        self.نسخ_الكل.setDefault(True)
        self.نسخ_الكل.clicked.connect(self.copyAll)
        self.إستماع=qt.QPushButton("الإستماع إلى الرسالة")
        self.إستماع.setDefault(True)
        self.إستماع.clicked.connect(self.listen)
        self.إظهار1=qt.QLabel("مسار الملف هو")
        self.مسار=qt.QLineEdit()
        self.مسار.setAccessibleName("مسار الملف هو")
        self.مسار.setReadOnly(True)
        self.نص_الرسالة=""
        l=qt.QVBoxLayout()
        l.addWidget(self.إظهار1)
        l.addWidget(self.مسار)
        l.addWidget(self.فتح)
        l.addWidget(self.إظهار)
        l.addWidget(self.السؤال)
        l.addWidget(self.إرسال)
        l.addWidget(self.الردود)
        l.addWidget(self.نسخ_الرد)
        l.addWidget(self.نسخ_الكل)
        l.addWidget(self.إستماع)
        self.setLayout(l)
    def main(self):
        ask1=self.السؤال.text()
        image_path=self.مسار.text()
        self.thread=Thread2(self.model, ask1, image_path)
        self.thread.finished.connect(self.show_warning)
        self.thread.download_finished.connect(self.update_responses)
        self.thread.start()
    def show_warning(self, message):
        qt.QMessageBox.warning(self, "عفوا", message)
    def update_responses(self, النتيجة):
        self.الردود.clear()
        self.الردود.addItems(النتيجة)
        self.نص_الرسالة = "\n".join(النتيجة)
        self.الردود.setFocus()
    def copy(self):
        pyperclip.copy(self.الردود.currentText())
    def copyAll(self):
        pyperclip.copy(self.نص_الرسالة)
    def listen(self):
        try:
            lang=langdetect.detect(self.نص_الرسالة)
            result=gtts.gTTS(self.نص_الرسالة, lang=lang)
            result.save("data/message.mp3")
            if self.m.isPlaying():
                self.إستماع.setText("الإستماع إلى الرسالة")
                self.m.stop()
            else:
                self.إستماع.setText("إيقاف")
                self.m.setSource(qt2.QUrl.fromLocalFile("data/message.mp3"))
                self.m.play()
        except:
            qt.QMessageBox.information(self, "عفوا", "لم يتم العثور على نص، إذا كان هناك نص قم بالتأكد من الإتصال بالإنترنت")
    def opinFile(self):
        file_dialog=qt.QFileDialog()
        file_dialog.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptOpen)
        if file_dialog.exec() == qt.QFileDialog.DialogCode.Accepted:
            self.مسار.setText(file_dialog.selectedFiles()[0])
class SpeechThread(qt2.QThread):
    finished=qt2.pyqtSignal(str)
    download_finished=qt2.pyqtSignal(str)
    def __init__(self, chat, lang):
        super().__init__()
        self.chat=chat
        self.lang=lang
    def run(self):
        SR=sr.Recognizer()
        with sr.Microphone() as src:
            winsound.PlaySound("data/1.wav", winsound.SND_FILENAME)
            audio=SR.listen(src)
        try:
            winsound.PlaySound("data/2.wav", winsound.SND_FILENAME)
            text=SR.recognize_google(audio, language=self.lang)
        except Exception as e:
            text="sorry"
            winsound.PlaySound("data/3.wav", winsound.SND_FILENAME)        
        try:
            res=self.chat.send_message(text).text
        except Exception as e:
            res="error"        
        try:
            Language=langdetect.detect(res)
        except:
            Language="en"        
        tts=gtts.gTTS(res, lang=Language)
        winsound.PlaySound("data/4.wav", winsound.SND_FILENAME)
        tts.save("data/speak.mp3")
        self.download_finished.emit("data/speak.mp3")        
class tab3(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.chat=model.start_chat()
        self.m=QMediaPlayer()
        self.w=QAudioOutput()
        self.m.setAudioOutput(self.w)
        self.إظهار=qt.QLabel("إختيار لغة التحدث مع الذكاء الإصطناعي")
        self.اللغة=qt.QComboBox()
        self.اللغة.setAccessibleName("إختيار لغة التحدث مع الذكاء الإصطناعي")
        self.اللغة.addItems(dic.languages.keys())
        self.التحدث=qt.QPushButton("بدء التحدث")
        self.التحدث.setDefault(True)
        self.التحدث.clicked.connect(self.OnSpeack)
        self.إيقاف=qt.QPushButton("إيقاف المساعد")
        self.إيقاف.setDefault(True)
        self.إيقاف.clicked.connect(lambda: self.m.stop())
        l=qt.QVBoxLayout()
        l.addWidget(self.إظهار)
        l.addWidget(self.اللغة)
        l.addWidget(self.التحدث)
        l.addWidget(self.إيقاف)
        self.setLayout(l)
    def OnSpeack(self):
        lang = dic.languages[self.اللغة.currentText()]
        self.thread = SpeechThread(self.chat, lang)
        self.thread.finished.connect(self.show_warning)
        self.thread.download_finished.connect(self.play_response)
        self.thread.start()
    def show_warning(self, message):
        qt.QMessageBox.warning(self, "عفوا", message)
    def play_response(self, filepath):
        self.m.setSource(qt2.QUrl.fromLocalFile(filepath))
        self.m.play()
class ExtractTextThread(qt2.QThread):
    text_extracted=qt2.pyqtSignal(str)
    error_occurred=qt2.pyqtSignal(str)
    def __init__(self, file_path, language_index, custom_token):
        super().__init__()
        self.file_path=file_path
        self.language_index=language_index
        self.custom_token=custom_token
    def run(self):
        recognizer=sr.Recognizer()
        with sr.AudioFile(self.file_path) as source:
            audio_data=recognizer.record(source)
            try:
                if self.language_index == 0:
                    text=recognizer.recognize_wit(audio_data, "")
                elif self.language_index == 1:
                    text=recognizer.recognize_wit(audio_data, "")
                elif self.language_index == 2:
                    if not self.custom_token:
                        self.error_occurred.emit("يرجى إدخال رمز اللغة المطلوب")
                        return
                    text=recognizer.recognize_wit(audio_data, self.custom_token)
                self.text_extracted.emit(text)                
            except sr.UnknownValueError:
                self.error_occurred.emit("حدث خطأ، ربما المقطع فارغ أو اللغة غير صحيحة أو لم يتم التعرف بشكل جيد على المقطع")
            except sr.RequestError:
                self.error_occurred.emit("فشلت عملية استخراج النص، ربما امتداد الملف غير مدعوم أو هناك مشكلة في الإنترنت")
class tab4(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.فتح=qt.QPushButton("فتح ملف wav")
        self.فتح.setDefault(True)
        self.فتح.clicked.connect(self.opinFile)
        self.إظهار1=qt.QLabel("مسار الملف")
        self.مسار=qt.QLineEdit()
        self.مسار.setAccessibleName("مسار الملف")
        self.مسار.setReadOnly(True)
        self.إظهار2=qt.QLabel("إختيار لغة المقطع الصوتي")
        self.اللغة=qt.QComboBox()
        self.اللغة.setAccessibleName("إختيار لغة المقطع الصوتي")
        self.اللغة.addItem("الإنجليزية")
        self.اللغة.addItem("العربية")
        self.اللغة.addItem("تحديد لغة مخصصة")
        self.إستخراج=qt.QPushButton("بدء الاستخراج")
        self.إستخراج.setDefault(True)
        self.إستخراج.clicked.connect(self.start_extraction)
        self.إظهار3=qt.QLabel("النص المستخرَج")
        self.النص=qt.QLineEdit()
        self.النص.setAccessibleName("النص المستخرَج")
        self.النص.setReadOnly(True)
        self.نسخ=qt.QPushButton("نسخ النص")
        self.نسخ.setDefault(True)
        self.نسخ.clicked.connect(self.copy_text)
        self.إظهار4=qt.QLabel("إدخال الرمز المميز Client Access Token للغة من موقع wit.ai")
        self.مخصص=qt.QLineEdit()
        self.مخصص.setAccessibleName("إدخال الرمز المميز Client Access Token للغة من موقع wit.ai")
        self.wit=qt.QPushButton("الذهاب الى موقع wit.ai")
        self.wit.setDefault(True)
        self.wit.clicked.connect(self.open_wit_ai)
        self.wit.setDisabled(True)
        self.مخصص.setDisabled(True)
        self.اللغة.currentIndexChanged.connect(self.toggle_custom_language)
        l=qt.QVBoxLayout()
        l.addWidget(self.فتح)
        l.addWidget(self.إظهار1)
        l.addWidget(self.مسار)
        l.addWidget(self.إظهار2)
        l.addWidget(self.اللغة)
        l.addWidget(self.إظهار4)
        l.addWidget(self.مخصص)
        l.addWidget(self.wit)
        l.addWidget(self.إستخراج)
        l.addWidget(self.إظهار3)
        l.addWidget(self.النص)
        l.addWidget(self.نسخ)
        self.setLayout(l)
    def open_wit_ai(self):
        webbrowser.open("https://wit.ai")
    def toggle_custom_language(self, index):
        if index == 2:
            self.wit.setDisabled(False)
            self.مخصص.setDisabled(False)
        else:
            self.wit.setDisabled(True)
            self.مخصص.setDisabled(True)
    def start_extraction(self):
        if not self.مسار.text().endswith(".wav"):
            qt.QMessageBox.warning(self, "تنبيه", "يرجى تحديد ملف بامتداد wav")
            return
        if not self.مسار.text():
            qt.QMessageBox.warning(self, "تنبيه", "لم يتم تحديد ملف للتعرف عليه")
            return        
        self.النص.setFocus()
        language_index=self.اللغة.currentIndex()
        custom_token=self.مخصص.text() if language_index == 2 else None
        self.thread=ExtractTextThread(self.مسار.text(), language_index, custom_token)
        self.thread.text_extracted.connect(self.show_extracted_text)
        self.thread.error_occurred.connect(self.show_error_message)
        self.thread.start()
    def show_extracted_text(self, text):
        self.النص.setText(text)        
    def show_error_message(self, message):
        qt.QMessageBox.warning(self, "تنبيه", message)
    def copy_text(self):
        pyperclip.copy(self.النص.text())
        qt.QMessageBox.information(self, "تنبيه", "تم نسخ النص إلى الحافظة")
    def opinFile(self):
        file_dialog = qt.QFileDialog()
        file_dialog.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptOpen)
        if file_dialog.exec() == qt.QFileDialog.DialogCode.Accepted:
            self.مسار.setText(file_dialog.selectedFiles()[0])        
class AudioExtractionThread(qt2.QThread):
    text_extracted=qt2.pyqtSignal(str)
    error_occurred=qt2.pyqtSignal(str)
    def __init__(self, file_path, language):
        super().__init__()
        self.file_path=file_path
        self.language=language
    def run(self):
        recognizer=sr.Recognizer()
        with sr.AudioFile(self.file_path) as source:
            audio_data=recognizer.record(source)
            try:
                text=recognizer.recognize_google(audio_data, language=self.language)
                self.text_extracted.emit(text)                
            except sr.UnknownValueError:
                self.error_occurred.emit("لم أتمكن من فهم الصوت")
            except sr.RequestError:
                self.error_occurred.emit("حدثت مشكلة في التعرف على الصوت")
class tab5(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.فتح=qt.QPushButton("فتح ملف wav")
        self.فتح.setDefault(True)
        self.فتح.clicked.connect(self.opinFile)
        self.إظهار1=qt.QLabel("مسار الملف")
        self.مسار=qt.QLineEdit()
        self.مسار.setAccessibleName("مسار الملف")
        self.مسار.setReadOnly(True)
        self.إظهار2=qt.QLabel("إختيار لغة المقطع الصوتي")
        self.اللغة=qt.QComboBox()
        self.اللغة.setAccessibleName("إختيار لغة المقطع الصوتي")
        self.اللغة.addItems(dic.languages.keys())
        self.إستخراج=qt.QPushButton("بدء الاستخراج")
        self.إستخراج.setDefault(True)
        self.إستخراج.clicked.connect(self.start_extraction)
        self.إظهار3=qt.QLabel("النص المستخرَج")
        self.النص=qt.QLineEdit()
        self.النص.setAccessibleName("النص المستخرَج")
        self.النص.setReadOnly(True)
        self.نسخ=qt.QPushButton("نسخ النص")
        self.نسخ.setDefault(True)
        self.نسخ.clicked.connect(self.copy_text)        
        l=qt.QVBoxLayout()
        l.addWidget(self.فتح)
        l.addWidget(self.إظهار1)
        l.addWidget(self.مسار)
        l.addWidget(self.إظهار2)
        l.addWidget(self.اللغة)
        l.addWidget(self.إستخراج)
        l.addWidget(self.إظهار3)
        l.addWidget(self.النص)
        l.addWidget(self.نسخ)
        self.setLayout(l)
    def start_extraction(self):
        if not self.مسار.text().endswith(".wav"):
            qt.QMessageBox.warning(self, "تنبيه", "يرجى تحديد ملف بامتداد wav")
            return
        if not self.مسار.text():
            qt.QMessageBox.warning(self, "تنبيه", "لم يتم تحديد ملف للتعرف عليه")
            return        
        self.النص.setFocus()
        lang=dic.languages[self.اللغة.currentText()]
        self.thread=AudioExtractionThread(self.مسار.text(), lang)
        self.thread.text_extracted.connect(self.show_extracted_text)
        self.thread.error_occurred.connect(self.show_error_message)
        self.thread.start()
    def show_extracted_text(self, text):
        self.النص.setText(text)        
    def show_error_message(self, message):
        qt.QMessageBox.warning(self, "تنبيه", message)
    def copy_text(self):
        pyperclip.copy(self.النص.text())
        qt.QMessageBox.information(self, "تنبيه", "تم نسخ النص إلى الحافظة")
    def opinFile(self):
        file_dialog=qt.QFileDialog()
        file_dialog.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptOpen)
        if file_dialog.exec() == qt.QFileDialog.DialogCode.Accepted:
            self.مسار.setText(file_dialog.selectedFiles()[0])
class tab6(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.إظهار=qt.QLabel("أكتب وصفا دقيقا للصورة, الأفضل أن يكون بالإنجليزية")
        self.الكتابة=qt.QLineEdit()
        self.الكتابة.setAccessibleName("أكتب وصفا دقيقا للصورة, الأفضل أن يكون بالإنجليزية")
        self.الحصول=qt.QPushButton("الحصول على صورة")
        self.الحصول.setDefault(True)
        self.الحصول.clicked.connect(self.git_image)
        l=qt.QVBoxLayout()
        l.addWidget(self.إظهار)
        l.addWidget(self.الكتابة)
        l.addWidget(self.الحصول)
        self.setLayout(l)
    def git_image(self):
        if not self.الكتابة.text():
            qt.QMessageBox.warning(self,"تنبيه","يرجى إدخال نص")
            return
        access_key= ""
        query=self.الكتابة.text()
        url=f"https://api.unsplash.com/photos/random?query={query}&client_id={access_key}"    
        try:
            response=requests.get(url)
            if response.status_code == 200:
                data=response.json()
                image_url=data["urls"]["regular"]
                image_response=requests.get(image_url)
                img=Image.open(BytesIO(image_response.content))
                img.show()
            else:
                qt.QMessageBox.warning(self, "خطأ", "حدث خطأ في جلب الصورة")
        except Exception as e:
            qt.QMessageBox.warning(self, "خطأ", f"حدث خطأ: {e}")
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()        
        self.setMinimumSize(1100,200)        
        self.setWindowTitle("أدوات الذكاء الإصتناعي")        
        self.التاب=qt.QTabWidget()
        self.التاب.setAccessibleName("الخيارات")
        self.التاب.addTab(tab1(),"المحادثة مع الذكاء الإصتناعي")
        self.التاب.addTab(tab2(),"التعرف على الصور")
        self.التاب.addTab(tab3(),"إجراء محادثة صوتية مع الذكاء الإصتناعي")
        self.التاب.addTab(tab4(),"إستخرج النص من الصوتيات باستخدام wit.ai")
        self.التاب.addTab(tab5(),"إستخرج النص من الصوتيات باستخدام google")
        self.التاب.addTab(tab6(),"توليد صور بالذكاء الإصتناعي")
        self.عن=qt.QPushButton("عن المطور")
        self.عن.setDefault(True)
        self.عن.clicked.connect(self.about)        
        l=qt.QVBoxLayout()        
        l.addWidget(self.التاب)
        l.addWidget(self.عن)        
        w=qt.QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)        
    def about(self):
        about.dialog(self).exec()            
app=qt.QApplication([])
app.setStyle('fusion')
w=main()
w.show()
app.exec()