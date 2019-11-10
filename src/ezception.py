
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
            
class EZMessageContainer(object):
    def __getattr__(self, name):
        if name[:5] == 'ezmsg':
            raise AttributeError(name)
        else:
            return getattr(self, 'ezmsg_' + name)()
    
    def __init_subclass__(cls):
        for name, obj in cls.__dict__.items():
            if name[:5] == 'ezmsg' and isinstance(obj, str):
                setattr(cls, name, EZMessage(obj))

    def __str__(self):
        msg = self.ezmsg
        return '' if msg is None else msg()
    
    def __repr__(self):
        return repr(str(self))
        
    @classmethod
    def FLEXIBLE(cls):
        def __init__(self, **_kw):
            self.__dict__.update(_kw)
        
        clsdict = {
            '__init__': __init__,
        }
        
        return type(cls.__name__, (cls,), clsdict)
        
class EZDocMessageContainer(EZMessageContainer):
    def __init_subclass__(cls):
        if 'ezmsg' not in cls.__dict__:
            doclines = (cls.__doc__ or '').split('\n')
            while doclines and not doclines[0]:
                del doclines[0]
            ezmsg = []
            while doclines and doclines[0]:
                ezmsg.append(doclines[0].strip())
                del doclines[0]
            cls.ezmsg = ' '.join(ezmsg)
        super().__init_subclass__()
        
class EZCeption(EZDocMessageContainer.FLEXIBLE(), Exception):
    '''
    Simplified API for defining and formatting exceptions.
    
    >>> class NotFound(EZCeption):
    ...     \'''
    ...     {self.what!r} was not found.
    ...
    ...     More details for programmers.  The first line is used for the
    ...     summary.
    ...     \'''
    ...
    ...     ezmsg_details = 'Could not find {self.what!r} in {self.where!r}'
    ...     where = None
   
    >>> raise NotFound(what='something')
    Traceback (most recent call last):
        ...
    ezception.NotFound: 'something' was not found.

    >>> NotFound(what='something', where='/somewhere/').details
    "Could not find 'something' in '/somewhere/'"

    '''
    
