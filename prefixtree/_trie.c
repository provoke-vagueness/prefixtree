#include "Python.h"
#include "structmember.h"

#if PY_MAJOR_VERSION < 3
#include "bytesobject.h"
#include "intobject.h"
#endif



/* Node object */

typedef struct {
    unsigned char key;
    PyObject * child;
} ChildObject;

typedef struct {
    PyObject_HEAD
    unsigned char flags;
    ChildObject ** children;
} PyNodeObject;
 
/* prototypes */
PyTypeObject PyNodeIterKeys_Type;
PyTypeObject PyNodeIterValues_Type;
PyTypeObject PyNodeIterItems_Type;
static PyObject *NodeIter_new(PyNodeObject *, PyTypeObject *);

PyDoc_STRVAR(Node_doc, "Node() -> new empty node");

static int
Node_parsekey(PyObject *py_key, unsigned char *key)
{
    //if py_key is a long, validate its range
    if (PyLong_Check(py_key)) {
        long value = PyLong_AS_LONG(py_key);
        if (value < 0 || value > 255) {
            PyErr_SetString(PyExc_ValueError, "key <0 || >255");
            return -1;
        }
        *key = (unsigned char)value;
        return 0;
    }

    //try convert py_key to bytes
    if (PyUnicode_Check(py_key)) {
        py_key = PyUnicode_AsUTF8String(py_key);
    }
    else
        py_key = PyBytes_FromObject(py_key);
    if (!py_key)
        return -1;
    if (PyBytes_GET_SIZE(py_key) != 1) {
        PyErr_SetString(PyExc_ValueError, "len(key) != 1");
        return -1;
    }
    Py_DECREF(py_key);
    *key = PyBytes_AS_STRING(py_key)[0];
    return 0;
}

static int
Node_delitem(PyNodeObject *self, PyObject *py_key)
{
    unsigned char key;
    ChildObject * item;
    ChildObject ** new_children;
    int i;
    int rm_index;

    if (Node_parsekey(py_key, &key) != 0)
        return -1;

    rm_index = -1;
    for (i = 0; i < Py_SIZE(self); i++) {
        item = self->children[i];
        if (item->key == key) {
            rm_index = i;
            break;
        }
    }

    if (rm_index == -1) {
        PyErr_SetString(PyExc_KeyError, "key not set");
        return -1;
    }

    //remove the item 
    Py_DECREF(item->child);
    PyMem_Free(item);
    Py_SIZE(self) -= 1;

    //only one object remains - clear it out
    if (Py_SIZE(self) == 0) {
        PyMem_Free(self->children);
        return 0;
    }

    //shuffle our index across 
    for (i = rm_index; i < Py_SIZE(self); i++)
        self->children[i] = self->children[i+1];
   
    //resize 
    new_children = (ChildObject **)PyMem_Resize(self->children,
            ChildObject *, Py_SIZE(self));
    if (new_children == NULL) {
        //Not much we can do here ---  we've broken the children, but 
        //Py_SIZE is consistent still.
        PyErr_NoMemory();
        return -1;
    }
    self->children = new_children;
    return 0;
}

static int 
Node_setitem(PyNodeObject *self, PyObject *py_key, PyObject *child)
{
    unsigned char key;
    ChildObject * item;
    ChildObject ** new_children;
    int i;

    if (Node_parsekey(py_key, &key) != 0)
        return -1;

    //increment the ref count on this child object
    Py_INCREF(child);

    //see if the key is already defined...  
    //if yes, swap out the old for the new
    for (i = 0; i < Py_SIZE(self); i++) {
        item = self->children[i];
        if (item->key == key) {
            Py_DECREF(item->child);
            item->child = child;
            return 0;
        }
    }

    //create the new child object
    item = (ChildObject *)PyMem_Malloc(sizeof(ChildObject));
    if (item == NULL) {
        Py_DECREF(child);
        PyErr_NoMemory();
        return -1;
    }
    item->key = key;
    item->child = child;

    //insert the new child object
    if (Py_SIZE(self) == 0) {
        self->children = (ChildObject **)PyMem_Malloc(sizeof(void *));
        if (self->children == NULL) {
            PyMem_Free(item);
            Py_DECREF(child);
            PyErr_NoMemory();
            return -1;
        }
        Py_SIZE(self) = 1;
    }
    else {
        Py_SIZE(self) += 1;
        new_children = (ChildObject **)PyMem_Resize(self->children,
                ChildObject *, Py_SIZE(self));
        if (new_children == NULL) {
            PyMem_Free(item);
            Py_DECREF(child);
            PyErr_NoMemory();
            return -1;
        }
        self->children = new_children;
    }
    self->children[Py_SIZE(self)-1] = item;

    return 0;
}

//Subscript gets items
static PyObject *
Node_subscript(PyNodeObject *self, PyObject *py_key)
{
    unsigned char key;
    ChildObject * item;
    int i;

    if (Node_parsekey(py_key, &key) != 0)
        return NULL;

    //find our key and return the child object
    for (i = 0; i < Py_SIZE(self); i++) {
        item = self->children[i];
        if (item->key == key) {
            Py_INCREF(item->child);
            return item->child;
        }
    }

    PyErr_SetString(PyExc_KeyError, "child key not set");
    return NULL;
}

//Assignment subscript sets and deletes items
static int 
Node_ass_subscript(PyNodeObject *self, PyObject *py_key, PyObject *child)
{
    if (child == NULL)
        return Node_delitem(self, py_key);
    else
        return Node_setitem(self, py_key, child);

}

static PyObject *
Node_contains(PyNodeObject *self, PyObject *py_key)
{
    unsigned char key;
    ChildObject * item;
    int i;

    if (Node_parsekey(py_key, &key) != 0)
        return NULL;

    for (i = 0; i < Py_SIZE(self); i++) {
        item = self->children[i];
        if (item->key == key) {
            Py_INCREF(Py_True);
            return Py_True;
        }
    }
    Py_INCREF(Py_False);
    return Py_False;
}

static Py_ssize_t
Node_length(PyNodeObject *self)
{
    return Py_SIZE(self);
}

static PyObject *
Node_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyNodeObject *self;
    self = (PyNodeObject*)type->tp_alloc(type, 0);
    self->flags = 0x00;
    Py_SIZE(self) = 0;
    return (PyObject *)self;
}

static int
Node_init(PyNodeObject *self, PyObject *args, PyObject *kw)
{
    return 0;
}

static PyObject *
Node_iterkeys(PyNodeObject *node)
{
    return NodeIter_new(node, &PyNodeIterKeys_Type);
}
    
static PyObject *
Node_itervalues(PyNodeObject *node)
{
    return NodeIter_new(node, &PyNodeIterValues_Type);
}

static PyObject *
Node_iteritems(PyNodeObject *node)
{
    return NodeIter_new(node, &PyNodeIterItems_Type);
}

static void
Node_dealloc(PyNodeObject *self)
{    
    ChildObject * item;
    int i;

    if (self) {
        if (Py_SIZE(self) > 0){
            for (i = 0; i < Py_SIZE(self); i++) {
                item = self->children[i];
                Py_DECREF(item->child);
                PyMem_Free(item);
            }
            PyMem_Free(self->children);
            Py_SIZE(self) = 0;
        }
    }

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
Node_sizeof(PyNodeObject *self)
{
    Py_ssize_t res;
    res = sizeof(PyNodeObject) +
            Py_SIZE(self) * sizeof(void *) * sizeof(ChildObject);
    return PyLong_FromSsize_t(res);
}

PyDoc_STRVAR(sizeof__doc__, "N.__sizeof__() -> size of N in memory, in bytes");
PyDoc_STRVAR(getitem__doc__, "N.__getitem__(y) <==> N[y]");
PyDoc_STRVAR(contains__doc__, "N.__contains__(y) <==> N[y]");
PyDoc_STRVAR(keys__doc__, "N.keys() -> iter keys");
PyDoc_STRVAR(items__doc__, "N.items() -> iter items");
PyDoc_STRVAR(values__doc__, "N.values() -> iter values");

static PyMethodDef Node_methods[] = {
    {"__contains__",   (PyCFunction)Node_contains,      METH_O | METH_COEXIST,
    contains__doc__},
    {"__getitem__",    (PyCFunction)Node_subscript,     METH_O | METH_COEXIST,
    getitem__doc__},
    {"__sizeof__",     (PyCFunction)Node_sizeof,        METH_NOARGS, 
    sizeof__doc__},
    {"keys",           (PyCFunction)Node_iterkeys,      METH_NOARGS,
    keys__doc__},
    {"items",          (PyCFunction)Node_iteritems,     METH_NOARGS,
    items__doc__},
    {"values",         (PyCFunction)Node_itervalues,    METH_NOARGS,
    values__doc__},
    {NULL}                                      /* sentinel */
};

static PyMappingMethods Node_as_mapping = {
    (lenfunc)Node_length,                    /*mp_length*/
    (binaryfunc)Node_subscript,              /*mp_subscript*/
    (objobjargproc)Node_ass_subscript,       /*mp_ass_subscript*/ 
};


static PyTypeObject PyNode_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "prefixtree._trie.Node",
    sizeof(PyNodeObject),
    0,
    (destructor)Node_dealloc,                   /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp34G_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    &Node_as_mapping,                           /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE |
        Py_TPFLAGS_DICT_SUBCLASS,               /* tp_flags */
    Node_doc,                                   /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    (getiterfunc)Node_iterkeys,                 /* tp_iter */
    0,                                          /* tp_iternext */
    Node_methods,                               /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)Node_init,                        /* tp_init */
    0,                                          /* tp_alloc */
    Node_new,                                   /* tp_new */
};

/* Node iterator types */

typedef struct {
    PyObject_HEAD
        PyNodeObject *ni_node;
        Py_ssize_t ni_pos;
        PyObject  *ni_iteritems_result;
        Py_ssize_t len;
} NodeIterObject;

static PyObject *
NodeIter_new(PyNodeObject *node, PyTypeObject *itertype)
{
    NodeIterObject *ni;
    ni = PyObject_GC_New(NodeIterObject, itertype);
    if (ni == NULL)
        return NULL;
    Py_INCREF(node);
    ni->ni_node = node;
    ni->ni_pos = 0;
    ni->len = Py_SIZE(node);
    if (itertype == &PyNodeIterItems_Type) {
        ni->ni_iteritems_result = PyTuple_Pack(2, Py_None, Py_None);
        if (ni->ni_iteritems_result == NULL) {
            Py_DECREF(ni);
            return NULL;
        }
    }
    else
        ni->ni_iteritems_result = NULL;
    return (PyObject *)ni;
}

static void
NodeIter_dealloc(NodeIterObject *ni)
{
    Py_XDECREF(ni->ni_node);
    Py_XDECREF(ni->ni_iteritems_result);
    PyObject_GC_Del(ni);
}

static int
NodeIter_traverse(NodeIterObject *ni, visitproc visit, void *arg)
{
    Py_VISIT(ni->ni_node);
    Py_VISIT(ni->ni_iteritems_result);
    return 0;
}

/*static PyObject *
NodeIter_len(NodeIterObject *ni)
{
    Py_ssize_t len = 0;
    if (ni->ni_node != NULL && ni->len == Py_SIZE(ni->ni_node))
        len = ni->len;
    return PyLong_FromSize_t(len);
}*/

static PyObject *
NodeIter_iternextkey(NodeIterObject *ni)
{

    return NULL;
}

PyTypeObject PyNodeIterKeys_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "prefixtree._trie.NodeIterKeys",             /* tp_name */
    sizeof(NodeIterObject),                     /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)NodeIter_dealloc,               /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,    /* tp_flags */
    0,                                          /* tp_doc */
    (traverseproc)NodeIter_traverse,            /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)NodeIter_iternextkey,         /* tp_iternext */
    0,                                          /* tp_methods */
    0,
};

static PyObject *
NodeIter_iternextvalue(NodeIterObject *ni)
{


    return NULL;
}

PyTypeObject PyNodeIterValues_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "prefixtree._trie.NodeIterValues",           /* tp_name */
    sizeof(NodeIterObject),                     /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)NodeIter_dealloc,               /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,    /* tp_flags */
    0,                                          /* tp_doc */
    (traverseproc)NodeIter_traverse,            /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)NodeIter_iternextvalue,      /* tp_iternext */
    0,                                          /* tp_methods */
    0,
};

static PyObject *
NodeIter_iternextitem(NodeIterObject *ni)
{


    return NULL;
}

PyTypeObject PyNodeIterItems_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "prefixtree._trie.NodeIterItems",           /* tp_name */
    sizeof(NodeIterObject),                     /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)NodeIter_dealloc,               /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,    /* tp_flags */
    0,                                          /* tp_doc */
    (traverseproc)NodeIter_traverse,            /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)NodeIter_iternextitem,      /* tp_iternext */
    0,                                          /* tp_methods */
    0,
};

/* Initialise module */

PyDoc_STRVAR(Module_doc, "C speedups extension for prefixtree");

#if PY_MAJOR_VERSION >= 3
    static PyModuleDef _triemodule = {
        PyModuleDef_HEAD_INIT,
        "_trie",                                    /* m_name */
        Module_doc,                                 /* m_doc */
        -1,                                         /* m_size */
        NULL,                                       /* m_methods */
        NULL,                                       /* m_relaod */
        NULL,                                       /* m_traverse */
        NULL,                                       /* m_clear */
        NULL                                        /* m_free */
    };
#endif 

static PyObject*
moduleinit(void)
{
    PyObject* module;

    if (PyType_Ready(&PyNode_Type) < 0)
        return NULL;

#if PY_MAJOR_VERSION >= 3
    module = PyModule_Create(&_triemodule);
#else
    module = Py_InitModule3("_trie", NULL, Module_doc);
#endif

    if (module == NULL)
        return NULL;

    Py_INCREF(&PyNode_Type);
    PyModule_AddObject(module, "Node", (PyObject*)&PyNode_Type);

    return module;
}


#if PY_MAJOR_VERSION >= 3
    PyMODINIT_FUNC
    PyInit__trie(void)
    {
        return moduleinit();
    }
#else
    PyMODINIT_FUNC
    init_trie(void)
    {
        moduleinit();
    }
#endif
