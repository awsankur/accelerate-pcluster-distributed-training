from torchdata.datapipes.iter import IterableWrapper, S3FileLister, S3FileLoader

s3_prefixes = IterableWrapper(['s3://pcluster-ml-workshop/DeepPhenotype_PBMC_ImageSet_YSeverin/'])

dp_s3_urls = S3FileLister(s3_prefixes,request_timeout_ms=100,region='us-west-2')

dp_s3_files = S3FileLoader(dp_s3_urls)
for url, fd in dp_s3_files: # Start loading data
    data = fd.read()
    import pdb;pdb.set_trace()

#for d in dp_s3_urls:
#    print(d)

#import pdb;pdb.set_trace()

#dp_s3_urls = s3_prefixes.list_files_by_s3(request_timeout_ms=100)

#for d in dp_s3_urls:
#    import pdb;pdb.set_trace()

