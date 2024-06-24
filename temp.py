from ratio import get_video_recommendation
from folder import get_files_with_extension

flist = get_files_with_extension('ex', 'mp4')
for i in flist:
    print(get_video_recommendation(i))