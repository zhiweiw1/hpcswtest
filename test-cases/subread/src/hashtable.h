/*--------------------------------------------------------------------------*\
 *                   -----===== HashTable =====-----
 *
 * Author: Keith Pomakis (pomakis@pobox.com)
 * Date:   August, 1998
 * Released to the public domain.
 *
 *--------------------------------------------------------------------------
 * $Id: hashtable.h,v 9999.30 2019/12/05 03:05:37 cvs Exp $
\*--------------------------------------------------------------------------*/

#ifndef _HASHTABLE_H
#define _HASHTABLE_H
#ifndef SRINT_64_DEFINED
#define SRINT_64_DEFINED
typedef long long srInt_64;
typedef unsigned long long srUInt_64;
#endif

/* These structs should not be accessed directly from user code.
 * All access should be via the public functions declared below. */

typedef struct KeyValuePair_struct {
    void *key;
    void *value;
    struct KeyValuePair_struct *next;
} KeyValuePair;

typedef struct {
    srInt_64 numOfBuckets;
    srInt_64 numOfElements;
    KeyValuePair **bucketArray;
    float idealRatio, lowerRehashThreshold, upperRehashThreshold;
    int (*keycmp)(const void *key1, const void *key2);
    int (*valuecmp)(const void *value1, const void *value2);
    srUInt_64 (*hashFunction)(const void *key);
    void (*keyDeallocator)(void *key);
    void (*valueDeallocator)(void *value);

    void * appendix1;
    void * appendix2;
    void * appendix3;
    srInt_64 counter1;
    srInt_64 counter2;
    srInt_64 counter3;
} HashTable;


typedef struct {
	void ** elementList;
	srInt_64 numOfElements;
	srInt_64 capacityOfElements;
	void (*elemDeallocator)(void *elem);
	void * appendix1;
} ArrayList;

int ArrayListContainsPtr(ArrayList * list, void * who);
ArrayList * ArrayListCreate(int init_capacity);
ArrayList * ArrayListDuplicate(ArrayList * ori);
void ArrayListDestroy(ArrayList * list);
void * ArrayListGet(ArrayList * list, srInt_64 n);
void * ArrayListRandom(ArrayList * list);
int ArrayListPush(ArrayList * list, void * new_elem);
int ArrayListPush_NoRepeatedPtr(ArrayList * list, void * new_elem);
// Shift is the other direction of Pop:
// Say, a list has elements 0,1,2,3,4
// Pop removes 4 from the list and returns it.
// Shift repoves 0 from the list and returns it.
//
// Caller has to be sure that at least one element is in the list or a NULL is returned. 
// Due to its nature, the caller has to deallocate the returned object. The internal deallocater is NOT called on the returned object.
void * ArrayListShift(ArrayList * list);
void * ArrayListPop(ArrayList * list);
void ArrayListSetDeallocationFunction(ArrayList * list,  void (*elem_deallocator)(void *elem));
void ArrayListSort(ArrayList * list, int compare_L_minus_R(void * L_elem, void * R_elem, ArrayList * me));

// A simple comparison function if you want to sort unsigned long long ints.
int ArrayListLLUComparison(void * L_elem, void * R_elem);

// This function returns the index of the value in the list that is the minumum value greater than "value_less_than_dent".
// The elements in the list are all zero-based unsigned long long ints. The list must be sorted (small -> large) before calling this function.
// If the "value_less_than_dent" is larger than all the values in the list, "-1" is returned;
// If there are repeated numbers in the list, this function will always return the index of the first of them when this repeated number is the next dent.
//
srInt_64 ArrayListFindNextDent(ArrayList * list, srUInt_64 value_less_than_dent);

ArrayList * HashTableKeys(HashTable * tab);
void HashTableIteration(HashTable * tab, void process_item(void * key, void * hashed_obj, HashTable * tab) );
ArrayList * HashTableKeyArray(HashTable * tab);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableCreate() - creates a new HashTable
 *  DESCRIPTION:
 *      Creates a new HashTable.  When finished with this HashTable, it
 *      should be explicitly destroyed by calling the HashTableDestroy()
 *      function.
 *  EFFICIENCY:
 *      O(1)
 *  ARGUMENTS:
 *      numOfBuckets - the number of buckets to start the HashTable out with.
 *                     Must be greater than zero, and should be prime.
 *                     Ideally, the number of buckets should between 1/5
 *                     and 1 times the expected number of elements in the
 *                     HashTable.  Values much more or less than this will
 *                     result in wasted memory or decreased performance
 *                     respectively.  The number of buckets in a HashTable
 *                     can be re-calculated to an appropriate number by
 *                     calling the HashTableRehash() function once the
 *                     HashTable has been populated.  The number of buckets
 *                     in a HashTable may also be re-calculated
 *                     automatically if the ratio of elements to buckets
 *                     passes the thresholds set by HashTableSetIdealRatio().
 *  RETURNS:
 *      HashTable    - a new Hashtable, or NULL on error
\*--------------------------------------------------------------------------*/

HashTable * StringTableCreate(srInt_64 numOfBuckets);
HashTable * StringTableReverse(HashTable * ori);
HashTable *HashTableCreate(srInt_64 numOfBuckets);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableDestroy() - destroys an existing HashTable
 *  DESCRIPTION:
 *      Destroys an existing HashTable.
 *  EFFICIENCY:
 *      O(n)
 *  ARGUMENTS:
 *      hashTable    - the HashTable to destroy
 *  RETURNS:
 *      <nothing>
\*--------------------------------------------------------------------------*/

void HashTableDestroy(HashTable *hashTable);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableContainsKey() - checks the existence of a key in a HashTable
 *  DESCRIPTION:
 *      Determines whether or not the specified HashTable contains the
 *      specified key.  Uses the comparison function specified by
 *      HashTableSetKeyComparisonFunction().
 *  EFFICIENCY:
 *      O(1), assuming a good hash function and element-to-bucket ratio
 *  ARGUMENTS:
 *      hashTable    - the HashTable to search
 *      key          - the key to search for
 *  RETURNS:
 *      bool         - whether or not the specified HashTable contains the
 *                     specified key.
\*--------------------------------------------------------------------------*/

int HashTableContainsKey(const HashTable *hashTable, const void *key);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableContainsValue()
 *                         - checks the existence of a value in a HashTable
 *  DESCRIPTION:
 *      Determines whether or not the specified HashTable contains the
 *      specified value.  Unlike HashTableContainsKey(), this function is
 *      not very efficient, since it has to scan linearly looking for a
 *      match.  Uses the comparison function specified by
 *      HashTableSetValueComparisonFunction().
 *  EFFICIENCY:
 *      O(n)
 *  ARGUMENTS:
 *      hashTable    - the HashTable to search
 *      value        - the value to search for
 *  RETURNS:
 *      bool         - whether or not the specified HashTable contains the
 *                     specified value.
\*--------------------------------------------------------------------------*/

int HashTableContainsValue(const HashTable *hashTable, const void *value);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTablePut() - adds a key/value pair to a HashTable
 *  DESCRIPTION:
 *      Adds the specified key/value pair to the specified HashTable.  If
 *      the key already exists in the HashTable (determined by the comparison
 *      function specified by HashTableSetKeyComparisonFunction()), its value
 *      is replaced by the new value.  May trigger an auto-rehash (see
 *      HashTableSetIdealRatio()).  It is illegal to specify NULL as the
 *      key or value.
 *  EFFICIENCY:
 *      O(1), assuming a good hash function and element-to-bucket ratio
 *  ARGUMENTS:
 *      hashTable    - the HashTable to add to
 *      key          - the key to add or whose value to replace
 *      value        - the value associated with the key
 *  RETURNS:
 *      err          - 0 if successful, -1 if an error was encountered
\*--------------------------------------------------------------------------*/

int HashTablePut(HashTable *hashTable, const void *key, void *value);
int HashTablePutReplace(HashTable *hashTable, const void *key, void *value, int replace_key);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableGet() - retrieves the value of a key in a HashTable
 *  DESCRIPTION:
 *      Retrieves the value of the specified key in the specified HashTable.
 *      Uses the comparison function specified by
 *      HashTableSetKeyComparisonFunction().
 *  EFFICIENCY:
 *      O(1), assuming a good hash function and element-to-bucket ratio
 *  ARGUMENTS:
 *      hashTable    - the HashTable to search
 *      key          - the key whose value is desired
 *  RETURNS:
 *      void *       - the value of the specified key, or NULL if the key
 *                     doesn't exist in the HashTable
\*--------------------------------------------------------------------------*/

void * HashTableGetKey(const HashTable *hashTable, const void *key);
void * HashTableGet(const HashTable *hashTable, const void *key);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableRemove() - removes a key/value pair from a HashTable
 *  DESCRIPTION:
 *      Removes the key/value pair identified by the specified key from the
 *      specified HashTable if the key exists in the HashTable.  May trigger
 *      an auto-rehash (see HashTableSetIdealRatio()).
 *  EFFICIENCY:
 *      O(1), assuming a good hash function and element-to-bucket ratio
 *  ARGUMENTS:
 *      hashTable    - the HashTable to remove the key/value pair from
 *      key          - the key specifying the key/value pair to be removed
 *  RETURNS:
 *      <nothing>
\*--------------------------------------------------------------------------*/

void HashTableRemove(HashTable *hashTable, const void *key);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableRemoveAll() - removes all key/value pairs from a HashTable
 *  DESCRIPTION:
 *      Removes all key/value pairs from the specified HashTable.  May trigger
 *      an auto-rehash (see HashTableSetIdealRatio()).
 *  EFFICIENCY:
 *      O(n)
 *  ARGUMENTS:
 *      hashTable    - the HashTable to remove all key/value pairs from
 *  RETURNS:
 *      <nothing>
\*--------------------------------------------------------------------------*/

void HashTableRemoveAll(HashTable *hashTable);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableIsEmpty() - determines if a HashTable is empty
 *  DESCRIPTION:
 *      Determines whether or not the specified HashTable contains any
 *      key/value pairs.
 *  EFFICIENCY:
 *      O(1)
 *  ARGUMENTS:
 *      hashTable    - the HashTable to check
 *  RETURNS:
 *      bool         - whether or not the specified HashTable contains any
 *                     key/value pairs
\*--------------------------------------------------------------------------*/

int HashTableIsEmpty(const HashTable *hashTable);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableSize() - returns the number of elements in a HashTable
 *  DESCRIPTION:
 *      Returns the number of key/value pairs that are present in the
 *      specified HashTable.
 *  EFFICIENCY:
 *      O(1)
 *  ARGUMENTS:
 *      hashTable    - the HashTable whose size is requested
 *  RETURNS:
 *      long         - the number of key/value pairs that are present in
 *                     the specified HashTable
\*--------------------------------------------------------------------------*/

srInt_64 HashTableSize(const HashTable *hashTable);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableGetNumBuckets() - returns the number of buckets in a HashTable
 *  DESCRIPTION:
 *      Returns the number of buckets that are in the specified HashTable.
 *      This may change dynamically throughout the life of a HashTable if
 *      automatic or manual rehashing is performed.
 *  EFFICIENCY:
 *      O(1)
 *  ARGUMENTS:
 *      hashTable    - the HashTable whose number of buckets is requested
 *  RETURNS:
 *      long         - the number of buckets that are in the specified
 *                     HashTable
\*--------------------------------------------------------------------------*/

srInt_64 HashTableGetNumBuckets(const HashTable *hashTable);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableSetKeyComparisonFunction()
 *              - specifies the function used to compare keys in a HashTable
 *  DESCRIPTION:
 *      Specifies the function used to compare keys in the specified
 *      HashTable.  The specified function should return zero if the two
 *      keys are considered equal, and non-zero otherwise.  The default
 *      function is one that simply compares pointers.
 *  ARGUMENTS:
 *      hashTable    - the HashTable whose key comparison function is being
 *                     specified
 *      keycmp       - a function which returns zero if the two arguments
 *                     passed to it are considered "equal" keys and non-zero
 *                     otherwise
 *  RETURNS:
 *      <nothing>
\*--------------------------------------------------------------------------*/

void HashTableSetKeyComparisonFunction(HashTable *hashTable,
                             int (*keycmp)(const void *key1, const void *key2));

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableSetValueComparisonFunction()
 *              - specifies the function used to compare values in a HashTable
 *  DESCRIPTION:
 *      Specifies the function used to compare values in the specified
 *      HashTable.  The specified function should return zero if the two
 *      values are considered equal, and non-zero otherwise.  The default
 *      function is one that simply compares pointers.
 *  ARGUMENTS:
 *      hashTable    - the HashTable whose value comparison function is being
 *                     specified
 *      valuecmp     - a function which returns zero if the two arguments
 *                     passed to it are considered "equal" values and non-zero
 *                     otherwise
 *  RETURNS:
 *      <nothing>
\*--------------------------------------------------------------------------*/

void HashTableSetValueComparisonFunction(HashTable *hashTable,
                       int (*valuecmp)(const void *value1, const void *value2));

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableSetHashFunction()
 *              - specifies the hash function used by a HashTable
 *  DESCRIPTION:
 *      Specifies the function used to determine the hash value for a key
 *      in the specified HashTable (before modulation).  An ideal hash
 *      function is one which is easy to compute and approximates a
 *      "random" function.  The default function is one that works
 *      relatively well for pointers.  If the HashTable keys are to be
 *      strings (which is probably the case), then this default function
 *      will not suffice, in which case consider using the provided
 *      HashTableStringHashFunction() function.
 *  ARGUMENTS:
 *      hashTable    - the HashTable whose hash function is being specified
 *      hashFunction - a function which returns an appropriate hash code
 *                     for a given key
 *  RETURNS:
 *      <nothing>
\*--------------------------------------------------------------------------*/

void HashTableSetHashFunction(HashTable *hashTable,
                              srUInt_64 (*hashFunction)(const void *key));

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableRehash() - reorganizes a HashTable to be more efficient
 *  DESCRIPTION:
 *      Reorganizes a HashTable to be more efficient.  If a number of
 *      buckets is specified, the HashTable is rehashed to that number of
 *      buckets.  If 0 is specified, the HashTable is rehashed to a number
 *      of buckets which is automatically calculated to be a prime number
 *      that achieves (as closely as possible) the ideal element-to-bucket 
 *      ratio specified by the HashTableSetIdealRatio() function.
 *  EFFICIENCY:
 *      O(n)
 *  ARGUMENTS:
 *      hashTable    - the HashTable to be reorganized
 *      numOfBuckets - the number of buckets to rehash the HashTable to.
 *                     Should be prime.  Ideally, the number of buckets
 *                     should be between 1/5 and 1 times the expected
 *                     number of elements in the HashTable.  Values much
 *                     more or less than this will result in wasted memory
 *                     or decreased performance respectively.  If 0 is
 *                     specified, an appropriate number of buckets is
 *                     automatically calculated.
 *  RETURNS:
 *      <nothing>
\*--------------------------------------------------------------------------*/

void HashTableRehash(HashTable *hashTable, srInt_64 numOfBuckets);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableSetIdealRatio()
 *              - sets the ideal element-to-bucket ratio of a HashTable
 *  DESCRIPTION:
 *      Sets the ideal element-to-bucket ratio, as well as the lower and
 *      upper auto-rehash thresholds, of the specified HashTable.  Note
 *      that this function doesn't actually perform a rehash.
 *
 *      The default values for these properties are 3.0, 0.0 and 15.0
 *      respectively.  This is likely fine for most situations, so there
 *      is probably no need to call this function.
 *  ARGUMENTS:
 *      hashTable    - a HashTable
 *      idealRatio   - the ideal element-to-bucket ratio.  When a rehash
 *                     occurs (either manually via a call to the
 *                     HashTableRehash() function or automatically due the
 *                     the triggering of one of the thresholds below), the
 *                     number of buckets in the HashTable will be
 *                     recalculated to be a prime number that achieves (as
 *                     closely as possible) this ideal ratio.  Must be a
 *                     positive number.
 *      lowerRehashThreshold
 *                   - the element-to-bucket ratio that is considered
 *                     unacceptably low (i.e., too few elements per bucket).
 *                     If the actual ratio falls below this number, a
 *                     rehash will automatically be performed.  Must be
 *                     lower than the value of idealRatio.  If no ratio
 *                     is considered unacceptably low, a value of 0.0 can
 *                     be specified.
 *      upperRehashThreshold
 *                   - the element-to-bucket ratio that is considered
 *                     unacceptably high (i.e., too many elements per bucket).
 *                     If the actual ratio rises above this number, a
 *                     rehash will automatically be performed.  Must be
 *                     higher than idealRatio.  However, if no ratio
 *                     is considered unacceptably high, a value of 0.0 can
 *                     be specified.
 *  RETURNS:
 *      <nothing>
\*--------------------------------------------------------------------------*/

void HashTableSetIdealRatio(HashTable *hashTable, float idealRatio,
                            float lowerRehashThreshold,
                            float upperRehashThreshold);

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableSetDeallocationFunctions()
 *              - sets the key and value deallocation functions of a HashTable
 *  DESCRIPTION:
 *      Sets the key and value deallocation functions of the specified
 *      HashTable.  This determines what happens to a key or a value when it
 *      is removed from the HashTable.  If the deallocation function is NULL
 *      (the default if this function is never called), its reference is
 *      simply dropped and it is up to the calling program to perform the
 *      proper memory management.  If the deallocation function is non-NULL,
 *      it is called to free the memory used by the object.  E.g., for simple
 *      objects, an appropriate deallocation function may be free().
 *
 *      This affects the behaviour of the HashTableDestroy(), HashTablePut(),
 *      HashTableRemove() and HashTableRemoveAll() functions.
 *  ARGUMENTS:
 *      hashTable    - a HashTable
 *      keyDeallocator
 *                   - if non-NULL, the function to be called when a key is
 *                     removed from the HashTable.
 *      valueDeallocator
 *                   - if non-NULL, the function to be called when a value is
 *                     removed from the HashTable.
 *  RETURNS:
 *      <nothing>
\*--------------------------------------------------------------------------*/

void HashTableSetDeallocationFunctions(HashTable *hashTable,
                                       void (*keyDeallocator)(void *key),
                                       void (*valueDeallocator)(void *value));

/*--------------------------------------------------------------------------*\
 *  NAME:
 *      HashTableStringHashFunction() - a good hash function for strings
 *  DESCRIPTION:
 *      A hash function that is appropriate for hashing strings.  Note that
 *      this is not the default hash function.  To make it the default hash
 *      function, call HashTableSetHashFunction(HashTableStringHashFunction).
 *  ARGUMENTS:
 *      key    - the key to be hashed
 *  RETURNS:
 *      long   - the unmodulated hash value of the key
\*--------------------------------------------------------------------------*/

srUInt_64 HashTableStringHashFunction(const void *key);

void free_values_destroy(HashTable * tab);
int HashTablePutReplaceEx(HashTable *hashTable, const void *key, void *value, int replace_key, int dealloc_key, int dealloc_value);

ArrayList * HashTableSortedIndexes(HashTable * k2int_tab, int larger_value_first);

// NOTE: values are all added by 1. 
HashTable * ArrayListToLookupTable_Int(ArrayList * arr);

#endif /* _HASHTABLE_H */


