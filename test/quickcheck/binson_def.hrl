-define(MAX_BINSON_SIZE, 16#FFFF).

-define(BOUND8,  (1 bsl 7)).
-define(BOUND16, (1 bsl 15)).
-define(BOUND32, (1 bsl 31)).

-define(BEGIN_OBJ,  16#40). %%64
-define(END_OBJ,    16#41). %%65
-define(BEGIN_ARR,  16#42). %%66
-define(END_ARR,    16#43). %%67
-define(TRUE,       16#44). %%68
-define(FALSE,      16#45). %%69
-define(DOUBLE,     16#46). %%70
-define(INT8,       16#10). %%16
-define(INT16,      16#11). %%17
-define(INT32,      16#12). %%18
-define(INT64,      16#13). %%19
-define(STR_LEN8,   16#14). %%20
-define(STR_LEN16,  16#15). %%21
-define(STR_LEN32,  16#16). %%22
-define(BYTE_LEN8,  16#18). %%24
-define(BYTE_LEN16, 16#19). %%25
-define(BYTE_LEN32, 16#1a). %%26

-define(BINSON_ID_OK,        16#00).
-define(BINSON_ID_BUF_FULL,  16#F0).
