import os
size=0
for path, dirs, files in os.walk('Downloads\\'):
                for f in files:
                    fp = os.path.join(path, f)
                    size += os.path.getsize(fp)
print(size)