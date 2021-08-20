def write_dept_view(dept_dic):
    f = open ("training/templates/training/stats/dept.html","w")
    f.write("<!doctype html>\n")
    f.write("<html lang=\"en\">\n")
    f.write("<head>\n")
    f.write("   <meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n")
    f.write("   <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\">\n")
    f.write("   <title>ECharts</title>\n")
    f.write("   {% load static %}\n")
    f.write("   <script src=\"{% static 'echarts.min.js'%}\"></script>\n")
    f.write("</head>\n")
    f.write("<body>\n")
    f.write("<nav class=\"navbar navbar-light\" style=\"background-color: #e3f2fd;\"> <span class=\"navbar-brand mb-0 h1\"> >>> Training >>> Stat Page >> Department</span></nav>\n")
    f.write("<div id=\"main\" style=\"width: 1700px;height:600px;\"></div>\n")
    f.write("<script type=\"text/javascript\">\n")
    f.write("   var myChart = echarts.init(document.getElementById('main'));\n")
    f.write("   option = { xAxis: {\n")
    f.write("                 type:'category',\n")
    f.write("                 data:[")
    key_number = len(dept_dic)
    write_counter = 0
    for key in dept_dic.keys():
        if write_counter < key_number - 1:
            f.write("\"" + key +"\",")
            write_counter = write_counter + 1
        else:
            f.write("\"" + key + "\"")
            write_counter = 0
    f.write("]},\n")
    f.write("              yAxis:{\n")
    f.write("                   type:'value'},\n")
    f.write("                   series:[{data:[")
    for value in dept_dic.values():
        if write_counter < key_number -1:
            f.write(str(value) + ",")
            write_counter = write_counter + 1
        else:
            f.write(str(value))
            write_counter = 0
    f.write("                   ],\n")
    f.write("                   type:'bar'}]\n")
    f.write("           };\n")
    f.write("   myChart.setOption(option);\n")
    f.write("</script>\n")
    f.write("   <button class = \"btn btn-outline-dark\" onclick=\"location.href = '/training/stat.do?$ACTION=list'\">Go back to stat page</button>\n")
    f.write("</body>\n")
    f.write("</html>\n")
    f.close()

def write_date_view(date_dic):
    f = open ("training/templates/training/stats/date.html","w")
    f.write("<!doctype html>\n")
    f.write("<html lang=\"en\">\n")
    f.write("<head>\n")
    f.write("   <meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n")
    f.write("   <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\">\n")
    f.write("   <title>ECharts</title>\n")
    f.write("   {% load static %}\n")
    f.write("   <script src=\"{% static 'echarts.min.js'%}\"></script>\n")
    f.write("</head>\n")
    f.write("<body>\n")
    f.write("<nav class=\"navbar navbar-light\" style=\"background-color: #e3f2fd;\"> <span class=\"navbar-brand mb-0 h1\"> >>> Training >>> Stat Page >> Department</span></nav>\n")
    f.write("<div id=\"main\" style=\"width: 1700px;height:600px;\"></div>\n")
    f.write("<script type=\"text/javascript\">\n")
    f.write("   var myChart = echarts.init(document.getElementById('main'));\n")
    f.write("   option = { xAxis: {\n")
    f.write("                 type:'category',\n")
    f.write("                 data:[")
    key_number = len(date_dic)
    write_counter = 0
    dict_items = date_dic.items()
    sorted_items = sorted(dict_items)
    for key in sorted_items:
        if write_counter < key_number - 1:
            f.write("\"" + key[0] +"\",")
            write_counter = write_counter + 1
        else:
            f.write("\"" + key[0] + "\"")
            write_counter = 0
    f.write("]},\n")
    f.write("              yAxis:{\n")
    f.write("                   type:'value'},\n")
    f.write("                   series:[{data:[")
    for value in sorted_items:
        if write_counter < key_number -1:
            f.write(str(value[1]) + ",")
            write_counter = write_counter + 1
        else:
            f.write(str(value[1]))
            write_counter = 0
    f.write("                   ],\n")
    f.write("                   type:'bar'}]\n")
    f.write("           };\n")
    f.write("   myChart.setOption(option);\n")
    f.write("</script>\n")
    f.write("   <button class = \"btn btn-outline-dark\" onclick=\"location.href = '/training/stat.do?$ACTION=list'\">Go back to stat page</button>\n")
    f.write("</body>\n")
    f.write("</html>\n")
    f.close()

def write_level_view(level_dic):
    f = open ("training/templates/training/stats/level.html","w")
    f.write("<!doctype html>\n")
    f.write("<html lang=\"en\">\n")
    f.write("<head>\n")
    f.write("   <meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n")
    f.write("   <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\">\n")
    f.write("   <title>ECharts</title>\n")
    f.write("   {% load static %}\n")
    f.write("   <script src=\"{% static 'echarts.min.js'%}\"></script>\n")
    f.write("</head>\n")
    f.write("<body>\n")
    f.write("<nav class=\"navbar navbar-light\" style=\"background-color: #e3f2fd;\"> <span class=\"navbar-brand mb-0 h1\"> >>> Training >>> Stat Page >> Department</span></nav>\n")
    f.write("<div id=\"main\" style=\"width: 1700px;height:600px;\"></div>\n")
    f.write("<script type=\"text/javascript\">\n")
    f.write("   var myChart = echarts.init(document.getElementById('main'));\n")
    f.write("   option = { xAxis: {\n")
    f.write("                 type:'category',\n")
    f.write("                 data:[")
    key_number = len(level_dic)
    write_counter = 0
    dict_items = level_dic.items()
    sorted_items = sorted(dict_items)
    for key in sorted_items:
        if write_counter < key_number - 1:
            f.write("\"" + str(key[0]) +"\",")
            write_counter = write_counter + 1
        else:
            f.write("\"" + str(key[0]) + "\"")
            write_counter = 0
    f.write("]},\n")
    f.write("              yAxis:{\n")
    f.write("                   type:'value'},\n")
    f.write("                   series:[{data:[")
    for value in sorted_items:
        if write_counter < key_number -1:
            f.write(str(value[1]) + ",")
            write_counter = write_counter + 1
        else:
            f.write(str(value[1]))
            write_counter = 0
    f.write("                   ],\n")
    f.write("                   type:'bar'}]\n")
    f.write("           };\n")
    f.write("   myChart.setOption(option);\n")
    f.write("</script>\n")
    f.write("   <button class = \"btn btn-outline-dark\" onclick=\"location.href = '/training/stat.do?$ACTION=list'\">Go back to stat page</button>\n")
    f.write("</body>\n")
    f.write("</html>\n")
    f.close()

def write_age_view(age_dic):
    f = open ("training/templates/training/stats/age.html","w")
    f.write("<!doctype html>\n")
    f.write("<html lang=\"en\">\n")
    f.write("<head>\n")
    f.write("   <meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n")
    f.write("   <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\">\n")
    f.write("   <title>ECharts</title>\n")
    f.write("   {% load static %}\n")
    f.write("   <script src=\"{% static 'echarts.min.js'%}\"></script>\n")
    f.write("</head>\n")
    f.write("<body>\n")
    f.write("<nav class=\"navbar navbar-light\" style=\"background-color: #e3f2fd;\"> <span class=\"navbar-brand mb-0 h1\"> >>> Training >>> Stat Page >> Department</span></nav>\n")
    f.write("<div id=\"main\" style=\"width: 1700px;height:600px;\"></div>\n")
    f.write("<script type=\"text/javascript\">\n")
    f.write("   var myChart = echarts.init(document.getElementById('main'));\n")
    f.write("   option = { xAxis: {\n")
    f.write("                 type:'category',\n")
    f.write("                 data:[")
    f.write("'20-29','30-39','40-49','50-59']},\n")
    f.write("              yAxis:{type:'value'},\n")
    f.write("                     series:[\n")
    f.write("                         {data:[")
    key_number = len(age_dic)
    print(key_number)
    write_counter = 0
    dict_items = age_dic.items()
    sorted_items = sorted(dict_items)
    for value in sorted_items:
        if write_counter < key_number -1:
            f.write(str(value[1]) + ",")
            write_counter = write_counter + 1
        else:
            f.write(str(value[1]))
    f.write("                          ],\n")
    f.write("                          type:'bar'}]\n")
    f.write("           };\n")
    f.write("   myChart.setOption(option);\n")
    f.write("</script>\n")
    f.write("   <button class = \"btn btn-outline-dark\" onclick=\"location.href = '/training/stat.do?$ACTION=list'\">Go back to stat page</button>\n")
    f.write("</body>\n")
    f.write("</html>\n")
    f.close()

def write_min_view(min_list,name_list):
    f = open ("training/templates/training/stats/min.html","w")
    f.write("<!doctype html>\n")
    f.write("<html lang=\"en\">\n")
    f.write("<head>\n")
    f.write("   <meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n")
    f.write("   <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\">\n")
    f.write("   <title>ECharts</title>\n")
    f.write("   {% load static %}\n")
    f.write("   <script src=\"{% static 'echarts.min.js'%}\"></script>\n")
    f.write("</head>\n")
    f.write("<body>\n")
    f.write("<nav class=\"navbar navbar-light\" style=\"background-color: #e3f2fd;\"> <span class=\"navbar-brand mb-0 h1\"> >>> Training >>> Stat Page >> Department</span></nav>\n")
    f.write("<div id=\"main\" style=\"width: 1700px;height:600px;\"></div>\n")
    f.write("<script type=\"text/javascript\">\n")
    f.write("   var myChart = echarts.init(document.getElementById('main'));\n")
    f.write("   option = { xAxis: {\n")
    f.write("                 type:'category',\n")
    f.write("                 data:[")
    write_counter = 0
    key_number = 10
    for value in name_list:
        if write_counter < key_number -1:
            f.write("\"" + str(value) + "\"" + ",")
            write_counter = write_counter + 1
        else:
            f.write( "\"" + str(value) + "\"")
    f.write("]},\n")
    f.write("              yAxis:{\n")
    f.write("                   type:'value'},\n")
    f.write("                   series:[{data:[")
    write_counter = 0
    for value in min_list:
        if write_counter < key_number -1:
            f.write(str(value) + ",")
            write_counter = write_counter + 1
        else:
            f.write(str(value))
    f.write("                   ],\n")
    f.write("                   type:'bar'}]\n")
    f.write("           };\n")
    f.write("   myChart.setOption(option);\n")
    f.write("</script>\n")
    f.write("   <button class = \"btn btn-outline-dark\" onclick=\"location.href = '/training/stat.do?$ACTION=list'\">Go back to stat page</button>\n")
    f.write("</body>\n")
    f.write("</html>\n")
    f.close()