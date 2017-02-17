from Tkinter import *
from ttk import Combobox
from bs4 import BeautifulSoup as bs4
from PIL import Image, ImageTk
from urllib2 import *
import io


class Window:

    bg = 'sienna' #default theme background
    fg = 'burlywood' #default theme foreground

    def __init__( self, master ):
        #Default window attributes are defined
        self.master = master
        self.master.configure( background = self.bg )
        self.master.title( 'Sehir Research Project Analyzer' )
        self.master.resizable( width = False, height = False )#Prevents user from changing the size of the window
        self.master.geometry( '+%d+%d' % ( self.master.winfo_screenwidth() / 2 - 650, self.master.winfo_screenheight() / 2 - 400 ) )#Initializes windows starting position

        #GUI creater functions are called
        self.initGui()
        self.displayGui()
        self.configureWidgets()
        self.temp()
        self.master.mainloop()


    def initGui( self ):# , bg = self.bg, fg = self.fg, activeforeground = self.fg, activebackground = self.bg
        #Headline Frame
        self.frame_head = Frame( self.master, bg = self.bg )
        self.label_head = Label( self.frame_head, text = 'SEHIR Research Projects Analyzer - Computer Science Edition', font = ('Helvetica', 20), bg = self.bg, fg = self.fg )
        
        #Top Frame
        self.frame_top = Frame( self.master, bg = self.bg )
        self.label_url = Label( self.frame_top, text = 'Please provide a URL:', bg = self.bg, fg = self.fg )
        self.entry_url = Entry( self.frame_top, bg = 'PeachPuff', fg = 'black', width = 65 )
        self.button_fetch = Button( self.frame_top, text = 'Fetch Research Projects', bg = self.bg, fg = self.fg, activeforeground = self.fg, activebackground = self.bg )
        self.button_x = Button( self.frame_top, text = 'X', width = 2, bg = self.bg, fg = self.fg, activeforeground = self.fg, activebackground = self.bg )
        
            
        #Middle Frame
        self.frame_mid = Frame( self.master, bg = self.bg )
        self.label_filter = Label( self.frame_top, text = 'Filter Research Projects:', bg = self.bg, fg = self.fg  )
        self.label_project = Label( self.frame_top, text = 'Pick a Project', bg = self.bg, fg = self.fg )
        self.label_year = Label( self.frame_top, text = 'Year:', bg = self.bg, fg = self.fg )
        self.label_inv = Label( self.frame_top, text = 'Principal Investigator:', bg = self.bg, fg = self.fg )
        self.label_ins = Label( self.frame_top, text = 'Funding Institution:', bg = self.bg, fg = self.fg )
        self.combo_year = Combobox( self.frame_top, state = 'readonly', width = 45 )
        self.combo_inv = Combobox( self.frame_top, state = 'readonly', width = 45 )
        self.combo_ins = Combobox( self.frame_top, state = 'readonly', width = 45 )
        self.scroll_listbox_project = Scrollbar( self.frame_mid )
        self.listbox_project = Listbox( self.frame_mid, width = 70, height = 22, yscrollcommand = self.scroll_listbox_project.set, bg = 'PeachPuff' )
        self.button_title = Button( self.frame_mid, text = 'Display Project Titles', bg = self.bg, fg = self.fg, activeforeground = self.fg, activebackground = self.bg )
        self.button_desc = Button( self.frame_mid, text = 'Show Description', bg = self.bg, fg = self.fg, activeforeground = self.fg, activebackground = self.bg )

        #Right Frame
        self.frame_right = Frame( self.master, bg = self.bg )
        self.scroll_text = Scrollbar( self.frame_right )
        self.text_desc = Text( self.frame_right, bg = 'PeachPuff', yscrollcommand = self.scroll_text.set, state = 'disabled', width = 98, height = 18 )
        self.canvas = Canvas( self.frame_right, bg = self.bg, width = 800, height = 300, scrollregion=( 0, 0, 800, 300 ) ) #canvas is exactly the size of the most of the images from the website
                                                                                                                        #adjusting the canvas size for each image will corrupt the geometry
        


    def displayGui( self ):# self.widget.grid( column = , row =  )  #Used for copying and pasting while coding
        #Headline Frame
        self.frame_head.grid( column = 0, row = 0, columnspan = 2 ) #Places the widgets accordingly
        self.label_head.grid( column = 0, row = 0 )
        
        #Top Frame
        self.frame_top.grid( column = 0, row = 1, padx = 10 )
        self.label_url.grid( column = 0, row = 0, stick = W )
        self.entry_url.grid( column = 0, row = 1, columnspan = 2, stick = W, pady = 5 )
        self.button_fetch.grid( column = 0, row = 2, stick = W )
        self.button_x.grid( column = 2, row = 1, padx = 5, stick = W )

        #Middle Frame
        self.frame_mid.grid( column = 0, row = 2 )
        self.label_filter.grid( column = 0, row = 3, columnspan = 2, pady = 10 )
        self.label_year.grid( column = 0, row = 4, stick = W )
        self.label_inv.grid( column = 0, row = 5, stick = W )
        self.label_ins.grid( column = 0, row = 6, stick = W )
        self.combo_year.grid( column = 1, row = 4, columnspan = 2 )
        self.combo_inv.grid( column = 1, row = 5, columnspan = 2 )
        self.combo_ins.grid( column = 1, row = 6, columnspan = 2 )
        self.button_title.grid( column = 0, row = 4, pady = 5 )
        self.listbox_project.grid( column = 0, row = 5, columnspan = 2 )
        self.scroll_listbox_project.grid( column = 2, row = 5, stick = W + N + S )
        self.button_desc.grid( column = 1, row = 4, pady = 5 )

        #Right Frame
        self.frame_right.grid( column = 1, row = 1, rowspan = 2 )
        self.text_desc.grid( column = 0, row = 0 )
        self.scroll_text.grid( column = 1, row = 0, stick = N + S + W )
        self.canvas.grid( column = 0, row = 4, columnspan = 2 )
        

    def configureWidgets( self ):#Configures the widgets with necessar
        self.scroll_listbox_project.config( command = self.listbox_project.yview )
        self.scroll_text.config( command = self.text_desc.yview )
        
        self.button_fetch.bind( '<ButtonRelease-1>', self.urlFetcher )
        self.button_x.bind( '<ButtonRelease-1>', self.clearEntry )
        self.button_title.bind( '<ButtonRelease-1>', self.displayTitles )
        self.button_desc.bind( '<ButtonRelease-1>', self.displayDescription )
        
        self.combo_year[ 'value' ] = [ 'All Years' ]#sets default values of the comboboxes "All" tags
        self.combo_inv[ 'value' ] = [ 'All Investigators' ]
        self.combo_ins[ 'value' ] = [ 'All Institutions' ]
        self.combo_year.current(0)
        self.combo_ins.current(0)
        self.combo_inv.current(0)

    def clearEntry( self, event ): self.entry_url.delete( 0, 'end' ) #The function of the X button next to the entry

    def urlFetcher( self, event ): #Reads the entire page of the given url
        try:
            self.data = [] #list to be filled with strings, tuples and more strings inside the tuples
            site = urlopen( self.entry_url.get() )
            contents = site.read()
            soup = bs4( contents, 'html.parser' )#creates a soup object so that the page can be read
            
            for project in soup.find_all( 'li',{'class':'list-group-item'} ): #starts splitting the page into projects
                name = project.find( 'h4',{'class':'bold'} ).get_text().strip() #project name
                years, inst, inv, image, desc = project.find_all( 'p' ) #filters and displayable values
                #everything except the pictures are loaded into the ram, since pictures are much bigger in size
                
                years = tuple( year for year in range( int(years.text.split()[2]),int(years.text.split()[-1]) + 1 ) ) #gets years via range( beginning year, ending year + 1 )
                inst = tuple( inst.get_text().split(':')[1].strip().split(' - ') ) #institutes just like other multiple value containing variables are placed into tuples
                inv = inv.find( 'a' ).get_text().strip() #people who had worked on the project
                image = self.getPath( self.entry_url.get() ) + str( project.img[ 'src' ] ) #image path only contains after the domain name so they are merged
                desc = desc.get_text().strip()
                
                self.data.append( [ years, inst, inv, image, desc, name ] ) #data is store as following
                #self.data = { [ ( range of years ), ( institutions ), investigator, image url, description, project name ], [ project 2 ], [ project 3 ], [...] }

            self.addFilters()
        except:
            print 'urlFetcher error catched'
        


    def addFilters( self ):
        try:
            self.combo_year[ 'value' ] = [ 'All Years' ] #resets comboboxes, this can be a function to refresh with ease
            self.combo_inv[ 'value' ] = [ 'All Investigators' ]
            self.combo_ins[ 'value' ] = [ 'All Institutions' ]
            self.combo_year.current(0)
            self.combo_ins.current(0)
            self.combo_inv.current(0)
            
            all_years = []#creating lists to fill later
            all_inst = []
            all_inv = []
            
            for index in xrange( len( self.data ) ):#every value exists only once
                for year in self.data[index][0]:
                    if year not in all_years:
                        all_years.append( year )

                for inst in self.data[index][1]:
                    if inst not in all_inst:
                        all_inst.append( inst )

                if self.data[index][2] not in all_inv: #no use of for loop since no more than 1 value ever exists
                    all_inv.append( self.data[index][2] )
                
            all_years.sort()#values are sorted for a an easier look up
            all_inst.sort()
            all_inv.sort()
            self.combo_year[ 'value' ] = self.combo_year[ 'value' ] + tuple( all_years ) #unique filters are added
            self.combo_ins[ 'value' ] = self.combo_ins[ 'value' ] + tuple( all_inst )
            self.combo_inv[ 'value' ] = self.combo_inv[ 'value' ] + tuple( all_inv )

            del all_years #data stored is deleted before waiting for pythons garbage collection
            del all_inst
            del all_inv
        except:
            print 'addFilters error catched'

    def displayTitles( self, event ): #displays project titles into listbox
        try:
            self.listbox_project.delete( 0, 'end' ) #before anything clears listbox
            year = self.combo_year.get()    #gets all user filters
            inst = self.combo_ins.get()
            inv = self.combo_inv.get()
            
            filtered = [ index for index in range( len( self.data ) ) ] #creates a list of indexes from 0 to length of the dataset
            
            if year != 'All Years': #checks if any filtering is applied or not
                for index in filtered:
                    if year not in self.data[index][0]:
                        filtered.remove( index )    #removes the index of the project from the list if the filter does not match

            if inst != 'All Institutions':
                for index in filtered:
                    if inst not in self.data[index][1]:
                        filtered.remove( index )

            if inv != 'All Investigators':
                for index in filtered:
                    if inv not in self.data[index][2]:
                        filtered.remove( index )

            for index in filtered:
                self.listbox_project.insert( 'end', self.data[index][-1] ) #displays whatever is remaining from the filtering

                
        except:
            print 'displayTitles error catched'

    

    def displayDescription( self, event ): #displays the selected description from the listbox
        try:
            selected = self.listbox_project.get( self.listbox_project.curselection() )
            for index in xrange( len( self.data ) ):
                if selected in self.data[index][-1]:
                    descr = self.data[index][4]
                    self.displayImage( index )
                    break
                
            self.text_desc[ 'state' ] = 'normal' #enables the textbox for a short period of time and disables after entering text
            self.text_desc.delete( 1.0, END )
            self.text_desc.insert( 1.0, descr )
            self.text_desc[ 'state' ] = 'disabled'
            
        except:
            print 'displayDescrition error catched'
        
        

    def displayImage( self, index ): #displays image from the url, takes time since the image is never loaded before
        try:                        #canvas is exactly the size of the downloaded image, so no need for adjustments
            self.img = ImageTk.PhotoImage( Image.open( io.BytesIO( urlopen( self.data[index][3] ).read() ) ) ) 
            self.canvas.create_image( 0, 0, image = self.img, anchor = N + W )
        except:
            print 'displayImage error catched'

    def getPath( self, raw_path ): #gets the domain name of the path give for image retrival
        path = raw_path.split('/')
        for index in xrange( len( path ) ):
            if '.tr' in path[index]:
                return '/'.join( path[ : index + 1 ] )
    
    def temp( self ):               #url initializer since the project doesnt work on other sites, for an easier usage
        self.entry_url.insert( 'end', 'http://cs.sehir.edu.tr/en/research/' )
        
if __name__ == '__main__':
    root = Tk()
    master = Window( root )


















