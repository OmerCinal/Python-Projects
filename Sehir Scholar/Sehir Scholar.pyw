from Tkinter import *
from ttk import Combobox
from bs4 import BeautifulSoup as bs4
from urllib2 import *
import shelve, time, tkFont, tkMessageBox


class Window:


    theme = { 1:{'bg' : 'sienna', 'fg' : 'burlywood'},2:{'bg':'darkgreen','fg':'white'}}
    selected = 2 # different themes can be selected and can be added 
    options_button = { 'bg' : theme[selected]['bg'], 'fg' : theme[selected]['fg'], 'activeforeground' : theme[selected]['fg'], 'activebackground' : theme[selected]['bg'] }
    options_label = { 'bg' : theme[selected]['bg'], 'fg' : theme[selected]['fg'] }
    options_entry = { 'bg' : theme[selected]['fg'] }

    page = 1

    def __init__( s ):
        #Default window attributes are defined
        s.master = Tk()
        s.master.configure( bg = s.theme[s.selected]['bg'] )
        s.master.title( 'SEHIR Scholar' )
        s.master.resizable( width = False, height = False )#Prevents user from changing the size of the window
        s.master.geometry( '+%d+%d' % ( s.master.winfo_screenwidth() / 6, s.master.winfo_screenheight() / 20 ) )#Initializes windows starting position

        #GUI creater functions are called
        s.initGui()
        s.displayGui()
        s.configureWidgets()
        s.openDatabase()
        s.temp()
        s.master.mainloop()


    def initGui( s ):#  , bg = s.theme[s.selected]['bg'], fg = s.theme[s.selected]['fg'], activeforeground = s.theme[s.selected]['fg'], activebackground = s.theme[s.selected]['bg']
        s.var_word = IntVar()
        s.var_word.set(1)
        s.var_citation = IntVar()
        s.var_citation.set(1)

        
        #Headline
        s.headline = Label( s.master, text = 'SEHIR Scholar', font = ('Helvatica',20), bg = s.theme[s.selected]['bg'], fg = s.theme[s.selected]['fg'] )

        #Top Frame
        s.frame_top = Frame( s.master, bg = s.theme[s.selected]['bg'] )
        s.label_url = Label( s.frame_top, s.options_label, text = 'URL for faculty list:' )
        s.entry_url = Entry( s.frame_top, s.options_entry, width = 50 )
        s.button_build = Button( s.frame_top, s.options_button, text = 'Build Index' )
        s.entry_search = Entry( s.frame_top, s.options_entry, width = 85 )
        s.label_comma = Label( s.frame_top, s.options_label, text = 'Seperate keywords with comma (No spaces)' )

        #Middle Frame
        s.frame_mid = Frame( s.master, bg = s.theme[s.selected]['bg'] )
        s.label_rank = Label( s.frame_mid, s.options_label, text = 'Ranking Criteria' )
        s.label_weight = Label( s.frame_mid, s.options_label, text = 'Weight' )
        s.label_filter = Label( s.frame_mid, s.options_label, text = 'Filter Papers' )
        s.check_word = Checkbutton( s.frame_mid, s.options_button, fg = 'black', text = 'Word Frequency', variable = s.var_word )
        s.check_citation = Checkbutton( s.frame_mid, s.options_button, fg = 'black', text = 'Citation Count', variable = s.var_citation )
        s.entry_word = Entry( s.frame_mid, s.options_entry, width = 3 )
        s.entry_citation = Entry( s.frame_mid, s.options_entry, width = 3 )
        s.listbox = Listbox( s.frame_mid, width = 50, height = 6, selectmode = 'multiple' )
        s.button_search = Button( s.frame_mid, s.options_button, text = 'Search' )
        

        #Bottom Frame
        s.frame_bot = Frame( s.master, bg = s.theme[s.selected]['bg'] )
        s.scroll = Scrollbar( s.frame_bot )
        s.label_info = Label( s.frame_bot, s.options_label, text = '0 Publications (0 Seconds)' )
        s.text = Text( s.frame_bot, bg = 'white', width = 100, height = 20, state = 'disabled', wrap = WORD, yscrollcommand = s.scroll.set )
        s.label_page = Label( s.frame_bot, s.options_label, text = 'Page:' )
        s.button_prev = Button( s.frame_bot, s.options_button, text = 'Previous', width = 8 )
        s.label_index = Label( s.frame_bot, s.options_label, text = '1' )
        s.button_next = Button( s.frame_bot, s.options_button, text = 'Next', width = 8 )
        


    def displayGui( s ):#  .grid( row = , column =  )
        #Headline
        s.headline.grid( row = 0, column = 0 )

        #Top Frame
        s.frame_top.grid( row = 1, column = 0, padx = 5, pady = 5 )
        s.label_url.grid( row = 0, column = 0, padx = 2, pady = 2 )
        s.entry_url.grid( row = 0, column = 1, padx = 2, pady = 2 )
        s.button_build.grid( row = 0, column = 2, padx = 2, pady = 2 )
        s.entry_search.grid( row = 1, column = 0, columnspan = 3, padx = 2, pady = 2 )
        s.label_comma.grid( row = 2, column = 0, columnspan = 3, padx = 2, pady = 2 )

        #Middle Frame
        s.frame_mid.grid( row = 2, column = 0, padx = 5, pady = 5 )
        s.label_rank.grid( row = 0, column = 0, padx = 2, pady = 2 )
        s.label_weight.grid( row = 0, column = 1, padx = 2, pady = 2 )
        s.label_filter.grid( row = 0, column = 2, padx = 2, pady = 2 )
        s.check_word.grid( row = 1, column = 0, padx = 2, pady = 2, stick = W )
        s.check_citation.grid( row = 2, column = 0, padx = 2, pady = 2, stick = W )
        s.entry_word.grid( row = 1, column = 1, padx = 2, pady = 2 )
        s.entry_citation.grid( row = 2, column = 1, padx = 2, pady = 2 )
        s.listbox.grid( row = 1, column = 2, rowspan = 2, padx = 2, pady = 2 )
        s.button_search.grid( row = 1, column = 3, padx = 2, pady = 2 )
        

        #Bottom Frame
        s.frame_bot.grid( row = 3, column = 0, padx = 5, pady = 5  )
        s.label_info.grid( row = 0, column = 0, padx = 2, pady = 2  )
        s.text.grid( row = 1, column = 0, columnspan = 5, padx = 2, pady = 2 )
        s.label_page.grid( row = 2, column = 2, stick = E )
        s.button_prev.grid( row = 2, column = 2 )
        s.label_index.grid( row = 2, column = 3 )
        s.button_next.grid( row = 2, column = 4, stick = W )
        s.scroll.grid( row = 1, column = 5, stick = N + S + W )




    def configureWidgets( s ):# .bind( '<ButtonRelease-1>',  ) # Buttons bind to functions
        s.button_build.bind( '<ButtonRelease-1>', s.fetchData ) # fetches data from website
        s.button_search.bind( '<ButtonRelease-1>', s.search )   # searches keywords in retreived data
        s.button_next.bind( '<ButtonRelease-1>', s.plusPage )   # increases the page number
        s.button_prev.bind( '<ButtonRelease-1>', s.minusPage )  # decreases the page number

        s.scroll.config( command = s.text.yview )   # scrollbar for textbox
        
        s.entry_word.insert( 'end', '1' )       # default values for weights
        s.entry_citation.insert( 'end', '1' )

        s.font_blue = tkFont.Font( weight = 'bold', size = 12 ) # configuring fonts for textbox
        s.font_red = tkFont.Font( size = 12 )
        s.font_normal = tkFont.Font( size = 12 )
        s.text.tag_configure( 'red', font = s.font_red, foreground = 'red' )
        s.text.tag_configure( 'blue', font = s.font_blue, foreground = 'blue' )
        s.text.tag_configure( 'normal', font = s.font_normal, foreground = 'black' )




    def search( s, event ): # Starts searching keywords inside the data
        start = time.time() # gets starting point of the search
        s.keywords = s.entry_search.get().lower().split( ',' )  # gets keywords 
        if s.keywords[0] == '' and s.var_word.get() == 1:       # checks if are there any keywords
            tkMessageBox.showwarning('Search','Please enter at least one keyword.')
            return
        filters = [ s.listbox.get(index) for index in s.listbox.curselection() ] # makes a list of the selected filters
        
        try:
            if s.var_word.get() == 1:   # gets ranking measures and checks if none is selected
                weight_word = int(s.entry_word.get())
            if s.var_citation.get() == 1:
                weight_citation = int(s.entry_citation.get())
        except:
            tkMessageBox.showerror('Weight','Please enter valid weights.')
            return 
        
        if s.var_word.get() == 1:   # if word frequency is selected
            results_freq = {}       # searches keywords
            for filter in filters:  # searches for each selected filter
                for publication in s.database[filter]: # loops pubs in each filter
                    score = 1 # sets score to one by default
                    counts = [] # new list for each keywords count in a pub
                    for keyword in s.keywords: # searches each keyword
                        word_count = 0
                        for word in publication[1].split(): # searches word by word to exclude ':;/'
                            if keyword.lower() in word.lower():
                                word_count += 1
                        counts.append( word_count ) # adds the number of findings
                    counts.sort() 
                    if counts[-1] == 0: continue    # if the biggest word count of the publication is 0
                    for count in counts:            # then nothing is found, goes to next publication
                        if count != 0:
                            score *= count          # gets the total score
                            
                    results_freq[ publication ] = score # gives score to the publication
                    
            results_freq = s.normalizeScores( results_freq ) 
                    
        if s.var_citation.get() == 1: # searches for the citations 
            results_citation = {}
            for filter in filters: # loops each filter
                for publication in s.database[filter]:
                    if publication[2] != 0: # if citation number is 0 doesnt add to dicitonary
                        results_citation[ publication ] = publication[ 2 ]

            results_citation = s.normalizeScores( results_citation )

        try: # group of conditions to merge two rankings, #TODO improve this
            if s.var_word.get() == 1 and s.var_citation.get() == 1 and len(results_freq) != 0 and len(results_citation) != 0:
                results = {} # if everything is how it is supposed to be, merges two rankings
                for pub in results_citation.keys():
                    if pub in results_freq.keys():
                        results[ pub ] = ( results_citation[ pub ] * weight_citation + results_freq[ pub ] * weight_word ) / ( weight_word + weight_citation )

            elif s.var_word.get() == 1 and len(results_freq) != 0: # if frequency is checked but nothing is found
                results = results_freq

            elif s.var_citation.get() == 1 and len(results_citation) != 0: # if citation is checked but nothing is found
                results = results_citation

            else: # if nothing is checked or found

                if s.var_word.get() == 0 and s.var_citation.get() == 0: # if nothing is checked
                    tkMessageBox.showwarning('Ranks','Please check at least one rank.')

                else:
                    tkMessageBox.showwarning('Ranks','Nothing found.') # if nothing is checked nor found
                    
                return 
            s.updateResults( results, str(time.time() - start)[:5] ) # prints the elapsed time and results
        except:
            tkMessageBox.showwarning('Filter','Please select more filters.')
            return 
                
                    

    def updateResults( s, results, elapsed ): # function to prepares the results
        try:
            s.page = 1 # resets the page to 1
            s.results = [ (score,pub) for (pub,score) in results.items() ] # switches key and values
            s.results.sort( reverse = True ) # sorts to have the biggest score first
            s.updateInfo( len(s.results), elapsed ) # prints the # of findings and the time passed
            s.updateText() # updates textbox
        except:
            print 'updateResults Error'

    def updateText( s ): # prints publications on the screen and paints them
        s.text[ 'state' ] = 'normal' # makes textbox editable 
        s.text.delete( '1.0', 'end' ) # clears everything
        count = s.page*10 - 10 # gets the first pub to be displayeds index
        if len(s.results) - (s.page*10) + 10 >= 10: # if there are more than 10 values in the current page
            for index in xrange( s.page*10 - 10, s.page*10 ): # loops through values from the x to x + 10
                count += 1
                s.text.insert( 'end', str(count) + '.\t', 'normal' ) # index number
                for word in s.results[index][1][1].split(): # starts printing word by word
                    if s.isIn( word.lower(), s.keywords ): # checks if the word is a keyword
                        s.text.insert( 'end', word + ' ', 'blue' ) # makes found word blue and bold
                    else:
                        s.text.insert( 'end', word + ' ', 'normal' ) # makes it normal 
                    
                s.text.insert( 'end', ' [' + str(s.results[index][1][2]) + ' Citations] ' + str(s.results[index][0])[:6] + '\n\n', 'red' ) # adds citation and score
        else:   # if there are less then 10 values in the current page
            for index in xrange( s.page*10 - 10, len(s.results) ):
                count += 1
                s.text.insert( 'end', str(count) + '.\t', 'normal' )
                for word in s.results[index][1][1].split():
                    if s.isIn( word.lower(), s.keywords ):
                        s.text.insert( 'end', word + ' ', 'blue' )
                    else:
                        s.text.insert( 'end', word + ' ', 'normal' )
                    
                s.text.insert( 'end', ' [' + str(s.results[index][1][2]) + ' Citations] ' + str(s.results[index][0])[:6] + '\n\n', 'red' )
        s.text[ 'state' ] = 'disabled'
        s.label_index[ 'text' ] = str( s.page )


    def isIn( s, word, data ): # checks if a word is inside a list, checks more carefully
        for item in data:
            if item in word:
                return True
        return False

    def normalizeScores( s, scores ): # normalizes scores (taken from mysearchengine.py)
        try:
            maxscore = max( scores.values() )
            if maxscore == 0: maxscore = 0.00001
            return dict([ ( pub, float( score ) / maxscore ) for ( pub, score ) in scores.items() ])
        except:
            return 
        

    # gets data from website and saves it to database
    def fetchData( s, event ):# database = { filter: [( UUID, publication, # of citations )] } 
        uuid = 0 # Universal Unique ID
        papers = {} # dictionary to put findings
        url = s.entry_url.get() # bs4 functions to create soup object
        soup = bs4( urlopen( url ).read(), 'html.parser' ) 
        for person in soup.findAll( 'div',{ 'class':'member' } ): # loops for each person on the people site
            soup_person = bs4( urlopen( 'http://cs.sehir.edu.tr' + person.find( 'a' ).get( 'href' ) ).read(), 'html.parser' ) # creates soup obj for each person
            item = soup_person.find( 'div',{ 'role':'tabpanel', 'id':'publication' } ) # gets to the tab with filters 
            filters = [ filter.text.strip() for filter in item.findAll( 'p' ) ] # gets filters
            
            for filter in filters: # gets each unique filter as key and gives them lists
                if filter not in papers.keys():
                    papers[ str(filter) ] = []
                    
            count = -1
            for paper in item.findAll( 'ul' ): # loops for every headline / filter
                count += 1
                for public in paper.findAll( 'li' ): # loops for every publication
                    uuid += 1 
                    try:
                        citation = int(public.text.split()[-2][1:]) # if there citation, this code should work
                        publication = ' '.join( public.text.split()[1:-2] )
                    except:
                        citation = 0 # if there is no citation this code should work
                        publication = ' '.join( public.text.split()[1:] )
                        
                    papers[ filters[count] ].append( ( uuid, publication , citation ) )
                    # database = { filter: [( UUID, publication, # of citations )] }
                    
        for filter in papers:
            s.database[filter] = papers[filter] # saves everything to the database

        s.updateListbox() # updates filter list


    def updateListbox( s ): # inserts filters into listbox
        s.listbox.delete( 0, 'end' ) # cleans previous filters
        filters = s.database.keys() # gets the list of filters
        filters.sort() # sorts them alphabetically
        for filter in filters: # inserts all filters
            s.listbox.insert( 'end', filter )
            
        
    def openDatabase( s ): s.database = shelve.open( 'cs.publications', writeback = True ) # opens database with writeback for reduced coding

    def updateInfo( s, count, time ): # updates the search info
        try:
            s.label_info[ 'text' ] = str( count ) + ' Publications (' + str( time ) + ' Seconds)'
        except:
            pass

    def plusPage( s, event ): # increases the page number
        try:
            if len(s.results) > s.page * 10: # checks if there should be more pages or not
                s.page += 1
                s.updateText()
        except:
            pass
        
    def minusPage( s, event ): # decreases the page number
        try:
            if s.page > 1: # checks if the number is lower than 1
                s.page -= 1
                s.updateText()
        except:
            pass

    
    def temp( s ): # list of functions and codes that should not be in the final product
        s.entry_url.insert( 'end', 'http://cs.sehir.edu.tr/en/people/' )
        # enabled for easier access while testing



if __name__ == '__main__':
    root = Window()

