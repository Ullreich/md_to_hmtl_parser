# -*- coding: utf-8 -*-


# reads the source
class CharacterReader:
    def __init__(self, buffer):
        self.buffer = buffer
        # self.index = 0
        
    def _print(self):
        print(self.buffer)
        
    def peek(self, i = 0):
        return self.buffer[i]
    
    def consume(self, i = 0):
        ret_char = self.buffer[i]
        self.buffer = self.buffer[:i]+self.buffer[i+1:]
        #self.index = self.index + i
        return ret_char
    
    #if the buffer is empty we return True
    def isEOF(self):
        try:
            self.buffer[0]
            return False
        except IndexError:
            return True
        
    # not needed at the moment because i dont want this index-stuff
    def set_index(self, i):
        self.index = i

    def get_index(self):
        return self.index        
            

# convert input from CharacterReader to tokens
class Lexer:
    def __init__(self):
        self.tokenlist = []
        self.list_chars = ["*", "+", "-"]
        self.special_chars = ["\n"] + self.list_chars #list of non-string chars
        #self.index = 0
    
    def peek(self, k = 0):
        return self.tokenlist[k]
    
    def consume(self, k = 0):
        #self.index = k
        del self.tokenlist[k]
        #self.index = self.index+k
        
    def isEOF(self):
        if len(self.tokenlist) == 0:
            return True
        return False
        
    def _print(self):
        for i in self.tokenlist:
            print(i)

# =============================================================================
# TODO: impolement \n as a type (and \t?)
#
#
# types:
# headings:
#   h1    | content of heading
#   h2    | content of heading
#   h3    | content of heading
#   h4    | content of heading
#   h5    | content of heading
#   h6    | content of heading
# string:
#   s     | content of string
# lineend:
#   n     | "<br>\n"
# tab:
#   t     | t (for now i guess)
# lists:
#   unordered:
#       ul    | content of list
#   ordered:
#       ol    | content of list
# =============================================================================
                  
    # pass charread object to function
    def next_token(self, charreaderobj):
        
        next_char = charreaderobj.peek(0)
        
        # headings
        if next_char == "#":
            self.head_find(charreaderobj)
        
        # special chars
        elif next_char == '\n': 
            self.tokenlist.append(("n", "<br>\n"))
            charreaderobj.consume(0)
        elif next_char == '\t':
            self.tokenlist.append(("t", "t"))
            charreaderobj.consume(0)
        
        # lists
        elif (next_char in self.list_chars) and (charreaderobj.peek(1) == " "): 
            # consume both the * as well as the following whitespace
            charreaderobj.consume()
            charreaderobj.consume()
            
            #call list_find to correctly lex body of list
            self.list_find(charreaderobj)
            
        # string stuff
        elif next_char not in self.special_chars:
            self.string_find(charreaderobj)
            
        # for now everything that isnt recognized is deleted lol
        else:
            charreaderobj.consume(0)
    
# =============================================================================
#     # if we are in a heading state call this function
# =============================================================================
    def head_find(self, charreaderobj):
        return_head = ""
        return_string = ""
        
        #count how many instances of # appear
        while (not charreaderobj.isEOF()) and (charreaderobj.peek(0) == "#"):
            return_head = return_head + "#"
            charreaderobj.consume(0)
        
        # make sure not more than 6 #'s and next char is a space
        # otherwise we return the #'s as a string and end here
        if (len(return_head) <= 6) and (charreaderobj.peek(0) == " "):
            
            #everything ucharreaderobj.consume(0)p to a \n is part of the heading
            while (not charreaderobj.isEOF()) and (not charreaderobj.peek(0) == "\n"):
                return_string = return_string + charreaderobj.peek(0)
                charreaderobj.consume(0)
            #consume \n
            charreaderobj.consume(0)
            
            # "parse" the two variables together
            return_head = f"h{len(return_head)}"
            self.tokenlist.append((return_head, return_string))
        #if there are too many #'s or no spaces
        else:
            self.tokenlist.append(("s", return_head))
            
# =============================================================================
#     # if we are oin a list state call this function
#     # TODO: accept ordered lists as well
# =============================================================================
    def list_find(self, charreaderobj):
        #turn list body into a string
        return_list = self.string_find(charreaderobj, append = False)
        
        self.tokenlist.append(("ul", return_list))

# =============================================================================
#     # if we are in a string state call this function                
# =============================================================================
    def string_find(self, charreaderobj, append = True):
        return_string = ""
        while True:
            if charreaderobj.isEOF():
                break
            elif (charreaderobj.peek(0) in self.special_chars):
                break
            return_string = return_string + charreaderobj.peek(0)
            charreaderobj.consume(0)
        
        # if you want the string returned instead of appended
        if append:
            self.tokenlist.append(("s", return_string))
        else:
            return return_string
        
        
    
    def tokenize(self, charreaderobj):
        while True:
            if charreaderobj.isEOF():
                break
            self.next_token(charreaderobj)
            
            
            

        
    
# The parser is responsible for reading the tokens from the lexer and 
# producing the parse-tree. It gets the next token from the lexer,
# analyzes it, and compare it against a defined grammar.


class Parser:
    def __init__(self, filename):
        self.filename = filename
        
        self.beginning =  "<!DOCTYPE html>\n<html>\n<body>\n"
        self.end = "</body>\n</html>\n"
        
        self.list_of_headers = ["h1", "h2", "h3", "h4", "h5", "h6"]
        
    #TODO
    def parse(self, lexer_obj):
        f = open(self.filename, "x")
        
        # write the beginning stuff of an html doc
        f.write(self.beginning)
        
        #this is where the fun begins
        # begin in a base state
        
        while True:
            if lexer_obj.isEOF():
                break
            
            next_token = lexer_obj.peek()
            
            # headings
            if next_token[0] in self.list_of_headers:
                self.parse_head(f, next_token, lexer_obj)
            
            # paragraphs
            elif next_token[0] == "s":
                f.write("<p>")
                while (not lexer_obj.isEOF()) and lexer_obj.peek()[0] in ["s", "n", "ul"]:
                    #print(len(lexer_obj.tokenlist))
                    #print(lexer_obj.peek()[1])
                    f.write(lexer_obj.peek()[1])
                    lexer_obj.consume(0)
                f.write("</p>\n")
                #lexer_obj.consume()
            
            # if the object is unknown we just boot it for now
            else:
                lexer_obj.consume()
        
        
        # write the end stuff of an html doc
        f.write(self.end)
        f.close()
        
    #parse heading stuff
    def parse_head(self, f, next_token, lexer_obj):
        f.write(f"<{next_token[0]}>")
        f.write(next_token[1])
        f.write(f"</{next_token[0]}>\n")
        lexer_obj.consume()
        
    
class ErrorHandler:
    def __init__(self):
        pass