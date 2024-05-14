from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
import gtts,os,langdetect,pyperclip,PIL.Image,about,dic,winsound,time,webbrowser
import speech_recognition as sr
import google.generativeai as genai
genai.configure(api_key="")
model=genai.GenerativeModel('gemini-pro')
response=model.start_chat()
if not os.path.exists("data"):
    os.makedirs("data")
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
        self.إستماع=qt.QPushButton("الإستماع الى الرسالة ")
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
        try:
            ask=self.الكتابة.text()
            response=self.chat.send_message(ask)
            self.الردود.clear()
            النتيجة=response.text.split("\n")
            self.الردود.addItems(النتيجة)
            self.نص_الرسالة=response.text
            self.الردود.setFocus()
        except:
            qt.QMessageBox.warning(self,"عفوا","يرجى إدخال نص, إذا تم هذا, تأكد من عدم وجود ألفاظ خارجة, أو تأكد من إتصالك بالإنترنت")
    def copy(self):
        pyperclip.copy(self.الردود.currentText())
    def copyAll(self):
        pyperclip.copy(self.نص_الرسالة)
    def listen(self):                                    
        try:
            lang=langdetect.detect(self.نص_الرسالة)
            result=gtts.gTTS(self.نص_الرسالة,lang=lang)
            result.save("data/message.mp3")            
            if self.m.isPlaying():
                self.إستماع.setText("الاستماع الى الرسالة")
                self.m.stop()
            else:
                self.إستماع.setText("إيقاف")
                self.m.setSource(qt2.QUrl.fromLocalFile("data/message.mp3"))
                self.m.play()                            
        except:
            qt.QMessageBox.information(self,"عفوا لم يتم العثور على نص, إذا كان هناك نص قم بالتأكد من الإتصال بالإنترنت")
class tab2(qt.QWidget):
    def __init__(self):        
        super().__init__()
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
        self.إستماع=qt.QPushButton("الإستماع الى الرسالة ")
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
        model=genai.GenerativeModel('gemini-pro-vision')        
        try:
            ask1=self.السؤال.text()
            ask=PIL.Image.open(self.مسار.text())
            response=model.generate_content([ask1,ask])
            self.الردود.clear()
            النتيجة=response.text.split("\n")
            self.الردود.addItems(النتيجة)
            self.الردود.setFocus()
            self.نص_الرسالة=response.text
        except:
            qt.QMessageBox.information(self,"عفوا","يرجى إرفاق سورة, أو التأكد من إتصالك بالإنترنت")
    def copy(self):
        pyperclip.copy(self.الردود.currentText())
    def copyAll(self):
        pyperclip.copy(self.نص_الرسالة)
    def listen(self):                                    
        try:
            lang=langdetect.detect(self.نص_الرسالة)
            result=gtts.gTTS(self.نص_الرسالة,lang=lang)
            result.save("data/message.mp3")            
            if self.m.isPlaying():
                self.إستماع.setText("الاستماع الى الرسالة")
                self.m.stop()                    
            else:
                self.إستماع.setText("إيقاف")
                self.m.setSource(qt2.QUrl.fromLocalFile("data/message.mp3"))
                self.m.play()                            
        except:
            qt.QMessageBox.information(self,"عفوا لم يتم العثور على نص, إذا كان هناك نص قم بالتأكد من الإتصال بالإنترنت")
    def opinFile(self):
        file=qt.QFileDialog()
        file.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptOpen)
        if file.exec()==qt.QFileDialog.DialogCode.Accepted:
            self.مسار.setText(file.selectedFiles()[0])
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
        self.m.setSource(qt2.QUrl(None))
        lang=dic.languages[self.اللغة.currentText()]
        SR=sr.Recognizer()                
        with sr.Microphone() as src:                
            winsound.PlaySound("data/1.wav",1)
            audio=SR.listen(src)            
        try:               
            winsound.PlaySound("data/2.wav",1)
            text=SR.recognize_google(audio,language=lang)
        except:
            text="sorry"                                
            winsound.PlaySound("data/3.wav",1)            
        try:
            res=self.chat.send_message(text).text
        except:            
            res="error"
        try:
            Language=langdetect.detect(res)
        except:
            Language="en"
        tts=gtts.gTTS(res,lang=Language)
        tts.save("data/speek.mp3")            
        winsound.PlaySound("data/4.wav",1)
        self.m.setSource(qt2.QUrl.fromLocalFile("data/speek.mp3"))
        self.is_playing=True
        self.m.play()            
class tab4(qt.QWidget):
    def __init__(self):
        super().__init__()    
        self.فتح=qt.QPushButton("فتح ملف .wav")
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
        self.إستخراج.clicked.connect(self.r)
        self.إظهار3=qt.QLabel("النص المستخرَج")
        self.النص=qt.QLineEdit()
        self.النص.setAccessibleName("النص المستخرَج")
        self.النص.setReadOnly(True)
        self.نسخ=qt.QPushButton("نسخ النص")
        self.نسخ.setDefault(True)
        self.نسخ.clicked.connect(self.c)
        self.إظهار4=qt.QLabel("إدخال الرمز المميز Client Access Token للغة من موقع wit.ai")
        self.مخصص=qt.QLineEdit()        
        self.مخصص.setAccessibleName("إدخال الرمز المميز Client Access Token للغة من موقع wit.ai")
        self.wit=qt.QPushButton("الذهاب الى موقع wit.ai")
        self.wit.setDefault(True)
        self.wit.clicked.connect(self.wit_ai)
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
    def wit_ai(self):                                                
        webbrowser.open("wit.ai")
    def r(self):                
        اللغات=self.اللغة.currentIndex()
        recognizer=sr.Recognizer()    
        audio_file=(self.مسار.text())    
        if not self.مسار.text():
            qt.QMessageBox.warning(self,"تنبيه","لم يتم تحديد ملف للتعرف عليه")
            return
        if not audio_file.endswith(".wav"):
            qt.QMessageBox.warning(self, "تنبيه", "يجب أن يكون الملف بامتداد .wav")
            return        
        with sr.AudioFile(audio_file) as source:
            audio_data=recognizer.record(source)        
            try:
                if اللغات==0:
                    text=recognizer.recognize_wit(audio_data,"")
                    self.النص.setText(text)
                if اللغات==1:
                    text=recognizer.recognize_wit(audio_data,"")
                    self.النص.setText(text)                                    
                if اللغات==2:                                        
                    try:
                        if not self.مخصص.text():        
                            qt.QMessageBox.warning(self,"تنبيه","يرجى إدخال رمز اللغة المطلوب")                        
                            return
                        text=recognizer.recognize_wit(audio_data,self.مخصص.text())
                        self.النص.setText(text)                                                        
                    except:
                        qt.QMessageBox.warning(self,"تنبيه","حدثت مشكلة, ربما رمز اللغة غير صحيح, أعد المحاولة")
            except sr.UnknownValueError:
                qt.QMessageBox.warning(self, "تنبيه", "حدث خطأ، ربما المقطع فارغ أو اللغة غير صحيحة أو لم يتم التعرف بشكل جيد على المقطع")
            except sr.RequestError as e:                
                qt.QMessageBox.warning(self, "تنبيه", "فشلت عملية استخراج النص، ربما امتداد الملف غير مدعوم أو هناك مشكلة في الإنترنت")    
        self.النص.setFocus()
    def c(self):
        pyperclip.copy(self.النص.text())
    def opinFile(self):
        file=qt.QFileDialog()
        file.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptOpen)
        if file.exec()==qt.QFileDialog.DialogCode.Accepted:
            self.مسار.setText(file.selectedFiles()[0])                                 
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()        
        self.setMinimumSize(900,200)        
        self.setWindowTitle("أدوات الذكاء الإصتناعي")        
        self.التاب=qt.QTabWidget()
        self.التاب.setAccessibleName("الخيارات")
        self.التاب.addTab(tab1(),"المحادثة مع الذكاء الإصتناعي")
        self.التاب.addTab(tab2(),"التعرف على الصور")
        self.التاب.addTab(tab3(),"إجراء محادثة صوتية مع الذكاء الإصتناعي")
        self.التاب.addTab(tab4(),"إستخرج النص من الصوتيات")
        self.عن=qt.QPushButton("عن المطور")
        self.عن.setDefault(True)
        self.عن.clicked.connect(self.about)
        self.مهم=qt.QPushButton("تنبيه هام")
        self.مهم.setDefault(True)
        self.مهم.clicked.connect(self.importint)
        l=qt.QVBoxLayout()        
        l.addWidget(self.التاب)
        l.addWidget(self.عن)
        l.addWidget(self.مهم)
        w=qt.QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)        
    def about(self):
        about.dialog(self).exec()        
    def importint(self):
        qt.QMessageBox.warning(self,"تنبيه هام","عند الضغت على زر الإرسال وزر بدء التحدث وزر بدء إستخراج النص, يرجى تجنب التحرك أبدا داخل الكمبيوتر حتى يأتي الرد, لأن التحرك سيعطل البرنامج أثناء تحميله للنتائج")
app=qt.QApplication([])
app.setStyle('fusion')
w=main()
w.show()
app.exec()