#include <assert.h>
#include <string.h>
#include "binson_parser.h"

/*
{
  "BBS1FFFFFFFFFFFFFFFFFFFFFFFFFFF3 d FFFFFFFFF F3  ?FFFFFF FFFFFFFFF??????FFF??????FF[?FFFF": 1.0347915464784313E10
}
*/
int main(void)
{
    uint8_t binson_bytes[163] = "\x40\x15\x95\x00\x42\x42\x53\x7f\x31\x12\x12\x12\x12\x12\x12\x12\x12\x16\x7f\x12\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x33\x14\x00\x14\x64\x00\x12\x1b\x46\x46\x46\x46\x46\x46\x46\x46\x46\x14\x01\x20\x46\x33\x14\x00\x14\x00\xef\xbf\xbd\x12\x1b\x46\x46\x46\x46\x46\x46\x7f\x00\x46\x46\x46\x46\x46\x46\x46\x46\x46\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xb5\x80\x3f\x46\x46\x46\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\x7f\xef\xbf\xbd\xef\xbf\xbd\x46\x14\x46\x5b\x3f\x46\x46\x46\x46\x46\x46\x46\x46\x46\x45\x46\x03\x42\x41";
    BINSON_PARSER_DEF(p);
    double dval; (void) dval;
    int64_t intval; (void) intval;
    bool boolval; (void) boolval;
    bbuf *rawval; (void) rawval;
    assert(binson_parser_init(&p, binson_bytes, sizeof(binson_bytes)));
    assert(binson_parser_verify(&p));
    assert(p.error_flags == BINSON_ID_OK);
    assert(binson_parser_go_into_object(&p));
    assert(p.error_flags == BINSON_ID_OK);
    assert(binson_parser_field_ensure_with_length(&p, "\x42\x42\x53\x7f\x31\x12\x12\x12\x12\x12\x12\x12\x12\x16\x7f\x12\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x46\x33\x14\x00\x14\x64\x00\x12\x1b\x46\x46\x46\x46\x46\x46\x46\x46\x46\x14\x01\x20\x46\x33\x14\x00\x14\x00\xef\xbf\xbd\x12\x1b\x46\x46\x46\x46\x46\x46\x7f\x00\x46\x46\x46\x46\x46\x46\x46\x46\x46\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xb5\x80\x3f\x46\x46\x46\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\x7f\xef\xbf\xbd\xef\xbf\xbd\x46\x14\x46\x5b\x3f\x46\x46\x46\x46", 149, BINSON_TYPE_DOUBLE));
    assert(p.error_flags == BINSON_ID_OK);
    dval = binson_parser_get_double(&p);
    assert(p.error_flags == BINSON_ID_OK);
    assert(dval == 1.0347915464784313E10);
    assert(!binson_parser_next(&p));
    assert(binson_parser_leave_object(&p));
    assert(p.error_flags == BINSON_ID_OK);
    return 0;
}

