#!/usr/bin/python
#Ceylon is micro version control
#Still a Work in Progress - feel free to hack around with it but DO NOT use in production YET. 
#If you have any questions, feel free to contact Mathew Pregasen at mathexl@gmail.com


############################
#Imports
import sys
import time


############################
#Global Variables 
global arguments
global all_classes 
global f #file variable
global flag #delineation of class, identifier, or native tag

############################
#terminal colors below
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[97m'
    OKGREEN = '\033[92m'
    WARNING = '\033[90m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

############################
#Valid arguments to add. 
arguments = {};
args_list = list();
args_list = sys.argv;
arguments['--add'] = False
arguments['--revert'] = False
arguments['--revert-nosave'] = False
arguments['--tag'] = False
arguments['--create'] = None
arguments['--version'] = None
arguments['--rollback'] = None
arguments['--hash'] = None
arguments['--file'] = None


############################
#check through arguments passed in to sort them. 
for i in args_list:
    if(i == '--add'):
        arguments['--add'] = True
    if(i == '--revert'):
        arguments['--revert'] = True
    if(i == '--revert-nosave'):
        arguments['--revert-nosave'] = True
    if(i == '--tag'):
        arguments['--tag'] = True
        
        
    # the main args above
    if(i[0:9] == '--create='):
        arguments['--create'] = i[9:]  
    
    if(i[0:10] == '--version='):
        arguments['--version'] = i[10:]  
        
    if(i[0:11] == '--rollback='):
        arguments['--rollback'] = i[11:]  
        
    if(i[0:7] == '--hash='):
        arguments['--hash'] = i[7:]  
        
    if(i[0:7] == '--file='):
        arguments['--file'] = i[7:]  

############################
if(len(sys.argv) > 2): #check if it is a class specific command
    all_classes = sys.argv[2] #declare the class the secondone
    all_classes = all_classes.split("/") #explode the string for classes in case multiple.
    
    
############################ FUNCTIONS ###############################
def legitimate_class(file_string,location):
    class_content_start = file_string.find("{", location)

    #check for the last preceding }

    find_next_space = file_string.find(' ',location)
    class_name = file_string[location:find_next_space]


    #checks if there are any selectors ahead of class

    if(file_string[find_next_space:class_content_start].isspace() == False and find_next_space != -1 and find_next_space < class_content_start):
        return False;


    find_last_bracket = file_string.rfind('}',0,location)

    if(find_last_bracket == -1):
        find_last_bracket = 0

    till_last_bracket = file_string[find_last_bracket+1:location] #checking for preceding selectors

    if(till_last_bracket == ''):
        return True;


    if(till_last_bracket.isspace() == False):

        if(file_string.rfind('}',0,location) != -1): #exclusion if */ or beginning 
            next_bracket = file_string.find("{", file_string.rfind('}',0,location))

            #############################
            #checks for @media precedence
            if(next_bracket != class_content_start):
                return True 
            #############################
            
        find_last_comment = file_string.rfind('*/',0,location) #checking for in between comment

        if(find_last_comment == -1):
            return False;
        till_last_comment = file_string[find_last_comment+2:location]
        if(till_last_comment.isspace() == False):
            return False;                



    return True;

def revert(f,classes,r_string = "False"):
    if (flag + classes) in open(f, 'r').read():
        phile = open(f, 'r').read()
        class_start = phile.find((flag + classes))
        class_content_start = phile.find("{", class_start)
        class_end = phile.find("}", class_content_start)
        timestamp = int(time.time())
        newclass = flag + str(classes) + str("_c_") + str(timestamp)
        content =  phile[class_content_start:class_end+1]
        complete_class = str(newclass) + " " + str(content)

        if(r_string == "False"):
            ceylon = open('ceylon/ceylon.css', 'r').read()

            if(arguments['--hash'] == None):
                cey_class_start = ceylon.rfind((flag + classes + "_c_"))
            else:
                cey_class_start = ceylon.find((flag + classes + "_c_" + str(arguments['--hash'])))

            cey_class_content_start = ceylon.find("{", cey_class_start)
            cey_class_end = ceylon.find("}", cey_class_content_start)
            cey_content =  ceylon[cey_class_content_start:cey_class_end+1]

            rc = flag + str(classes) + cey_content
        else:
            rc = r_string

        #print rc
        new_replacement_file = phile[0:class_start] + rc + phile[class_end+1:len(phile)]
        replace = open(f, 'w')
        replace.write(new_replacement_file)

        if(arguments['--revert'] == True):
            ceylon = open('ceylon/ceylon.css', 'a')
            ceylon.write("\n")
            ceylon.write("\n")
            ceylon.write(complete_class)    

        return True;    

#################################  [MAIN]  #####################################
if __name__ == '__main__':

    try:


        
        f = arguments['--file']

        if(arguments['--file'] == None):
            f = "style.css"        
        
        
        if(arguments['--tag'] == True):
            flag = ""
        else:
            flag = "."
            
        
        
        if(arguments['--create'] != None):
            version_name = arguments['--create']
            ceylon = open('ceylon/ceylon.css', 'a')
            ceylon.write("\n")
            ceylon.write("\n")
            ceylon.write("/**** [" + str(version_name) + "] ****/")
            ceylon.write("\n")
            ceylon.write("\n")
            ceylon.write("/**** END[" + str(version_name) + "] ****/")

            print(bcolors.WARNING + "Version Created" + bcolors.ENDC + "::" + bcolors.OKBLUE + str(version_name) + bcolors.ENDC)
        

        if(arguments['--rollback'] != None):
            ceylon = open('ceylon/ceylon.css', 'r').read()
            start_point = ceylon.find("/**** [" + str(arguments['--rollback']) + "]")
            end_point = ceylon.find("/**** END[" + str(arguments['--rollback']) + "]")



            search_point = start_point
            while(search_point < end_point):
                new_class_begin = ceylon.find(".",search_point)

                if(new_class_begin == -1): #no more classes exist
                    search_point = end_point
                    break

                class_name_end = ceylon.find("_c_",new_class_begin)

                check_next = ceylon[new_class_begin+1:new_class_begin+2] #check if its a class opposed to a number



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
                print(bcolors.WARNING + "Reverted" + bcolors.ENDC + "::" + bcolors.OKBLUE + str(class_name) + bcolors.ENDC)
                revert(f,class_name[1:],new_class)

                search_point = end_bracket

            #new look checking for attributes
            ceylon = open('ceylon/ceylon.css', 'r').read()
            start_point = ceylon.find("/**** [" + str(arguments['--rollback']) + "]")
            end_point = ceylon.find("/**** END[" + str(arguments['--rollback']) + "]")



            search_point = start_point
            flag = ""
            while(search_point < end_point):
                new_class_begin = ceylon.find("[--tag]",search_point)

                if(new_class_begin == -1): #no more classes exist
                    search_point = end_point
                    break

                class_name_end = ceylon.find("_c_",new_class_begin)

                check_next = ceylon[new_class_begin+1:new_class_begin+2] #check if its a class opposed to a number



                if(new_class_begin > end_point): #past the ending point
                    search_point = end_point
                    break



                first_bracket = ceylon.find("{",new_class_begin)
                end_bracket = ceylon.find("}",first_bracket+1)

                class_name = ceylon[new_class_begin + 7:class_name_end]

                #print str(first_bracket) + " | " + str(end_bracket)
                new_class = class_name + " " + ceylon[first_bracket:end_bracket+1]

                revert(f,class_name,new_class)

                search_point = end_bracket

        if(len(sys.argv) > 2):
            for classes in all_classes:
                if(arguments['--add'] == True and len(classes) > 0):
                    if (classes) in open(f, 'r').read():
                        phile = open(f, 'r').read()
                        check_for_space_only = False;
                        class_start = 0;
                        output = False;




                        while(class_start != -1):
                            class_start = phile.find((flag + classes), class_start)

                            if(class_start == -1):
                                break;

                            class_content_start = phile.find("{", class_start)
                            check_for_space_only = legitimate_class(phile,class_start)
                            if(check_for_space_only == True):

                                output = True;
                                class_end = phile.find("}", class_content_start)
                                timestamp = int(time.time())
                                newclass = flag + str(classes) + str("_c_") + str(timestamp)

                                content =  phile[class_content_start:class_end+1]

                                complete_class = str(newclass) + " " + str(content)

                                if(flag == ""):
                                    complete_class = "[--tag]" + complete_class

                                if(arguments['--version'] == None):
                                    ceylon = open('ceylon/ceylon.css', 'a')
                                    ceylon.write("\n")
                                    ceylon.write("\n")
                                    ceylon.write(complete_class)
                                else:
                                    ceylon = open('ceylon/ceylon.css', 'r').read()
                                    insertion_point = ceylon.find("/**** END[" + str(arguments['--version']) + "]")

                                    new_file = ceylon[0:insertion_point]
                                    new_ceylon = open('ceylon/ceylon.css', 'w')
                                    new_ceylon.write(new_file)
                                    new_ceylon.close()

                                    insert_ceylon = open('ceylon/ceylon.css', 'a')
                                    insert_ceylon.write("\n")
                                    insert_ceylon.write("\n")
                                    insert_ceylon.write(complete_class)
                                    insert_ceylon.write("\n")
                                    insert_ceylon.write("\n")
                                    insert_ceylon.write(ceylon[insertion_point:])

                                print(bcolors.WARNING + "Version Saved" + bcolors.ENDC + "::" + bcolors.OKBLUE + str(classes) + bcolors.ENDC + "::" + bcolors.HEADER + str(timestamp) + bcolors.ENDC)
                            class_start = class_start + 1
                        if(output == False):
                            print("Error::Cannot Find Class")


                if(arguments['--revert'] == True or arguments['--revert-nosave'] == True and len(classes) > 0):
                    rev = revert(f,classes)
                    if(rev == True):
                        print(bcolors.WARNING + "Reverted" + bcolors.ENDC + "::" + bcolors.OKBLUE + str(classes) + bcolors.ENDC)


        
        key = ''
                
                
    except ValueError:
        print("Error")
