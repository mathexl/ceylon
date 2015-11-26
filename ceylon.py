"""Usage: print.py [--create=str] [--add] [--version=str] [--rollback=str] [--revert] [--revert-nosave] [--hash=str] [--file=str]  [CLASS]


Arguments:
    Class to be versioned. 


Options:
    --add  create a new version
    --revert  go back a version
    --revert-nosave  go back a version and don't save current version.
"""

#Ceylon is micro version control
#Still a Work in Progress - feel free to hack around with it but DO NOT use in production YET. 
#If you have any questions, feel free to contact Mathew Pregasen at mathexl@gmail.com

# Docopt is a library for parsing command line arguments
import docopt
import time

if __name__ == '__main__':

    try:
        # Parse arguments, use file docstring as a parameter definition
        global arguments
        global f

        arguments = docopt.docopt(__doc__)
        f = arguments['--file']
        if(arguments['--file'] == None):
            f = "style.css"        
        
        classes = arguments['CLASS']

        def legitimate_class(file_string,location):
            class_content_start = file_string.find("{", location)
            #print file_string[location:class_content_start]
            #check for the last preceding }
            
            find_next_space = file_string.find(' ',location)
            class_name = file_string[location:find_next_space]
            #print class_name
            #print class_content_start
            #print file_string[find_next_space:class_content_start]
            
            #checks if there are any selectors ahead of class
            if(file_string[find_next_space:class_content_start].isspace() == False):
                return False;
            

            find_last_bracket = file_string.rfind('}',0,location)
            till_last_bracket = file_string[find_last_bracket+1:location] #checking for preceding selectors
            if(till_last_bracket.isspace() == False):
                find_last_comment = file_string.rfind('*/',0,location) #checking for in between comment
                #print find_last_comment
                if(find_last_comment == -1):
                    return False;
                till_last_comment = file_string[find_last_comment+2:location]
                if(till_last_comment.isspace() == False):
                    return False;                


            
            return True;
        
        def revert(f,classes,r_string = "False"):
            if(len(str(f)) == 0):
                f = "style.css"
            if ("." + classes) in open(f, 'r').read():
                phile = open(f, 'r').read()
                class_start = phile.find(("." + classes))
                class_content_start = phile.find("{", class_start)
                class_end = phile.find("}", class_content_start)
                timestamp = int(time.time())
                newclass = "." + str(classes) + str("_c_") + str(timestamp)
                content =  phile[class_content_start:class_end+1]
                complete_class = str(newclass) + " " + str(content)
                
                if(r_string == "False"):
                    ceylon = open('ceylon.css', 'r').read()

                    if(arguments['--hash'] == None):
                        cey_class_start = ceylon.rfind(("." + classes + "_c_"))
                    else:
                        cey_class_start = ceylon.find(("." + classes + "_c_" + str(arguments['--hash'])))

                    cey_class_content_start = ceylon.find("{", cey_class_start)
                    cey_class_end = ceylon.find("}", cey_class_content_start)
                    cey_content =  ceylon[cey_class_content_start:cey_class_end+1]

                    rc = "." + str(classes) + cey_content
                else:
                    rc = r_string
                    
                #print rc
                new_replacement_file = phile[0:class_start] + rc + phile[class_end+1:len(phile)]
                replace = open(f, 'w')
                replace.write(new_replacement_file)
                
                if(arguments['--revert'] == True):
                    ceylon = open('ceylon.css', 'a')
                    ceylon.write("\n")
                    ceylon.write("\n")
                    ceylon.write(complete_class)        
        
        if(arguments['--create'] != None):
            version_name = arguments['--create']
            ceylon = open('ceylon.css', 'a')
            ceylon.write("\n")
            ceylon.write("\n")
            ceylon.write("/**** [" + str(version_name) + "] ****/")
            ceylon.write("\n")
            ceylon.write("\n")
            ceylon.write("/**** END[" + str(version_name) + "] ****/")

            print "Version Created::" +  str(version_name)
        

        
        if(arguments['--add'] == True and len(classes) > 0):

            if ("." + classes) in open(f, 'r').read():
                
                phile = open(f, 'r').read()
                
                check_for_space_only = False;
                class_start = 0;
                output = False;
                while(class_start != -1):
                    class_start = phile.find(("." + classes + " "), class_start + 1)                
                    class_content_start = phile.find("{", class_start)
                    check_for_space_only = legitimate_class(phile,class_start)
                    if(check_for_space_only == True):
                        output = True;
                        class_end = phile.find("}", class_content_start)
                        timestamp = int(time.time())
                        newclass = "." + str(classes) + str("_c_") + str(timestamp)

                        content =  phile[class_content_start:class_end+1]

                        complete_class = str(newclass) + " " + str(content)
                        

                        if(arguments['--version'] == None):
                            ceylon = open('ceylon.css', 'a')
                            ceylon.write("\n")
                            ceylon.write("\n")
                            ceylon.write(complete_class)
                        else:
                            ceylon = open('ceylon.css', 'r').read()
                            insertion_point = ceylon.find("/**** END[" + str(arguments['--version']) + "]")

                            new_file = ceylon[0:insertion_point]
                            new_ceylon = open('ceylon.css', 'w')
                            new_ceylon.write(new_file)
                            new_ceylon.close()

                            insert_ceylon = open('ceylon.css', 'a')
                            insert_ceylon.write("\n")
                            insert_ceylon.write("\n")
                            insert_ceylon.write(complete_class)
                            insert_ceylon.write("\n")
                            insert_ceylon.write("\n")
                            insert_ceylon.write(ceylon[insertion_point:])
                    
                        print "Version Saved::" + str(timestamp)
                if(output == False):
                    print "Error::Cannot Find Class"

        if(arguments['--rollback'] != None):
            ceylon = open('ceylon.css', 'r').read()
            start_point = ceylon.find("/**** [" + str(arguments['--rollback']) + "]")
            end_point = ceylon.find("/**** END[" + str(arguments['--rollback']) + "]")
            
            
            
            search_point = start_point
            while(search_point < end_point):
                new_class_begin = ceylon.find(".",search_point)
                class_name_end = ceylon.find("_c_",new_class_begin)

                check_next = ceylon[new_class_begin+1:new_class_begin+2] #check if its a class opposed to a number

                if(new_class_begin == -1): #no more classes exist
                    search_point = end_point
                    break
                    
                if(new_class_begin > end_point): #past the ending point
                    search_point = end_point
                    break
                
                if(check_next.isalpha() == False): 
                    continue #skip if its a nonclass but an int
                

            
                first_bracket = ceylon.find("{",new_class_begin)
                end_bracket = ceylon.find("}",first_bracket+1)

                class_name = ceylon[new_class_begin:class_name_end]
                
                #print str(first_bracket) + " | " + str(end_bracket)
                new_class = class_name + " " + ceylon[first_bracket:end_bracket+1]
                print "Rolled Back::" + str(class_name)
                revert(f,class_name[1:],new_class)

                search_point = end_bracket
            

                
                
        if(arguments['--revert'] == True or arguments['--revert-nosave'] == True and len(classes) > 0):
            revert(f,classes)


        
        key = ''
                
                
    except docopt.DocoptExit as e:
        print e.message
  