# http://data.noahlab.com.hk/conversation/
POST_TXT_PATH = '/home/cai/Downloads/weibo_data/post.index'
RESPONSE_TXT_PATH = '/home/cai/Downloads/weibo_data/response.index'
PAIR_PATH = '/home/cai/Downloads/weibo_data/original.pair'

post_dict = {}
response_dict = {}
pair_dict = {}


def read_pairs():
    with open(POST_TXT_PATH, 'r') as f:
        for line in f.readlines():
            iid = line.split("##")[0]
            line = line.replace(iid+"##", "")
            post_dict[iid] = line.strip()

    with open(RESPONSE_TXT_PATH, 'r') as f:
        for line in f.readlines():
            iid = line.split("##")[0]
            line = line.replace(iid+"##", "")
            response_dict[iid] = line.strip()

    with open(PAIR_PATH, 'r') as f:
        for line in f.readlines():
            post_id, response_ids = line.split(":")
            response_ids = map(str.strip, response_ids.split(","))
            pair_dict[post_id] = response_ids

def get_pari():
    for post_id, response_id in pair_dict.items():
        print 'post:', post_dict[post_id].replace(' ','')
        for id in response_id:
            print 'response', response_dict[id]

        break

read_pairs()
# get_pari()







