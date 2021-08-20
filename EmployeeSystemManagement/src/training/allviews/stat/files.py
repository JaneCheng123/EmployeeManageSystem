def write_dept_view(dept_dic):
    f = open ("training/templates/training/stats/dept.html","w")
    f.write("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
    f.write("<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\">")
    f.write("<head><meta charset=\"utf-8\"><title>ECharts</title>")
    f.write("{% load static %}<script src=\"{% static 'echarts.min.js'%}\"></script></head><body>")
    f.write("<div id=\"main\" style=\"width: 1800px;height:600px;\"></div><script type=\"text/javascript\">")
    f.write("var myChart = echarts.init(document.getElementById('main'));")
    f.write("option = { xAxis: {type:'category',data:[")
    key_number = len(dept_dic)
    write_counter = 0
    for key in dept_dic.keys():
        if write_counter < key_number - 1:
            f.write("\"" + key +"\",")
            write_counter = write_counter + 1
        else:
            f.write("\"" + key + "\"")
            write_counter = 0
    f.write("]},yAxis:{type:'value'},series:[{data:[")
    for value in dept_dic.values():
        if write_counter < key_number -1:
            f.write(str(value) + ",")
            write_counter = write_counter + 1
        else:
            f.write(str(value))
            write_counter = 0
    f.write("],type:'bar'}]};myChart.setOption(option);</script><body></html>")
    f.write("<button class = \"btn btn-outline-dark\" onclick=\"location.href = '/training/stat.do?$ACTION=list'\">Go back to stat page</button>")
    f.write(" <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js\" integrity=\"")
    f.write("sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM\" crossorigin=\"anonymous\"></script> </body></html>")
    f.close()

def write_date_view(date_dic):
    f = open ("training/templates/training/stats/date.html","w")
    f.write("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
    f.write("<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\">")
    f.write("<head><meta charset=\"utf-8\"><title>ECharts</title>")
    f.write("{% load static %}<script src=\"{% static 'echarts.min.js'%}\"></script></head><body>")
    f.write("<div id=\"main\" style=\"width: 1000px;height:600px;\"></div><script type=\"text/javascript\">")
    f.write("var myChart = echarts.init(document.getElementById('main'));")
    f.write("option = { xAxis: {type:'category',data:[")
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
    f.write("]},yAxis:{type:'value'},series:[{data:[")
    for value in sorted_items:
        if write_counter < key_number -1:
            f.write(str(value[1]) + ",")
            write_counter = write_counter + 1
        else:
            f.write(str(value[1]))
            write_counter = 0
    f.write("],type:'bar'}]};myChart.setOption(option);</script><body></html>")
    f.write("<button class = \"btn btn-outline-dark\" onclick=\"location.href = '/training/stat.do?$ACTION=list'\">Go back to stat page</button>")
    f.write("<script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js\" integrity=\"")
    f.write("sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM\" crossorigin=\"anonymous\"></script> </body></html>")
    f.close()

def write_level_view(level_dic):
    f = open ("training/templates/training/stats/level.html","w")
    f.write("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
    f.write("<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\">")
    f.write("<head><meta charset=\"utf-8\"><title>ECharts</title>")
    f.write("{% load static %}<script src=\"{% static 'echarts.min.js'%}\"></script></head><body>")
    f.write("<div id=\"main\" style=\"width: 1000px;height:600px;\"></div><script type=\"text/javascript\">")
    f.write("var myChart = echarts.init(document.getElementById('main'));")
    f.write("option = { xAxis: {type:'category',data:[")
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
    f.write("]},yAxis:{type:'value'},series:[{data:[")
    for value in sorted_items:
        if write_counter < key_number -1:
            f.write(str(value[1]) + ",")
            write_counter = write_counter + 1
        else:
            f.write(str(value[1]))
            write_counter = 0
    f.write("],type:'line'}]};myChart.setOption(option);</script><body></html>")
    f.write("<button class=\"btn btn-outline-dark\" onclick=\"location.href = '/training/stat.do?$ACTION=list'\">Go back to stat page</button>")
    f.write(" <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js\" integrity=\"")
    f.write("sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM\" crossorigin=\"anonymous\"></script> </body></html>")
    f.close()

def write_age_view(age_dic):
    f = open ("training/templates/training/stats/age.html","w")
    f.write("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
    f.write("<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\">")
    f.write("<head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
    f.write("<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\">")
    f.write("<head><meta charset=\"utf-8\"><title>ECharts</title>")
    f.write("{% load static %}<script src=\"{% static 'echarts.min.js'%}\"></script></head><body>")
    f.write("<div id=\"main\" style=\"width: 1000px;height:600px;\"></div><script type=\"text/javascript\">")
    f.write("var myChart = echarts.init(document.getElementById('main'));")
    f.write("option = { xAxis: {type:'category',data:[")
    f.write("'20-29','30-39','40-49','50-59']},yAxis:{type:'value'},series:[{data:[")
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
    f.write("],type:'bar'}]};myChart.setOption(option);</script><body></html>")
    f.write("<button class=\"btn btn-outline-dark\" onclick=\"location.href = '/training/stat.do?$ACTION=list'\">Go back to stat page</button>")
    f.write(" <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js\" integrity=\"")
    f.write("sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM\" crossorigin=\"anonymous\"></script> </body></html>")
    f.close()

def write_min_view(min_list,name_list):
    f = open ("training/templates/training/stats/min.html","w")
    f.write("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
    f.write("<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\">")
    f.write("<head><meta charset=\"utf-8\"><title>ECharts</title>")
    f.write("{% load static %}<script src=\"{% static 'echarts.min.js'%}\"></script></head><body>")
    f.write("<div id=\"main\" style=\"width: 1000px;height:600px;\"></div><script type=\"text/javascript\">")
    f.write("var myChart = echarts.init(document.getElementById('main'));")
    f.write("option = { xAxis: {type:'category',data:[")
    write_counter = 0
    key_number = 10
    for value in name_list:
        if write_counter < key_number -1:
            f.write("\"" + str(value) + "\"" + ",")
            write_counter = write_counter + 1
        else:
            f.write( "\"" + str(value) + "\"")
    f.write("]},yAxis:{type:'value'},series:[{data:[")
    write_counter = 0
    for value in min_list:
        if write_counter < key_number -1:
            f.write(str(value) + ",")
            write_counter = write_counter + 1
        else:
            f.write(str(value))
    f.write("],type:'bar'}]};myChart.setOption(option);</script><body></html>")
    f.write("<button class=\"btn btn-outline-dark\" onclick=\"location.href = '/training/stat.do?$ACTION=list'\">Go back to stat page</button>")
    f.write(" <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js\" integrity=\"")
    f.write("sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM\" crossorigin=\"anonymous\"></script> </body></html>")
    f.close()