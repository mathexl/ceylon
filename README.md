# ceylon (WIP)
Micro-Version Control for CSS.  

**Ceylon is micro asynchronous version control for CSS.  Ceylon isn't a replacement for Git or Subversion; rather, it is an indepedent way for you to have strong, readable, and CSS-oriented version control for your styles (and doesn't conflict with the file-level version control on your repository).  Ceylon lets you save previous versions of individual classes in CSS opposed to the entire file.  It is asynchronous in that you can name certain versions of a style set but add classes attached to that style set whenever you want.  Further, since Ceylon saves its data in a seperate .css file, it doesn't conflict with the git flow and can function independently of it.** *Note, this is still a work in progress.  The main functions work but still need to account for things that can be thrown into the mix, like selector, attribute styling, direct tag styling etc.  If you are not using selectors in your project (though I highly recommend using them), Ceylon should be usable in its current state. You can still use Ceylon with selectors but it will ignore them during it.*

What is Ceylon good for:
- Large CSS files with multiple developers
- Products that involved many classes and often change
- Products where swapping between UI interfaces is often and Git flows get too complicated. 


Currently, Ceylon is a python file that does all the version control.  Ceylon is a work in progress in that I am working on creating a package that let's you interact with the program by simply calling `ceylon` insead of `python ceylon.py`  


### Stating a File. 
By default, Ceylon assumes the file that it is operating on is named `style.css`.  However, you may have other .css files to edit.  To declare the file you are working on, simply go `--file=your_css_file.css`

### Saving A Version of a Class
Ceylon saves all its data in a file called `ceylon.css`.  You can see all the saved versions in that file.  To save a state of a version in general, simply call `--add` function and then pass in the name of the CSS class.  For instance, if you had the class in the file `home.css`: 

```CSS
.cool_class{
  width:100%;
  text-align:center;
  height:30px;
  border: 1px grey solid;
}
```

You would call in terminal (order does not matter):

```
python ceylon.py --add cool_class --file=home.css
```

In the saved ```ceylon.css``` file, you will see the following class:

```CSS
.cool_class_c_TIMESTAMP {
    color:yellow;
    position:relative;
    width:100%;
    background:none;
}
```

Where TIMESTAMP would just be the UNIX timestamp when the class was created.

You can also save native tags too, i.e. styling of `<a></a>` tags but you need to let Ceylon know that's the case.  Simply add the `--tag` flag for it to work, so to edit `<hr></hr>` we would go (assuming the file is `style.css`:


```
python ceylon.py --add hr --file=home.css --tag
```

### Roll Back to the Last Version of the Class

If you wanted to roll back to the immediately last version of the class, simply call in terminal:

```
python ceylon.py --revert cool_class --file=home.css
```

By doing this, your `home.css` file will be modified with the old version.  Further, this command will auto-add the current version of the class for safe keeping as the last version.  If you want to suppress the auto addition of the current version, call `--revert-nosave` instead of `--revert`. So: 

```
python ceylon.py --revert-nosave cool_class --file=home.css
```

To rollback to a specific version, you can state the timestamp it was created in using `--version=TIMESTAMP` (the timestamp is printed whenever you create a version).  Thus: 
```
python ceylon.py --revert-nosave --version=TIMESTAMP cool_class --file=home.css
```

Use `--tag` again for a native tag.  Obviously, finding out the version can be a bit of a pain, so instead check out the next section:

### Create Static Versions of Multiple Classes

Sometimes when you are trying new styles, you are adding consistent changes and new looks to multiple elements.  Ceylon has static versioning to adapt to that. You can declare a version that is composite of a group of classes which can be added at different points of time and later rollback to that complete version of the file.  To create a version, simply call `--create=YOUR_VERSION_NAME` in terminal, with YOUR_VERSION_NAME being the static version (one word).  So (assuming you are working within `style.css` this time):

```
python ceylon.py --create=old_metro_style
```

Then, let's say you are about to change a class. You can add it to this version by adding `--version=VERSION_TO_ADD_TO` on the file: 

```
python ceylon.py --add cool_class --version=old_metro_style
```
In the Ceylon.css file, we will see all the versions grouped together with something like this: 

```CSS

/**** [old_metro_style] ****/

.cool_class_c_TIMESTAMP {
    color:yellow;
    position:relative;
    width:100%;
    background:none;
}

/**** END[old_metro_style] ****/

```
Remember, you can add to a version whenever, so it completely obfuscates the linear flow.  To rollback to a version, simply use the `--rollback=YOUR_VERSION` function.  For instance, to rollback to our last state: 

```
python ceylon.py --rollback=old_metro_style
```

We will see the terminal print out all the classes affected by the Rollback: 

```
Rolled Back::.cool_class
```
