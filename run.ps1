$allArgs = $PSBoundParameters.Values + $args

python -O .\src\main.py $allArgs
