import sys
import os
import subprocess
import io
import string
import pprint
import random
from enum import Enum


class BinsonType(Enum):
    BINSON_TYPE_UNKNOWN     = 0
    BINSON_TYPE_RANDOM      = 1
    BINSON_TYPE_NAME        = 2

    BINSON_TYPE_OBJECT      = 3
    BINSON_TYPE_ARRAY       = 4

    BINSON_TYPE_BOOLEAN     = 5
    BINSON_TYPE_INTEGER     = 6
    BINSON_TYPE_DOUBLE      = 7

    BINSON_TYPE_STRING      = 8
    BINSON_TYPE_BYTES       = 9

def str_hexencode(str):
    return ''.join(['\\x%02x' % c for c in str])


class PyFuzz():

    def __init__(self, level=1):
        self.binson_writer_txt = None
        self.binson_parser_txt = None

        if level <= 1:
            self.alphanum = True
            self.maxdepth = 8
            self.maxfields = 3
            self.namelen = 1
            self.strlen = 1
            self.byteslen = 1
        elif level == 2:
            self.alphanum = True
            self.maxdepth = 8
            self.maxfields = 4
            self.namelen = 5
            self.strlen = 5
            self.byteslen = 5
        elif level == 3:
            self.alphanum = True
            self.maxdepth = 5
            self.maxfields = 12
            self.namelen = 10
            self.strlen = 10
            self.byteslen = 10
        else:
            self.alphanum = False
            self.maxdepth = 6
            self.maxfields = 12
            self.namelen = 10
            self.strlen = 10
            self.byteslen = 10

    def gen_binson_item(self, btype, array_context=False):
    
        if array_context:
            print('binson_parser_next(&p);   ASSERT_FLAGS(&p);', file=self.binson_parser_txt)
    
        if btype == BinsonType.BINSON_TYPE_STRING:
            if self.alphanum:
                res = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(self.strlen))
            else:
                res = str_hexencode(os.urandom(self.strlen))

            print('binson_write_string( &w, "{:s}" ); ASSERT_FLAGS(&w);'.format(res), file=self.binson_writer_txt)
            print('assert(binson_parser_string_equals( &p, "{:s}" ));  ASSERT_FLAGS(&p);'.format(res), file=self.binson_parser_txt)
            return res
    
        if btype == BinsonType.BINSON_TYPE_NAME:
            if self.alphanum:
                res = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(self.namelen))
            else:
                res = str_hexencode(os.urandom(self.namelen))

            print('binson_write_name( &w, "{:s}" ); ASSERT_FLAGS(&w);'.format(res), file=self.binson_writer_txt)
            print('assert(binson_parser_field( &p, "{:s}" )); ASSERT_FLAGS(&p);'.format(res), file=self.binson_parser_txt)
            print('assert(binson_parser_name_equals( &p, "{:s}" )); ASSERT_FLAGS(&p);'.format(res), file=self.binson_parser_txt)
            return res
    
        elif btype == BinsonType.BINSON_TYPE_BYTES:
            if self.alphanum:
                res = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(self.byteslen))
            else:
                res = str_hexencode(os.urandom(self.byteslen))

            print('binson_write_bytes( &w, (const uint8_t *)"{:s}", {:d} ); ASSERT_FLAGS(&w);'.format(res, len(res)), file=self.binson_writer_txt)
            print('assert(binson_parser_get_bytes_len( &p ) == {} ); ASSERT_FLAGS(&p);'.format(len(res)), file=self.binson_parser_txt)
            return res
    
        elif btype == BinsonType.BINSON_TYPE_BOOLEAN:
            res = True if random.randint(0,1) == 1 else False
            print('binson_write_boolean( &w, {} ); ASSERT_FLAGS(&w);'.format(int(res)), file=self.binson_writer_txt)
            print('assert(binson_parser_get_boolean( &p ) == {} ); ASSERT_FLAGS(&p);'.format(int(res)), file=self.binson_parser_txt)
            return res
    
        elif btype == BinsonType.BINSON_TYPE_INTEGER:
            res = int(random.getrandbits(32))
            print('binson_write_integer( &w, {}L ); ASSERT_FLAGS(&w);'.format(int(res)), file=self.binson_writer_txt)
            print('assert(binson_parser_get_integer( &p ) == {}L ); ASSERT_FLAGS(&p);'.format(int(res)), file=self.binson_parser_txt)
            return res
    
        elif btype == BinsonType.BINSON_TYPE_DOUBLE:
            res = float(random.getrandbits(32))
            print('binson_write_double( &w, {} ); ASSERT_FLAGS(&w);'.format(float(res)), file=self.binson_writer_txt)
            print('assert(binson_parser_get_double( &p ) == {} ); ASSERT_FLAGS(&p);'.format(float(res)), file=self.binson_parser_txt)
            return res
        else:
            return None


    # binson_array ==  python_list
    # binson_object == python_dict
    def binson_gen(self, depth, btype=BinsonType.BINSON_TYPE_RANDOM, array_context=False):

        if depth > self.maxdepth:
            return None

        if btype == BinsonType.BINSON_TYPE_RANDOM:
            if depth == 0:
                btype = BinsonType.BINSON_TYPE_OBJECT
            elif depth == self.maxdepth-1:
                btype = BinsonType(random.randint(BinsonType.BINSON_TYPE_BOOLEAN.value, BinsonType.BINSON_TYPE_BYTES.value))
            else:
                btype = BinsonType(random.randint(BinsonType.BINSON_TYPE_OBJECT.value, BinsonType.BINSON_TYPE_BYTES.value))

        if btype == BinsonType.BINSON_TYPE_OBJECT:
            print('binson_write_object_begin( &w ); ASSERT_FLAGS(&w);', file=self.binson_writer_txt)

            print('binson_parser_go_into( &p ); ASSERT_FLAGS(&p);', file=self.binson_parser_txt)
            res = {}
            for _ in range(random.randint(0, self.maxfields)):
                k = self.gen_binson_item(BinsonType.BINSON_TYPE_NAME, array_context=False)
                v = self.binson_gen(depth=depth+1, btype=BinsonType.BINSON_TYPE_RANDOM, array_context=False)
                res[k] = v

            print('binson_write_object_end( &w ); ASSERT_FLAGS(&w);', file=self.binson_writer_txt)
            print('binson_parser_go_up( &p ); ASSERT_FLAGS(&p);', file=self.binson_parser_txt)
            return res

        elif btype == BinsonType.BINSON_TYPE_ARRAY:
            print('binson_write_array_begin( &w ); ASSERT_FLAGS(&w);', file=self.binson_writer_txt)

            print('binson_parser_go_into_array( &p ); ASSERT_FLAGS(&p);', file=self.binson_parser_txt)

            res = [self.binson_gen(depth=depth+1, btype=BinsonType.BINSON_TYPE_RANDOM, array_context=True)
                    for _ in range(random.randint(0, self.maxfields))]
            print('binson_write_array_end( &w ); ASSERT_FLAGS(&w);', file=self.binson_writer_txt)
            print('binson_parser_go_up( &p ); ASSERT_FLAGS(&p);', file=self.binson_parser_txt)
            return res

        else:
            return self.gen_binson_item(btype, array_context)


    def process_step(self, fileno):

        self.binson_writer_txt = io.StringIO()
        self.binson_parser_txt = io.StringIO()

        #print("Random composite object. BINSON_ENC_PYTHON")
        obj = self.binson_gen(depth=0, btype=BinsonType.BINSON_TYPE_RANDOM, array_context=False)
        #pprint.pprint(obj)



        #pprint.pprint(self.binson_writer_txt.getvalue())
        #pprint.pprint(self.binson_parser_txt.getvalue())

        try:
            os.mkdir('./build', 0o777)
            os.mkdir('./build/bin', 0o777)
        except:
            pass

        src_name = './build/{}.c'.format(fileno)
        out = open(src_name, 'w+')

        # include tree repr in C file's comment
        print("/*", file=out)
        comment = str(pprint.pformat(obj)).replace("*", "\\x2a")
        print(comment, file=out)
        print("*/\n", file=out)

        src_header = '''
    #include <stdint.h>
    #include <inttypes.h>
    #include <math.h>
    #include <stdio.h>
    #include <assert.h>
    #include <limits.h>
    
    #define MAX_DEPTH   16

void print_hex_byte(uint8_t src_byte)
{
    unsigned char _s2='0';
    char i=2;

    do {
        i--;
        _s2 = (unsigned char)  ((src_byte >> i*4 ) & 0x0f);
        if(_s2<10)
            _s2=_s2+48;
        else
            _s2=_s2+55;

        putchar(_s2);    
    } while(i);   
}

#define ASSERT_STR(x, y) \
      if (strcmp(x, y)) \
         { printf(" %s != %s ", x, y);  \
           assert(strcmp(x, y) == 0); }

#define ASSERT_FLAGS(x)  if ((x)->error_flags != BINSON_ID_OK) {printf("error_flags=%x, line=%d", (x)->error_flags, __LINE__); \
                      return ((x)->error_flags);}

    
    #include "binson_light.h"
    
    uint8_t buf[65534];
    uint8_t strbuf[65534];
    
    binson_writer w;
    binson_parser p;
    
    int main() {
         
    '''

        str_footer= '''
#ifdef WITH_TO_STRING
  binson_parser_reset(&p);
  binson_parser_to_string(&p, (uint8_t*)&strbuf, sizeof(strbuf), false);
  printf("%s", strbuf);
  //
#endif
'''
        out.write(src_header)
        print("\nbinson_writer_init( &w, buf, sizeof(buf) );", file=out)
        print("\n//writing", file=out)
        out.write(self.binson_writer_txt.getvalue())

  #      print("\nsetmode(fileno(stdout), O_BINARY); ", file=out)
        print("\nfwrite( buf, 1, binson_writer_get_counter(&w), stdout); ", file=out)


        print("\nbinson_parser_init( &p, buf, sizeof(buf) );", file=out)
        print("\n//parsing", file=out)
        out.write(self.binson_parser_txt.getvalue())

        #print("\n//_to_str", file=out)
        #out.write(str_footer);
        print("\nreturn 0;\n}", file=out)

        out.close()

        # build with gcc
        #gcc -I../../  -g -Os -std=c99 -Wall  ../../binson_light.c ./build/0.c -o build/0.out
        cmd = ["gcc", "-I../../",  "-DWITH_TO_STRING", "-g", "-std=c99", "-Wall",  "../../binson_light.c", "./build/" + str(fileno) + ".c",
              "-o./build/" + str(fileno) + ".o" ]
        p = subprocess.Popen(cmd)
        p.wait()

        self.binson_writer_txt.close()
        self.binson_parser_txt.close()

        out = "./build/bin/{}.bin".format(fileno)
        #p = subprocess.Popen("./build/{}.o".format(fileno), stdout=out)

        with open(out, 'w+') as f:
            subprocess.Popen(["./build/{}.o".format(fileno), 'R'], stdout=f, stderr=f)

        p.wait()
        if p.returncode == 0:
            print("\r\n=========================")
            print("random tree number: {}, maxdepth={}, maxfields={}".format(fileno, self.maxdepth, self.maxfields))
            try:
                os.remove("./build/{}.c".format(fileno))
                os.remove("./build/{}.o".format(fileno))
                pass
            except:
                pass
        else:
            print("./build/{}.o returned on exit '{:x}' "
                  .format(fileno, p.returncode))

            #print("./build/{}.o returned on exit '{:x} (error_flags={:x}, line={:d})', "
            #      .format(fileno, p.returncode, p.returncode & 0xff, p.returncode >> 8))



def main():
    fileno = 0
    opt = {}

    for arg in sys.argv[1:]:
        arg_dict = arg.split('=')
        opt.update({arg_dict[0]: arg_dict[1]})

    level = 1
    if 'level' in opt:
        level = opt['level']

    print("PyFuzzing level: {}\n".format(level))

    fuzz = PyFuzz(level=int(level))

    while True:
        fuzz.process_step(fileno)
        fileno += 1

if __name__ == '__main__':
    main()
    exit(0)
