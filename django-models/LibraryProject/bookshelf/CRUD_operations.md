obj = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
# object created succesfuly
obj = Book.objects.all()
# 1984, George Orwell, 1949
obj.title = 'Nineteen Eighty-Four'      
# Nineteen Eighty-Four 
obj.delete()
# object deleted successfuly