import math
from collections import defaultdict



class BM25:
    def __init__(self, utils, query):
        self.utils = utils
        self.query = query

        # Weights and parameters 
        # continue to develop as documents grow!!
        self.title_weight = 1.0
        self.body_weight = 0.05
        self.b25title = 0.5
        self.b25body = 0.9
        self.k1 = 2.0
        self.pageRank_lambda = 0.8
        self.pageRank_lambda_prime = 0.9

        # bm25 storages
        self.lengths = {}
        self.avg_lengths = {}
        self.pagerank_scores = {}

        # Calculate average lengths
        self.calc_average_lengths()

    def calc_average_lengths(self):
        total_title_length = 0.0
        total_body_length = 0.0
        count = 0

        for docs in self.query_dict.values():
            for doc in docs.values():
                title_length = len(doc.title.split()) if doc.title else 0
                body_length = len(doc.body_hits) if doc.body_hits else 0

                self.lengths[doc] = {
                    "title": title_length,
                    "body": body_length
                }

                total_title_length += title_length
                total_body_length += body_length
                count += 1

                # PageRank score handling (example logic, modify as needed)
                pagerank_score = self.pageRank_lambda_prime * self.pagerank_scores.get(doc, 0.0)
                self.pagerank_scores[doc] = pagerank_score

        self.avg_lengths["title"] = total_title_length / count if count > 0 else 0.0
        self.avg_lengths["body"] = total_body_length / count if count > 0 else 0.0


    # TODO 
    #get_num_of docs needs to be filled in
    #get_docs_with_query needs to be filled out
    def get_idf(self, term):
        docs_containing_terms =  get_docs_with_query(self, term)
        idf = math.log(get_num_of_docs() / docs_containing_terms)
        return idf

    def get_docs_with_query(self, term):
        #to be included
        pass   
    def get_num_of_docs():
        #TODO
        pass

    def get_net_score(self, tfs, query, tf_query, doc):
        score = 0.0

        for term in query.query_words:
            Wf = self.title_weight if term in tfs.get("title", {}) else self.body_weight
            ftf = (tfs.get("title", {}).get(term, 0.0) + tfs.get("body", {}).get(term, 0.0))
            idf = self.get_idf(term)

            pagerank_score = math.log(1 + self.pagerank_scores.get(doc, 0.0))

            score += (Wf * ftf) / (self.k1 + ftf * Wf) * idf + self.pageRank_lambda * pagerank_score

        return score

    def normalize_tfs(self, tfs, doc, query):
        for tf_type in ["title", "body"]:
            length = self.lengths[doc][tf_type]
            avg_length = self.avg_lengths[tf_type]
            Bf = self.btitle if tf_type == "title" else self.bbody

            for term in tfs.get(tf_type, {}).keys():
                raw_tf = tfs[tf_type][term]
                normalized_tf = raw_tf / ((1 - Bf) + Bf * (length / avg_length))
                tfs[tf_type][term] = normalized_tf

    

