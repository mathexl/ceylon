"""Usage: print.py [--add] [--revert] [--file=str] CLASS


Arguments:
    Class to be versioned. 

Options:
    --add  create a new version
    --revert go back a version
"""

# Docopt is a library for parsing command line arguments
import docopt
import time

if __name__ == '__main__':

    try:
        # Parse arguments, use file docstring as a parameter definition
        arguments = docopt.docopt(__doc__)
        
        
        
        classes = arguments['CLASS']
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
                
                ceylon = open('ceylon.css', 'a')
                ceylon.write("\n")
                ceylon.write("\n")
                ceylon.write(complete_class)
            
                print "Old Version Saved!"

                
        if(arguments['--revert'] == True and len(classes) > 0):
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
                cey_class_start = ceylon.rfind(("." + classes + "_c_"))
                cey_class_content_start = ceylon.find("{", cey_class_start)
                cey_class_end = ceylon.find("}", cey_class_content_start)
                cey_content =  ceylon[cey_class_content_start:cey_class_end+1]
                
                rc = "." + str(classes) + cey_content
                new_replacement_file = phile[0:class_start] + rc + phile[class_end+1:len(phile)]
                
                
                replace = open(f, 'w')
                replace.write(new_replacement_file)

                ceylon = open('ceylon.css', 'a')
                ceylon.write("\n")
                ceylon.write("\n")
                ceylon.write(complete_class)
        
        key = ''
                
                
    except docopt.DocoptExit as e:
        print e.message
  