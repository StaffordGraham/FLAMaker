import wx
from CaseDetails import CaseDetails
case_details=CaseDetails()
current_page=0
class Case(wx.Panel):


    
    def __init__(self, parent,app):
        super(Case, self).__init__(parent)
        self.app=app
        
        #Arrays for comboboxes
        judge_options =["District Judge","Dep District Judge","Circuit Judge","Recorder"]
        court_options = ["Brighton", "Hastings", "Horsham", "Worthing", "Guildford", "Reigate", "Kingston"]
        judge_titles=["District Judge","Deputy District Judge", "His Honour Judge", "Her Honour Judge", "Mr Justice","Mrs Justice"]
        self.SetBackgroundColour(wx.Colour(255,255,204))
        Yspacer =50
        case_details.court_name="Horsham"
        
        
        
        
        
        #Set Panel 
        sizer = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title=wx.StaticText(self,label="Case Details")
        title.SetFont(font)
        title.SetForegroundColour(wx.Colour(0,0,255))
        sizer.Add(title, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)  # Centered vertically
        self.SetSizer(sizer)

    
        
        #Set Labels & ComboBoxes/TextEntry 

        #label_width,label_height=label.GetSize()
        y_pos =0
        y_pos +=Yspacer
        combo_label_y_pos =y_pos
        lab_x= 50
        widge_x =lab_x+250
        
        
        combo_label_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        combo_label_color=wx.Colour(0, 0, 255)
        court_combo_label = wx.StaticText(self, label="Court")
        court_combo_label.SetFont(combo_label_font)
        court_combo_label.SetPosition((lab_x,y_pos ))
        court_combo_label.SetForegroundColour(combo_label_color)
        self.court_combo_box=wx.ComboBox(self,choices=court_options,style =wx.CB_READONLY)
        combo_font=wx.Font(12,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.court_combo_box.SetPosition((widge_x, y_pos))
        self.court_combo_box.SetSize(200,25)
        self.court_combo_box.ForegroundColour=(combo_label_color)
        self.court_combo_box.SetFont(combo_font)
        if case_details.court_name in self.court_combo_box.GetItems():
            self.court_combo_box.SetValue(case_details.court_name)
            
        y_pos += Yspacer
        
        combo_label_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        combo_label_color = wx.Colour(0, 0, 255)
        judge_title_label = wx.StaticText(self, label="Title of Judge")
        judge_title_label.SetFont(combo_label_font)
        judge_title_label.SetPosition((lab_x, y_pos))
        judge_title_label.SetForegroundColour(combo_label_color)
        self.judge_title_combo_box = wx.ComboBox(self, choices=judge_titles, style=wx.CB_READONLY)
        combo_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.judge_title_combo_box.SetPosition((widge_x, y_pos))
        self.judge_title_combo_box.SetSize(200, 25)
        self.judge_title_combo_box.SetForegroundColour(combo_label_color)
        self.judge_title_combo_box.SetFont(combo_font)
        if case_details.judge_rank in self.judge_title_combo_box.GetItems():
            self.judge_title_combo_box.SetValue(case_details.judge_rank)
            
        
        y_pos += Yspacer
        combo_label_x_pos = y_pos
        combo_label_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        combo_label_color = wx.Colour(0, 0, 255)
        judge_name_label = wx.StaticText(self, label="Judge Name")
        judge_name_label.SetFont(combo_label_font)
        judge_name_label.SetPosition((lab_x, y_pos))
        judge_name_label.SetForegroundColour(combo_label_color)
        self.judge_name_textentry=wx.TextCtrl(self,pos=(widge_x,y_pos),size=(250,25))
        self.judge_name_textentry.Font=combo_font
        
        y_pos += Yspacer
        combo_label_x_pos = y_pos
        combo_label_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        combo_label_color = wx.Colour(0, 0, 255)
        case_no_label = wx.StaticText(self, label="Case Number")
        case_no_label.SetFont(combo_label_font)
        case_no_label.SetPosition((lab_x, y_pos))
        case_no_label.SetForegroundColour(combo_label_color)
        self.case_no_textentry = wx.TextCtrl(self, pos=(widge_x, y_pos), size=(250, 25))
        self.case_no_textentry.Font = combo_font
        sizer.AddStretchSpacer()
        button_background_colour=wx.Colour((255,255,255))
        button_text_colour=wx.Colour((0,0,255))
        button_Sizer=wx.BoxSizer(wx.HORIZONTAL)
        
        back_button = wx.Button(self, label="Back")
        back_button.SetBackgroundColour(button_background_colour)
        back_button.SetForegroundColour(button_text_colour)

        back_button.Bind(wx.EVT_BUTTON, self.handle_back)
        button_Sizer.Add(back_button, 0, wx.ALL | wx.ALL, 5)
        button_Sizer.AddStretchSpacer()
        next_button = wx.Button(self, label="Next")
        next_button.SetBackgroundColour(button_background_colour)
        next_button.SetForegroundColour(button_text_colour)
        next_button.Bind(wx.EVT_BUTTON, self.handle_next)
        button_Sizer.Add(next_button, 0, wx.ALL | wx.ALL, 5)
        sizer.Add(button_Sizer,0,wx.EXPAND | wx.LEFT|wx.RIGHT|wx.BOTTOM,15)
        
        
    def handle_back(self, event):
            global current_page
            current_page-=1
            case_details.judge_rank=self.judge_title_combo_box.GetValue()
            case_details.judge_name=self.judge_name_textentry.GetValue()
            case_details.court_name = self.court_combo_box.GetValue()
            case_details.case_number=self.case_no_textentry.GetValue()
            


    def handle_next(self, event):
            global current_page
            current_page +=1
            case_details.court_name = self.court_combo_box.GetValue()
            case_details.judge_rank=self.judge_title_combo_box.GetValue()
            case_details.judge_name=self.judge_name_textentry.GetValue()
            case_details.case_number=self.case_no_textentry.GetValue()
            self.app.on_next(event)  # Call the app's method to handle the transition
                
    def on_form_load(self):
        
            self.court_combo_box.SetValue(case_details.court_name) 
            self.judge_title_combo_box.SetValue(case_details.judge_rank) 
            self.judge_name_textentry.SetValue(case_details.judge_name)  
            self.case_no_textentry.SetValue(case_details.case_number)
            
class Hearing(wx.Panel):
    app_options=["Injunction","Occupation Order","Injunction & Directions","Occupation Order & Directions","Directions"]
    hearing_type_options =["Interim","Final"]
    exparte_options=["On Notice","Ex Parte","Short Notice"]
    salut_options=["Mr","Mrs","Miss","Mrs"]
    
    def __init__(self, parent,app):
        super(Hearing,self).__init__(parent)
        self.app=app
        self.SetBackgroundColour(wx.Colour(255,255,204))
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        combo_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        label_font= wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        title=wx.StaticText(self,label="The Hearing")
        title.SetFont(font)
        title.SetForegroundColour(wx.Colour(0,0,255))
        main_sizer.Add(title, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)  # Centered vertically
        
        label_start_position = 50
        input_widget_start_position =100
        left_spacer_width=input_widget_start_position-label_start_position

        
        row_sizer=wx.BoxSizer(wx.HORIZONTAL)
        
        row_sizer.AddSpacer(label_start_position)
        Application_label = wx.StaticText(self, label="The Application")
        Application_label.SetFont(label_font)
        Application_label.SetForegroundColour(wx.Colour(0,0,255))
        self.Application_combo_box = wx.ComboBox(self, choices=self.app_options, style=wx.CB_READONLY)
        self.Application_combo_box.SetForegroundColour(wx.Colour(0, 0, 255))
        self.Application_combo_box.SetFont(combo_font)
        dc = wx.ClientDC(self)
        width =29
        #width = max(dc.GetTextExtent(option)[0] for option in self.app_options)  # Get width of longest option
        self.Application_combo_box.SetSize((width+20, 25))  # Width of 200, height automatic
        row_sizer.AddSpacer(50)
        row_sizer.Add(Application_label,0,wx.ALIGN_CENTRE_VERTICAL | wx.RIGHT,5)
        row_sizer.AddSpacer(left_spacer_width)
        row_sizer.Add(self.Application_combo_box, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        main_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL)
        
        row2_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row2_sizer.AddSpacer(label_start_position)

        
        hearing_type_label=wx.StaticText(self, label="Hearing Listed For : ")
        hearing_type_label.SetFont(label_font)
        hearing_type_label.SetForegroundColour(wx.Colour(0,0,255))
        hearing_type_combo= wx.ComboBox(self, choices=self.hearing_type_options, style=wx.CB_READONLY)
        hearing_type_combo.SetFont(combo_font)
        hearing_type_combo.SetForegroundColour(wx.Colour(0,0,255))
                
        row2_sizer.Add(hearing_type_label,0,wx.ALIGN_CENTER_VERTICAL|wx.RIGHT,5)
        row2_sizer.AddSpacer(left_spacer_width)
        row2_sizer.Add(hearing_type_combo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        
        main_sizer.Add(row2_sizer, 0, wx.EXPAND | wx.ALL)
        
        self.exparte_options = ["Ex Parte","On Notice","Short Notice"]
        
        exparte_sizer = wx.BoxSizer(wx.HORIZONTAL)
        exparte_sizer.AddSpacer(label_start_position)
        
        exparte_label = wx.StaticText(self, label="Ex Parte or On Notice")
        exparte_label.SetFont(label_font)
        exparte_label.SetForegroundColour(wx.Colour(0, 0, 255))
        exparte_combo = wx.ComboBox(self, choices=self.exparte_options, style=wx.CB_READONLY)
        exparte_combo.SetFont(combo_font)
        exparte_combo.SetForegroundColour(wx.Colour(0, 0, 255))
        
        exparte_sizer.Add(exparte_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        exparte_sizer.AddSpacer(left_spacer_width)
        exparte_sizer.Add(exparte_combo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        
        main_sizer.Add(exparte_sizer, 0, wx.EXPAND | wx.ALL)

        self.SetSizer(main_sizer)

        self.Layout()
        
        

        
class FLAOrder(wx.App):
    def __init__(self):
        super().__init__()
         
    def OnInit(self):
        self.current_page = 0
        self.frame = wx.Frame(parent=None, title="FLA Order")
        self.frame.SetSize(800, 600)

        self.main_panel = wx.Panel(self.frame)
        self.stacked_sizer = wx.BoxSizer(wx.VERTICAL)

        # Correctly instantiate the panels
        self.case_panel = Case(self.main_panel, self)
        self.hearing_panel = Hearing(self.main_panel,self)

        # Add both panels to the stacked sizer
        self.stacked_sizer.Add(self.case_panel, 1, wx.EXPAND)
        self.stacked_sizer.Add(self.hearing_panel, 1, wx.EXPAND)

        self.main_panel.SetSizer(self.stacked_sizer)
        self.frame.Show()

        # Show the initial panel
        self.show_page(self.current_page)
        return True
    
    def on_next(self, event):
        self.current_page += 1  
        if self.current_page < len(self.main_panel.GetChildren()):
            self.show_page(self.current_page)  
        else:
            self.current_page = len(self.main_panel.GetChildren()) - 1  

    def on_back(self, event):
        self.current_page -= 1
        if self.current_page >= 0:
            self.show_page(self.current_page)

    def show_page(self, page_number):
        children = self.main_panel.GetChildren()
        print("length of children ", len(children))
        print("page_number ", page_number)
        if 0 <= page_number < len(children):
            for child in children:
                child.Hide()  # Hide all pages
            children[page_number].Show()  # Show the selected page
            self.main_panel.Layout()  # Refresh layout

if __name__ == '__main__':
    app = FLAOrder()
    app.MainLoop()
