$allArgs = $PSBoundParameters.Values + $args

python .\src\main.py $allArgs
