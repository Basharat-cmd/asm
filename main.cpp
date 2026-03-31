#include <iostream>
#include <string>
#include <array>
#include <stack>
#include <sstream>
#include <cstdio>
#include <memory>
#include <unordered_map>
std::stack<std::string> _stack;
std::unordered_map<std::string, std::string> __vars_;
 
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


void handle_stack(bool _if, std::string __v_){
    
    if (__v_ != ""){
        if (_if){
        _stack.push(__vars_[__v_]);
        } else {
            __vars_[__v_] = _stack.top();
            _stack.pop();
        }
    } else if (_if){
        _stack.push(__vars_["_1"]);
        _stack.push(__vars_["_2"]);
        _stack.push(__vars_["_3"]);
        _stack.push(__vars_["_4"]); 
        _stack.push(__vars_["_5"]); 
        _stack.push(__vars_["_6"]); 
        _stack.push(__vars_["_7"]); 
        _stack.push(__vars_["_8"]); 
        _stack.push(__vars_["_9"]); 
        _stack.push(__vars_["_10"]); 
        _stack.push(__vars_["_return"]);
    } else {
        if (_stack.size() >= 3) {
            __vars_["_return"] = _stack.top();
            _stack.pop();
            __vars_["_10"] = _stack.top();
            _stack.pop();
            __vars_["_9"] = _stack.top();
            _stack.pop();
            __vars_["_8"] = _stack.top();
            _stack.pop();
            __vars_["_7"] = _stack.top();
            _stack.pop();
            __vars_["_6"] = _stack.top();
            _stack.pop();
            __vars_["_5"] = _stack.top();
            _stack.pop();
            __vars_["_4"] = _stack.top();
            _stack.pop();
            __vars_["_3"] = _stack.top();
            _stack.pop() ;
            __vars_["_2"] = _stack.top();
            _stack.pop();
            __vars_["_1"] = _stack.top();
            _stack.pop();
        } else {
            std::cerr << "Stack underflow!";
        }
    }
}
    

void __isNumber_(const std::string& __s_) {
    if (__s_.empty()){ __vars_["_return"] = "0"; return; }

    std::istringstream __iss_(__s_);
    double __val_;
    char __extra_;

    // Try to read a number and ensure there's nothing extra left
    if (!(__iss_ >> __val_)){ __vars_["_return"] = "0"; return; }
    if (__iss_ >> __extra_) {__vars_["_return"] = "0"; return; }

    __vars_["_return"] = "1";
}

void __add_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_["_return"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_["_return"] == "1") {
        __num2_ = std::stod(__b_);
    }

    double __sum_ = __num1_ + __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_["_return"] = __oss_.str();
}




void __sub_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_["_return"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_["_return"] == "1") {
        __num2_ = std::stod(__b_);
    }

    double __sum_ = __num1_ - __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_["_return"]= __oss_.str();
}




void __mul_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_["_return"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_["_return"] == "1") {
        __num2_ = std::stod(__b_);
    }

    double __sum_ = __num1_ * __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_["_return"] = __oss_.str();
}




void __div_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 1.0;
    
    __isNumber_(__a_);

    if (__vars_["_return"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_["_return"] == "1") {
        __num2_ = std::stod(__b_);
    }

    double __sum_ = __num1_ / __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_["_return"] = __oss_.str();
}




void __cmp_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_["_return"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_["_return"] == "1") {
        __num2_ = std::stod(__b_);
    }

    int __sum_ = __num1_ == __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_["_return"] = __oss_.str();
}




void __gtn_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_["_return"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_["_return"] == "1") {
        __num2_ = std::stod(__b_);
    }

    int __sum_ = __num1_ > __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_["_return"] = __oss_.str();
}




void __ltn_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_["_return"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_["_return"] == "1") {
        __num2_ = std::stod(__b_);
    }

    int __sum_ = __num1_ < __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_["_return"] = __oss_.str();
}




void __gte_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_["_return"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_["_return"] == "1") {
        __num2_ = std::stod(__b_);
    }

    int __sum_ = __num1_ >= __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_["_return"] = __oss_.str();
}




void __lte_(std::string __a_, std::string __b_) {
    double __num1_ = 0.0;
    double __num2_ = 0.0;
    
    __isNumber_(__a_);

    if (__vars_["_return"] == "1") {
        __num1_ = std::stod(__a_);
    }
    __isNumber_(__b_);
    if (__vars_["_return"] == "1") {
        __num2_ = std::stod(__b_);
    }

    int __sum_ = __num1_ <= __num2_;

    std::ostringstream __oss_;

    __oss_ << __sum_;

    __vars_["_return"] = __oss_.str();
}


int main(){
goto start;
/*label*/start:
__vars_["_1"]="Basharat";
__vars_["a"]="hi";
/*label_goto*/goto greet;
/*label*/_greet_end:
std::cout << "a = " << __vars_["a"];
std::cout<<std::endl;
end:
return 0;
/*label*/greet:
handle_stack(true, "a");
__vars_["a"]=__vars_["_1"];
handle_stack(true, "");
std::cout << "Hello " << __vars_["a"];
handle_stack(false, "");
handle_stack(false, "a");
std::cout<<std::endl;
/*label_goto*/goto _greet_end;
return 0;}