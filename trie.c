
#include "Python.h"
#include "trie.h"

    
static Py_ssize_t
trienode_length(PyTrieNodeObject *a)
{
    return Py_SIZE(a);
}

static PyObject *
trienode_item(PyTrieNodeObject *a, Py_ssize_t i)
{
    return NULL;
}

static void
list_dealloc(PyTrieNodeObject *op)
{

}

static int
trienode_init(PyTrieNodeObject *self, PyObject *args, PyObject *kw)
{

    return 0;
}

static PyObject *
trienode_sizeof(PyTrieNodeObject *self)
{
    Py_ssize_t res;
    res = 0;
    return PyLong_FromSsize_t(res);
}

static PyObject *trienode_iter(PyObject *seq);

PyDoc_STRVAR(trienodeinsert_doc,
"L.insert(index, object) -- insert object before index");

static PyMethodDef trienode_methods[] = {
    {"insert",       (PyCFunction)trienodeinsert,   METH_O, trienodeinsert_doc},
    {NULL,              NULL}           /* sentinel */
};

static PySequenceMethods trienode_as_sequence = {
    (lenfunc)trienode_length,                       /* sq_length */
    0,                    /* sq_concat */
    0,                  /* sq_repeat */
    (ssizeargfunc)trienode_item,                    /* sq_item */
    0,                                          /* sq_slice */
    0,             /* sq_ass_item */
    0,                                          /* sq_ass_slice */
    0,                  /* sq_contains */
    0,            /* sq_inplace_concat */
    0,          /* sq_inplace_repeat */
};

PyDoc_STRVAR(trienode_doc,"TrieNode() -> new empty node");

PyTypeObject PyTrieNode_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "TrieNode",
    sizeof(PyTrieNodeObject),
    0,
    (destructor)trienode_dealloc,               /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    &trienode_as_sequence,                      /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    PyObject_HashNotImplemented,                /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_BASETYPE | Py_TPFLAGS_LIST_SUBCLASS,         /* tp_flags */
    trienode_doc,                                   /* tp_doc */
    (traverseproc)list_traverse,                /* tp_traverse */
    (inquiry)list_clear,                        /* tp_clear */
    list_richcompare,                           /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    list_iter,                                  /* tp_iter */
    0,                                          /* tp_iternext */
    trienode_methods,                           /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)trienode_init,                    /* tp_init */
    PyType_GenericAlloc,                        /* tp_alloc */
    PyType_GenericNew,                          /* tp_new */
    PyObject_GC_Del,                            /* tp_free */
};

/*********************** TrieNode Iterator **************************/

static PyObject *
trienode_iter(PyObject *seq)
{
    listiterobject *it;

    if (!PyList_Check(seq)) {
        PyErr_BadInternalCall();
        return NULL;
    }
    it = PyObject_GC_New(listiterobject, &PyListIter_Type);
    if (it == NULL)
        return NULL;
    it->it_index = 0;
    Py_INCREF(seq);
    it->it_seq = (PyListObject *)seq;
    _PyObject_GC_TRACK(it);
    return (PyObject *)it;
}
