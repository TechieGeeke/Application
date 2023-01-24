__version__ = '1.1.0'

# =========== MODULES ==============
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('kivy','window_icon','assets/icon.ico')
Config.set('kivy', 'exit_on_escape', 0)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'maxfps', '30')

import kivy, threading, time, socket, pyautogui
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.utils import platform
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import LabelBase
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from kivy.uix.gridlayout import GridLayout

# ============ INTIALISATION =============
Window.size = (350, 450)
Window.clearcolor = (0.186,0.2046,0.235,1.13)
if platform == 'win':
    from win32api import GetSystemMetrics
    Window.left = (GetSystemMetrics(0) - 350)/2
    Window.top = (GetSystemMetrics(1) - 450)/2
elif platform == 'android':
    Window.left = 225
    Window.top = 125
    
LabelBase.register(name='Oswald',
                   fn_regular='fonts/Oswald.ttf')
LabelBase.register(name='Teko',
                   fn_regular='fonts/Teko-Bold.ttf')
LabelBase.register(name='Dash',
                   fn_regular='fonts/Dashboard-Regular.ttf')

# ===== sounds =====
sound = SoundLoader.load('assets/sound.mp3')
errorsound = SoundLoader.load('assets/errorsound.mp3')

# ================ GUI =================
class LoadingWindow(Screen):
    def __init__(self, **kwargs):
        super(LoadingWindow, self).__init__(**kwargs)
        self.network = Label(text ="[b]Checking connectivity.[/b]", font_size ='9sp' , markup = True, pos=(0,-180))
        self.add_widget(Image(source= 'assets/load.gif', anim_delay = 0))
        self.add_widget(self.network)
        threading.Thread(target=self.connect).start()

    def screen_transition(self, *args):
        self.manager.current = 'login'
        
    def connect(self, host='http://google.com'):
        try:
            time.sleep(1)
            conn = socket.create_connection((socket.gethostbyname('one.one.one.one'), 80), 2)
            conn.close()
            threading.Thread(target=self.server).start()
            return True
        except Exception as err:
            print("No internet:", err)
            # popop
            return False

    def server(self, host='http://google.com'):
        self.network.text = "[b]Establishing connection to server.[/b]"
        try:
            global db
            import db
            threading.Thread(target=self.version).start()
            return True
        except Exception as err:
            return err

    def version(self,host='http://google.com'):
        self.network.text = "[b]Checking for updates...[/b]"
        self.version = db.fetch('version','1.1.0')
        if self.version['version'] == __version__:
            Clock.schedule_once(self.screen_transition, 1/60)
            return True
        else:
            print(f"Not latest version.. Current version is {version['version']}")
            return False
            #popup

# ============= LOGIN SCREEN ===============
class LoginWindow(Screen):
    def __init__(self, **kwargs):
        super(LoginWindow, self).__init__(**kwargs)
        self.add_widget(Label(text ="[b]Welcome Back[/b]", font_size ='30sp' , markup = True, halign="center", valign="top", text_size= (200,350)))
        self.add_widget(Label(text ="[color=6b727d][b]Login to continue[/b][/color]", font_size ='13sp' , markup = True, halign="center", valign="top", text_size= (131,272)))
        self.add_widget(Label(text ="[color=b7b9bd][b]Username[/b][/color]", font_size ='14sp' , markup = True, halign="left", valign="top", text_size= (200,150)))
        self.add_widget(Label(text ="[color=b7b9bd][b]Password[/b][/color]", font_size ='14sp' , markup = True, halign="left", valign="bottom",pos=(1,2), text_size= (200,55)))
        self.add_widget(Image(source='assets/typebox.png', pos= (0,35)))
        self.add_widget(Image(source='assets/typebox.png',y=-47))
        self.add_widget(Image(source="assets/user.png",size_hint= (0.06,0.06),x=78,y=246))
        self.add_widget(Image(source="assets/pass.png",size_hint= (0.05,0.05),x=78,y=166))
        self.add_widget(Label(text ="[color=b7b9bd][b]Don't have an account?[/b][/color]", font_size =12 , markup = True, halign="left", valign="bottom",size_hint=(0.1,0.1),x=104,y=50))
        self.usernameinp = TextInput(hint_text='Username',cursor_color = 'white', font_size = 17, size_hint= (0.5,0.075),x=100,y=243, foreground_color = (1,1,1,1) ,background_color= (0,0,0,0),multiline = False)
        self.passinp = TextInput(hint_text='Password',password_mask='•',cursor_color = 'white', password = True,font_size = 17, size_hint= (0.5,0.075),x=100,y=160, foreground_color = (1,1,1,1) ,background_color= (0,0,0,0),multiline = False)
        self.loginbtn = Button(text ="[b]Login[/b]", markup=True, background_normal = '',background_color ="#30b344", font_size = 12, size_hint =(0.38, 0.065), x=110, y=100)
        self.linkbtn = Button(text ="[color=0084ff]Create an account.[/color]", markup=True, background_color = (0,0,0,0) , font_size = 12, size_hint =(0.38, 0.065), x=170, y=58)
        self.add_widget(self.usernameinp)
        self.add_widget(self.passinp)
        self.add_widget(self.loginbtn)
        self.add_widget(self.linkbtn)
        self.loginbtn.bind(on_press = self.submit)
        self.linkbtn.bind(on_press = self.errorpopup)
        
    def errorpopup(self, button):
        self.box=FloatLayout()
        #self.lab=(Label(text="[b]Problem Connecting![/b]",markup=True,font_size=15,
        	#size_hint=(None,None),pos_hint={'x':.3,'y':.6}))
        #self.box.add_widget(self.lab)
        #self.but=(Button(text="close",size_hint=(None,None),
        	#width=50,height=25,pos_hint={'x':0,'y':0}))
        #self.box.add_widget(self.but)
        #self.box.add_widget(Button(text="blank",size_hint=(None,None),
        	#width=50,height=25,pos_hint={'x':.5,'y':0}))
        self.main_pop = Popup(title="",content=self.box,
        	size_hint=(None,None),size=(170,210),auto_dismiss=1, separator_height= 0,
                              background = 'assets/nonett.jpg')
        #self.but.bind(on_press=self.main_pop.dismiss)
        self.main_pop.open()
        
    def submit(self, *args):
        global username, password
        username = self.usernameinp.text
        password = self.passinp.text
        auth = db.auth(username,password)
        if auth == True:
            self.loginbtn.disabled = True
            self.manager.current = 'app'
            Window.clearcolor = (.08,.10222222222222223,0.2311111111111111,1)
            Window.size=(800,500)
            Window.borderless = 0
            
# =========== APPLICATION SCREEN =============
class AppWindow(Screen):
    def __init__(self, x=None,**kwargs):
        super(AppWindow, self).__init__(**kwargs)
        Clock.schedule_once(self.window, 1/60)
        Window.clearcolor = (.08,.10222222222222223,0.2311111111111111,1)
        Window.size=(800,500)
        Window.borderless = 0
        self.menu = None
        self.bgmode = 'dark'
        self.overlay = 0

    def switchmode(self):
        sound.play()
        if self.bgmode == 'dark':
            try:
                self.bgmode = 'light'
                Window.clearcolor = (173/255,216/255,230/255)
                self.categorylabel.color = "#000000"
                self.category1label.color = "#000000"
                self.h1label.color = "#000000"
                self.h2label.color = "#000000"
                self.versionlabel.color = "#000000"
                self.copyrightlabel.color = "#000000"
            except:
                pass
        else:
            try:
                self.bgmode = 'dark'
                self.categorylabel.color = "#ffffff"
                self.category1label.color = "#ffffff"
                self.h1label.color = "#ffffff"
                self.h2label.color = "#ffffff"
                self.versionlabel.color = "#ffffff"
                self.copyrightlabel.color = "#ffffff"
                Window.clearcolor = (.08,.102,0.231,1)
            except:
                pass
            
    def window(self, dt = None, **kwargs):
        Window.bind(mouse_pos= lambda w, p: on_motion(p))
        Window.bind(on_touch_down = lambda obj,p: on_touch_down(self, obj,p))

        # ==== DASH BG ====
        self.toprect = Rectangle(pos=(200, 410), size=(600, 90))
        self.siderect = Rectangle(pos=(0, 0), size=(200, 500))
        self.rectpiece = RoundedRectangle(pos=(199, 410), size=(1, 1), radius=[(0, 0), (0, 0), (-50, -50), (0, 0)])
        self.notif = Line(circle = (490, 455, 5), width = 15)
        self.mode = Line(circle = (540, 455, 5), width = 15)
        self.divider = Line(points=[189, 260, 11, 260, 11, 260], width=1)
        self.profilelayout = RoundedRectangle(pos = (700,435), size = (70,40), radius=[(20, 20), (20, 20), (20, 20), (20, 20)])
        self.hovereff = RoundedRectangle(pos=(10, 327), size_hint = (None, None), size = (180,40), radius=[(10, 10), (10, 10), (10, 10), (10, 10)])
        self.clickeff = RoundedRectangle(pos=(10, 327), size_hint = (None, None), size = (180,40), radius=[(10, 10), (10, 10), (10, 10), (10, 10)])
        
        # ===== IMAGES ====
        self.logo = Image(source='assets/logo.png', pos= (20,410), size_hint = (None,None) ,size = (100,100))
        self.home = Image(source='assets/home.png', pos= (27,341), size_hint = (None,None) ,size = (16,16), color = '7c4dff')
        self.settings = Image(source='assets/settings.png', pos= (27,289), size_hint = (None,None) ,size = (16,16))
        self.bellicon = Image(source='assets/bell.png', pos= (530,445), size_hint = (None,None) ,size = (21,21))
        self.stati = Image(source='assets/statistics.png', pos= (27,180), size_hint = (None,None) ,size = (16,16))
        self.moderateicon = Image(source='assets/manage.png', pos= (27,130), size_hint = (None,None) ,size = (16,16))
        self.messicon = Image(source='assets/announce.png', pos= (27,80), size_hint = (None,None) ,size = (16,16))
        self.historyicon = Image(source='assets/history.png', pos= (27,30), size_hint = (None,None) ,size = (16,16))
        self.psettings = Image(source='assets/settingsblue.png', pos= (743,445), size_hint = (None,None) ,size = (18,18))
        self.usericon = Image(source='assets/ui.png', pos= (705,440), size_hint = (None,None) ,size = (30,30))
        self.boticon = Image(source='assets/bot.png', pos= (300,150), size_hint = (None,None), size = (100,100))
        self.bombicon = Image(source='assets/bot.png', pos= (600,150), size_hint = (None,None), size = (100,100))
        self.hovercircle1 = Image(source='assets/circle.png', pos= (290,150), size_hint = (None,None), size = (120,120), opacity = 0)
        self.hovercircle2 = Image(source='assets/circle.png', pos= (590,150), size_hint = (None,None), size = (120,120), opacity = 0)
        self.lightmode = Image(source='assets/sun.png', pos= (478,443), size_hint = (None,None) ,size = (25,25))

        # ===== LABELS =====
        self.namelabel = Label(text = "[b]USERNAME??[/b]", pos = (260,215), font_size ='15sp' , markup = True, text_size= (90,40), font_name="Oswald")
        self.dashlabel = Label(text ="[b]DASHBOARD[/b]", pos = (-345,150), font_size ='13sp' , markup = True, text_size= (90,40), color= '#d9d7d7',font_name="Teko")
        self.homelabel = Label(text ="Home", pos = (-300,110), font_size ='12sp' , markup = True, text_size= (90,40), font_name="Oswald")
        self.settingslabel = Label(text ="Settings", pos = (-300,60), font_size ='12sp' , markup = True, text_size= (90,40), font_name="Oswald")
        self.utilitieslabel = Label(text ="[b]UTILITIES[/b]", pos = (-345,-5), font_size ='13sp' , markup = True, text_size= (90,40), color= '#d9d7d7',font_name="Teko")
        self.statilabel = Label(text ="Statistics", pos = (-300,-50), font_size ='12sp' , markup = True, text_size= (90,40), font_name="Oswald")
        self.managelabel = Label(text ="Moderate", pos = (-300,-100), font_size ='12sp' , markup = True, text_size= (90,40), font_name="Oswald")
        self.announce = Label(text ="Message", pos = (-300,-150), font_size ='12sp' , markup = True, text_size= (90,40), font_name="Oswald")
        self.history = Label(text ="History", pos = (-300,-200), font_size ='12sp' , markup = True, text_size= (90,40), font_name="Oswald")
        self.categorylabel = Label(text ="Choose a category...", pos = (-50,100), font_size ='25sp' , markup = True, text_size= (200,40), font_name="Teko")
        self.serverlabel = Label(text ="Select a server to view history!", pos = (50,100), font_size ='25sp' , markup = True, text_size= (400,40), font_name="Teko")
        self.chatlabel = Label(text ="Select a server to view live chat!", pos = (50,100), font_size ='25sp' , markup = True, text_size= (400,40), font_name="Teko")
        self.category1label = Label(text ="Select a category from below inorder to start moderating and to proceed further!", pos = (0,100), font_size ='12sp' , markup = True, text_size= (300,100), font_name="Oswald")
        self.h1label = Label(text ="BOMB SQUAD", pos = (-20.5,-130), font_size ='20sp' , markup = True, text_size= (200,40), font_name="Dash")
        self.h2label = Label(text ="DISCORD BOT", pos = (280.5,-130), font_size ='20sp' , markup = True, text_size= (200,40), font_name="Dash")
        self.versionlabel = Label(text =f"v{__version__}", pos = (-40,-190), font_size ='15sp' , markup = True, text_size= (300,100), font_name="Teko")
        self.copyrightlabel = Label(text ="© 2022 ROCKY (DISCORD)", pos = (390,-190), font_size ='15sp' , markup = True, text_size= (300,100), font_name="Teko")

        # ===== WIDGETS =====
        self.canvas.add(Color(14/225,6/225,36/225))
        self.canvas.add(self.toprect)
        self.canvas.add(self.siderect)
        self.canvas.add(self.rectpiece)
        self.canvas.add(Color(38/225/225,47/225,76/225,255/225))
        self.canvas.add(self.notif)
        self.canvas.add(self.mode)
        self.canvas.add(Color(38/225/225,47/225,76/225,255/225))
        self.canvas.add(self.profilelayout)
        self.canvas.add(Color(30/225, 17/225, 66/225))
        self.canvas.add(self.hovereff)
        self.canvas.add(self.clickeff)
        self.add_widget(self.logo)
        self.add_widget(self.home)
        self.add_widget(self.settings)
        self.add_widget(self.bellicon)
        self.add_widget(self.psettings)
        self.add_widget(self.usericon)
        self.add_widget(self.categorylabel)
        self.add_widget(self.category1label)
        self.add_widget(self.namelabel)
        self.add_widget(self.dashlabel)
        self.add_widget(self.homelabel)
        self.add_widget(self.settingslabel)
        self.add_widget(self.h1label)
        self.add_widget(self.h2label)
        self.add_widget(self.versionlabel)
        self.add_widget(self.copyrightlabel)
        self.add_widget(self.boticon)
        self.add_widget(self.bombicon)
        self.add_widget(self.hovercircle1)
        self.add_widget(self.hovercircle2)
        self.add_widget(self.lightmode)
        

        def clearscreen():
            try:
                self.remove_widget(self.h1label)
            except:
                pass
            try:
                self.remove_widget(self.h2label)
            except:
                pass
            try:
                self.remove_widget(self.versionlabel)
            except:
                pass
            try:
                self.remove_widget(self.copyrightlabel)
            except:
                pass
            try:
                self.remove_widget(self.boticon)
            except:
                pass
            try:
                self.remove_widget(self.bombicon)
            except:
                pass
            try:
                self.remove_widget(self.hovercircle1)
            except:
                pass
            try:
                self.remove_widget(self.hovercircle2)
            except:
                pass
            try:
                self.remove_widget(self.categorylabel)
            except:
                pass
            try:
                self.remove_widget(self.category1label)
            except:
                pass
            try:
                self.remove_widget(self.serverlabel)
            except:
                pass
            try:
                self.remove_widget(self.chatlabel)
            except:
                pass
            try:
                self.root.remove_widget(self.chatlayout)
            except:
                pass
            try:
                self.root.remove_widget(self.layout)
            except:
                pass
            try:
                self.remove_widget(self.root)
            except:
                pass
            try:
                self.remove_widget(self.chatroot)
            except:
                pass
            try:
                self.remove_widget(self.msgroot)
            except:
                pass
            try:
                self.remove_widget(self.gr)
            except:
                pass
            try:
                self.remove_widget(self.clabel)
            except:
                pass
            

        def popy(self, x, y):
            layout = GridLayout(cols = 1, padding = (-13,-33,-13,-14))
            refresh = Button(text = "Refresh",background_color = 'black')
            refresh1 = Button(text = "Refresh",background_color = 'black')
            refresh2 = Button(text = "Refresh",background_color = 'black')
            refresh3 = Button(text = "Refresh",background_color = 'black')
            closeButton = Button(text = "Close the pop-up", background_color = 'black')
            layout.add_widget(refresh)
            layout.add_widget(refresh1)
            layout.add_widget(refresh2)
            layout.add_widget(refresh3)
            layout.add_widget(closeButton)       
            popup = Popup(title ='', content = layout,border=(10,10,10,10), size_hint =(None, None), size =(200, 150),  pos_hint={'x': x / Window.width, 
                            'y': y /  Window.height}, auto_dismiss=False, separator_height= 0)
            def closeit(self):
                self.overlay = 0
            def openit(self):
                self.overlay = 1
            popup.bind(on_open=openit)
            popup.bind(on_dismiss=closeit)
            popup.open()
            closeButton.bind(on_press = popup.dismiss)
            
        def on_touch_down(self, obj, p):
            if self.overlay == 0:
                if p.button == 'left':

                    if self.lightmode.collide_point(p.x,p.y):
                        self.switchmode()
                    
                    if self.boticon.collide_point(p.x,p.y) and self.boticon in list(self.children):
                        if self.menu != 'bomb':
                            self.menu = "bomb"
                            self.canvas.add(Color(27/225,32/225,64/225,255/225))
                            self.canvas.add(self.divider)
                            self.add_widget(self.utilitieslabel)
                            self.add_widget(self.statilabel)
                            self.add_widget(self.managelabel)
                            self.add_widget(self.announce)
                            self.add_widget(self.history)
                            self.add_widget(self.stati)
                            self.add_widget(self.moderateicon)
                            self.add_widget(self.messicon)
                            self.add_widget(self.historyicon)
                            sound.play()
                        else:
                            errorsound.play()
                    
                    if self.bombicon.collide_point(p.x,p.y) and self.bombicon in list(self.children):
                        if self.menu != "bot":
                            self.menu = "bot"
                            self.clickeff.pos = (10, 327)
                            self.canvas.remove(self.divider)
                            self.canvas.remove(Color(27/225,32/225,64/225,255/225))
                            self.remove_widget(self.utilitieslabel)
                            self.remove_widget(self.statilabel)
                            self.remove_widget(self.managelabel)
                            self.remove_widget(self.announce)
                            self.remove_widget(self.history)
                            self.remove_widget(self.stati)
                            self.remove_widget(self.moderateicon)
                            self.remove_widget(self.messicon)
                            self.remove_widget(self.historyicon)
                            self.clickeff.pos = (10, 327)
                            self.home.color = "#7c4dff"
                            self.settings.color = "#ffffff"
                            self.stati.color = "#ffffff"
                            self.moderateicon.color = "#ffffff"
                            self.messicon.color = "#ffffff"
                            self.historyicon.color = "#ffffff"
                            sound.play()
                            
                        else:
                            errorsound.play()
    
                    if p.x >= 10 and p.x <= 189 and p.y >= 327 and p.y <= 367:
                        if self.clickeff.pos != (10, 327):
                            sound.play()
                            clearscreen()
                            self.clickeff.pos = (10, 327)
                            self.home.color = "#7c4dff"
                            self.settings.color = "#ffffff"
                            self.stati.color = "#ffffff"
                            self.moderateicon.color = "#ffffff"
                            self.messicon.color = "#ffffff"
                            self.historyicon.color = "#ffffff"

                            self.add_widget(self.h1label)
                            self.add_widget(self.h2label)
                            self.add_widget(self.versionlabel)
                            self.add_widget(self.copyrightlabel)
                            self.add_widget(self.boticon)
                            self.add_widget(self.bombicon)
                            self.add_widget(self.hovercircle1)
                            self.add_widget(self.hovercircle2)
                            self.add_widget(self.categorylabel)
                            self.add_widget(self.category1label)
                        else:
                            errorsound.play()
                    
                    if p.x >= 10 and p.x <= 189 and p.y >= 277 and p.y <= 320:
                        if self.clickeff.pos != (10,277):
                            clearscreen()
                            sound.play()
                            self.clickeff.pos = (10,277)
                            self.home.color = "#ffffff"
                            self.settings.color = "#7c4dff"
                            self.stati.color = "#ffffff"
                            self.moderateicon.color = "#ffffff"
                            self.messicon.color = "#ffffff"
                            self.historyicon.color = "#ffffff"                     
                        
                        else:
                            errorsound.play()
                    
                    if self.menu == "bomb":
                        if p.x >= 10 and p.x <= 189 and p.y >= 167 and p.y <= 210:
                            if self.clickeff.pos != (10,167):
                                sound.play()
                                clearscreen()
                                self.clickeff.pos = (10,167)
                                self.home.color = "#ffffff"
                                self.settings.color = "#ffffff"
                                self.stati.color = "#7c4dff"
                                self.moderateicon.color = "#ffffff"
                                self.messicon.color = "#ffffff"
                                self.historyicon.color = "#ffffff"
                            else:
                               errorsound.play()
                    
                        elif p.x >= 10 and p.x <= 189 and p.y >= 117 and p.y <= 160:
                            if self.clickeff.pos != (10,117):
                                sound.play()
                                clearscreen()
                                self.clickeff.pos = (10,117)
                                self.home.color = "#ffffff"
                                self.settings.color = "#ffffff"
                                self.stati.color = "#ffffff"
                                self.moderateicon.color = "#7c4dff"
                                self.messicon.color = "#ffffff"
                                self.historyicon.color = "#ffffff"
                            else:
                                errorsound.play()

                        elif p.x >= 10 and p.x <= 189 and p.y >= 67 and p.y <= 110:
                            if self.clickeff.pos != (10,67):
                                sound.play()
                                clearscreen()
                                self.clickeff.pos = (10,67)
                                self.home.color = "#ffffff"
                                self.settings.color = "#ffffff"
                                self.stati.color = "#ffffff"
                                self.moderateicon.color = "#ffffff"
                                self.messicon.color = "#7c4dff"
                                self.historyicon.color = "#ffffff"
                                self.add_widget(self.chatlabel)
                                self.chatlayout = GridLayout(cols=1, spacing=0, size = (0,0), size_hint= (None,None))
                                self.chatlayout.bind(minimum_height=self.chatlayout.setter('height'))
                                for i in range(10):
                                    self.vr = Image(source='assets/rect.png', size_hint = (None,None) ,size = (500,80))
                                    self.chatlayout.add_widget(self.vr)
                                self.chatroot = ScrollView(pos = (250,30) ,size_hint=(1, None), size=(0, 280),do_scroll_x=0)
                                self.chatroot.add_widget(self.chatlayout)
                                self.add_widget(self.chatroot)
                            else:
                                errorsound.play()
                    
                        elif p.x >= 10 and p.x <= 189 and p.y >= 17 and p.y <= 65:
                            if self.clickeff.pos != (10,17):
                                sound.play()
                                clearscreen()
                                self.clickeff.pos = (10,17)
                                self.home.color = "#ffffff"
                                self.settings.color = "#ffffff"
                                self.stati.color = "#ffffff"
                                self.moderateicon.color = "#ffffff"
                                self.messicon.color = "#ffffff"
                                self.historyicon.color = "#7c4dff"
                                self.add_widget(self.serverlabel)
                                self.layout = GridLayout(cols=1, spacing=15, size = (0,0), size_hint= (None,None))
                                self.layout.bind(minimum_height=self.layout.setter('height'))
                                self.vr = Button(text='',background_normal = 'assets/rect.png',size_hint=(None, None),width=500,height=70)
                                self.layout.add_widget(self.vr)
                                self.vr.bind(on_press=lambda y: showmsgs('VORTEX VS ROCKY BANG'))
                                self.root = ScrollView(pos = (250,30) ,size_hint=(1, None), size=(0, 280),do_scroll_x=0)
                                self.root.add_widget(self.layout)
                                self.add_widget(self.root)
                            else:
                                errorsound.play()
                elif p.button == 'right':
                    popy(self,p.x,p.y)
                    
        def showmsgs(sn):
            clearscreen()
            self.msglayout = GridLayout(cols=1, spacing=20, size = (500,0), size_hint= (None,None))
            self.msglayout.bind(minimum_height=self.msglayout.setter('height'))
            self.msgroot = ScrollView(pos = (250,30) ,size_hint=(1, None), size=(0, 280),do_scroll_x=0,scroll_y=0,effect_cls="DampedScrollEffect")
            
            self.gr = Image(source='assets/gr.png', pos= (235,325), size_hint = (None,None) ,size = (20,50))
            self.clabel = Label(text =f"LIVE CHAT FOR: [color=3333ff]{sn}[/color]", pos = (87,100), font_size ='25sp', text_size= (450,40), font_name="Teko",markup=True)
            #self.plr = Image(source='assets/player.png', size_hint = (None,None) ,size = (10,10))
            
            self.add_widget(self.gr)
            self.add_widget(self.clabel)
            self.msgroot.add_widget(self.msglayout)
            test = {'Abhi (pb-aadsada5644d) ':('hey','date time'),'Hellola (pb-aadsada5644d)':('what?','date time'),'asaasda':('nooo<','dasda'),'asasda':('nooo<','dasda'),'asaasda':('nooo<','dasda'),'asasda':('nooo<','dasda'),'asaasasda':('nooo<','dasda'),'asasdfa':('nooo<','dasda')}
            
            for i,j in test.items():
                self.chat_history = Label(size_hint_y = None, size = (0,50), text=f'[color=ff3300]{i} {j[1]}[/color]: \n{j[0]}', text_size = (500,None),markup=True, font_size ='18sp',color='yellow')
                self.msglayout.add_widget(self.chat_history)  
            #self.msglayout.remove_widget(self.msglayout.children[5])
            self.add_widget(self.msgroot)
            
                            
        def on_motion(p):
            if self.overlay == 0:
                if self.boticon.collide_point(p[0],p[1]):
                    Animation(x = 290, size = (120,120), duration=0).start(self.boticon)
                    self.hovercircle1.opacity  = 100
                else:
                    self.hovercircle1.opacity  = 0
                    Animation(x = 300, size = (100,100), duration=0).start(self.boticon)

                if self.bombicon.collide_point(p[0],p[1]):
                    Animation(x = 590,size = (120,120), duration=0).start(self.bombicon)
                    self.hovercircle2.opacity  = 100
                else:
                    self.hovercircle2.opacity  = 0
                    Animation(x = 600,size = (100,100), duration=0).start(self.bombicon)

                if p[0] >= 10 and p[0] <= 189 and p[1] >= 327 and p[1] <= 367:
                    self.hovereff.pos = (10, 327)
                    self.homelabel.color = '#7c4dff'
                    self.settingslabel.color = '#ffffff'
                    self.announce.color = '#ffffff'
                    self.statilabel.color = '#ffffff'
                    self.managelabel.color = '#ffffff'
                    self.history.color = '#ffffff'
                    
                elif p[0] >= 10 and p[0] <= 189 and p[1] >= 277 and p[1] <= 320:
                    self.hovereff.pos = (10,277)
                    self.homelabel.color = '#ffffff'
                    self.settingslabel.color = '#7c4dff'
                    self.announce.color = '#ffffff'
                    self.statilabel.color = '#ffffff'
                    self.managelabel.color = '#ffffff'
                    self.history.color = '#ffffff'

                elif self.menu == 'bomb':    
                    if p[0] >= 10 and p[0] <= 189 and p[1] >= 167 and p[1] <= 210:
                        self.hovereff.pos = (10,167)
                        self.homelabel.color = '#ffffff'
                        self.settingslabel.color = '#ffffff'
                        self.announce.color = '#ffffff'
                        self.statilabel.color = '#7c4dff'
                        self.managelabel.color = '#ffffff'
                        self.history.color = '#ffffff'

                    elif p[0] >= 10 and p[0] <= 189 and p[1] >= 117 and p[1] <= 160:
                        self.hovereff.pos = (10,117)
                        self.homelabel.color = '#ffffff'
                        self.settingslabel.color = '#ffffff'
                        self.announce.color = '#ffffff'
                        self.statilabel.color = '#ffffff'
                        self.managelabel.color = '#7c4dff'
                        self.history.color = '#ffffff'

                    elif p[0] >= 10 and p[0] <= 189 and p[1] >= 67 and p[1] <= 110:
                        self.hovereff.pos = (10,67)
                        self.homelabel.color = '#ffffff'
                        self.settingslabel.color = '#ffffff'
                        self.announce.color = '#7c4dff'
                        self.statilabel.color = '#ffffff'
                        self.managelabel.color = '#ffffff'
                        self.history.color = '#ffffff'

                    elif p[0] >= 10 and p[0] <= 189 and p[1] >= 17 and p[1] <= 65:
                        self.hovereff.pos = (10,17)
                        self.homelabel.color = '#ffffff'
                        self.settingslabel.color = '#ffffff'
                        self.announce.color = '#ffffff'
                        self.statilabel.color = '#ffffff'
                        self.managelabel.color = '#ffffff'
                        self.history.color = '#7c4dff'

                    else:
                        self.hovereff.pos = (-1000, 10)
                        self.homelabel.color = '#ffffff'
                        self.settingslabel.color = '#ffffff'
                        self.announce.color = '#ffffff'
                        self.statilabel.color = '#ffffff'
                        self.managelabel.color = '#ffffff'
                        self.history.color = '#ffffff'
                    
                else:
                    self.hovereff.pos = (-1000, 10)
                    self.homelabel.color = '#ffffff'
                    self.settingslabel.color = '#ffffff'
                    self.announce.color = '#ffffff'
                    self.statilabel.color = '#ffffff'
                    self.managelabel.color = '#ffffff'
                    self.history.color = '#ffffff'
    
class Vortex(App):
    def build(self):
        self.title = 'Vortex Control Panel'
        sm = ScreenManager(transition = FadeTransition())
        #sm.add_widget(LoadingWindow(name='loader'))
        #sm.add_widget(LoginWindow(name='login'))
        sm.add_widget(AppWindow(name='app'))
        return sm

if __name__ == "__main__":
    Vortex().run()
    Window.close()
