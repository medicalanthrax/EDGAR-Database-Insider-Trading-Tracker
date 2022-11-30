#to prevent Nonetype errors when calling .text
def text(field):
	if field != None: return field.text
	return "N/A"