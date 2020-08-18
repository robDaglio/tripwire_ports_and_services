# | ========== parameters =========== |
param (
    [Parameter(Mandatory=$true)][String]$ci_function,
    [Parameter(Mandatory=$true)][String]$excel_file,
    [Parameter(Mandatory=$true)][String]$output_directory,
    [String]$s_name
)

$node_data = New-Object -TypeName psobject
$node_data | Add-Member -MemberType NoteProperty -Name ci_function -Value $null
$node_data | Add-Member -MemberType NoteProperty -Name protocol -Value $null
$node_data | Add-Member -MemberType NoteProperty -Name port -Value $null
$node_data | Add-Member -MemberType NoteProperty -Name service -Value $null
$node_data | Add-Member -MemberType NoteProperty -Name description -Value $null
$node_data | Add-Member -MemberType NoteProperty -Name justification -Value $null
$node_data | Add-Member -MemberType NoteProperty -Name documentation -Value $null

function create_output_file {
    # create output file
    $remove_path = $excel_file.SubString($excel_file.LastIndexOf("\") + 1)
    $output_file_name = "$($output_directory)\$($remove_path -Replace 'xlsx', 'csv')"
    
    return $output_file_name
}

# | ========== variables =========== |

# Create a new excel COM object
$excel_object = New-Object -com Excel.Application
$wb = $excel_object.workbooks.open($(Resolve-Path $excel_file))

# Default sheet name if not provided
if (!$s_name) {
    $sheet = $wb.Worksheets.Item("Ports and Services")
} else {
    $sheet = $wb.Worksheets.Item($s_name)
}

# get number of rows in document
$row_max = ($sheet.UsedRange.Rows).Count

# | ========== Execution =========== |

# Format output file name
$output_file_name = create_output_file
$csv_file = new-item -type file $output_file_name
Add-Content -Path $csv_file -Value "## Authorized Ports for CIFunction - $($ci_function)"

# Check for defects and read cell data
for ($i = 17; $i -le $row_max; $i++) {
    $new_object = $node_data | Select-Object *
    
    if ($new_object.protocol = $sheet.Cells.Item($i, 4).Text){
        $new_object.ci_function = $ci_function
        $new_object.protocol = $sheet.Cells.Item($i, 4).Text
        
        # Port annotation defect "*", "ALL","x.x"
        $new_object.port = $sheet.Cells.Item($i, 3).Text
            if (($new_object.port -eq "*") -or ($new_object.port -eq "ALL")){
                $new_object.port = "0-65535"
            }
            if ($new_object.port.contains(".")){
                $new_object.port = $new_object.port -replace "\.", "-"
            }
        
        # Unterminated double quotes
        $new_object.service = $sheet.Cells.Item($i, 2).Text
        $new_object.description = $sheet.Cells.Item($i, 6).Text
            if ($new_object.description.contains('"')){
                $new_object.description = $new_object.description -replace '"', ''
            }
        $new_object.justification = $sheet.Cells.Item($i, 7).Text
            if ($new_object.justification.contains('"')){
                $new_object.justification = $new_object.justification -replace '"', ''
            }
        $new_object.documentation = $sheet.Cells.Item($i, 9).Text
            if ($new_object.documentation.contains('"')){
                $new_object.documentation = $new_object.documentation -replace '"', ''
            }

        $data = "$($new_object.ci_function), $($new_object.protocol), $($new_object.port), $($new_object.service), ""$($new_object.description)"", ""$($new_object.justification)"", ""$($new_object.documentation)"""
        Add-Content -Path $csv_file -Value $data
    }
}

# Quit out of the excel COM object instance
$excel_object.Quit()

write-host("[+] Processed $($excel_file)")