import re
import os
import sys

"""
import file f

:start
$_1 = "test.txt"
goto _f_read_file
:_f__read_file_end
"content of $"test.txt$": $_return"
:end
"""

def escape_handler(s: str, lineno):
    i = 0
    literal = ""
    parts = []

    def flush_literal():
        nonlocal literal
        if literal != "":
            parts.append(f'"{literal}"')
            literal = ""

    while i < len(s):
        c = s[i]

        if c != '$':
            literal += c
            i += 1
            continue

        i += 1
        if i >= len(s):
            print(lineno)
            print("error")
            return

        c = s[i]

        # === ESCAPES ===
        if c == '$':
            literal += '$'
            i += 1

        elif c == '"':
            literal += r'\"'
            i += 1

        elif c == "'":
            literal += r"\'"
            i += 1

        elif c == '\\':
            literal += r'\\'
            i += 1

        # === VARIABLE ===
        elif c.isalpha() or c == '_':
            flush_literal()

            start = i
            while i < len(s) and (s[i].isalnum() or s[i] == '_'):
                i += 1

            var_name = s[start:i]

            if var_name == "":
                print("error")
                return

            parts.append("__vars_[\"" + var_name + "\"]")

        else:
            print("error")
            return

    flush_literal()

    # remove any accidental empty entries (extra safety)
    parts = [p for p in parts if p != ""]

    if not parts:
        print("error")
        return
    # << __vars_[\"name\"]
    return " << ".join(parts)


def main():
    filename = ""
    header_file = False
    store_imports = []
    end_labels = []
    used_end_labels = []
    try:
        filename = sys.argv[1]
        header_file = True if sys.argv[2] == "-c" else False
    except:
        print(sys.argv)
    code = ""
    with open(filename, "r") as ff:
        code = ff.read()

    stack_func = """
void handle_stack(bool _if, std::string __v_){
    
    if (__v_ != ""){
        if (_if){
        _stack.push(__vars_[__v_]);
        } else {
            __vars_[__v_] = _stack.top();
            _stack.pop();
        }
    } else if (_if){
        _stack.push(__vars_[\"_1\"]);
        _stack.push(__vars_[\"_2\"]);
        _stack.push(__vars_[\"_3\"]);
        _stack.push(__vars_[\"_4\"]); 
        _stack.push(__vars_[\"_5\"]); 
        _stack.push(__vars_[\"_6\"]); 
        _stack.push(__vars_[\"_7\"]); 
        _stack.push(__vars_[\"_8\"]); 
        _stack.push(__vars_[\"_9\"]); 
        _stack.push(__vars_[\"_10\"]); 
        _stack.push(__vars_[\"_return\"]);
    } else {
        if (_stack.size() >= 3) {
            __vars_[\"_return\"] = _stack.top();
            _stack.pop();
            __vars_[\"_10\"] = _stack.top();
            _stack.pop();
            __vars_[\"_9\"] = _stack.top();
            _stack.pop();
            __vars_[\"_8\"] = _stack.top();
            _stack.pop();
            __vars_[\"_7\"] = _stack.top();
            _stack.pop();
            __vars_[\"_6\"] = _stack.top();
            _stack.pop();
            __vars_[\"_5\"] = _stack.top();
            _stack.pop();
            __vars_[\"_4\"] = _stack.top();
            _stack.pop();
            __vars_[\"_3\"] = _stack.top();
            _stack.pop() ;
            __vars_[\"_2\"] = _stack.top();
            _stack.pop();
            __vars_[\"_1\"] = _stack.top();
            _stack.pop();
        } else {
            std::cerr << "Stack underflow!";
        }
    }
}
    """
    system_func = """ 
std::string exec(const std::string& __cmd_) {
    std::array<char, 128> __buffer_;
    std::string __result_;
    // Open pipe to file
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(__cmd_.c_str(), "r"), pclose);
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    // Read till end of process:
    while (fgets(__buffer_.data(), __buffer_.size(), pipe.get()) != nullptr) {
        __result_ += __buffer_.data();
    }
    return __result_;
}
"""

    add_func = """
void __isNumber_(const std::string& __s_) {
    if (__s_.empty()){ __vars_[\"_return\"] = "0"; return; }

    std::istringstream __iss_(__s_);
    double __val_;
    char __extra_;

    // Try to read a number and ensure there's nothing extra left
    if (!(__iss_ >> __val_)){ __vars_[\"_return\"] = "0"; return; }
    if (__iss_ >> __extra_) {__vars_[\"_return\"] = "0"; return; }

    __vars_[\"_return\"] = "1";
}

void __add_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_[\"_return\"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_[\"_return\"] == "1") {
        __num2_ = std::stod(__b_);
    }

    double __sum_ = __num1_ + __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_[\"_return\"] = __oss_.str();
}

"""


    sub_func = """

void __sub_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_[\"_return\"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_[\"_return\"] == "1") {
        __num2_ = std::stod(__b_);
    }

    double __sum_ = __num1_ - __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_[\"_return\"]= __oss_.str();
}

"""

    mul_func = """

void __mul_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_[\"_return\"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_[\"_return\"] == "1") {
        __num2_ = std::stod(__b_);
    }

    double __sum_ = __num1_ * __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_[\"_return\"] = __oss_.str();
}

"""



    div_func = """

void __div_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 1.0;
    
    __isNumber_(__a_);

    if (__vars_[\"_return\"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_[\"_return\"] == "1") {
        __num2_ = std::stod(__b_);
    }

    double __sum_ = __num1_ / __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_[\"_return\"] = __oss_.str();
}

"""


    gtn_func = """

void __gtn_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_[\"_return\"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_[\"_return\"] == "1") {
        __num2_ = std::stod(__b_);
    }

    int __sum_ = __num1_ > __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_[\"_return\"] = __oss_.str();
}

"""

    ltn_func = """

void __ltn_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_[\"_return\"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_[\"_return\"] == "1") {
        __num2_ = std::stod(__b_);
    }

    int __sum_ = __num1_ < __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_[\"_return\"] = __oss_.str();
}

"""

    gte_func = """

void __gte_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_[\"_return\"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_[\"_return\"] == "1") {
        __num2_ = std::stod(__b_);
    }

    int __sum_ = __num1_ >= __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_[\"_return\"] = __oss_.str();
}

"""

    lte_func = """

void __lte_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_[\"_return\"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_[\"_return\"] == "1") {
        __num2_ = std::stod(__b_);
    }

    int __sum_ = __num1_ <= __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_[\"_return\"] = __oss_.str();
}

"""

    cmp_func = """

void __cmp_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_[\"_return\"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_[\"_return\"] == "1") {
        __num2_ = std::stod(__b_);
    }

    int __sum_ = __num1_ == __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_[\"_return\"] = __oss_.str();
}

"""

    result = [
            "#include <iostream>", 
            "#include <string>", 
            "#include <array>",
            "#include <stack>",
            "#include <sstream>",
            "#include <cstdio>", 
            "#include <memory>",
            "#include <unordered_map>",
            "std::stack<std::string> _stack;",
            "std::unordered_map<std::string, std::string> __vars_;",
            system_func,
            stack_func,
            add_func,
            sub_func,
            mul_func,
            div_func,
            cmp_func,
            gtn_func,
            ltn_func,
            gte_func,
            lte_func,
            "int main(){",
            "goto start;"
            ]
    if header_file:
        result = []
    last = "return 0;}"

    c_keywords = {
    "auto","break","case","char","const","continue","default","do","double",
    "else","enum","extern","float","for","goto","if","inline","int","long",
    "register","restrict","return","short","signed","sizeof","static","struct",
    "switch","typedef","union","unsigned","void","volatile","while","_Bool",
    "_Complex","_Imaginary", "std", "endl"
    }

    id_v = lambda s: bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", s)) and s not in c_keywords

    for lineno, line in enumerate(code.split("\n"), start=1):
        line = line.strip()   
        n = '\n'
        
        if line=="" or not line or line==n or line.startswith(";"):
            pass
        elif line == ":end":
            result.append("end:")
            result.append("return 0;")
        elif line == "endl":
            result.append("std::cout<<std::endl;")
        elif line.startswith(":"):
            lb = line[1:]
            print("asds" + lb)
            if lb.endswith("_end"):
                print("hate:" + lb)
                end_labels.append(lb)
            if id_v(lb):
                result.append(f"/*label*/{lb}:")
            else:
                print(f"Error invalid identifier label :{lb}")
        elif line.startswith("goto"):
            ln = line[4:-1]
            result.append(f"/*label_goto*/{line};")
        elif line.startswith("\""):
            s = line[1:-1]
            s = escape_handler(s, lineno)
            result.append("std::cout << " + s + ";")
        elif line.startswith("$"):
            vn, vl = line.split("=", 1)
            vn = vn[1:].strip()
            vl = vl.strip()
            result.append("__vars_[\"" + vn + "\"]" + "=" + escape_handler(vl[1:-1],lineno)+";")
        elif line == "ontrue":
            result.append("if (__flag_ == \"1\")")
        elif line == "onfalse":
            result.append("if (__flag_ == \"0\")")
        elif line.startswith("system"):
            c = line[6:]
            c = c.strip()
            c = escape_handler(c[1:-1], lineno)
            result.append("__vars_[\"_system_output\"] = exec(" + c + ")")

        elif line.startswith("push"):
            a = line[4:].strip()
            if a.startswith("$"):
                result.append("handle_stack(true, \""+a[1:]+"\");")
            else:
                result.append("handle_stack(true, \"\");")
        elif line.startswith("pop"):
            a = line[4:].strip()
            if a.startswith("$"):
                result.append("handle_stack(false, \""+a[1:]+"\");")
            else:
                result.append("handle_stack(false, \"\");")
        elif line.startswith("input"):
            vn = line[5:].strip()
            vn = vn[1:].strip()
            result.append("std::cin >> " + "__vars_[\"" + vn + "\"]" + ";")

        elif line.startswith("__"):
            c = line[:6]
            a = line[6:].strip()
            v1, v2 = a.split(",", 1)
            v1 = v1.strip()
            v2 = v2.strip()
            v1 = "__vars_[\"" + v1[1:].strip() + "\"]"
            v2 = "__vars_[\"" + v2[1:].strip() + "\"]"
            result.append(c + "(" + v1 + "," + v2 + ");")
        elif line == "__version_":
            result.append("__vars_[\"return\"] = \"alpha snapshot Aw1a\";")
        elif line.startswith("import"):
            line = line[6:].strip()
            fname, falies = line.split(" ", 1)
            fname = fname.strip()
            falies = falies.strip()
            fcon = ""
            fresult = []
            try:
                with open(fname+".a","r") as ff:
                    fcon = ff.read()
            except FileNotFoundError:
                print(f"Error Imported File not found \"{fname}.a\"")
            if fcon:
                for l in fcon.split("\n"):
                    if l=="" or not l or l==n or l.startswith(";"):
                        pass
                    elif l.startswith("/*label*/"):
                        flname = l[9:-1]
                        flname = "_" + falies + "_" + flname
                        fresult.append("/*label*/"+flname+":")
                    elif l.startswith("/*label_goto*/goto"):

                        flname = l[18:-1].strip()
                        flname = "_" + falies + "_" + flname
                        fresult.append("/*label_goto*/goto "+flname+";")
                        if l.endswith("_end;"):
                            used_end_labels.append(flname)
                    else:
                        fresult.append(l)
                store_imports.append("\n".join(fresult))

        else:
            print(f'unknown command "{line}"')

    s_store_imports = "\n".join(store_imports)
    result.append(s_store_imports)

    set_end_labels = set(end_labels)
    set_used_end_labels = set(used_end_labels)
    need_labels = set_used_end_labels - set_end_labels
    for lls in list(need_labels):
        result.append(lls+":")
    result.append(last if not header_file else "")
    filename = filename.replace(".as", "")
    with open(filename +".a" if header_file else filename+".cpp", "w") as fff:
        fff.write("\n".join(result))

if __name__ == '__main__':
    main()


