from counts import get_species_list
    
def html():
    species_list = get_species_list()
    html = """
    <!DOCTYPE html>
<html>
  <head>
    <title>Species to Observe</title>
    <style>
      h3 {
        font-family: Verdana, sans-serif;
      }
    </style>
  </head>
  <body>
    <h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;25 Most Observed Species I Haven't Recorded</h3>
    """
    html = "<h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;25 Most Observed Species I Haven't Recorded</h3>\n"
    html += "<ol style='line-height: 1.5;'>"
    for species in species_list:
        html += "<li style='line-height: 1.5;'>{}</li>".format(species)
    html += "</ol>"
    html += """
  </body>
</html>
    """
    print(html)
    return html