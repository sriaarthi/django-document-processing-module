import boto3
import sys
import re
import json
import io,os
from PIL import Image
import base64
from pdf2image import convert_from_path
import glob
import comtypes.client
import sys

class Form_scanner():

    def word_to_pdf(self, file_name):
        ###########
        # Convert the file_name(.DOC) to (.PDF) and store in the current working directory
        # Both should have same filename
        wdFormatPDF = 17

        in_file = os.path.abspath(file_name)
        abs_path_split = in_file.split('.')
        abs_path_split[2] = 'pdf'
        out_file = '.'.join(abs_path_split)
        word = comtypes.client.CreateObject('Word.Application')
        doc = word.Documents.Open(in_file)
        doc.SaveAs(out_file, FileFormat=wdFormatPDF)
        doc.Close()
        word.Quit()

        return out_file

    def get_kv_map(self, file_name):

        #Removing the image files
        dir_name = '.'
        items = os.listdir(dir_name)

        for item in items:
            if item.endswith(".jpg"):
                os.remove(os.path.join(dir_name,item))
        # # #End of Removing

        # #Converting pages to .jpg
        pages = convert_from_path(file_name, 500)
        count = 1

        for page in pages:
            page.save('page_'+str(count)+'.jpg', 'JPEG')
    #End of Converting
            count += 1
        key_map = {}
        value_map = {}
        block_map = {}
        table_map = {}
        all_tables_list = list()


        for file_name in glob.glob('*.jpg'):
            with open(file_name, 'rb') as file:
                img_test = file.read()
                bytes_test = bytearray(img_test)
            print('Image loaded', file_name)

            # process using image bytes
            client = boto3.client('textract')
            response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['FORMS','TABLES'])

            # Get the text blocks
            blocks=response['Blocks']


            # get key and value maps
            for block in blocks:
                block_id = block['Id']
                block_map[block_id] = block
                if block['BlockType'] == "PAGE":
                    pass

                if block['BlockType'] == "CELL":
                    pass

                if block['BlockType'] == "LINE":
                    pass

                if block['BlockType'] == "WORD":
                    pass

                if block['BlockType'] == "KEY_VALUE_SET":
                    if 'KEY' in block['EntityTypes']:
                        key_map[block_id] = block
                    else:
                        value_map[block_id] = block

                elif block['BlockType'] == "TABLE":
                    table_map[block_id] = block
                        
        return key_map, value_map, block_map, table_map


    def get_kv_relationship(self, key_map, value_map, block_map, table_map, all_tables_list):
        kvs = {}
        for block_id, key_block in key_map.items():
            value_block = self.find_value_block(key_block, value_map)
            key = self.get_text(key_block, block_map)
            if "'" in key:
                key = key.replace("'",'')
            key = key.replace(':','').strip()
            val = self.get_text(value_block, block_map)
            val = val.strip()
            kvs[key] = val
        for table_block in table_map.values():
            tables = self.get_text(table_block, block_map, all_tables_list)

        return json.dumps(kvs)


    def find_value_block(self, key_block, value_map):
        for relationship in key_block['Relationships']:
            if relationship['Type'] == 'VALUE':
                for value_id in relationship['Ids']:
                    value_block = value_map[value_id]

        return value_block


    def get_text(self, result, blocks_map, all_tables_list=''):
        text = ''
        table_headings = list()
        table_values = list()
        values = list()
        output_table = dict()
        count = 1
        if 'Relationships' in result:
            for relationship in result['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        word = blocks_map[child_id]
                        if word['BlockType'] == 'CELL':
                            if 'Relationships' in word:
                                for relationship in word['Relationships']:
                                    if relationship['Type'] == 'CHILD':
                                        for child_id in relationship['Ids']:
                                            cell_word = blocks_map[child_id]
                                            text += cell_word['Text']+ ' '
                            
                            if word['RowIndex'] == 1: # Table Headings
                                table_headings.append(text)
                                text = ''
                            if word['RowIndex'] > 1: # Table Values
                                values.append(text + ' ')
                                text = ''
                                if len(values) == len(table_headings):
                                    table_values.append(values)
                                    values = []
                                    
                        if word['BlockType'] == 'WORD':
                            text += word['Text'] + ' '
                        if word['BlockType'] == 'LINE':
                            text  += word['Text'] + ' '
                        if word['BlockType'] == 'SELECTION_ELEMENT':
                            if word['SelectionStatus'] == 'SELECTED':
                                text += 'X '
                            if word['SelectionStatus'] != 'NOT_SELECTED':
                                text += ''

        #Mapping Column Names and its Values
        if result['BlockType'] == 'TABLE':
            for key in table_headings:
                append_list = list() #List containing the values according to the column index
                for value in table_values:
                    append_list.append(value[table_headings.index(key)])
                    output_table[key] = append_list
            self.store_all_tables(output_table, all_tables_list)
        #End of Mapping
                            
        return text

    def store_all_tables(self, output_table, all_tables_list):
         all_tables_list.append(output_table)

    def print_all_tables(self, all_tables_list):
        for table in all_tables_list:
            for key,val in table.items():
                print(key,end='\n')
                print(val,end='\n')
        return all_tables_list

    def print_kvs(self, kvs):
        for key, value in kvs.items():
            print(key, ":", value)

        decision = 'Y'
        while decision == "Y" or decision == "y":
            search_key = input("Key you want to search: ")
            if search_key in kvs.keys():
                print("Key found")
            else:
                print("Key not found")
            decision = input("Do you want to search(Y/N): ")

