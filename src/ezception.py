
import gettext

class EZMessage(object):
    '''
    >>> class Hello(object):
    ...     def __init__(self, who='world'):
    ...         self.who = who
    ...
    ...     msg = EZMessage('Hello {self.who!r}')
    
    >>> hello = Hello()
    >>> hello.msg()
    "Hello 'world'"
    '''
    
    ALL_MSGS = set()
    _ = staticmethod(gettext.gettext)
    
    def __init__(self, _msg, _=..., **_kw):
        self.ALL_MSGS.add(_msg)
        self._msg = _msg
        self._kw = _kw
        if _ is not ...:
            self._ = _

    def __call__(self, _src, _=None, **_kw):
        if _ is None:
            _ = self._
        kw = self._kw
        if _kw:
            kw = dict(kw, **_kw)
        if _ is None:
            return self._msg.format(self=_src, ez=self, **kw)
        else:
            return _(self._msg).format(self=_src, ez=self, **kw)

    def __get__(self, target, cls=None):
        if target is None:
            return self
        else:
            return lambda **_k: self(target, **_k)
            
class EZCeption(Exception):
    '''
    Simplified API for defining and formatting exceptions.
    
    >>> class NotFound(EZCeption):
    ...     ezmsg = '{self.what!r} was not found'
    ...     ezmsg_details = 'Could not find {self.what!r} in {self.where!r}'
    ...     where = None
   
    >>> raise NotFound(what='something')
    Traceback (most recent call last):
        ...
    ezception.NotFound: 'something' was not found

    >>> NotFound(what='something', where='/somewhere/').details
    "Could not find 'something' in '/somewhere/'"

    >>> NotFound = EZCeption['NotFound':'{self.what!r} was not found']

    >>> class Reader(EZCeption.Container):
    ...     Error = EZCeption[:]
    ...     OpenError = Error[:]
    ...     NotFoundError = OpenError['{self.src!r} was not found']
    ...     PermissionDeniedError = OpenError[
    ...         'Permission denied for {self.src!r}'
    ...     ]
   
    >>> Reader.OpenError()
    ''
    >>> Reader.NotFoundError(src='something.txt')
    "'something.txt' was not found"
    >>> isinstance(Reader.NotFoundError(src='something.txt'), Reader.Error)
    True
    
    >>> issubclass(EZCeption[::TypeError], TypeError)
    True
    
    '''
    
    __ezunnamed__ = False

    def __init__(self, **_kw):
        self.__dict__.update(_kw)
        
    def __getattr__(self, name):
        if name[:5] == 'ezmsg':
            raise AttributeError(name)
        else:
            return getattr(self, 'ezmsg_' + name)()
    
    def __str__(self):
        msg = self.ezmsg
        return '' if msg is None else msg()
    
    def __repr__(self):
        return repr(str(self))

    def __init_subclass__(cls):
        for name, obj in cls.__dict__.items():
            if name[:5] == 'ezmsg' and isinstance(obj, str):
                setattr(cls, name, EZMessage(obj))

    def __class_getitem__(cls, msg, name=None, bases=()):
        if type(msg) is slice:
            name = msg.start
            bases = msg.step or ()
            msg = msg.stop
            
        if bases is not None and not isinstance(bases, tuple):
            bases = (bases,)
        if cls not in bases:
            bases = (cls,) + bases
            
        clsdict = {
            'ezmsg': msg,
            '__ezunnamed__': name is None,
        }
        
        if name is None:
            name = '%s[%r]' % (cls.__name__, msg)

        return type(name, bases, clsdict)

    class Container(object):
        # Needed because __set_name__ doesn't work for class members (maybe it 
        # will someday).  Classes wanting to use EZCeptionClass[:] will need to
        # use this.
        
        def __init_subclass__(cls):
            super().__init_subclass__()
            for name in dir(cls):
                obj = getattr(cls, name)
                if getattr(obj, '__ezunnamed__', False):
                    obj.__qualname__ = name
                    obj.__ezunnamed__ = False
