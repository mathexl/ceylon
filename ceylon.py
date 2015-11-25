"""Usage: print.py [--create=str] [--add] [--version=str] [--rollback=str] [--revert] [--revert-nosave] [--hash=str] [--file=str]  [CLASS]


Arguments:
    Class to be versioned. 


Options:
    --add  create a new version
    --revert  go back a version
    --revert-nosave  go back a version and don't save current version.
"""

# Docopt is a library for parsing command line arguments
import docopt
import time

if __name__ == '__main__':

    try:
        # Parse arguments, use file docstring as a parameter definition
        arguments = docopt.docopt(__doc__)
        
        
        
        classes = arguments['CLASS']
        
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
        
        
        f = arguments['--file']

        
        if(arguments['--add'] == True and len(classes) > 0):
            if(len(f) == 0):
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

        if(arguments['--rollback'] != None):
            ceylon = open('ceylon.css', 'r').read()
            start_point = ceylon.find("/**** [" + str(arguments['--rollback']) + "]")
            end_point = ceylon.find("/**** END[" + str(arguments['--rollback']) + "]")
            
            
            
            search_point = start_point
            while(search_point < end_point):
                new_class_begin = ceylon.find(".",search_point)
                check_next = ceylon[new_class_begin+1:new_class_begin+2] #check if its a class opposed to a number
                
                if(check_next.isalpha() == False):
                    continue #skip if its a nonclass but an int
                
                if(new_class_begin == -1):
                    search_point = end_point
                    continue
                else:
                    search_point = new_class_begin + 1
            
            
            

                
                
        if(arguments['--revert'] == True or arguments['--revert-nosave'] == True and len(classes) > 0):
            if(len(f) == 0):
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
                
                ceylon = open('ceylon.css', 'r').read()
                
                if(arguments['--hash'] == None):
                    cey_class_start = ceylon.rfind(("." + classes + "_c_"))
                else:
                    cey_class_start = ceylon.find(("." + classes + "_c_" + str(arguments['--hash'])))

                cey_class_content_start = ceylon.find("{", cey_class_start)
                cey_class_end = ceylon.find("}", cey_class_content_start)
                cey_content =  ceylon[cey_class_content_start:cey_class_end+1]
                
                rc = "." + str(classes) + cey_content
                new_replacement_file = phile[0:class_start] + rc + phile[class_end+1:len(phile)]
                
                
                replace = open(f, 'w')
                replace.write(new_replacement_file)
                if(arguments['--revert'] == True):
                    ceylon = open('ceylon.css', 'a')
                    ceylon.write("\n")
                    ceylon.write("\n")
                    ceylon.write(complete_class)


        
        key = ''
                
                
    except docopt.DocoptExit as e:
        print e.message
  