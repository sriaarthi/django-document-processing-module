from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer
from django.core.files.storage import FileSystemStorage
from .Form_scanner import Form_scanner
from django.conf import settings
import time
import os


# Create your views here.
def index(request):
    customers = Customer.objects.all()
    return render(request, 'index.html', {'customers': customers})

# def uploadPage(request):
#     customers = Customer.objects.all()
#     return render(request, 'uploadPage.html', {'customers': customers})

def uploadPage(request):
    context={}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print(request.FILES.getlist('document'))
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        time.sleep(5)
        context['url'] = fs.url(name)
        file_path = settings.MEDIA_ROOT + "\\" + name
        print(file_path)
        textract_obj = Form_scanner()
        # file_name = textract_obj.word_to_pdf(file_name)
        key_map, value_map, block_map, table_map = textract_obj.get_kv_map(file_path)
        all_tables_list = list()
        # Get Key Value relationship
        kvs = textract_obj.get_kv_relationship(key_map, value_map, block_map, table_map, all_tables_list)
        tables = textract_obj.print_all_tables(all_tables_list)
        print("\n\n== FOUND KEY : VALUE pairs ===\n")
        print("KVS----", kvs)
        filename = os.path.splitext(uploaded_file.name)
        filename = filename[0]
        return render(request, 'store.html', {'Data': kvs, 'Tables':tables, 'Filename': filename})
    return render(request, 'uploadPage.html')

# def confirmPage(request):
#     context={}
#     uploaded_file = request.FILES['document']
#     print(request.FILES.getlist('document'))
#     fs = FileSystemStorage()
#     name = fs.save(uploaded_file.name, uploaded_file)
#     time.sleep(5)
#     context['url'] = fs.url(name)
#     file_path = settings.MEDIA_ROOT + "\\" + name
#     print(file_path)
#     textract_obj = Form_scanner()
#     # file_name = textract_obj.word_to_pdf(file_name)
#     key_map, value_map, block_map, table_map = textract_obj.get_kv_map(file_path)
#     all_tables_list = list()
#     # Get Key Value relationship
#     kvs = textract_obj.get_kv_relationship(key_map, value_map, block_map, table_map, all_tables_list)
#     textract_obj.print_all_tables(all_tables_list)
#     print("\n\n== FOUND KEY : VALUE pairs ===\n")
#     print("KVS----", kvs)
#     return render(request, 'store.html', {'Data': kvs})

    


