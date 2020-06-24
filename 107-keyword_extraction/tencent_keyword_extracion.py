from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.nlp.v20190408 import nlp_client, models 
try: 
    cred = credential.Credential("AKIDvbE19DTqAuPdsrgiWhGWVnrgFYMtBDAq", "wXs0xd2LK4btFRN3St3vYDccQyWprd64") 
    httpProfile = HttpProfile()
    httpProfile.endpoint = "nlp.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile) 

    req = models.KeywordsExtractionRequest()
    params = '{\"Num\":20,\"Text\":\"前两天新传研圈又炸了，为什么呢？因为女神出新书了，彭兰老师的新作品《新媒体用户研究：节点化、媒介化、赛博格化的人》已经上新，有新的成熟的受众研究这作品上新，对于学术研究当然是好事，可以体系化的思考当前媒介环境下用户的特征及其认知模式与行为路径。但是对于考研的同学却犯了难，其实大家根本不知道这本书讲的是什么。只是一味的跟风在思考“到底要不要买？”的问题。\"}'
    req.from_json_string(params)

    resp = client.KeywordsExtraction(req) 
    print(resp.to_json_string()) 

except TencentCloudSDKException as err: 
    print(err) 