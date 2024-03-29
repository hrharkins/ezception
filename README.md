# EZCeption (and EZMessage)

These classes provide a simplified means to define exception classes and
message attributes.

# Benefits

* Less boilerplate to define error classes so they'll be used more.
* Foramtting does not happen at raise time.
* Fields are easier to probe in exception handlers.
* Class-bases exceptions are a snap to define.
* Works with regular Python exception classes.
* Interfaces with the gettext module by default.
* Allows for associating other i18n messaging in the error classes.

# Installation.

```bash
pip install ezception
```

NOTE: ezception is not on pypi yet.  Until official releases are available:

```bash
pip install https://github.com/hrharkins/ezception/archive/master.zip
```

# Basics

```python
import ezception

class MyWebRequester(object):

    class Error(ezception.EZCeption):
        'A general error has occurred.'
        
    class OpenError(Error):
        'An error opening {self.url!r} has occurred.'
    
    class NoURLError(OpenError):
        '''
        No URL was provided.
        ''''
        
    class NoURLError(OpenError):
        '''
        The scheme {self.scheme!r} is not acceptable.
        '''

    ...
    
    def open(self, url):
        ... stuff happens.
        
        ... Oh noes!
        raise self.BadSchemeError(scheme=url.scheme)
        
```

So in the example the class defines a simple hierarchy of errors.  Progreammers 
can trivially trap MyWebRequester.Error to catch anything generated by 
MyWebRequester.  Because it's very simple to define those errors, a more 
robust exception hierarchy is more likely to emerge.

In addition, the message is NOT generated at exception time.  Because of this,
it is easy to catch and determine better handling code.  The default Python
exceptions use args, which requires the programmer to have tighter coupling 
with the error classes to acquire the parameters of the failure (or the
error class needs to define more properties).

Only when the exception is printed does stringification occur.  In addition,
the message to be presented is processed using the gettext module, so adding
support for other languages for such messages is possible using regular .po
files.  All messages are tracked by a global ezception.ALL_MSGS dict so
generating base .po files is also simplified.

