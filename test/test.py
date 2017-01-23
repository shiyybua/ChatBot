# -*- coding: utf-8 -*-

import re

string = "回复@EVA_LuckyCharm:[害羞]//@EVA_LuckyCharm:[爱你]//@CodyKarey:回复@停转的牧马:I was! But dat coffee!!!! [哈哈]//@停转的牧马:you look so tired[困]"


re_t = r'(回复@|@).+?[\s:]'
one = re.sub(re_t, ' ', string)
print one

re_t = r'\[.*?\]'

one = re.sub(re_t, ' ', one)
print one

print one.replace("//",' ')
