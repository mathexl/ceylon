# ceylon
Micro-Version Control for CSS

#### Ceylon is micro asynchronous version control for CSS.  Ceylon isn't a replacement for Git or Subversion; rather, it is an indepedent way for you to have strong, readable, and CSS-oriented version control for your styles.  Ceylon lets you save previous versions of individual classes in CSS opposed to the entire file.  It is asynchronous in that you can name certain versions of a style set but add classes attached to that style set whenever you want. 

What is Ceylon good for:
- Large CSS files with multiple developers
- Products that involved many classes and often change
- Products where swapping between UI interfaces is often and Git flows get too complicated. 


Currently, Ceylon is a python file that does all the version control.  Ceylon is a work in progress in that I am working on creating a package that let's you interact with the program by simply calling `ceylon` insead of `python celyon.py`  

#### Stating a File. 
By default, Ceylon assumes the file that it is operating on is named `style.css`.  However, you may have other .css files to edit.  To declare the file you are working on, simply go `--file=your_css_file.css`

#### Saving A Version of a Class
Ceylon saves all its data in a file called `ceylon.css`.  You can see all the saved versions in that file.  To save a state of a version in general, simply call `--add` function and then pass in the name of the CSS class.  For instance, if I had the class in the file `home.css`: 

```CSS
.cool_class{
  width:100%;
  text-align:center;
  height:30px;
  border: 1px grey solid;
}
```

You would call in terminal:

```
python ceylon.py --add cool_class --file=home.css
```

