import boto3
session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
)
bucket_name = 'ee891ff0c591-fat-cloud'

# Загрузить объекты в бакет

## Из строки
s3.put_object(Bucket=bucket_name, Key='object_name', Body='TEST')

## Из файла
s3.upload_file('main.py', bucket_name, 'py_script.py')
s3.upload_file('main.py', bucket_name, 'script/py_script.py')

# Получить список объектов в бакете
for key in s3.list_objects(Bucket=bucket_name)['Contents']:
    print(key['Key'])

# Удалить несколько объектов
# forDeletion = [{'Key':'object_name'}, {'Key':'script/py_script.py'}]
# response = s3.delete_objects(Bucket='bucket-name', Delete={'Objects': forDeletion})

# Получить объект
get_object_response = s3.get_object(Bucket=bucket_name,Key='py_script.py')
print(get_object_response['Body'].read())