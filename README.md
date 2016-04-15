#ExpandCMacro

Sublime Text 3 plugin that expands C/C++ macros. Currently only works on Linux/OS X

##Example

```C
#include <stdio.h>


#define PRINT_2(MSG, ARGS...) printf(MSG, ##ARGS);
#define PRINT(MSG,ARGS...) PRINT_2(MSG,##ARGS)
#define MACRO(X)                                              \
{                                                             \
    if (1)                                                    \
        PRINT("this is a test %d\n", X)                       \
    else                                                      \
        PRINT("---- %s -----\n", "this is another test")      \
}

int main()
{
    MACRO(25)
    return 0;
}
```

Executing the command on the line `MACRO(25)` will result in following output

```C
{ if (1) printf("this is a test %d\n", 25); else printf("---- %s -----\n", "this is another test"); }`
```


##Installation

1. Install "clang" or "gcc".
2. Clone this repository and put it in your Sublime's packages directory.
3. Edit the settings to your needs.
4. Default key bindings are:  "ctrl-alt-z" to put result output panel.
5. To modify those bindings, simply edit "Default (OSX).sublime-keymap" or its linux counterpart.

##Settings

 - include_dirs: List of directories where relevant header files are located
 - compiler: Use gcc or clang to get result
 - other_flags: You can define compile time macros here with "-D DEFINE_SOMETHING"
 
