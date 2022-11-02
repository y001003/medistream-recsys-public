from utils import *

class CustomEvaluator:
    # relavence 모두 1로 동일하게 봄
    def _idcg(self, l):
        return sum((1.0 / np.log(i + 2) for i in range(l)))
    

    def __init__(self):
        self._idcgs = [self._idcg(i) for i in range(1000)]

    def _ndcg(self, gt, rec):
        dcg = 0.0
        for i, r in enumerate(rec):
            if r in gt:
                dcg += 1.0 / np.log(i + 2)

        return dcg / self._idcgs[len(gt)]
    
    def _entropy_diversity(self,rec_list):
        import six
        import math
        
        topn = len(rec_list[0]['items'])
        users = [i.get('id',None) for i in rec_list]
        sz = float(len(users)) * topn
        freq = {}
        for rec in rec_list:
            for r in rec['items']:
                freq[r] = freq.get(r, 0) + 1
        ent = -sum([v / sz * math.log(v / sz) for v in six.itervalues(freq)])
        return ent

    def _eval(self, gt_list, rec_list):
        gt_dict = {g["id"]: g for g in gt_list}
        ndcg_score = 0.0

        for rec in rec_list:
            gt = gt_dict[rec["id"]]
            ndcg_score += self._ndcg(gt["items"], rec["items"])


        ndcg_score = ndcg_score / len(rec_list)
        ent = self._entropy_diversity(rec_list)
        
        return ndcg_score, ent

    def evaluate(self, gt_list, rec_list):
        try:
            ndcg_score, ent_score = self._eval(gt_list, rec_list)
            print(f"NDCG: {ndcg_score:.6}")
            print(f"Entropy Diversity: {ent_score:.6} ")
        except Exception as e:
            print(e)