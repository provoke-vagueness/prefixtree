
#include "Python.h"
#include "trienode.h"

    
static void
PyTrieNode_dealloc(PyTrieNodeObject *op)
{
    return NULL;
}

static int
PyTrieNode_init(PyTrieNodeObject *self, PyObject *args, PyObject *kw)
{

    return 0;
}

static PyObject *
PyTrieNode_sizeof(PyTrieNodeObject *self)
{
    Py_ssize_t res;
    res = 0;
    return PyLong_FromSsize_t(res);
}

static int
PyTrieNode_contains(PyObject *op, PyObject *key)
{
    return 1;
}

static int
PyTrieNode_delitem(PyObject *op, PyObject *key)
{
    return NULL;
}

static int
PyTrieNode_getitem(PyObject *op, PyObject *key)
{
    return NULL;
}

static PyObject *
PyTrieNode_iter(PyObject *op)
{
    return NULL;
}

static PyObject *
PyTrieNode_reversed(PyObject *op)
{
    return NULL;
}

static Py_ssize_t
PyTrieNode_length(PyTrieNodeObject *a)
{
    return Py_SIZE(a);
}

static PyObject *
PyTrieNode_reversed(PyTrieNodeObject *a)
{
    return NULL;
}

static Py_ssize_t
PyTrieNode_setitem(PyTrieNodeObject *a)
{
    return NULL;
}


static PyObject *PyTrieNode_iter(PyObject *seq);

PyDoc_STRVAR(insert_doc,
"L.insert(index, object) -- insert object before index");

PyDoc_STRVAR(contains__doc__,
"D.__contains__(k) -> True if D has a key k, else False");

PyDoc_STRVAR(delitem__doc__, "x.__delitem__(y) <==> del x[y]");

PyDoc_STRVAR(getitem__doc__, "x.__getitem__(y) <==> x[y]");

PyDoc_STRVAR(iter__doc__, "x.__iter__() <==> iter(x)");

PyDoc_STRVAR(len__doc__, "x.__len__() <==> len(x)");

PyDoc_STRVAR(reversed__doc__, "x.reverse() -- reverse *IN PLACE*");

PyDoc_STRVAR(setitem__doc__, "x.__setitem__(i, y) <==> x[i]=y");

PyDoc_STRVAR(sizeof__doc__, "D.__sizeof__() -> size of N in memory, in bytes");

PyDoc_STRVAR(getitem__doc__, "x.__getitem__(y) <==> x[y]");


static PyMethodDef PyTrieNode_methods[] = {
    {"__contains__",  (PyCFunction)PyTrieNode_contains, METH_O | METH_COEXIST,
     contains__doc__},
    {"__delitem__", (PyCFunction)PyTrieNode_delitem, METH_O, delitem__doc__},
    {"__getitem__", (PyCFunction)PyTrieNode_getitem, METH_O, getitem__doc__},
    {"__iter__", (PyCFunction)PyTrieNode_iter, METH_O, iter__doc__},
    {"__len__",  (PyCFunction)PyTrieNode_length, METH_O, iter__doc__},
    {"reversed", (PyCFunction)PyTrieNode_reversed, METH_O, reversed__doc__},
    {"__setitem__", (PyCFunction)PyTrieNode_setitem, METH_O, setitem__doc__},
    {"insert",   (PyCFunction)PyTrieNode_insert,   METH_O, insert_doc},
    {"__sizeof__", (PyCFunction)PyTrieNode_sizeof, METH_NOARGS, sizeof__doc__},
    {NULL,              NULL}           /* sentinel */
};

PyDoc_STRVAR(PyTrieNode_doc,"TrieNode() -> new empty node");

PyTypeObject PyTrieNodeObject_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "TrieNode",
    sizeof(PyTrieNodeObject),
    0,
    (destructor)PyTrieNode_dealloc,             /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    &PyTrieNode_as_sequence,                    /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    PyObject_HashNotImplemented,                /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_BASETYPE | Py_TPFLAGS_LIST_SUBCLASS, /* tp_flags */
    PyTrieNode_doc,                                     /* tp_doc */
    (traverseproc)list_traverse,                /* tp_traverse */
    (inquiry)list_clear,                        /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    PyTrieNode_iter,                            /* tp_iter */
    0,                                          /* tp_iternext */
    PyTrieNode_methods,                         /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)PyTrieNode_init,                  /* tp_init */
    PyType_GenericAlloc,                        /* tp_alloc */
    PyType_GenericNew,                          /* tp_new */
    PyObject_GC_Del,                            /* tp_free */
};

/*********************** TrieNode Iterator **************************/

static PyObject *
PyTrieNode_iter(PyObject *seq)
{
    return NULL;
}
