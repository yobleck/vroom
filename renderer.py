import sys, os, time, random;
import car;

vroom = car.car();

from Xlib import X, display, Xutil; #https://github.com/python-xlib/
#from Xlib.protocol import event;
#my_event = event.Expose(window=my_window, x=0,y=0, width=500,height=500, count=0); #http://python-xlib.sourceforge.net/doc/html/python-xlib_13.html#SEC12

#sys.path.append(os.path.join(os.path.dirname(__file__), '..'));

from PIL import Image;
im = Image.open("./images/test.png");
car_im = Image.open("./images/FuroreGT-GTA2_test.png").rotate(90, expand=1);

my_display = display.Display();
my_display.bell(percent=100);
my_screen = my_display.screen();

my_window = my_screen.root.create_window(2560-500, 0, 500, 500, 0,
                                my_screen.root_depth,
                                X.InputOutput,
                                X.CopyFromParent,

                                # special attribute values
                                background_pixel = my_screen.black_pixel, #remove this to take screen shot of behind window lmao
                                event_mask=(X.ExposureMask | #https://github.com/python-xlib/python-xlib/blob/master/Xlib/X.py
                                            X.StructureNotifyMask |
                                            #X.ButtonPressMask |
                                            #X.ButtonReleaseMask |
                                            #X.Button1MotionMask |
                                            
                                            #X.FocusChangeMask |
                                            #X.LeaveWindowMask |
                                            #X.EnterWindowMask |
                                            X.KeyPressMask |
                                            X.KeyReleaseMask),
                                colormap=X.CopyFromParent);


#colormap https://github.com/python-xlib/python-xlib/blob/4d07023fab1fdefd9152fe2082a0f9d1569dfa56/examples/xdamage.py#L88
colormap = my_screen.default_colormap; blue = colormap.alloc_named_color("blue").pixel; green = colormap.alloc_named_color("green").pixel;

#graphics contexts
timegc = my_window.create_gc(foreground=green, background=my_screen.black_pixel);
bgc = my_window.create_gc(foreground=my_screen.black_pixel, background=my_screen.black_pixel);
#cargc = my_window.create_gc(foreground=blue, background=my_screen.black_pixel);
pilgc = my_window.create_gc(foreground=0, background=0);


#Window info and settings
WM_DELETE_WINDOW = my_display.intern_atom('WM_DELETE_WINDOW');
WM_PROTOCOLS = my_display.intern_atom('WM_PROTOCOLS');

my_window.set_wm_name('VROOM!');
my_window.set_wm_icon_name('vroom.py');
my_window.set_wm_class('my_win', 'Vroom');

my_window.set_wm_protocols([WM_DELETE_WINDOW]); #clean exit?
my_window.set_wm_hints(
    flags=Xutil.StateHint,
    initial_state=Xutil.NormalState);

my_window.set_wm_normal_hints(
    flags=(Xutil.PPosition | Xutil.PSize | Xutil.PMinSize),
    min_width=50,
    min_height=50);

my_window.map();
#my_window.put_image(gc=pilgc, x=400,y=400, width=100,height=100, format=1,depth=1,left_pad=0, data=); #failed put_image attempt

def render(tick, fps_cap=0):
    if(fps_cap):
        time.sleep( (1/fps_cap)-((time.time()-tick)*30) ); #TODO: make this take time since previous frame into account
    
    my_window.fill_rectangle(bgc, 0,0, 500,500); #overwrites previous frame
    #my_window.fill_rectangle(cargc, random.randint(100,500),random.randint(10,500), 10,10);
    
    my_window.put_pil_image(pilgc, 0, 300, im);
    
    vroom.update(tick);
    pos, size, rot = vroom.get_state();
    global car_im;
    temp_im = car_im.rotate(rot, expand=True);
    my_window.put_pil_image(pilgc, round(pos[0]-(temp_im.size[0]//2)), round(pos[1]-(temp_im.size[1]//2)), temp_im);
    
    my_window.image_text(timegc, 0, 10, "time: " + str(tick)); #render time frametime fps etc.
    my_window.image_text( timegc, 0, 25, "frametime: %.4f"%(time.time() - tick) + " ms" );
    my_window.image_text( timegc, 0, 40, "fps: %.2f"%(1/(time.time() - tick)) );
    
    my_display.flush();
    
    return time.time();


tick = time.time();
while True:
    
    tick = render(tick, fps_cap=60);
    
    if(my_display.pending_events()): #can put while here
        e = my_display.next_event();
        
        # Window has been destroyed, quit
        """if(e.type == X.DestroyNotify):
            sys.exit(0);"""
        if(e.type == X.ClientMessage):
            if(e.client_type == WM_PROTOCOLS):
                fmt, data = e.data;
                if(fmt == 32 and data[0] == WM_DELETE_WINDOW):
                    sys.exit(0);
        if(e.type == X.KeyPress):
            #print(e.detail);
            if(e.detail == 25): #w
                vroom.gas(1);
                #vroom.trans_temp(0,-5);
            if(e.detail == 38): #a
                vroom.turn(2);
                #vroom.trans_temp(-5,0);
            if(e.detail == 39): #s
                vroom.gas(-1);
                #vroom.trans_temp(0,5);
            if(e.detail == 40): #d
                vroom.turn(1);
                #vroom.trans_temp(5,0);
            
            if(e.detail in [9,24]): #yet another way to exit
                sys.exit(0);
        
        if(e.type == X.KeyRelease):
            if(e.detail in [25,39]):
                vroom.gas(0);
            if(e.detail in [38,40]):
                vroom.turn(0);
    
#end while loop

