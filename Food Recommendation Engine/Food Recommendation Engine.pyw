


try:#Checks if the required classes exist in users computer
    from recommendations import *
    from Tkinter import *
    from ttk import Combobox
    import anydbm, pickle, xlrd
except:
    print 'Encountered Problem With Libraries'
    raw_input( '\n\tPress Enter to Exit' )
    exit()

class Window:#Main class for application

    #Settings are initialized
    num_of_rec = 10
    rec_method = 'user'
    sim_metric = 'sim_distance'
    metric_dict = { 'sim_distance': sim_distance, 'sim_jaccard': sim_jaccard, 'sim_pearson': sim_pearson }
    data_format = 'user'

    
    def __init__(self,master):
        self.master = master
        self.master.configure( background = 'darkred' )
        self.master.title( 'Recommendation Engine' )
        self.master.resizable( width = False, height = False )#Prevents user from changing the size of the window
        self.master.geometry( '+%d+%d' % ( self.master.winfo_screenwidth() / 2 - 500, self.master.winfo_screenheight() / 2 - 300 ) )#Initializes windows starting position
        self.settings = Settings( self.num_of_rec, self.rec_method, self.sim_metric )#Creates a settings object so it can contain optional variables
        
        #Necessary functions are called
        self.open_database()
        self.load_menu()
        self.init_gui()
        self.display_gui()
        self.configure_widgets()
        self.master.mainloop()


    def init_gui( self ):#Initializes GUI
        #Top Frame
        self.frame_head = Frame( self.master, background = 'darkred' )#For headline color red is choosen since red has an effect on hunger
        Label( self.frame_head, font = ( 'Helvetica', 26 ), width = 33, fg = 'white', bg = 'darkred', text = 'Cafe Crown Recommendation Engine \nSEHIR Special Edition').grid(row = 0, column = 0, columnspan = 3, stick = E + W)
        Label( self.frame_head, font = ( 'Helvetica', 14 ), fg = 'white', bg = 'darkred', text = 'Please rate entries that you have had at CC,\n and we will recommend you what you may like to have').grid(row = 1, column = 0, columnspan = 3, stick = E + W)

        #Entry mid Frame
        self.frame_entry = Frame( self.master)
        self.label_combo_menu = Label( self.frame_entry, font = ( 'Helvetica', 10), text = 'Choose a meal' )
        self.combo_menu = Combobox( self.frame_entry, state = 'readonly', width = 25)
        self.label_rating = Label( self.frame_entry, font = ( 'Helvetica', 10), text = '\nEnter your rating' )
        self.scale_rating = Scale( self.frame_entry, from_ = 1, to = 10, orient = HORIZONTAL )
        self.button_add = Button( self.frame_entry, fg = 'darkblue', text = 'Add >>', width = 10 )
        self.button_remove = Button( self.frame_entry, fg = 'darkred', text = '<< Remove', width = 10 )
        self.scrollbar_listbox_user = Scrollbar(self.frame_entry)
        self.listbox_user = Listbox( self.frame_entry, height = 8, width = 45, yscrollcommand = self.scrollbar_listbox_user.set)
        self.scrollbar_listbox_user.config( command = self.listbox_user.yview )
        self.button_recommend = Button( self.frame_entry, text = 'Get Recommendations' )
        self.button_settings = Button( self.frame_entry, text = 'Settings', width = 10 )
        
        #Result bottom frame
        self.frame_result = Frame( self.master, pady = 5, padx = 3 )
        self.label_rec_meal = Label( self.frame_result, font = ( 'Helvetica', 10), text = 'Recommendations' )
        self.label_rec_left = Label( self.frame_result, font = ( 'Helvetica', 10), text = 'Users similar to you' )
        self.label_rec_right = Label( self.frame_result, font = ( 'Helvetica', 10), text = 'User ratings' )
        self.scrollbar_meal = Scrollbar( self.frame_result)
        self.scrollbar_rating = Scrollbar( self.frame_result)
        self.scrollbar_people = Scrollbar( self.frame_result)
        self.listbox_meal = Listbox( self.frame_result, height = 8, width = 35, yscrollcommand = self.scrollbar_meal.set )
        self.listbox_left = Listbox( self.frame_result, height = 8, width = 25, yscrollcommand = self.scrollbar_rating.set )
        self.listbox_right = Listbox( self.frame_result, height = 8, width = 35, yscrollcommand = self.scrollbar_people.set )
        self.scrollbar_meal.config( command = self.listbox_meal.yview)
        self.scrollbar_rating.config( command = self.listbox_left.yview)
        self.scrollbar_people.config( command = self.listbox_right.yview)
        

    def display_gui( self ):#Places widgets in their preffered positions
        #headline frame
        self.frame_head.grid(row = 0, column = 0, columnspan = 5, stick = E + W)
        
        #entry mid frame
        self.frame_entry.grid(row = 1, column = 0, columnspan = 4, stick = E + W, pady = 10)
        self.label_combo_menu.grid(row = 0, column = 0, stick = W)
        self.combo_menu.grid(row = 0, column = 1)
        self.label_rating.grid(row = 1, column = 0, stick = N + W)
        self.scale_rating.grid(row = 1, column = 1, stick = N)
        self.button_add.grid(row = 0, column = 2, stick = S, padx = 10)
        self.button_remove.grid(row = 1, column = 2, padx = 10)
        self.listbox_user.grid(row = 0, column = 3, rowspan = 3, stick = E)
        self.scrollbar_listbox_user.grid(row = 0, column = 4, rowspan = 3, stick = N + S)
        self.button_recommend.grid(row = 2, column = 1, pady = 5)
        self.button_settings.grid(row = 2, column = 2, pady = 5)
        
        #bottom result frame
        self.frame_result.grid(row = 3, column = 0, columnspan = 4, stick = E + W)
        self.label_rec_meal.grid(row = 0, column = 0)
        self.label_rec_left.grid(row = 0, column = 2) 
        self.label_rec_right.grid(row = 0, column = 4)
        self.listbox_meal.grid(row = 1, column = 0, pady = 5)
        self.listbox_left.grid(row = 1, column = 2, pady = 5)
        self.listbox_right.grid(row = 1, column = 4, pady = 5)
        self.scrollbar_meal.grid(row = 1, column = 1, rowspan = 3, stick = N + S + E, padx = 5)
        self.scrollbar_rating.grid(row = 1, column = 3, rowspan = 3, stick = N + S + E, padx = 5)
        self.scrollbar_people.grid(row = 1, column = 5, rowspan = 3, stick = N + S + E, padx = 5)


    def configure_widgets( self ):
        #Binding Widgets
        self.button_settings.bind( '<Button-1>', self.get_settings )
        self.button_add.bind( '<Button-1>', self.add_to_list )
        self.button_remove.bind( '<Button-1>', self.remove_from_list )
        self.button_recommend.bind( '<Button-1>', self.recommend )
        self.listbox_left.bind( '<ButtonRelease-1>', self.displayPickedItem )

        #Inserting meals into combobox
        meals = self.meal_menu.keys()
        meals.sort()
        self.combo_menu[ 'values' ] = meals
        self.combo_menu.current( 0 )


    def add_to_list( self, event ):#Add button
        try:
            item = self.combo_menu.get()
            for index in range( self.listbox_user.size() ):#If the item is in the list, it will be deleted
                if item in self.listbox_user.get( index ):
                    self.listbox_user.delete( index )
                    break
            #Then the item will be inserted with the new rating
            self.listbox_user.insert( END, item + ( ' --> ' + str( self.scale_rating.get() ) ).encode( 'utf-8' ) )
        except:
            print 'add_to_list error catched'
        

    def remove_from_list(self, event):#Remove Button
        try:
            self.listbox_user.delete( self.listbox_user.curselection() )
        except:
            pass


    def recommend(self, event):#Get Recommendations Button
        user_prefs = self.getUserPrefs()
        if type(user_prefs) == type(float): return      #Whether the user has entered ratings
        self.database_user[ 'user' ] = user_prefs
        self.database_item = transformPrefs( self.database_user )
        
        self.listbox_meal.delete( 0, END )
        if self.rec_method == 'user':
            recommended = getRecommendations( self.database_user, 'user', self.metric_dict[ self.sim_metric ] )
        else:
            recommended = getRecommendations( self.database_user, 'user', self.metric_dict[ self.sim_metric ] )
        self.similarmeals = [ meals for score, meals in recommended[ :10 ] ]
        self.rec_size = len( recommended )
        self.listbox_left.delete( 0, END )
        if len(recommended) != 0:
            for score, food in recommended:
                self.listbox_meal.insert( END, str( food + ' --> ' + str( score )[ 0:4 ] ))
        else:
            error_box = ErrorBox( 'Warning', 'Please rate more items' )
            return
            
        #Starts working on other listboxes
        if self.rec_method == 'user':
            self.recommendUser()
            self.data_format = 'user'   #data_format can only change when recommendation is done again
        else:                           #data_format will be used to navigate in the listbox_left to listbox_right
            self.recommendItem()
            self.data_format = 'item'

        self.saveToDatabase()
        

    def recommendUser( self ):#This will update the middlebox for user method
        try:
            people = self.topMatches_modified( self.database_user, 'user', self.num_of_rec, self.metric_dict[ self.sim_metric ] )
            self.listbox_left.delete( 0, END )
            #Label changes
            self.label_rec_left.configure( text = 'Users similar to you' )
            self.label_rec_right.configure( text = 'User ratings' )
            if self.rec_size != 0:
                for score, person in people:
                    self.listbox_left.insert( END, str( score )[ 0:4 ] + ' --> ' + person )
        except:
            print 'recommendUser error catched'


    def recommendItem( self ):#This will update the middlebox for item method
        try:
            #Label changes
            self.label_rec_left.configure( text = 'Selected items' )
            self.label_rec_right.configure( text = 'Item ratings' )            
            self.listbox_left.delete( 0, END )
            if self.rec_size != 0:
                for index in range( self.listbox_user.size() ):
                    self.listbox_left.insert( END, self.listbox_user.get( index ) )
        except:
            print 'recommendItem error catched'


    def displayPickedItem( self, event ):#When listbox_left is clicked this will insert values into listbox_right
        try:
            if self.data_format == 'user':
                #listbox changes
                self.listbox_right.delete( 0, END )
                rating, person = self.listbox_left.get( self.listbox_left.curselection()[0] ).split( ' --> ' )
                self.label_rec_right.configure( text = person )
                user_list = list( ( str( self.database_user[ person ][ key ] ), key ) for key in self.database_user[ person ] )
                user_list.sort( reverse = True )
                for score, food in user_list:
                    self.listbox_right.insert( END, str( self.database_user[ person ][ food ] ) + ' --> ' + food )                
            else:#item based
                #listbox changes
                self.listbox_right.delete( 0, END )
                for items in self.similarmeals:
                    self.listbox_right.insert( END, items )
                
        except IndexError:
            print 'displayPickedItem clicked on empty space'       
        except:
            print 'displayPickedItem error catched'
        

    def calculateSimilarItems_modified( self, prefs, n ):
        result = {}
        itemPrefs = transformPrefs(prefs)
        for item in itemPrefs:
            scores = self.topMatches_modified( itemPrefs, item, n, sim_distance )
            result[item] = scores
        return result


    def topMatches_modified( self, prefs, person, n, similarity ):
        scores = []
        for other in prefs:
            if other != person:
                scores.append( (similarity( prefs, person, other ), other ) )
        try:
            scores.sort( reverse = True )
        except:
            pass
        return scores[0:n]


    def getUserPrefs( self ):#Enter users preferences into main dictionary depending on the method
        user_prefs = {}
        if self.listbox_user.size() == 0:
            error_box = ErrorBox( 'Warning', 'Please rate meals from menu first' )
            self.master.lift()
            return 1.0
        elif self.rec_method == 'user':#User based
            for pair in self.listbox_user.get( 0, END ):
                food, score = pair.split( ' --> ' )
                user_prefs[ food ] = int( score )
        else:#Item based
            for pair in self.listbox_user.get( 0, END ):
                food, score = pair.split( ' --> ' )
                user_prefs[ food ] = { 'user': int( score ) }
        return user_prefs



    def open_database(self):#Saves the previously saved ratings in RAM for an easier and faster access
        cc_ratings = anydbm.open('cc_ratings.db','c')
        self.database_user = {}#User based dictionary
        for element in cc_ratings.keys():
            self.database_user[element] = pickle.loads( cc_ratings[element] )
        self.database_item = transformPrefs( self.database_user )#Item based dictionary
            

    def get_settings(self, event):#Settings Button, after the window is closed retrieves choosen settings from the object
        try:#While the settings window is open, user will not be able to use parent window
            self.settings.popup()
            self.master.lift()
            self.num_of_rec = self.settings.num_of_rec
            self.rec_method = self.settings.rec_method
            self.sim_metric = self.settings.sim_metric
        except:
            print 'get_settings error catched'


    def load_menu(self):#Saves menu from hard drive to RAM for an easier and faster access
        try:
            menu_file = xlrd.open_workbook( 'menu.xlsx' )
            page = menu_file.sheet_by_index( 0 )
            self.meal_menu = {}
            for row in range( 1, page.nrows ):
                self.meal_menu[ page.cell( row, 0 ).value ] = str( page.cell( row, 1 ).value )
        except:
            print 'Could not find "menu.xlsx", please relocate the file and restart the application'

    def saveToDatabase( self ):
        database = anydbm.open( 'cc_rating.db', 'c' )
        for key in self.database_user:
            database[ key ] = pickle.dumps( self.database_user[ key ] )
        database.close()
    
class Settings:

    def __init__(self, number, method, sim):
        self.num_of_rec = number
        self.rec_method = method
        self.sim_metric = sim
        self.var = StringVar()
        self.var2 = StringVar()
        self.var.set('method')
        self.var2.set('metric')


    def popup(self): #The window will not appear unless this function is called from outside
        self.master = Tk()
        self.master.title('Settings')
        self.master.resizable(width = False, height = False)
        self.master.geometry('+%d+%d' % (self.master.winfo_screenwidth()/2 - 200,self.master.winfo_screenheight()/2 - 100))
        self.master.attributes( '-toolwindow', True )
        self.start_gui()
        self.display_gui()
        self.bind_widgets()
        self.master.mainloop()
        

    def start_gui(self):
        self.label_num = Label(self.master,text = 'Number of Recommendations\n(Use Scroll Wheel)')
        self.entry_num = Entry(self.master,width = 5)
        self.entry_num.insert('end', str(self.num_of_rec))
        self.label_method = Label(self.master,text = 'Recommendation Method')
        self.radio_method = Radiobutton(self.master,text = 'User-Based', value = 'user', variable = self.var)
        self.radio2_method = Radiobutton(self.master,text = 'Item-Based', value = 'item', variable = self.var)
        self.label_sim = Label(self.master, text = 'Similarity Metric')
        self.radio_sim = Radiobutton(self.master, text = 'Euclidean Score', value = "sim_distance", variable = self.var2)
        self.radio2_sim = Radiobutton(self.master, text = 'Pearson Score', value = "sim_pearson", variable = self.var2)
        self.radio3_sim = Radiobutton(self.master, text = 'Jaccard Score', value = "sim_jaccard", variable = self.var2)
        self.accept = Button(self.master, text = 'Accept')
        self.cancel = Button(self.master, text = 'Cancel', command = self.master.destroy)


    def display_gui(self):
        self.label_num.grid(row = 0, column = 0, pady = 10, padx = 10, stick = W)
        self.entry_num.grid(row = 0, column = 1, pady = 10, padx = 10, stick = W)
        self.label_method.grid(row = 1, column = 0, pady = 2, padx = 5, stick = W)
        self.radio_method.grid(row = 2, column = 0, padx = 5, stick = W)
        self.radio2_method.grid(row = 3, column = 0, padx = 5, stick = W)
        self.label_sim.grid(row = 4, column = 0, pady = 2, padx = 5, stick = W)
        self.radio_sim.grid(row = 5, column = 0, padx = 5, stick = W)
        self.radio2_sim.grid(row = 6, column = 0, padx = 5, stick = W)
        self.radio3_sim.grid(row = 7, column = 0, padx = 5, stick = W)
        self.accept.grid(row = 8, column = 0, pady = 5, padx = 30, stick = W, columnspan = 2)
        self.cancel.grid(row = 8, column = 0, pady = 5, padx = 30, stick = E, columnspan = 2)


    def bind_widgets(self):
        #Buttons are binded
        self.master.bind( '<MouseWheel>', self.scroll_entry )
        self.accept.bind( '<Button-1>', self.saver )
        self.radio_method.bind( '<Button-1>', self.clicked )
        self.radio2_method.bind( '<Button-1>', self.clicked )
        self.radio_sim.bind( '<Button-1>', self.clicked )
        self.radio2_sim.bind( '<Button-1>', self.clicked )
        self.radio3_sim.bind( '<Button-1>', self.clicked )

        #Overrides the X button for further modifications if needed
        self.master.protocol( 'WM_DELETE_WINDOW', self.master.destroy )
        

    def scroll_entry(self, event):
        try:
            number = int( self.entry_num.get() )
            self.entry_num.delete( 0, END )
            self.entry_num.insert( END, str( abs(number + int( event.delta / 120 ) ) ) )
            del number
        except:
            self.entry_num.delete( 0, END )
            self.entry_num.insert( END, str( 10 ) )
            

    def clicked(self, event):
        widget = event.widget['value']
        if widget in ['user', 'item']:
            self.rec_method = widget
        else:
            self.sim_metric = widget
        

    def saver(self, event):
        try:
            self.num_of_rec = int( self.entry_num.get() )
        except:
            self.error_box = ErrorBox('Warning', 'You can only enter numbers')
            self.master.lift()
        try:
            self.master.quit()
            self.master.destroy()
        except:
            print 'Settings Error Catched'


    

class ErrorBox:

    def __init__(self, title, message):
        self.error_box = Tk()
        self.error_box.grab_set()
        self.error_box.title( str( title ) )
        self.error_box.resizable(width = False, height = False)
        self.error_box.geometry('+%d+%d' % (self.error_box.winfo_screenwidth() / 2 - 200, self.error_box.winfo_screenheight() / 2 - 100))
        self.error_box.attributes( '-toolwindow', True )
        
        #Starts calling necessary functions
        self.start_gui(message)
        self.display_gui()
        self.error_box.attributes("-topmost", True)
        self.error_box.lift()
        self.error_box.focus_force()
        self.error_box.mainloop()
        

    def start_gui(self, message):
        self.error_box_message = Label(self.error_box, text = '\n' + message + '\n')
        self.error_box_button = Button(self.error_box, text = 'Ok', width = 10)
        
        #Over rides the X button for further modifications if needed
        self.error_box.protocol('WM_DELETE_WINDOW', self.error_box.destroy)


    def display_gui(self):
        self.error_box_message.grid(column = 0, row = 0, pady = 5)
        self.error_box_button.grid(column = 0, row = 1, pady = 5)
        
        #Button Binding
        self.error_box.bind('<Return>', self.destroyer)
        self.error_box_button.bind('<Button-1>', self.destroyer)


    def destroyer(self, event):#Since destroy function cant take event, a function is made
        self.error_box.destroy()
        

    def __del__(self):#The object might have been deleted
        try:
            self.error_box.destroy()
            self.error_box.grab_release()
        except:
            pass
        
if __name__ == '__main__':#Imitates a main function
    root = Tk()
    gui = Window(root)
