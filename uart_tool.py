#A flash and test tool for sony xarina
#20130626. fantao
import wx
import os
#import socket
import serial
import binascii
import encodings
import string

#the whole panel set into
#   8 rows and 5 colums
ROW   = 9
COLUM = 9
WHOLE_SIZE  = (520, 415)

#location, in row 1
button_size = (75, 28)
button1_loc = (1, 0)
button2_loc = (1, 1)
button3_loc = (1, 2)
button4_loc = (1, 3)
button5_loc = (1, 4)
button6_loc = (1, 5)
button7_loc = (2, 0)

class Frame(wx.Frame):
    def __init__(self, parent = None, title = "Tool"):
        wx.Frame.__init__(self, parent = None, title = "Flash Tool",
                          size = WHOLE_SIZE)
        self.InitUi()
        self.Centre()
        
    def InitUi(self):
        #set menubar and statusbar
        self.InitBar()

        panel = wx.Panel(self)
        #set the whole panel into 8 rows and 5 colums
        sizer = wx.GridBagSizer(ROW, COLUM)
        #sizer = wx.GridSizer(ROW, COLUM, ROW, COLUM)
  
        self.FlashFunction(panel, sizer)
        
    def FlashFunction(self, panel, sizer):
        '''
            pain the pannel of Flash Function
        '''

        button1 = wx.Button(panel, label="放大", size=button_size)
        button2 = wx.Button(panel, label="缩小", size=button_size)
        button3 = wx.Button(panel, label="停止", size=button_size)
        button4 = wx.Button(panel, label="4", size=button_size)
        button5 = wx.Button(panel, label="放大-十进制", size=button_size)
        button6 = wx.Button(panel, label="放大-字串/B", size=button_size)
        button7 = wx.Button(panel, label="放大-字串/7B", size=button_size)
        
        sizer.Add(button1, pos = button1_loc,flag = wx.ALIGN_LEFT, border = 10)
        sizer.Add(button2, pos = button2_loc,flag = wx.ALIGN_LEFT, border = 10)
        sizer.Add(button3, pos = button3_loc,flag = wx.ALIGN_LEFT, border = 10)
        sizer.Add(button4, pos = button4_loc,flag = wx.ALIGN_LEFT, border = 10)
        sizer.Add(button5, pos = button5_loc,flag = wx.ALIGN_LEFT, border = 10)
        sizer.Add(button6, pos = button6_loc,flag = wx.ALIGN_LEFT, border = 10)
        sizer.Add(button7, pos = button7_loc,flag = wx.ALIGN_LEFT, border = 10)
        
        self.Bind(wx.EVT_BUTTON, self.button1_func, button1)
        self.Bind(wx.EVT_BUTTON, self.button2_func, button2)
        self.Bind(wx.EVT_BUTTON, self.button3_func, button3)
        self.Bind(wx.EVT_BUTTON, self.button4_func, button4)
        self.Bind(wx.EVT_BUTTON, self.button5_func, button5)
        self.Bind(wx.EVT_BUTTON, self.button6_func, button6)
        self.Bind(wx.EVT_BUTTON, self.button7_func, button7)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(2)
        panel.SetSizerAndFit(sizer)

        return True

    def start_con(self):
        global ser
        com_val = ch_com.GetValue()
        bd_val = ch_bd.GetValue()
        bd = string.atoi(bd_val)
        #print type(bd)
        com_val_str = com_val.encode('utf-8')
        ser = serial.Serial(com_val_str, bd)

        if ser.isOpen() != True:
            print "failed to open uart"
            return False
        
    def button1_func(self, a):
        val = "ff010020000000"
        val1 = binascii.b2a_hex(val)
        hexval = val1.decode("hex")
        #print hexval
        num = ser.write(hexval)
        
    def button2_func(self, a):
        val = "ff 01 00 40 00 00 00"
        val1 = binascii.b2a_hex(val)
        hexval = val1.decode("hex")
        #print type(val1)
        num = ser.write(hexval)

    def button3_func(self, a):
        val = "ff010000000000"
        #print type(val)
        hexval = val.decode("hex")
        #print hexval
        #print type(hexval)
        num = ser.write(hexval)

    def button4_func(self, a):
        val = "ff010020000000"
        hexval = int(val, 16)
        #print hexval
        #print type(hexval)
        num = ser.write(hexval)

    def button5_func(self, a):
        val = ["FF",'01','00','20','00','00','00']
        for i in val:
            byt = int(i, 16)
            num = ser.write(byt)
            #print val
            #print type(i)
            
    def button6_func(self, a):
        val = ["FF",'01','00','20','00','00','00']
        for i in val:
            num = ser.write(i)
            #print val
            
    def button7_func(self, a):
        val = "ff010020000000"
        num = ser.write(val)
            
    def InitBar(self):
        '''
            init the menubar and statusbar
        '''      
        menubar  = wx.MenuBar()
        
        filemenu = wx.Menu()
        confmenu = wx.Menu()
        helpmenu = wx.Menu()
        connect  = wx.Menu()
        
        menubar.Append(filemenu, "&File")
        menubar.Append(confmenu, "&Configure")
        menubar.Append(helpmenu, "&Help")
        
        filemenu.AppendMenu(wx.ID_ANY, '&Connect', connect)
        filemenu.AppendSeparator()
        ConnectUart = connect.Append(wx.ID_ANY, 'Serial Port')
        WinClose = filemenu.Append(wx.ID_EXIT, 'Quit')
        
        conf_uart = confmenu.Append(wx.ID_ANY, 'Serial Port')
        help_help = helpmenu.Append(wx.ID_ANY, 'Help')
        Help_About = helpmenu.Append(wx.ID_ANY, 'About')
        
        self.Bind(wx.EVT_MENU, self.ConfUart, conf_uart)
        self.Bind(wx.EVT_MENU, self.About, Help_About)
        self.Bind(wx.EVT_MENU, self.Help, help_help)
        self.Bind(wx.EVT_MENU, self.OnQuit, WinClose)
        
        self.SetMenuBar(menubar)

        statusbar = self.CreateStatusBar()
        statusbar.SetStatusText('status: Unconnect')

        return True

    def ConfUart(self, e):
        serial = Configure(None, title='Configure serial port')
        serial.Ui_Uart()
        serial.SetSize((270, 320))
        serial.ShowModal()
        serial.Destroy()

    def About(sel, e):
        AboutDia = Configure(None, title = 'About this tool')
        AboutDia.Ui_About()
        AboutDia.SetSize((200, 200))
        AboutDia.ShowModal()
        AboutDia.Destroy()

    def Help(sel, e):
        HelpDia = Configure(None, title = 'Help')
        HelpDia.Ui_Help()
        HelpDia.SetSize((200, 200))
        HelpDia.ShowModal()
        HelpDia.Destroy()
        
    def OnQuit(self, e):
        if ser.isOpen() == True:
            ser.close()
        self.Close()
 
class Configure(wx.Dialog):
    def __init__(self, parent = None,
                 title = "Configure"):
        wx.Dialog.__init__(self, parent, title = title)   
    
    def Ui_Uart(self):
        global ch_com
        global ch_bd
        Port_Cho   = ['com1', 'com2','com3','com4','com5','com6','com7']
        BaudRt_Cho = ['9600', '19200', '38400', '57600', '115200']
        Data_Cho   = ['8 bit', '7 bit']
        Parity_Cho = ['None', 'Odd', 'Even', 'Space']
        Stop_Cho   = ['1 bit', '1.5 bit', '2 bit']
        Flow_Cho   = ['None', 'Xon/Xoff', 'Hardware']
        UartItems  = ["Port:", "BaudRate:", "Data:", "Parity:",
                      "Stop:", "Flow Control:"]
        pan = wx.Panel(self)
        sizer = wx.GridBagSizer(8, 8)
        
        text1 = wx.StaticText(pan, label=UartItems[0])
        sizer.Add(text1, pos=(0, 0), flag=wx.LEFT | wx.TOP, border=15)
        
        ch_com = wx.ComboBox(pan, choices = Port_Cho)
        ch_com.SetValue(Port_Cho[0])
        sizer.Add(ch_com, pos = (0, 1), span=(1, 1),
                  flag=wx.TOP|wx.EXPAND, border = 10)
            
        text2 = wx.StaticText(pan, label=UartItems[1])
        sizer.Add(text2, pos=(1, 0), flag=wx.LEFT | wx.TOP, border=15)       
        ch_bd = wx.ComboBox(pan, choices = BaudRt_Cho)
        sizer.Add(ch_bd, pos = (1, 1), span=(1, 1),
                  flag=wx.TOP|wx.EXPAND, border = 5)
        ch_bd.SetValue(BaudRt_Cho[0])
          
        text3 = wx.StaticText(pan, label=UartItems[2])
        sizer.Add(text3, pos=(2, 0), flag=wx.LEFT | wx.TOP, border=15)       
        self.ch3 = wx.ComboBox(pan, choices = Data_Cho)
        sizer.Add(self.ch3, pos = (2, 1), span=(1, 1),
                  flag=wx.TOP|wx.EXPAND, border = 5)
        self.ch3.SetValue(Data_Cho[0])
        
        text4 = wx.StaticText(pan, label=UartItems[3])
        sizer.Add(text4, pos=(3, 0), flag=wx.LEFT | wx.TOP, border=15)       
        self.ch4 = wx.ComboBox(pan, choices = Parity_Cho)
        sizer.Add(self.ch4, pos = (3, 1), span=(1, 1),
                  flag=wx.TOP|wx.EXPAND, border = 5)
        self.ch4.SetValue(Parity_Cho[0])
        
        text5 = wx.StaticText(pan, label=UartItems[4])
        sizer.Add(text5, pos=(4, 0), flag=wx.LEFT | wx.TOP, border=15)       
        self.ch5 = wx.ComboBox(pan, choices = Stop_Cho)
        sizer.Add(self.ch5, pos = (4, 1), span=(1, 1),
                  flag=wx.TOP|wx.EXPAND, border = 5)
        self.ch5.SetValue(Stop_Cho[0])
        
        text6 = wx.StaticText(pan, label=UartItems[5])
        sizer.Add(text6, pos=(5, 0), flag=wx.LEFT | wx.TOP, border=15)       
        self.ch6 = wx.ComboBox(pan, choices = Flow_Cho)
        sizer.Add(self.ch6, pos = (5, 1), span=(1, 1),
                  flag=wx.TOP|wx.EXPAND, border = 5)
        self.ch6.SetValue(Flow_Cho[0])
        
        OkBtn = wx.Button(pan, label='Ok')
        CloBtn = wx.Button(pan, label='Close')
        sizer.Add(OkBtn, pos = (7, 0),flag=wx.LEFT, border = 45)
        sizer.Add(CloBtn, pos = (7, 1),flag=wx.RIGHT, border = 35)
        self.Bind(wx.EVT_BUTTON, self.UartOk, OkBtn)
        self.Bind(wx.EVT_BUTTON, self.OnQuit, CloBtn)
        
        sizer.AddGrowableCol(2)
        pan.SetSizer(sizer)

    def UartOk(self, a):
        con = Frame()
        con.start_con()
        self.Destroy()

    def OnQuit(self, e):
        self.Destroy()
    
    def Ui_About(self):
        pan = wx.Panel(self)
        text = wx.StaticText(pan, label = "about!!!")

    def Ui_Help(self):
        pan = wx.Panel(self)
        text = wx.StaticText(pan, label = "help!!!")
        
class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent = None, title = "tool")
        self.frame.Show()
        return True
    
if __name__ == "__main__":
    app = App()
    app.MainLoop()
