# -*- coding: utf-8 -*-

# =============================================================================
# # CHARACTER READER
#
# # reads the source
# =============================================================================

class CharacterReader:
    def __init__(self, buffer):
        self.buffer = buffer
        
    def _print(self):
        print(self.buffer)
        
    def peek(self, i = 0):
        return self.buffer[i]
    
    def consume(self, i = 0):
        ret_char = self.buffer[i]
        self.buffer = self.buffer[:i]+self.buffer[i+1:]
        return ret_char
    
    #if the buffer is empty we return True
    def isEOF(self):
        try:
            self.buffer[0]
            return False
        except IndexError:
            return True
    
# =============================================================================
# #LEXER
# 
# # convert input from CharacterReader to tokens
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
#   t     | number of \t's that follow each other
# lists:
#   unordered:
#       ul    | content of list
#   ordered:
#       ol    | content of list
# italics:
#   i     | content of italics
# bold:
#   b     | contents of bold
# =============================================================================

class Lexer:
    def __init__(self, charreaderobj):
        self.tokenlist = []
        self.list_chars = ["*", "+", "-"]
        self.special_chars = ["\n"] # list of non-string chars
        self.bold_italic_chars = ["*", "_"]
        self.charreaderobj = charreaderobj
    
    def peek(self, k = 0):
        return self.tokenlist[k]
    
    def consume(self, k = 0):
        del self.tokenlist[k]
        
    def isEOF(self):
        if len(self.tokenlist) == 0:
            return True
        return False
        
    def _print(self):
        for i in self.tokenlist:
            print(i)
                  
    def next_token(self):
        
        # headings
        if self.charreaderobj.peek(0) == "#":
            self.head_find()
        
        # special chars
        elif self.charreaderobj.peek(0) in ['\n', '\t']:\
            self.special_find()
        
        # lists
        elif (self.charreaderobj.peek(0) in self.list_chars) and (self.charreaderobj.peek(1) == " "): 
            # consume both the * as well as the following whitespace
            self.charreaderobj.consume()
            self.charreaderobj.consume()
            
            #call list_find to correctly lex body of list
            self.list_find()
         
        # italics
        #elif (self.charreaderobj.peek(0) in self.bold_italic_chars) and not (self.charreaderobj.peek(1) == " "): 
        #    self.italics_find()
            
        # string stuff. do this last so it doesnt accidentally swallow stuff
        elif self.charreaderobj.peek(0) not in self.special_chars:
            self.string_find()
            
        # for now everything that isnt recognized is deleted lol
        else:
            self.charreaderobj.consume(0)
            
# =============================================================================
#     # if we are in a italics state
# =============================================================================
    def italics_find(self, passed_symbol):
        return_italics = ""
        is_italics = "False"
        # delete the *
        self.charreaderobj.consume()
        
        while True:
            # in this case we dont find the end of the italics part
            # dont forget to add the swallowed * at the beginning
            if self.charreaderobj.isEOF() or self.charreaderobj.peek() == "\n":
                return_italics = passed_symbol + return_italics
                break
            # in this case we find the end of the italics part
            elif (self.charreaderobj.peek() == passed_symbol) and (return_italics[-1] != " "):
                self.charreaderobj.consume()
                is_italics = True
                break
            else:
                return_italics += self.charreaderobj.peek()
                self.charreaderobj.consume()
        
        if is_italics:
            return "<em>"+return_italics+"</em>"
        else:
            return return_italics
        
# =============================================================================
#     # if we are in a bold state
# =============================================================================
    def bold_find(self, passed_symbol):
        return_bold = ""
        is_bold = "False"
        
        #delete the ** or __
        self.charreaderobj.consume()
        self.charreaderobj.consume()
        
        while True:
            # in this case we dont find the end of the italics part
            # dont forget to add the swallowed ** at the beginning
            if self.charreaderobj.isEOF() or self.charreaderobj.peek() == "\n":
                return_bold = passed_symbol*2+return_bold
                break
            # in this case we find the end of the italics part
            elif (self.charreaderobj.peek() == passed_symbol) and \
                 (self.charreaderobj.peek(1) == passed_symbol) and \
                 (return_bold[-1] != " "):
                self.charreaderobj.consume()
                self.charreaderobj.consume()
                is_bold = True
                break
            else:
                return_bold += self.charreaderobj.peek()
                self.charreaderobj.consume()
        
        if is_bold:
            return "<strong>"+return_bold+"</strong>"
        else:
            return return_bold
# =============================================================================
#     # if we are in a special char state
# =============================================================================
    def special_find(self):
        if self.charreaderobj.peek(0) == '\n': 
            self.tokenlist.append(("n", "<br>\n"))
            self.charreaderobj.consume(0)
        elif self.charreaderobj.peek(0) == '\t':
            if self.tokenlist[-1][0] == "t":
                self.tokenlist[-1] = ("t", self.tokenlist[-1][1] + 1)
            else:
                self.tokenlist.append(("t", 1))
            self.charreaderobj.consume(0)

# =============================================================================
#     # if we are in a heading state call this function
# =============================================================================
    def head_find(self):
        return_head = ""
        return_string = ""
        
        #count how many instances of # appear
        while (not self.charreaderobj.isEOF()) and (self.charreaderobj.peek(0) == "#"):
            return_head = return_head + "#"
            self.charreaderobj.consume(0)
        
        # make sure not more than 6 #'s and next char is a space
        # otherwise we return the #'s as a string and end here
        if (len(return_head) <= 6) and (self.charreaderobj.peek(0) == " "):
            
            #everything ucharreaderobj.consume(0)p to a \n is part of the heading
            while (not self.charreaderobj.isEOF()) and not \
                  (self.charreaderobj.peek(0) == "\n"):
                return_string = return_string + self.charreaderobj.peek(0)
                self.charreaderobj.consume(0)
            #consume \n
            self.charreaderobj.consume(0)
            
            # "parse" the two variables together
            return_head = f"h{len(return_head)}"
            self.tokenlist.append((return_head, return_string))
        #if there are too many #'s or no spaces
        else:
            self.tokenlist.append(("s", return_head))
            
# =============================================================================
#     # if we are in a list state call this function
#     # TODO: accept ordered lists as well
# =============================================================================
    def list_find(self):
        #turn list body into a string
        return_list = self.string_find(append = False)
        
        self.tokenlist.append(("ul", return_list))

# =============================================================================
#     # if we are in a string state call this function                
# =============================================================================
    def string_find(self, append = True):
        return_string = ""
        while True:
            if self.charreaderobj.isEOF():
                break
            # check for bold
            elif (self.charreaderobj.peek(0) in self.bold_italic_chars) and \
                 (self.charreaderobj.peek(1) in self.bold_italic_chars) and not \
                 (self.charreaderobj.peek(2) in [" ", self.charreaderobj.peek(0)]):
                return_string += self.bold_find(self.charreaderobj.peek())
            # check for italics
            if (self.charreaderobj.peek(0) in self.bold_italic_chars) and not \
               (self.charreaderobj.peek(1) in [" ", self.charreaderobj.peek(0)]):
                return_string += self.italics_find(self.charreaderobj.peek())
            # check for special chars
            if (self.charreaderobj.peek(0) in self.special_chars):
                break
            return_string = return_string + self.charreaderobj.peek(0)
            self.charreaderobj.consume(0)
        
        # if you want the string returned instead of appended
        if append:
            self.tokenlist.append(("s", return_string))
        else:
            return return_string

# Run this function to tokenize all items in the buffer
    def tokenize(self):
        while True:
            if self.charreaderobj.isEOF():# unordered list
                break
            self.next_token()
            
            
            

        
# =============================================================================
# # PARSER    
#     
# # The parser is responsible for reading the tokens from the lexer and 
# # producing the parse-tree. It gets the next token from the lexer,
# # analyzes it, and compare it against a defined grammar.
# =============================================================================

class Parser:
    def __init__(self, filename, lexer_obj):
        self.filename = filename+".html"
        
        # things that always need to be written
        self.beginning =  f"<!DOCTYPE html>\n<html>\n<head>\n<title>{filename}</title>\n</head><body>\n"
        self.end = "</body>\n</html>\n"
        
        # list of special chars
        self.list_of_headers = ["h1", "h2", "h3", "h4", "h5", "h6"]
        self.list_of_lists = ["ul", "ol"]
        
        # imported types
        self.lexer_obj = lexer_obj
        self.f = open(self.filename, "x")
        
    def parse(self):
        # write the beginning stuff of an html doc
        self.f.write(self.beginning)
        
        #this is where the fun begins
        # begin in a base state
        
        while True:
            if self.lexer_obj.isEOF():
                break
            
            # headings
            if self.lexer_obj.peek()[0] in self.list_of_headers:
                self.parse_head()
                
            # lists
            elif self.lexer_obj.peek()[0] in self.list_of_lists:
                self.parse_list(list_depth = 0)

            # paragraphs
            elif self.lexer_obj.peek()[0] in ["s", "i"]:
                self.parse_paragraph()
                
            # if the object is unknown we just boot it for now
            else:
                self.lexer_obj.consume()
        
        
        # write the end stuff of an html doc
        self.f.write(self.end)
        self.f.close()
        
# =============================================================================
#     # parse paragraph stuff
# =============================================================================
    def parse_paragraph(self):
        self.f.write("<p>")
        while (not self.lexer_obj.isEOF()) and self.lexer_obj.peek()[0] in ["s", "n", "i"]:
            #print(len(self.lexer_obj.tokenlist))
            #print(self.lexer_obj.peek()[1])
            if self.lexer_obj.peek()[0] in ["s", "n"]:
                self.f.write(self.lexer_obj.peek()[1])
            elif self.lexer_obj.peek()[0] in ["i"]:
                self.f.write("<em>")
                self.f.write(self.lexer_obj.peek()[1])
                self.f.write("</em>")
            self.lexer_obj.consume(0)
        self.f.write("</p>\n")
        
        
# =============================================================================
#     # parse heading stuff
# =============================================================================
    def parse_head(self):
        self.f.write(f"<{self.lexer_obj.peek()[0]}>")
        self.f.write(self.lexer_obj.peek()[1])
        self.f.write(f"</{self.lexer_obj.peek()[0]}>\n")
        self.lexer_obj.consume()
        
# =============================================================================
#     def parse_list(self, f, list_depth):
#         if self.lexer_obj.peek()[0] == "ul":
#             # start by writing the list enclosure
#             f.write("<ul>\n")
#             
#             # parse content of list and, if nescesary, call for sublist
#             while (not self.lexer_obj.isEOF()):
#                 # TODO: this will break if the user writes a nested list
#                 # and indents it twice instead of once. fix this
#                 # check if we are at correct depth, else we break
#                 if (list_depth > 0) and (self.lexer_obj.peek()[0] == "t"):
#                     if list_depth <= self.lexer_obj.peek()[1]:
#                         self.lexer_obj.peek()[1] -= list_depth
#                     else:
#                         break
#                 
#                 # if the next token is a \t we call parse list recursively
#                 if self.lexer_obj.peek(0)[0] == "t":
#                     self.parse_list(f, self.lexer_obj.peek(), self.lexer_obj, list_depth+1)
#                     
#                 # if we dont get another list element we break
#                 if not (self.lexer_obj.peek(0)[0] == "ul"):
#                     break
#                 
#                 # write new list element
#                 f.write("<li>")
#                 
#                 # write what is in list element
#                 #print(self.lexer_obj.peek(0)[1])
#                 f.write(self.lexer_obj.peek(0)[1])
#                 
#                 # consume the list element and the following break
#                 #TODO: do this with an assertion
#                 self.lexer_obj.consume(0)
#                 self.lexer_obj.consume(0)
#                 
#                 # writte the end of list element
#                 f.write("</li>\n")
#                 
#             # close list
#             f.write("</ul>\n")
#         # ordered lists
#         else:
#             pass
# =============================================================================

# =============================================================================
#     # parse list stuff
# =============================================================================
    def parse_list(self, list_depth):
        if self.lexer_obj.peek()[0] == "ul":
            # start by writing the list enclosure
            self.f.write("<ul>\n")
            
            # parse content of list and, if nescesary, call for sublist
            while (not self.lexer_obj.isEOF()):
                
                #get rid of tabs
                while (self.lexer_obj.peek(0)[0] == "t"):
                    self.lexer_obj.consume(0)
                    
                # if we dont get another list element we break
                if not (self.lexer_obj.peek(0)[0] == "ul"):
                    break
                
                # write new list element
                self.f.write("<li>")
                
                # write what is in list element
                #print(lexer_obj.peek(0)[1])
                self.f.write(self.lexer_obj.peek(0)[1])
                
                # consume the list element and the following break
                #TODO: do this with an assertion
                self.lexer_obj.consume(0)
                self.lexer_obj.consume(0)
                
                # writte the end of list element
                self.f.write("</li>\n")
                
            # close list
            self.f.write("</ul>\n")
        # ordered lists
        else:
            pass
        
    
class ErrorHandler:
    def __init__(self):
        pass