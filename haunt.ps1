param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$CommandArgs
)

$PythonExe = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
$ScriptPy  = Join-Path $PSScriptRoot "haunt.py"

& $PythonExe $ScriptPy @CommandArgs

