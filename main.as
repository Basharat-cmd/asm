:start
$_1 = "Basharat"
$a = "hi"
goto greet
:_greet_end
"a = $a"
endl
:end

:greet
push $a
$a = "$_1"
push
"Hello $a"
pop
pop $a
endl
goto _greet_end
