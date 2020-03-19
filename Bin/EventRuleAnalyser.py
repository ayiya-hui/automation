import wx
import sys

class eventRuleAnalyser(wx.Frame):
    def __init__(self, parent, version):
        wx.Frame.__init__(self, parent, -1, 'Accelops EventRuleAnalyser version '+version, size=(690, 710))
        self.runtimeStats={}
        fileMenu=wx.Menu()
        fileMenu.Append(101, '&About', 'About Accelops EventRuleAnalyser')
        wx.EVT_MENU(self, 101, self.onAbout)
        fileMenu.Append(102, '&Exit', 'Exit Accelops EventRuleAnalyser')
        wx.EVT_MENU(self, 102, self.onExit)
        menuBar=wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        self.SetMenuBar(menuBar)
        panel=wx.Panel(self)
        self.testTargetTextbox=wx.TextCtrl(panel, -1, '192.168.20.116')
        self.deviceIpTextbox=wx.TextCtrl(panel, -1, '20.20.20.20')
        self.deviceTypeCheckbox=wx.CheckBox(panel, -1, 'Deivce Group')
        self.label=wx.StaticText(panel, -1, 'Please select options to run analysis:')
        self.deviceApproveCheckbox=wx.CheckBox(panel, -1, 'Device Approved')
        self.deviceApproveCheckbox.SetValue(True)
        self.eventTypeCheckbox=wx.CheckBox(panel, -1, 'Message Event Type')
        self.eventTypeCheckbox.SetValue(True)
        self.eventParamCheckbox=wx.CheckBox(panel, -1, 'Event Critiria')
        self.eventParamCheckbox.SetValue(True)
        self.button=wx.Button(panel, -1, 'Run Analysis')
        dataSizer=wx.GridSizer(0, 6, 0, 0)
        dataSizer.Add(wx.StaticText(panel, -1, 'Target System'), 0, wx.TOP|wx.LEFT, 8)
        dataSizer.Add(self.testTargetTextbox, 0, wx.TOP|wx.LEFT, 8)
        dataSizer.Add(wx.StaticText(panel, -1, 'Device IP'), 0, wx.TOP|wx.LEFT, 8)
        dataSizer.Add(self.deviceIpTextbox, 0, wx.TOP|wx.LEFT, 8)
        optionSizer=wx.GridBagSizer(5, 5)
        optionSizer.Add(self.label, (0, 1), (1, 3), wx.ALIGN_CENTRE)
        optionSizer.Add(self.deviceTypeCheckbox, (1, 1))
        optionSizer.Add(self.deviceApproveCheckbox, (2, 1))
        optionSizer.Add(self.eventTypeCheckbox, (3, 1))
        optionSizer.Add(self.eventParamCheckbox, (4, 1))
        optionSizer.Add(self.button, (5, 0), (1, 3), wx.ALIGN_CENTER)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(dataSizer, 0, wx.ALL, 3)
        sizer.Add(optionSizer, 0, wx.ALL, 33)
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.buttonClick, self.button)
        self.Show(True)

    def onAbout(self, evt):
        info=wx.AboutDialogInfo()
        info.SetName('Accelops EventRuleAnalyser Info')
        info.SetCopyright('This is Accelops Inc. internal analyser tool created by Sha.')
        wx.AboutBox(info)

    def onExit(self, evt):
        sys.exit(0)

    def buttonClick(self, evt):
        target=self.testTargetTextbox.GetValue()
        device=self.deviceIpTextbox.GetValue()
        optDevType=self.deviceTypeCheckbox.GetValue()
        optDevApprove=self.deviceApproveCheckbox.GetValue()
        optEventType=self.eventTypeCheckbox.GetValue()
        optEventParam=self.eventParamCheckbox.GetValue()
        print 'target is %s' % target
        print 'device is %s' % device
        print 'devType is %s' % optDevType
        print 'devApprove is %s' % optDevApprove
        print 'eventtype is %s' % optEventType
        print 'eventParam is %s' % optEventParam

app=wx.App(False)
eventRuleAnalyser(None, '1')
app.MainLoop()
