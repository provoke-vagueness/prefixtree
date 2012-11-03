#include "Python.h"
#include "structmember.h"

#if PY_MAJOR_VERSION < 3
#include "bytesobject.h"
#include "intobject.h"
#endif

typedef struct {
    unsigned char key;
    PyObject * child;
} ChildObject;

/* Python Node object */
typedef struct {
    PyObject_HEAD
    unsigned char flags;
    ChildObject ** children;
} PyNodeObject;
 

PyDoc_STRVAR(Node_doc,"Node() -> new empty node");

static PyObject *
Node_subscript(PyNodeObject *self, PyObject *py_key)
{
    unsigned char key;
    ChildObject * item;
    int i;

    //Validate item is correct
    if (PyBytes_Check(py_key)){
        PyErr_SetString(PyExc_TypeError, "type(key) != bytes");
        return NULL;
    }
    if (PyBytes_GET_SIZE(py_key) != 1){
        PyErr_SetString(PyExc_ValueError, "len(key) != 1");
        return NULL;
    }
    key = PyBytes_AS_STRING(py_key)[0];

    //find our key and return the child object
    for (i = 0; i < Py_SIZE(self); i++){
        item = self->children[i];
        if (item->key == key)
            return item->child;
    }

    PyErr_SetString(PyExc_KeyError, "child key not set");
    return NULL;
}

static int 
Node_ass_subscript(PyNodeObject *self, PyObject *py_key, PyObject *child)
{
    unsigned char key;
    ChildObject * item;
    ChildObject ** new_children;
    int i;

    //Validate item is correct
    if (PyBytes_Check(py_key)){
        PyErr_SetString(PyExc_TypeError, "type(key) != bytes");
        return -1;
    }
    if (PyBytes_GET_SIZE(py_key) != 1){
        PyErr_SetString(PyExc_ValueError, "len(key) != 1");
        return -1;
    }
    key = PyBytes_AS_STRING(py_key)[0];

    //increment the ref count on this child object
    Py_INCREF(child);

    //see if the key is already defined...  
    //if yes, swap out the old for the new
    for (i = 0; i < Py_SIZE(self); i++) {
        item = self->children[i];
        if (item->key == key){
            Py_DECREF(item->child);
            item->child = child;
            return 0;
        }
    }

    //create the new child object
    item = (ChildObject *)PyMem_Malloc(sizeof(ChildObject));
    if (item == NULL){
        PyErr_NoMemory();
        return -1;
    }
    item->key = key;
    item->child = child;

    //insert the new child object
    if (Py_SIZE(self) == 0){
        self->children = (ChildObject **)PyMem_Malloc(sizeof(void *));
        if (self->children == NULL){
            PyMem_Free(item);
            Py_DECREF(child);
            PyErr_NoMemory();
            return -1;
        }
        Py_SIZE(self) = 1;
    }else{
        Py_SIZE(self) += 1;
        new_children = (ChildObject **)PyMem_Resize(self->children,
                ChildObject *, Py_SIZE(self));
        if (new_children == NULL){
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

static PyObject *
Node_contains(PyNodeObject *self, PyObject *args)
{
    unsigned char key;
    ChildObject * item;
    int i;

    if (!PyArg_ParseTuple(args, "b", &key))
        return NULL;

    for (i = 0; i < Py_SIZE(self); i++){
        item = self->children[i];
        if (item->key == key)
            return Py_True;
    }
    return Py_False;
}

static PyObject *
Node_delitem(PyNodeObject *self, PyObject *args)
{
    unsigned char key;
    ChildObject * item;
    ChildObject ** new_children;
    int i;
    int new_size;
    int rm_index;

    if (!PyArg_ParseTuple(args, "b", &key))
        return NULL;

    rm_index = -1;
    for (i = 0; i < Py_SIZE(self); i++) {
        item = self->children[i];
        if (item->key == key){
            rm_index = i;
            break;
        }
    }

    if (rm_index == -1){
        PyErr_SetString(PyExc_KeyError, "key not set");
        return NULL;
    }

    //we found the key, let's remove it... 
    new_size = Py_SIZE(self) -= 1;

    //only one object remains - clear it out
    if (new_size == 0){
        Py_DECREF(self->children[0]->child);
        PyMem_Free(self->children[0]);
        PyMem_Free(self->children);
        Py_SIZE(self) = 0;
        return Py_None;
    }

    //shuffle our index across 
    for (i = rm_index; i < Py_SIZE(self) - 1; i++)
        self->children[i] = self->children[i+1];
    
    //resize 
    Py_SIZE(self) = new_size;
    new_children = (ChildObject **)PyMem_Resize(self->children,
            ChildObject *, Py_SIZE(self));
    if (new_children == NULL){
        //Not much we can do here ---  we've broken the children, but 
        //Py_SIZE is consistent still.
        return PyErr_NoMemory();
    }
    self->children = new_children;
    return Py_None;
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
    self->children = NULL;
    return (PyObject *)self;
}


static int
Node_init(PyNodeObject *self, PyObject *args, PyObject *kw)
{
    return 0;
}

static PyObject *
Node_iter(PyDictObject *dict)
{
    return Py_None;
}



static void
Node_dealloc(PyNodeObject *self)
{    
    ChildObject * item;
    int i;

    if (self)
    {
        if (self->children){
            for (i = 0; i < Py_SIZE(self); i++){
                item = self->children[i];
                Py_DECREF(item->child);
                PyMem_Free(item);
            }
            PyMem_Free(self->children);
            self->children = NULL;
            Py_SIZE(self) = 0;
        }
    }

    Py_TYPE(self)->tp_free((PyObject*)self);
}


static PyMemberDef Node_members[] = {
    {NULL}                                      /* sentinel */
};


static PyObject *
Node_sizeof(PyNodeObject *self)
{
    Py_ssize_t res;
    res = sizeof(PyNodeObject) +
            Py_SIZE(self) * sizeof(void *) * sizeof(ChildObject);
    return PyLong_FromSsize_t(res);
}

PyDoc_STRVAR(sizeof__doc__, "N.__sizeof__() -> size of N in memory, in bytes");

PyDoc_STRVAR(getitem__doc__, "x.__getitem__(y) <==> x[y]");

PyDoc_STRVAR(setitem__doc__, "x.__setitem__(i, y) <==> x[i]=y");

PyDoc_STRVAR(delitem__doc__, "x.__delitem__(y) <==> del x[y]");

PyDoc_STRVAR(length__doc__, "x.__len__() <==> len(x)");

PyDoc_STRVAR(contains__doc__, "x.__contains__(y) <==> x[y]");

static PyMethodDef Node_methods[] = {
    {"__sizeof__",
        (PyCFunction)Node_sizeof, METH_NOARGS, sizeof__doc__},
    {"__getitem__", 
        (PyCFunction)Node_subscript, METH_O | METH_COEXIST, getitem__doc__},
    {"__setitem__", 
        (PyCFunction)Node_ass_subscript, METH_VARARGS, setitem__doc__},
    {"__delitem__", 
        (PyCFunction)Node_delitem, METH_VARARGS, delitem__doc__},
    {"__len__", 
        (PyCFunction)Node_length, METH_NOARGS, length__doc__},
    {"__contains__", 
        (PyCFunction)Node_contains, METH_VARARGS, contains__doc__},
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
    (getiterfunc)Node_iter,                     /* tp_iter */
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
