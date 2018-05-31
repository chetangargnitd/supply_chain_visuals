from django.shortcuts import render

from django.http import JsonResponse
import json
import logging
from django.contrib import messages
from django.shortcuts import reverse, HttpResponseRedirect
from .csv_to_json_treemap import csv_to_tree
from .csv_to_json_force_directed import csv_to_force
from .csvtomatrixlayout import csv_to_matrix
from .csvtochord import csv_to_chord
# Create your views here.
import pandas as pd

def index(request):
	return render(request , 'visualizations/index.html')

def treemap(request):
    return render(request , 'visualizations/treemap.html')

def chord_diagram(request):
    return render(request , 'visualizations/chord_diagram.html')

def force_directed(request):
    return render(request , 'visualizations/force_directed_layout.html')

def matrix(request):
    return render(request , 'visualizations/matrix_layout.html')


def upload_csv(request):
    if "GET" == request.method:
        return render(request, "visualizations/index.html")
    # if not GET, then proceed
    try:
        csv_file1 = request.FILES["csv_file1"]
        csv_file2 = request.FILES["csv_file2"]
        if not csv_file1.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("visualizations:index"))
        if not csv_file2.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("visualizations:index"))
        # if file is too large, return
        if csv_file1.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file1.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("visualizations:index"))

        if csv_file2.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file2.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("visualizations:index"))

        node = pd.read_csv(csv_file1)
        link = pd.read_csv(csv_file2)
        print(node)
        print(link)
        # file_data = csv_file.read().decode("utf-8")
        #
        # lines = file_data.split("\n")
        # # loop over the lines and save them in db. If error , store as string and then display
        # for line in lines:
        #     fields = line.split(",")
        #     data_dict = {}
        #     data_dict["stageName"] = fields[0]
        #     data_dict["stageCost"] = fields[1]
        #     data_dict["stageClassification"] = fields[3]
        #     data_dict["avgDemand"] = fields[4]
        #     data_dict["stageTime"] = fields[8]
            # print(data_dict)
        csv_to_tree(node , link)
        csv_to_force(node , link)
        csv_to_matrix(node, link)
        csv_to_chord(node , link)

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("visualizations:treemap"))