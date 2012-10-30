


#ifndef Py_TRIEOBJECT_H
#define Py_TRIEOBJECT_H
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
#endif


