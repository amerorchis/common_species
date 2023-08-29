if __name__ != "__main__":
  from api.counts import get_species_list, species_seen
    
def html():
    species_list = get_species_list()
    html = """
    <!DOCTYPE html>
<html>
  <head>
    <title>Species to Observe</title>
    <style>
      body {
        font-family: Verdana, sans-serif;
      }
    </style>
  </head>
  <body>
    <h3>&nbsp;&nbsp;&nbsp;25 Most Observed Species I Haven't Recorded</h3>
    """
    html += "<ol style='line-height: 1.5;'>"
    for species in species_list:
        html += "<li style='line-height: 1.5;'>{}</li>".format(species)
    html += "</ol>"
    seen = int(species_seen())
    html += f'\n&nbsp;&nbsp;Observed {seen} of 1,132 vascular plants in Glacier, {round((seen/1132)*100)}%.'
    html += """

  </body>
</html>
    """
    return html

if __name__ == "__main__":
  from counts import get_species_list, species_seen
  print(html())