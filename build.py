import cffi
import re
import StringIO
from pcpp.preprocessor import Preprocessor


def main():
    ffibuilder = maker()
    ffibuilder.compile(verbose=True)


def maker():
    """ Make the ffibuilder object for parsing the bif.h header. """
    
    header_filename = "bif.h"
    
    header_contents = open(header_filename, 'r').read()
    
    source = """
    #define BIF_IMPLEMENTATION
    """ + header_contents
    
    defs = build_cdef(header_contents)
    
    ffibuilder = cffi.FFI()
    ffibuilder.cdef(defs)
    ffibuilder.set_source("_bif", source, libraries=[])
    return ffibuilder


def build_cdef(header_contents):
    header_only_options = """
    """
    preprocessed_text = run_c_preprocessor(header_only_options + header_contents)
    preprocessed_text = evaluate_shift(preprocessed_text)
    preprocessed_text = evaluate_or(preprocessed_text)
    write_debug_file(preprocessed_text, "cdef.h")
    return preprocessed_text


def run_c_preprocessor(header_contents):
    cpp = Preprocessor()
    cpp.parse(header_contents)
    output = StringIO.StringIO()
    cpp.write(output)
    return output.getvalue()


def evaluate_shift(preprocessed_text):
    shift_expr = "\\(1 << \\(([0-9]+)\\)\\)"
    def evaluate_shift(match):
        return str(1 << int(match.group(1)))
    return re.sub(shift_expr, evaluate_shift, preprocessed_text)


def evaluate_or(preprocessed_text):
    val_expr = "(bif|BIF)_[a-zA-Z0-9_]+"
    or_expr = "%s( *\\| *%s)+" % (val_expr, val_expr)
    def lookup_value(value_name):
        ret = 0
        assignment = re.search("%s *= *([^\n,]*)" % value_name, preprocessed_text)
        if assignment:
            value = assignment.group(1)
            if re.match(or_expr, value) or re.match(val_expr, value):
                ret = evaluate_or(value)
            else:
                ret = int(value, 0)
        else:
            raise Exception("Cannot find definition for value '%s'" % value_name)
        return ret
    def evaluate_or(expression_text):
        values = map(lambda x: lookup_value(x.strip()), expression_text.split("|"))
        return reduce(lambda x,y: x|y, values)
    def replace_or(match):
        return str(evaluate_or(match.group(0)))
    return re.sub(or_expr, replace_or, preprocessed_text)
    
    
def write_debug_file(contents, filename):
    open(filename, 'w').write(contents)


if __name__ == '__main__':
    main()