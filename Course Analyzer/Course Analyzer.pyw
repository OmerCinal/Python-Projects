from Tkinter import *
from tkFileDialog import *
import os
try:
    from clusters import *
except:
    print "Clusters can not be found"


class GUI:

    #Creating default values     #Will be used to...
    database = { 'Null':"Null" } #check if file is opened
    measure = 'pearson'          #default measurement
    measure_dict = { 'pearson' : pearson, 'tanimoto': tanimoto } #to call functions
    mouse_pos_x = 0 #mouse position X for canvas grabbing
    mouse_pos_y = 0 #mouse position X for canvas grabbing
    full = False
    
    def __init__( self, master ):
        #Default window attributes are defined
        self.master = master
        self.master.configure( background = 'darkred' )
        self.master.title( 'Course Analyzer' )
        self.master.resizable( width = False, height = False )#Prevents user from changing the size of the window
        self.master.geometry( '+%d+%d' % ( self.master.winfo_screenwidth() / 2 - 500, self.master.winfo_screenheight() / 2 - 300 ) )#Initializes windows starting position
        
        #RadioButton variable
        self.var = IntVar()
        self.var.set(1)
        
        #GUI creater functions are called
        self.initGui()
        self.displayGui()
        self.configureWidgets()
        self.master.mainloop()


    def initGui( self ):
        #Top Frame
        self.frame_top = Frame( self.master, bg = 'darkred' )
        self.label_head = Label( self.frame_top, text = 'COURSE ANALYZER - SEHIR LIMITED EDITION', font = ('Helvetica', 20), bg = 'darkred', fg = 'grey' )
        self.label_browse = Label( self.frame_top, text = 'Upload a file that contains course description:', bg = 'darkred', fg = 'grey' )
        self.label_file = Label( self.frame_top, text = 'Selected File:', bg = 'darkred', fg = 'grey' )
        self.label_selected = Label( self.frame_top, text = 'Please select a file', bg = 'darkred', fg = 'grey', bd = 1, relief = GROOVE, width = 75 )
        self.button_browse = Button( self.frame_top, text = 'Browse', bg = 'darkred', fg = 'grey', width = 10, activeforeground = 'grey', activebackground = 'darkred' )
        self.button_clear = Button( self.frame_top, text = 'Clear', bg = 'darkred', fg = 'grey', width = 10, activeforeground = 'grey', activebackground = 'darkred' )
    
        #Bottom Frame
        self.frame_bottom = Frame( self.master, bg = 'darkred' )
        self.scrollbar_listbox = Scrollbar( self.frame_bottom )
        self.scrollbar_canvas_x = Scrollbar( self.frame_bottom, orient = 'horizontal' )
        self.scrollbar_canvas_y = Scrollbar( self.frame_bottom )
        self.label_similarity = Label( self.frame_bottom, text = 'Similarity Measure:', bg = 'darkred', fg = 'grey' )
        self.radio_pearson = Radiobutton( self.frame_bottom, text = 'Pearson', value = 'pearson', variable = self.var, bg = 'darkred', activebackground = 'darkred' )
        self.radio_tanimoto = Radiobutton( self.frame_bottom, text = 'Tanimoto', value = 'tanimoto', variable = self.var, bg = 'darkred',activebackground = 'darkred' )
        self.label_listbox = Label( self.frame_bottom, text = 'Select Course Codes:', bg = 'darkred', fg = 'grey' )
        self.listbox = Listbox( self.frame_bottom, width = 25, height = 6, bg = 'PeachPuff', yscrollcommand = self.scrollbar_listbox.set, selectmode = MULTIPLE )
        self.button_diagram = Button( self.frame_bottom, text = 'Draw Hierarchical Cluster Diagram', bg = 'darkred', fg = 'grey', activeforeground = 'grey', activebackground = 'darkred' )
        self.button_text = Button( self.frame_bottom, text = 'Print Hierarchical Cluster as Text', bg = 'darkred', fg = 'grey', activeforeground = 'grey', activebackground = 'darkred' )
        self.button_matrix = Button( self.frame_bottom, text = 'Show Data Matrix', bg = 'darkred', fg = 'grey', activeforeground = 'grey', activebackground = 'darkred' )
        self.label_info = Label( self.frame_bottom, text = 'Hold right mouse button to navigate', bg = 'darkred', fg = 'grey', font = ( 'Halvetica', 8 ) )
        self.canvas = Canvas( self.frame_bottom, cursor = 'fleur', bg = 'PeachPuff', yscrollcommand = self.scrollbar_canvas_y.set, xscrollcommand = self.scrollbar_canvas_x.set, scrollregion=( 0, 0, 16000, 2500 ) )
        

    def displayGui( self ):
        #Top Frame
        self.frame_top.grid( column = 0, row = 0 )
        self.label_head.grid( column = 0, row = 0 , columnspan = 2)
        self.label_browse.grid( column = 0, row = 1, stick = W )
        self.label_file.grid( column = 0, row = 2, stick = W )
        self.label_selected.grid( column = 0, row = 2, columnspan = 2, stick = E )
        self.button_browse.grid( column = 0, row = 1, stick = E)
        self.button_clear.grid( column = 1, row = 1 )

        #Bottom Frame
        self.frame_bottom.grid( column = 0, row = 1, padx = 10, pady = 10 )
        self.label_similarity.grid( column = 0, row = 0, rowspan = 2 )
        self.radio_pearson.grid( column = 1, row = 0, stick = W + S )
        self.radio_tanimoto.grid( column = 1, row = 1, stick = W + N )
        self.label_listbox.grid( column = 2, row = 0 )
        self.listbox.grid( column = 3, row = 0, rowspan = 2 )
        self.scrollbar_listbox.grid( column = 4, row = 0, rowspan = 2, stick = W + N + S )
        self.button_diagram.grid( column = 0, row = 2 )
        self.button_text.grid( column = 1, row = 2 )
        self.button_matrix.grid( column = 2, row = 2 )
        self.label_info.grid( column = 0, row = 3, columnspan = 4 )
        self.canvas.grid( column = 0, row = 4, columnspan = 4, stick = E + W )
        self.scrollbar_canvas_x.grid( column = 0, row = 5, columnspan = 4, stick = E + W + S )
        self.scrollbar_canvas_y.grid( column = 4, row = 4, stick = N + W + S )
        

    def configureWidgets( self ):
        #All configurations defined for widgets
        
        #Scrollbars
        self.scrollbar_listbox.config( command = self.listbox.yview )
        self.scrollbar_canvas_y.config( command = self.canvas.yview )
        self.scrollbar_canvas_x.config( command = self.canvas.xview )

        #Selecting pearson for radio buttons
        self.radio_pearson.select()

        #Listbox scrolling with scrollwheel
        self.listbox.bind( '<MouseWheel>', self.scrollListbox )

        #Binding widgets to keys and functions
        self.button_browse.bind( "<ButtonRelease-1>", self.openFile )       #Browsing and opening a file
        self.button_clear.bind( "<ButtonRelease-1>", self.clearAll )        #Clears all visual additions
        self.button_matrix.bind( "<ButtonRelease-1>", self.createMatrix )   #3rd button from the left
        self.button_text.bind( "<ButtonRelease-1>", self.createText )       #2nd button from the left
        self.button_diagram.bind( "<ButtonRelease-1>", self.createDiagram ) #1st button from the left
        
        self.radio_pearson.bind( "<ButtonRelease-1>", self.setMeasure )     #radiobutton configuration
        self.radio_tanimoto.bind( '<ButtonRelease-1>', self.setMeasure )    #radiobutton configuration
        
        self.canvas.bind_all( '<MouseWheel>', self.scrollCanvas )           #canvas scrolling with mousewheel
        self.canvas.bind_all( '<B3-Motion>', self.moveCanvas )              #canvas scrolling with mouse right click
        self.canvas.bind_all( '<Button-3>', self.clickedCanvas )            #canvas scrolling with mouse right click
        

    def scrollListbox( self, event ): self.listbox.yview_scroll( event.delta / -120, 'units' )

    def clickedCanvas( self, event ):
        self.mouse_pos_x = event.x
        self.mouse_pos_y = event.y

    def scrollCanvas( self, event ): self.canvas.yview_scroll( -1 * event.delta / 120, 'units' )

    def moveCanvas( self, event ):
        self.canvas.yview_scroll( -1 * ( event.y - self.mouse_pos_y ) / 4, 'units' )
        self.canvas.xview_scroll( -1 * ( event.x - self.mouse_pos_x ) / 6, 'units' )
        self.mouse_pos_x = event.x
        self.mouse_pos_y = event.y


    def openFile( self, event ):
        try:
            file_name = askopenfilename( parent = self.master,title = 'Choose an excel file', filetypes = [ ( 'Text Files', '.txt' ), ( 'All Files', '.*' ) ] )
            if len( file_name ) < 2: return #Checks if the file name is valid
            self.label_selected[ 'text' ] = file_name
            self.database = self.getFile( self.fileName( file_name ) )

            #Inserting course names into listbox
            self.listbox.delete( "0", "end" )
            course_names = self.database.keys()
            course_names.sort()
            for course in course_names:
                self.listbox.insert( "end", course )
        except:
            print 'openFile error catched'

    def createMatrixFile( self ):#Creates a matrix file using the clusters.py function
        try:
            selected_courses = [ self.listbox.get( index ) for index in self.listbox.curselection() ]
            if len( selected_courses ) < 1: return 1 #Exits if user did not choose a file
            dataset = {}
            for course in selected_courses:
                for code in self.database[ course ]:
                    dataset[ course + " " + code ] = self.database[ course ][ code ][ 1 ]
            create_matrix( dataset, 'matrix_file.txt' )
            return 0
        except:
            print 'createMatrixFile error catched'

    def createMatrix( self, event ): #reads the created matrix file and draws it in to the canvas
        try:
            if self.createMatrixFile() == 1: #calling the function to make a matrix file
                raise
            #Displays the contents of the matrix file
            self.canvas.delete( 'all' )
            self.canvas.config( scrollregion=( 0, 0, 16000, 2500 ) )
            matrix = []
            matrix_file = open( 'matrix_file.txt', 'r' )
            for line in matrix_file:
                matrix.append( line.strip() )
            cord_y = 40
            cord_x = 105
            for word in matrix[ 0 ].split():
                self.canvas.create_text( ( cord_x - 75, 20 ), text = word )
                cord_x += 75
            cord_x = 105
            for line in matrix[ 1 : ]:
                self.canvas.create_text( ( 30, cord_y ), text = line.strip().split()[ : 2 ] )
                for item in line.strip().split()[ 2 : ]:
                    self.canvas.create_text( ( cord_x, cord_y ), text = item )
                    cord_x += 75
                cord_y += 20
                cord_x = 105
            matrix_file.close()
        except:
            print 'createMatrix error catched'

        
    def createText( self, event ): #reads from the matrix file and draws it in to the canvas
        try:
            if self.createMatrixFile() == 1: raise #creates a matrix with the current selections
            self.canvas.config( scrollregion=( 0, 0, 16000, 2500 ) )
            self.canvas.delete( 'all' )
            rows, cols, data = readfile( 'matrix_file.txt' )
            diagram = clust2str( hcluster( data, self.measure_dict[ self.measure ] ), rows )
            self.canvas.create_text( ( 75, len(diagram.split()) * 5.2 ), text = diagram )
        except:
            print 'createText error catched'
        
    def createDiagram( self, event ): #1st function to start drawing the diagram
        try:
            if self.createMatrixFile() == 1: raise #creates a matrix with current selections
            self.canvas.delete( 'all' ) #clears canvas
            rows, cols, data = readfile( 'matrix_file.txt' ) #reads from the matrix file
            cluster = hcluster( data, self.measure_dict[ self.measure ] ) #creates the cluster object with read matrix file data

            #Calls the function to draw the cluster into the canvas
            self.drawCluster( cluster, rows )
        except:
            print 'createDiagram error catched'
            

    def drawCluster( self, cluster, labels ):   #Sub function to be able to control errors 
        try:                                    #This function is callable without an event object
            self.canvas.config( scrollregion=( -8000, 0, 8500, 2500 ) )

            #Drawing the cluster tree
            self.drawBranch( cluster, labels, 300, 30 )
        except:
            print 'drawCluster error cathced'


    def drawBranch( self, cluster, labels, cord_x, cord_y ): #Main recursive function which draws the branches and the leafs

        #checks if the cluster is a leaf or not
        if cluster.id >= 0: #Cluster is a leaf
            
            self.canvas.create_line( cord_x, cord_y - 30, cord_x, cord_y - 20 )
            self.canvas.create_text( ( cord_x, cord_y - 10 ), text = labels[ cluster.id ] )
            
        else: #Cluster is not a leaf
            
            #Creates the vertical line
            self.canvas.create_line( cord_x, cord_y - 30, cord_x, cord_y )
            
            #finds the distance between branches
            width_left = self.getClusterWidth( cluster.left ) * 60
            width_right = self.getClusterWidth( cluster.right ) * 60
            
            #gets the coordiantes using distances
            left = cord_x - ( width_right / 2 ) 
            right = cord_x + ( width_left / 2 )
            
            #draws the horizontal line from left branch end to right branch end
            self.canvas.create_line( left, cord_y, right, cord_y )
            
            #calls the function again to draw the next branches
            self.drawBranch( cluster.left, labels, left, cord_y + 30 )      #Starts drawing the left of the cluster tree
            self.drawBranch( cluster.right, labels, right, cord_y + 30 )    #Starts drawing the right of the cluster tree


    #Adjusted function to find the width of the clusters
    def getClusterWidth( self, cluster ): return ( ( self.getClusterWidth( cluster.left ) + self.getClusterWidth( cluster.right )) if cluster.left != None or cluster.right != None else 1 )
    

    #Adjusted function to find the depth of the clusters
    def getClusterDepth( self, cluster ): return ( ( max( self.getClusterDepth( cluster.left ), self.getClusterDepth( cluster.right ) + cluster.distance ) if cluster.left != None or cluster.right != None else 0 ) )
    
            
    #Changes the measurement function when radiobuttons are clicked
    def setMeasure( self, event ): self.measure = event.widget[ 'value' ]
    

    #returns the file name out of the full given path
    def fileName( self, file_path ):
        try:
            for i in xrange( 1, len( file_path ) + 1 ):
                if file_path[ -i ] == chr( 47 ):
                    return file_path[ -i + 1 : ]
            return file_path
        except:
            print 'fileName error catched'
            
            
    #Reads a raw dataset from a file and transfers it to a database
    def getFile( self, file_name ):
        try:
            file_len = self.fileLength( file_name )
            file_obj = open( file_name, 'r' )
            database = {}
            for i in xrange( file_len ):
                line = file_obj.readline().strip().split()
                key1, key2, rest = line[0], line[1], line[2:]
                line = file_obj.readline().strip()
                value = ( ' '.join(rest), line )
                if key1 not in database.keys():
                    database[ key1 ] = { key2: value }
                else:
                    database[ key1 ][ key2 ] = value
            file_obj.close()
            return database    
        except:
            print 'getFile error catched'

    
    def fileLength( self, file_name ):
        try:
            file_obj = open( file_name, 'r' )
            count = 0
            for i in file_obj:
                count += 1
            file_obj.close()
            return count / 2    #This will work in all conditions since the file contains key value pairs
        except:                 #Which is always even
            print 'fileLength error catched'


    #Clears all includings of the canvas, listbox and label
    def clearAll( self, event ):
        self.label_selected[ "text" ] = "Please select a file"
        self.listbox.delete( "0", "end" )
        self.canvas.delete( 'all' )

    def __del__( self ): #Tries to delete the matrix file when the program is closed
        try:
            os.system( 'del matrix_file.txt' )
        except:
            pass


if __name__ == '__main__':
    root = Tk()
    master = GUI( root )


