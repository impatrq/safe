def whatColor(variable):
    if variable == "BAJO" or variable == "Low" or variable == "SEGURO":
        return "success-dark"
    elif variable == "MEDIO" or variable == "Medium":
        return "warning" 
    elif variable == "ALTO" or variable == "High" or variable == "NO SEGURO":
        return "danger-dark"

    