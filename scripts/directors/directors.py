import csv

year             = 2017
fn               = "ReceiptExport.csv"
active_members   = "active.csv" 
inactive_members = "inactive.csv"
output_file      = "candidates_%d.html" %year
template         = """

<table border="1" frame="above">
    <tbody>
        <tr valign="middle"  style="background : #eff8fd">
            <td style="border: 0px; width:100px"><img style="width: 100px; float: left; margin-right: 10px; margin-left: 10px;" src="%s" alt="" /></td>
            <td style="border: 0px; width:200px; margin-top: 0px; margin-right: 10px; margin-bottom: 5px; margin-left: 10px; outline-width: 0px; outline-style: initial; outline-color: initial; line-height: 18px; padding: 0px;">
                <p><strong><a href="%s" target="_blank">%s</a></strong></p>
                <address>%s</address>
                <address>%s<br />%s<br />%s</address>
            </td>
            <td style="width:400px; border: 0px; margin-top: 0px; margin-right: 0px; margin-bottom: 5px; margin-left: 0px; outline-width: 0px; outline-style: initial; outline-color: initial; line-height: 18px; padding: 0px;">
                <p>%s</p>
            </td>
        </tr>
    </tbody>
</table>
<table border="1" frame="below">
    <tbody>
        <tr>
            <td style="border: 0px; width: 10px; float: left; margin-right: 10px; margin-left: 10px;">&nbsp;</td>
            <td style="border: 0px; margin-top: 0px; margin-right: 0px; margin-bottom: 1px; margin-left: 0px; outline-width: 0px; outline-style: initial; outline-color: initial; line-height: 18px; padding: 0px;">
                <p><h2>Motivation:</h2>&nbsp;%s</p>
                <p>%s</p>
                <p>%s</p>
            </td>
        </tr>
    </tbody>
</table>
"""

out        = open(output_file, "w")
body       = ""
candidates = {}

with open(fn, 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    
    for row in reader:
        candidates["%s %s" %(row['Last Name'].title(), row['First Name'].title())] = row

    ordered = []
    for n in candidates.keys():
        ordered.append(n)
    ordered.sort()

with open(active_members, 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        
    for row in reader:
        name = "%s %s" %(row['Last Name'].title(), row['First Name'].title())
        if candidates.has_key(name):
            for key in ['Group', 'City', 'Institution', 'Country']:
                candidates[name][key] = row[key].title()

with open(inactive_members, 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        
    for row in reader:
        name = "%s %s" %(row['Last Name'].title(), row['First Name'].title())
        if candidates.has_key(name):
            for key in ['Group', 'City', 'Institution', 'Country']:
                candidates[name][key] = row[key].title()

for surname in ordered:
    
    row  = candidates[surname]
    name = row['First Name'] + " " + row['Last Name']
        
    ## SHOULD BE RETRIEVED FROM VALID MEMBERS
    if row.has_key('Country'):
        addr1 =  row['Institution']
        addr2 =  row['City']
        addr3 =  row['Country']
        memb  =  row['Group']
    else:
        print surname, "is not a valid member: details should be manually provided"
        addr1 = ''
        addr2 = ''
        addr3 = ''
        memb  =  ''
            
    info = row['Biography']
    mot  = row['Motivation']          
    oth  = row['Other activities']
    if len(oth)>1:
        oth = '<h2>Other information:</h2>&nbsp;%s'%oth
                        
    att = row['Attend CNS']
    if att == 'none':
        att = '0'
            
    rev  = ", was reviewer for %s meetings"%row['Review CNS'] if row['Review CNS'] != "none" else ""
    year = row['Member start']
           
    particip = "<h2>OCNS and CNS participation:</h2> attended %s CNS meeting(s)%s. OCNS member since %s."%(att, rev, year)
                    
    pic = row['File Attachment']            
    url = row['URL']

    body += template %(pic, url, name, memb, addr1, addr2, addr3, info, mot, particip, oth)
            
out.write(body)
out.close()