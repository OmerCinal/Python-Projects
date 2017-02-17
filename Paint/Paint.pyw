from Tkinter import *
from PIL import Image, ImageTk
import os
from tkColorChooser import askcolor  


class Window:

    def __init__( s, selected_theme = 1 ):
        #Default window attributes are defined
        s.master = Tk()
        s.theme = Theme( selected_theme )
        s.master.configure( bg = s.theme.bg )
        s.master.title( 'Canvas' )
        s.master.resizable( width = False, height = False )#Prevents user from changing the size of the window
        s.master.geometry( '+%d+%d' % ( s.master.winfo_screenwidth() / 4, s.master.winfo_screenheight() / 5 ) )#Initializes windows starting position

        s.path = '\\'.join((os.getcwd(), 'assets'))

        #GUI creater functions are called
        s.initGui()
        s.displayGui()
        s.configureWidgets()
        s.temp()
        s.master.mainloop()

    def initGui( s ):
        #Headline
        

        #Tool Frame
        s.frame_tool = Frame( s.master, s.theme.frame )
        s.headline = Label( s.frame_tool, s.theme.label, text = 'Canvas', font = ( 'Helvetica', 20 ), width = 50, anchor = W )
        s.var = StringVar()
        s.var.set( 'hand' )
        w,h = 30, 30
        
        s.image_rectangle = ImageTk.PhotoImage( Image.open( '\\'.join( ( os.getcwd(), 'assets', 'rectangle.png' ) )))
        s.tool_rectangle = Radiobutton( s.frame_tool, s.theme.radio, width = w, height = h, image = s.image_rectangle, indicatoron = 0, fg = 'black', text = 'Rectangle', variable = s.var, value = 'rectangle' )
        
        s.image_oval = ImageTk.PhotoImage( Image.open( '\\'.join( ( s.path, 'oval.png' ) )))
        s.tool_oval = Radiobutton( s.frame_tool, s.theme.radio, width = w, height = h, image = s.image_oval, indicatoron = 0, fg = 'black', variable = s.var, value = 'oval' )
        
        s.image_line = ImageTk.PhotoImage( Image.open( '\\'.join( ( s.path, 'line.png' ) )))
        s.tool_line = Radiobutton( s.frame_tool, s.theme.radio, width = w, height = h, image = s.image_line, indicatoron = 0, fg = 'black', variable = s.var, value = 'line' )
        
        s.image_hand = ImageTk.PhotoImage( Image.open( '\\'.join( ( s.path, 'drag.png' ) )))
        s.tool_hand = Radiobutton( s.frame_tool, s.theme.radio, width = w, height = h, image = s.image_hand, indicatoron = 0, fg = 'black', variable = s.var, value = 'hand' )
        
        s.image_eraser = ImageTk.PhotoImage( Image.open( '\\'.join( ( s.path, 'eraser.png' ) )))
        s.tool_eraser = Radiobutton( s.frame_tool, s.theme.radio, width = w, height = h, image = s.image_eraser, indicatoron = 0, fg = 'black', variable = s.var, value = 'eraser' )


        s.label_fill = Label( s.frame_tool, s.theme.label, text = 'Fill Color:' )
        s.label_border = Label( s.frame_tool, s.theme.label, text = 'Border Color:' )
        s.label_weight = Label( s.frame_tool, s.theme.label, text = 'Weight:' )

        s.color_fill = Label( s.frame_tool, width = 5, height = 2, bg = 'white', relief = RAISED )
        s.color_border = Label( s.frame_tool, width = 5, height = 2, bg = 'black', relief = RAISED )

        s.weight = Spinbox( s.frame_tool, s.theme.entry, width = 3, from_ = 0, to = 10 )
        s.button_clear = Button( s.frame_tool, s.theme.button, text = 'Reset', width = 10 )
        

        #Canvas
        s.frame_canvas = Frame( s.master, s.theme.frame )
        s.canvas = Canvas( s.frame_canvas, width = 800, height = 500 )
        s.label_xy = Label( s.frame_canvas, s.theme.label, width = 20, anchor = W, text = 'X: 0.0 Y: 0.0' )
        s.button_magic = Button( s.frame_canvas, s.theme.button, text = 'Beautify Layout', width = 30 )
        



    def displayGui( s ):    # .grid( row = , column = , stick = E, padx = 2, pady = 2 )

        #Tool Frame
        s.frame_tool.grid( row = 1, column = 0 )
        s.headline.grid( row = 0, column = 0, columnspan = 15 )
        s.tool_rectangle.grid( row = 1, column = 0, stick = W, padx = 1, pady = 2 )
        s.tool_oval.grid( row = 1, column = 1, stick = W, padx = 1, pady = 2 )
        s.tool_line.grid( row = 1, column = 2, stick = W, padx = 1, pady = 2 )
        s.tool_hand.grid( row = 1, column = 3, stick = W, padx = 1, pady = 2 )
        s.tool_eraser.grid( row = 1, column = 4, stick = W, padx = 1, pady = 2 )

        s.label_fill.grid( row = 1, column = 6, stick = E, padx = 2, pady = 2 )
        s.color_fill.grid( row = 1, column = 7, stick = E, padx = 2, pady = 2 )
        s.label_border.grid( row = 1, column = 8, stick = E, padx = 2, pady = 2 )
        s.color_border.grid( row = 1, column = 9, stick = E, padx = 2, pady = 2 )
        s.label_weight.grid( row = 1, column = 10, stick = E, padx = 2, pady = 2 )
        s.weight.grid( row = 1, column = 11, stick = E, padx = 2, pady = 2 )
        s.button_clear.grid( row = 1, column = 12, stick = E, padx = 2, pady = 2 )

        #Canvas
        s.frame_canvas.grid( row = 2, column = 0, padx = 5, pady = 5 )
        s.canvas.grid( row = 0, column = 0, columnspan = 3, padx = 5 )
        s.label_xy.grid( row = 1, column = 2, padx = 5, pady = ( 2, 0 ), stick = E )
        #s.button_magic.grid( row = 1, column = 1, padx = 5, pady = ( 2, 0 ) )
        
        

    def configureWidgets( s ):
        s.weight.delete( 0, 'end' )
        s.weight.insert( 'end', '1' )

        s.canvas.bind( '<Motion>', s.mouseXY )
        s.canvas.bind( '<Button-1>', s.canvasClick )
        s.canvas.bind( '<B1-Motion>', s.canvasMove )

        s.color_fill.bind( '<ButtonRelease-1>', s.colorWheel )
        s.color_border.bind( '<ButtonRelease-1>', s.colorWheel )
        s.button_clear.bind( '<ButtonRelease-1>', s.clearAll )

        s.weight.bind( '<MouseWheel>', s.scrollWeight )
        s.button_magic.bind( '<ButtonRelease-1>' , s.magic )


    def magic( s, event ):
        pass


    def getOverlapping( s ):
        all_items = s.canvas.find_all()
        overlaps = []
        for x1,y1,x2,y2 in [ s.canvas.coords( item ) for item in all_items ]:
            overlaps.append( len( s.canvas.find_overlapping( x1, y1, x2, y2 ) ) )
        return sum( overlaps )
        
    

    def scrollWeight( s, event ):
        value =  str( abs( ( int( s.weight.get()) + event.delta / 120 ) % ( int( s.weight[ 'to' ] ) + 1 ) ) )
        s.weight.delete( 0, 'end' )
        s.weight.insert( 'end', value )


    def clearAll( s, event ):
        for item in s.canvas.find_all():
            s.canvas.delete( item )
        s.var.set( 'hand' )
        s.weight.delete( 0, 'end' )
        s.weight.insert( 'end', '1' )
        s.color_fill[ 'bg' ] = 'white'
        s.color_border[ 'bg' ] = 'black'


    def colorWheel( s, event ):
        color = askcolor()
        event.widget[ 'bg' ] = color[1]


    def canvasClick( s, event ):
        s.start_x, s.start_y = event.x, event.y
        s.object = None
        switch = { 'rectangle': s.makeRectangle,
                   'oval': s.makeOval,
                   'line': s.makeLine,
                   'hand': s.drag,
                   'eraser': s.erase }[ s.var.get() ]( event )


    def makeRectangle( s, event ):
        s.object = s.canvas.create_rectangle( s.start_x, s.start_y, event.x, event.y, fill = s.color_fill[ 'bg' ], outline = s.color_border[ 'bg' ], width = int(s.weight.get()) )


    def makeOval( s, event ):
        s.object = s.canvas.create_oval( s.start_x, s.start_y, event.x, event.y, fill = s.color_fill[ 'bg' ], outline = s.color_border[ 'bg' ], width = int(s.weight.get()) )


    def makeLine( s, event ):
        s.object = s.canvas.create_line( s.start_x, s.start_y, event.x, event.y, fill = s.color_border[ 'bg' ], width = int(s.weight.get()) )


    def drag( s, event ):
        try:
            temp = s.canvas.find_closest( event.x, event.y )[ 0 ]
            x1,y1,x2,y2 = s.canvas.coords( temp )
            if x1 < s.start_x and x2 > s.start_x and y1 < s.start_y and y2 > s.start_y:
                s.object = temp
        except:
            pass


    def erase( s, event ):
        try:
            temp = s.canvas.find_closest( event.x, event.y )[ 0 ]
            x1,y1,x2,y2 = s.canvas.coords( temp )
            if x1 < s.start_x and x2 > s.start_x and y1 < s.start_y and y2 > s.start_y:
                s.canvas.delete( temp )
        except:
            pass
        
            

    def canvasMove( s, event ):
        tool = s.var.get()
        if tool not in [ 'hand', 'eraser' ]:
            s.canvas.coords( s.object, s.start_x, s.start_y, event.x, event.y )
        elif tool == 'hand':
            try:
                s.canvas.move( s.object, event.x - s.start_x, event.y - s.start_y )
                s.start_x, s.start_y = event.x, event.y
            except:
                pass

            
        s.mouseXY( event )



    def mouseXY( s, event ):
        s.label_xy[ 'text' ] = 'X: %g\t Y: %g' % ( event.x, event.y )



    def temp( s ):
        pass

class Theme:


    def __init__( s, selected = 1 ):
        s.theme = { 0 : {'bg' : 'sienna', 'fg' : 'burlywood'}, 1 : { 'bg' : 'darkgreen', 'fg' : 'white'}, 2 : { 'bg' : 'darkred', 'fg' : 'white' }, 3 : { 'bg' : 'steel blue', 'fg' : 'white' } }
        s.selected = selected % len( s.theme )

        s.bg = s.theme[s.selected]['bg']
        s.fg = s.theme[s.selected]['fg']

        s.button = { 'bg' : s.bg, 'fg' : s.fg, 'activeforeground' : s.fg, 'activebackground' : s.bg }
        s.label = { 'bg' : s.bg, 'fg' : s.fg }
        s.entry = { 'bg' : s.fg }
        s.frame = { 'bg' : s.bg }
        s.radio = { 'bg' : s.bg, 'fg' : s.fg, 'selectcolor' : s.fg, 'activeforeground' : s.fg, 'activebackground' : s.fg }




def Main():
    root = Window( 3 )


if __name__ == '__main__':
    Main()






