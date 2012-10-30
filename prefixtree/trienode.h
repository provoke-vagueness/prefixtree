

#ifndef Py_TRIENODEOBJECT_H
#define Py_TRIENODEOBJECT_H
#ifdef __cplusplus
extern "C" {
#endif


typedef struct {
    unsigned char id;
    PyObject * obj;
} TrieElement;

typedef struct {
    PyObject_VAR_HEAD
    
    TrieElement **element;
    Py_ssize_t allocated;

} PyTrieNodeObject;

PyAPI_DATA(PyTypeObject) PyTrieNodeObject_Type;

#ifdef __cplusplus
}
#endif
#endif


