#!python

def clean(ci_function, child_list):
    # Clean up service data
    if "WIN" in ci_function: service = f"{str(child_list[0])}.exe"
    else: service =  str(child_list[0])

    # Spelling Corrections
    if child_list[0] == "PowerShell Server.exe" or child_list[0] == "PowerShell Server":
        service = "PowerShellServer.exe"
    
    # Child Services (svchost)
    # if child_list[1] == 135: service = "!(RpcSs)" # note: svchost and rpcSs are listed
    if child_list[1] == 123: service = "!(W32Time)" # ntp.exe
    if child_list[1] == 500: service = "!(IKEEXT)" # IPsec ISAKMP.exe
    if child_list[1] == 4500: service = "!(IKEEXT)" # IPsec Network Address Translator Traversal NAT-T.exe
    if child_list[0] == "TermService" or child_list[0] == "TermService.exe": # TermService.exe
        service = "!(TermService)"
    if child_list[1] == "5353-5355" or child_list[1] == 5353 or child_list[1] == 5355:
        service = "!(Dnscache)"
    if child_list[1] == 49668: service = "!(SessionEnv)" # SessionEnv.exe
    if child_list[1] == 49665: service = "!(EventLog)" # EventLog.exe
    if child_list[1] == 58324: service = "!(PolicyAgent)" # PolicyAgent.exe
    
    # Child Services (System)
    if child_list[1] == 137: service = "!(netbios-ns)" # netbios-ns.exe
    if child_list[1] == 138: service = "!(netbios-dgm)" # netbios-dgm.exe 
    if child_list[1] == 139: service = "!(netbios-ssn)" # netbios-ssn.exe
    if child_list[1] == 445: service = "!(microsoft-ds)" # microsoft-ds.exe (SMB)
    if child_list[1] == 5985: service = "!(WinRM)" # WinRM.exe
    if child_list[1] == 47001: service = "!(WinRM)" # WinRM.exe
    # if child_list[1] == 8443: service = "!(?)"
    
    # Clean up port data
    if child_list[1] == "*" or child_list[1] == "ALL": port = "0-65535"
    elif "." in str(child_list[1]): port = str(child_list[1].replace(".", "-"))
    elif " " in str(child_list[1]): port = str(child_list[1].replace(" ", ""))
    else: port = str(child_list[1])

    # Clean up description data
    if '"' in child_list[4]: description = child_list[4].replace('"', '')
    elif "," in child_list[4]: description = child_list[4].replace(",", "")
    elif "'" in child_list[4]: description = child_list[4].replace("'", '')
    else: description = child_list[4]

    # Clean up justification data
    if '"' in child_list[5]: justification = child_list[5].replace('"', '')
    elif "," in child_list[5]: justification = child_list[5].replace(",", "")
    elif "'" in child_list[5]: justification = child_list[5].replace("'", '')
    else: justification = child_list[5]

    # Clean up documentation data
    if '"' in child_list[7]: documentation = child_list[7].replace('"', '')
    elif "," in child_list[7]: documentation = child_list[7].replace(",", "")
    elif "'" in child_list[7]: documentation = child_list[7].replace("'", '')
    else: documentation = child_list[7]
    
    # Clean up page number data
    if '"' in str(child_list[8]): page_numbers = "page(s) " + str(child_list[8].replace('"', ''))
    elif "'" in str(child_list[8]): page_numbers = "page(s) " + str(child_list[8].replace("'", ''))
    else: page_numbers = "page(s) " + str(child_list[8]) 
            
    raw = [
        service,        # service (child_list[0])
        port,           # port (child_list[1])
        child_list[2],  # protocol
        description,    # description (child_list[4])
        justification,  # justification (child_list[5])
        documentation,  # documentation (child_list[7])
        page_numbers,   # page numbers (child_list[8])
]

    return [x.replace("\n", "") for x in raw]

def sort_pas_data(mapped_data):
    relevant_data = dict()
    
    for ci_function, parent_list in mapped_data.items():
        new_parent_list = list()
        for child_list in parent_list:
            new_child_list = clean(ci_function, child_list)
            new_parent_list.append(new_child_list)
        relevant_data[ci_function] = new_parent_list

    return relevant_data

# TODO: duplicates





            
