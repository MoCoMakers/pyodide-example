"""
Demo by MoCo Makers

License:  MIT License
"""

import js
from pyodide.code import run_js 

div = js.document.getElementById("main-area")
div.innerHTML = "<h1>This element was created from Python</h1>"

class ScriptStack():
    def __init__(self, script_stack=[]):
        self.script_stack = script_stack
    
    def add_script(self, new_script):
        self.script_stack.append(new_script)
    
    def get_script_stack(self):
        return self.script_stack

class HeaderStack(ScriptStack):
    def __init__(self, script_stack=[]):
        ScriptStack.__init__(self, script_stack=script_stack)

class FooterStack(ScriptStack):
    def __init__(self, script_stack=[]):
        ScriptStack.__init__(self, script_stack=script_stack) 

class PageContext():
    def __init__(self, header_stack, footer_stack, element_count = 0):
        self.header_stack = header_stack
        self.footer_stack = footer_stack
        self.element_count = element_count
    
    def add_footer_script(self, new_script):
        self.footer_stack.add_script(new_script)
    
    def get_footer_js(self):
        footer_js = ""
        count = 0
        for elem in self.footer_stack.get_script_stack():
            footer_js = footer_js+'''

            /*** start of footer_js: '''+str(count)+'''***/
            '''+elem
            count = count+1
        return footer_js
    
    def add_header_script(self, new_script):
        self.header_stack.add_script(new_script)
    
    def get_header_js(self):
        header_js = ""
        count = 0
        for elem in self.header_stack.get_script_stack():
            header_js = header_js+'''
            /*** start of header_js: '''+str(count)+'''***/
            '''+elem
            count = count+1
        return header_js

    def increment_element_count(self):
        self.element_count = self.element_count + 1
    
    def get_element_count(self):
        return self.element_count
    

class PageElement():
    def __init__(self, ctx, unique_id=None):
        self.unique_count = ctx.get_element_count()
        if not unique_id:
            self.unique_id  = "py-uid-"+str(self.unique_count)
        else:
            self.unique_id = unique_id
            
        self.ctx = ctx

        # Each new element created should affect the page context
        self.ctx.increment_element_count()

class DraggableDemoElement(PageElement):
    def __init__(self, ctx, unique_id=None, z_index=None):
        super().__init__(ctx, unique_id)

        if not z_index:
            self.z_index = 10+ctx.get_element_count()
        else:
            self.z_index = z_index
        
        footer_js = self.getSupportingJS()
        # Enque the special JS that tracks this element in the page context
        ctx.add_footer_script(footer_js)

    def getElementHTML(self):
        draggable_frame = '''
            <div id="'''+self.unique_id+'''" class="draggable">
            <!-- Include a header DIV with the same name as the draggable DIV, followed by "header" -->
            <div class="mydivheader header-'''+str(self.unique_count)+'''">Click here to move</div>
            <p>Move</p>
            <p>this</p>
            <p>DIV</p>
            </div>
        '''
        return draggable_frame
    
    def getSupportingJS(self):
        print(self.unique_id)
        supporting_JS = '''
        // Make the DIV element draggable:
        dragElement(document.getElementById("'''+self.unique_id+'''"));
        '''
        return supporting_JS

"""
Begin a render stack with this style of render stack:

run_js(ctx.get_header_js())
div.innerHTML = myElement1.getElementHTML()+myElement1.getElementHTML()
run_js(ctx.get_footer_js())
"""


# Intialize a PageContext object, which allows us to subscribe and register script elements, rendered in order of being appended
ctx = PageContext(header_stack=HeaderStack(), footer_stack=FooterStack())

# Any given script is just a python string. Ensure your JS has proper syntax!
starter_js = '''
console.log("Running starter_js block");

function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (document.getElementById(elmnt.id + "header")) {
        // if present, the header is where you move the DIV from:
        document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
    } else {
        // otherwise, move the DIV from anywhere inside the DIV:
        elmnt.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
    }
}
'''
# Add the script to a queue/list of scripts
ctx.add_footer_script(starter_js)

print("Before elements")

# Using a convention of your design, create your primary HTML elements here as Python Objects
myElement1 = DraggableDemoElement(ctx=ctx)
myElement2 = DraggableDemoElement(ctx=ctx)

#Begin render of context
run_js(ctx.get_header_js())

# Render your primary page elements from their object form
div.innerHTML = myElement1.getElementHTML()+myElement2.getElementHTML()

footer_script = '''
console.log("running footer scripts");
'''
ctx.add_footer_script(footer_script)

#js.alert(ctx.get_footer_js())
run_js(ctx.get_footer_js())