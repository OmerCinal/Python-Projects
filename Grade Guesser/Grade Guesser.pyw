from Tkinter import *
from ttk import Combobox
from urllib2 import *
from tkFileDialog import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import tkMessageBox, xlrd, time, tkFont
import docclass as doc

class Window:


    theme = { 1:{'bg' : 'sienna', 'fg' : 'burlywood'},2:{'bg':'darkgreen','fg':'white'},3:{'bg':'darkred','fg':'white'}}
    selected = 2 # different themes can be selected and can be added 
    options_button = { 'bg' : theme[selected]['bg'], 'fg' : theme[selected]['fg'], 'activeforeground' : theme[selected]['fg'], 'activebackground' : theme[selected]['bg'] }
    options_label = { 'bg' : theme[selected]['bg'], 'fg' : theme[selected]['fg'] }
    options_entry = { 'bg' : theme[selected]['fg'] }
    options_frame = { 'bg' : theme[selected]['bg'] }

    page = 1

    def __init__( s ):
        #Default window attributes are defined
        s.master = Tk()
        s.master.configure( bg = s.theme[s.selected]['bg'] )
        s.master.title( 'Guess My Grade' )
        s.master.resizable( width = False, height = False )#Prevents user from changing the size of the window
        s.master.geometry( '+%d+%d' % ( s.master.winfo_screenwidth() / 4, s.master.winfo_screenheight() / 5 ) )#Initializes windows starting position

        #GUI creater functions are called
        s.initGui()
        s.displayGui()
        s.configureWidgets()
        s.temp()
        s.master.mainloop()


    def initGui( s ):# each element of GUI is defined in this method
        s.headline = Label( s.master, s.options_label, text = 'Grade Guesser', font = ('Helvetica',20) )

        #Top Frame
        s.frame_top = Frame( s.master, s.options_frame )
        s.label_browse = Label( s.frame_top, s.options_label, text = 'Please upload your curriculum file with grades:' )
        s.label_file = Label( s.frame_top, s.options_label, relief = RIDGE, width = 75 )
        s.button_browse = Button( s.frame_top, s.options_button, text = 'Browse', width = 10 )

        #URL Frame
        s.frame_url = Frame( s.master, s.options_frame )
        s.label_url = Label( s.frame_url, s.options_label, text = 'Enter urls for course descriptions' )
        s.url_scroll = Scrollbar( s.frame_url )
        s.text_url = Text( s.frame_url, width = 75, height = 5, yscrollcommand = s.url_scroll.set )

        #Key Frame
        s.frame_key = Frame( s.master, s.options_frame )
        s.label_key = Label( s.frame_key, s.options_label, text = 'Key' )
        # Legend labels are defined in a loop
        s.labels = [ Label( s.frame_key, s.options_label, text = letter, relief = RAISED, bg = color, width = 10 ) for (letter,color) in [ ('A','darkgreen'), ('B','green3'), ('C','darkorange'), ('D','red'), ('F','darkred') ] ]
        s.button_predict = Button( s.frame_key, s.options_button, text = 'Predict Grades' )

        #Bottom Frame
        s.frame_bot = Frame( s.master, s.options_frame )
        s.label_grade = Label( s.frame_bot, s.options_label, text = 'Predicted Grades' )
        s.grade_scroll = Scrollbar( s.frame_bot )
        s.text_grade = Text( s.frame_bot, width = 75, height = 15, yscrollcommand = s.grade_scroll.set, state = 'disabled' )

        

    def displayGui( s ):# the widgets that were defined in the initGui method are grided
        s.headline.grid( row = 0, column = 0 )

        #Top Frame
        s.frame_top.grid( row = 1, column = 0, padx = 2, pady = 2 )
        s.label_browse.grid( row = 0, column = 0, padx = 2, pady = 2, stick = W )
        s.label_file.grid( row = 1, column = 0, padx = 2, pady = 2, columnspan = 2)
        s.button_browse.grid( row = 0, column = 1, padx = 2, pady = 2, stick = E )

        #URL Frame
        s.frame_url.grid( row = 2, column = 0, padx = 2, pady = 2 )
        s.label_url.grid( row = 0, column = 0, padx = 2, pady = 2 )
        s.text_url.grid( row = 1, column = 0, padx = 2, pady = 2 )
        s.url_scroll.grid( row = 1, column = 1, stick = S + N + W )
        
        #Key Frame
        s.frame_key.grid( row = 3, column = 0, padx = 2, pady = 2 )
        s.label_key.grid( row = 0, column = 0, padx = 2, pady = 2 )
        for i in xrange( len( s.labels ) ): # legend labels are grided with a loop
            s.labels[i].grid( row = 1, column = i, padx = 5, pady = 2 )
        s.button_predict.grid( row = 1, column = 5, padx = 2, pady = 2 )

        #Bottom Frame
        s.frame_bot.grid( row = 4, column = 0, padx = 2, pady = 2 )
        s.label_grade.grid( row = 0, column = 0, padx = 2, pady = 2 )
        s.text_grade.grid( row = 1, column = 0, padx = 2, pady = 2 )
        s.grade_scroll.grid( row = 1, column = 1, stick = S + N + W )

    

    def configureWidgets( s ):# Button bindings are defined here
        s.button_browse.bind( '<ButtonRelease-1>', s.browseExcel ) #Browse button
        s.button_predict.bind( '<ButtonRelease-1>', s.fetchCourses ) #Predict button

        s.url_scroll.config( command = s.text_url.yview )       # Scroll for url box
        s.grade_scroll.config( command = s.text_grade.yview )   # Scroll for results box

        n = 12 # size of the widget for easier adjustment

        s.font_a = tkFont.Font( size = n )  # configuring fonts for textbox
        s.font_b = tkFont.Font( size = n )  
        s.font_c = tkFont.Font( size = n )
        s.font_d = tkFont.Font( size = n )
        s.font_f = tkFont.Font( size = n )
        s.font_normal = tkFont.Font( size = n )
        
        s.text_grade.tag_configure( 'A', font = s.font_a, foreground = 'darkgreen' ) # fonts are named after grades
        s.text_grade.tag_configure( 'B', font = s.font_b, foreground = 'green3' )
        s.text_grade.tag_configure( 'C', font = s.font_c, foreground = 'darkorange' )
        s.text_grade.tag_configure( 'D', font = s.font_d, foreground = 'red' )
        s.text_grade.tag_configure( 'F', font = s.font_f, foreground = 'darkred' )
        s.text_grade.tag_configure( 'normal', font = s.font_normal, foreground = 'black' )
        

        

    def fetchCourses( s, event ): # fetches description for each course in each link
        # gets links from text box
        links = [ url for url in s.text_url.get( 1.0, 'end' ).split('\n') if len(url) > 3 ]

        try: # tries to open firefox
            driver = webdriver.Firefox()
        except: 
            tkMessageBox.showinfo( title = "Error", message = "There has been an error with Firefox" )
            return

        data_list = [] # creates a list for all retreived data
        # this will be merged later

        for url in links: # gets courses from each link
            driver.get( url ) # opens url
            data = {} # creates an empty dict for courses 

            try:      # Tries to click on course description
                elem = driver.find_element_by_link_text( "Course Descriptions" )
                elem.send_keys( 'seleniumhq' + Keys.RETURN )
                UNI_page = False # if it can click, then it is not UNI page
            except:
                UNI_page = True # if it cant click, then it is UNI page

            for timer in xrange(3): #Tries to get the main description part
                                    #waits 2, 4 or 6 seconds then quits
                try:
                    time.sleep( 2 )
                    pageText = driver.find_element_by_xpath( "//div[@class='fakulte_ack']" ).text
                    break
                except: continue
            
            page = pageText.split('\n') # Splits the page to lines

            line = 0 # initializes while loop variable

            if not UNI_page: # for normal pages

                while line < len( page ) - 1:
                    try:
                        if int(page[line].split()[1][:3]): # if a lines second word is an integer, it means it is a course name
                            data[ ' '.join(page[line].split()[:2]) ] = page[line + 1] # and the line after that is the description
                            line += 2 # increases the line by 2 to omit the description
                    except:
                        line += 1
            else: # for UNI page

                while line < len( page ) - 1:
                    try:
                        if int(page[line].split()[1]): # same logic applies here
                            raw_courses = page[line].split(' / ') # splits the courses by / since there are multiple courses in one line
                            for course in s.clearCourseNames( raw_courses ): # send to a funciton which gets the course names
                                data[ course ] = page[line + 2] # the second line after the name is description this time
                    except:
                        pass
                    line += 1
                    
            data_list.append( data ) # puts every pages descriptions into a list
        driver.quit()    # closes firefox
        s.database = s.mergeDictionaries( data_list ) # merges all dictionaries

        if 0 == s.predictCourses(): # if prediction is successful
            s.displayPredictions() # displays data



    def clearCourseNames( s, raw ): # this funciton is clears the following
        new = {} # * / spaces are cleaned and names are appropirately placed
        for item in raw:
            if item.strip()[0] == '*': item = item.strip()[1:]
            else: item = item.strip()
            try:
                if int( item ): item = 'UNI ' + item
            except:
                try:
                    if int(item[:3]): item = 'UNI ' + item[:3]
                except:
                    item = item[:7]
            new[ item ] = 1 #dictionary used for saving, since keys are unique
        return new
         

    def mergeDictionaries( s, dictlist ): # merges dicitonaries to make one database
        united_dictionary = {}
        
        for dictionary in dictlist:
            for key in dictionary:
                
                united_dictionary[ key ] = dictionary[ key ]
                
        return united_dictionary


    def predictCourses( s ): # After acquiring info from excel and web
        try: # predicts courses
            handler = doc.naivebayes( doc.getwords ) # creates a to be trained classifier
            scoring = { 'A':4, 'B':3, 'C':2, 'D':1, 'F':0 } #dictionaries for less ifs
            letters = [ 'F', 'D', 'C', 'B', 'A' ]
            s.predictions = {} # makes an empty predicitons dict
            
            for course in s.data_excel: # for every course that user TOOK
                if s.data_excel[ course ] != 'Null':
                    try: # trains classifier with descriptions
                        handler.train( s.database[ course ], s.data_excel[ course ] )
                    except: pass # if there is a missing course in database, passes it
            
            for score in scoring: # sets treshhold for each score to 1
                handler.setthreshold( score, 1 )
                
            for course in s.data_excel: # for each course that useres has not taken yet
                if s.data_excel[ course ] == 'Null':
                    if course in s.database: # gets predictions for each course
                        scr = 0
                        for word in s.database[ course ].split():
                            scr += scoring[ handler.classify( word ) ] # adds the prediction scores together
                        s.predictions[ course ] = letters[ int( round( scr / len( s.database[ course ].split() ))) ] # then divides the scores to total
            return 0 # if everything works it is successfull
        except:
            return 1 # if there is an error
        



    def browseExcel( s, event ): # explores excel and records courses with and without grades
        try:
            s.filename = askopenfilename()
            if len(s.filename) < 3: return  # opens file if the format is not correct gives error
            elif ".xls" not in s.filename: raise
        except:
            tkMessageBox.showinfo( title = "Error", message = "Wrong File Type" )
            return
        
        s.label_file.configure( text = s.filename ) # opens file and sheet and shows the file path
        sheet = xlrd.open_workbook( s.filename ).sheet_by_index(0)
        s.data_excel = {}       # [('coursecode': 'Grade' or Null), ()...]
        s.semesters = {}        # ['semester':(coursecode)]
        s.taken_courses = []    # ['coursecode',''...]
        semester_count = -1
        for c in xrange( sheet.ncols ): # loops columns
            for r in xrange( 2,sheet.nrows ): # loops rows
                if semester_count == 15: # resets semester count
                    semester_count = 0
                if "Semester" in str(sheet.cell_value( r, c )) and sheet.cell_value( r,c+1 ) == "": #finds Semester for count and 
                    semester_count += 2
                    s.semesters[semester_count] = []
                for i in xrange( r, sheet.nrows ):
                        
                    if sheet.cell_value(r, c) == "Code" and sheet.cell_value(r+1,c+6) != "":
                                
                        if "Semester" in sheet.cell_value(i+2,c) or i > 45: break
                        else:
                            course_code = str(sheet.cell_value(i+1,c))
                            try:        
                                s.data_excel[course_code] = (str(sheet.cell_value(i+1,c+6))[0])
                                s.taken_courses.append(course_code)
                                s.semesters[semester_count].append(course_code)
                            except:
                                pass
                    elif sheet.cell_value(r, c) == "Code" and sheet.cell_value(r+1,c+6) == "":
                        
                        if "Semester" in sheet.cell_value(i+2,c) or i > 45: break
                        elif "xxx" in str(sheet.cell_value(i+1,c)) or str(sheet.cell_value(i+1,c)) == "" : continue
                        else:
                            course_code = str(sheet.cell_value(i+1,c))
                            s.data_excel[course_code] = ( "Null" )
                            s.semesters[semester_count].append(course_code)
         
        for key, val in s.semesters.items():
            if len( val ) == 0:
                del s.semesters[key]


    def displayPredictions( s ): # displays what is predicted 
        s.text_grade[ 'state' ] = 'normal' # opens textbox for editing
        s.text_grade.delete( '1.0', 'end' ) # clears everything
        results = { 'UNI':[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[] } #makes a dictionary for sorted results
        semester_list = [ 'Null' ] + [ 'Semester ' + str(i) for i in xrange(1,9) ] # makes a semester list first index is semester I
        
        for course in s.predictions: #for every predicted course
            
            if 'UNI' in course: #if it is a uni course
                results[ 'UNI' ].append( course ) # it is placed in UNI list
                continue
            
            for semester in s.semesters: # for every semester
                if course in s.semesters[ semester ]:
                    results[ semester ].append( course ) # puts each class in related semester

        for semester in xrange( 1, 9 ): # for every semester except UNI
            if len( results[ semester ] ) > 0: # if there is a prediction for that semester
                s.text_grade.insert( 'end', semester_list[ semester ] + '\n\n', 'normal' ) # places semester name
                for course in results[ semester ]: # for every course in semester, inserts them with grade colors
                    s.text_grade.insert( 'end', str( course ) + ' --> ' + str( s.predictions[ course ] ) + '\n', s.predictions[ course ] )
                s.text_grade.insert( 'end', '\n', 'normal' ) # leaves a space

        if len( results[ 'UNI' ] ) > 0:
            s.text_grade.insert( 'end', 'UNI Courses' + '\n\n', 'normal' ) # writes uni name
            for course in results[ 'UNI' ]:
                s.text_grade.insert( 'end', str( course ) + ' --> ' + str( s.predictions[ course ] ) + '\n', s.predictions[ course ] )

        s.text_grade[ 'state' ] = 'disabled' # disables the textbox

                        
    def temp( s ):
        s.text_url.insert( 'end', 'http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=12\n' )
        s.text_url.insert( 'end', 'http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=13\n' )
        s.text_url.insert( 'end', 'http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=14\n' )
        s.text_url.insert( 'end', 'http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=32\n' )


def Main():
    root = Window()


if __name__ == '__main__':
    Main()



















