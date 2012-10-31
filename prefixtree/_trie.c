#include "Python.h"
#include "structmember.h"

#if PY_MAJOR_VERSION < 3
#include "bytesobject.h"
#include "intobject.h"
#endif

/* Python Node object */
typedef struct {
    PyObject_HEAD
} NodeObject;

PyDoc_STRVAR(Node_doc,"Node() -> new empty node");


static PyObject *
Node_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    NodeObject *self;
    self = (NodeObject*)type->tp_alloc(type, 0);
    return (PyObject *)self;
}


static int
Node_init(NodeObject *self, PyObject *args, PyObject *kw)
{
    return 0;
}


static void
Node_dealloc(NodeObject *self)
{
    Py_TYPE(self)->tp_free((PyObject*)self);
}


static PyMemberDef Node_members[] = {
    {NULL}                                      /* sentinel */
};


static PyObject *
Node_sizeof(NodeObject *self)
{
    Py_ssize_t res;
    res = sizeof(NodeObject);
    return PyLong_FromSsize_t(res);
}

PyDoc_STRVAR(sizeof__doc__, "D.__sizeof__() -> size of N in memory, in bytes");


static PyMethodDef Node_methods[] = {
    {"__sizeof__",
        (PyCFunction)Node_sizeof, METH_NOARGS, sizeof__doc__},
    {NULL}                                      /* sentinel */
};


static PyTypeObject NodeType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "prefixtree._trie.Node",
    sizeof(NodeObject),
    0,
    (destructor)Node_dealloc,                   /* tp_dealloc */
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
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   /* tp_flags */
    Node_doc,                                   /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    Node_methods,                               /* tp_methods */
    Node_members,                               /* tp_members */
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

    if (PyType_Ready(&NodeType) < 0)
        return NULL;

#if PY_MAJOR_VERSION >= 3
    module = PyModule_Create(&_triemodule);
#else
    module = Py_InitModule3("_trie", NULL, Module_doc);
#endif

    if (module == NULL)
        return NULL;

    Py_INCREF(&NodeType);
    PyModule_AddObject(module, "Node", (PyObject*)&NodeType);

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
