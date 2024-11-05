import os
import re
import math
from collections import defaultdict

class BM25:
    def __init__(self, docs, term_freq, total_number_of_docs, query):
        self.docs = docs
        self.query = query
        self.term_freq = term_freq

        self.title_weight = 1.0
        self.body_weight = 0.05
        self.b25title = 0.5
        self.b25body = 0.9
        self.k1 = 2.0
        self.pageRank_lambda = 0.8
        self.pageRank_lambda_prime = 0.9
        self.total_number_of_docs = total_number_of_docs

        # BM25 storages
        self.lengths = {} 
        self.avg_lengths = {} 
        self.pagerank_scores = {}
        
        # Calculate average lengths
        self.calc_average_lengths()

    def calc_average_lengths(self):
        total_title_length = 0.0
        total_body_length = 0.0
        count = 0
        for index, doc in enumerate(self.docs):
            title_length = doc["TITLE_LENGTH"]
            body_length = doc["BODY_LENGTH"]

            self.lengths[index] = {
                "title": title_length,
                "body": body_length
            }

            total_title_length += title_length
            total_body_length += body_length
            count += 1

            pagerank_score = self.pageRank_lambda_prime * self.pagerank_scores.get(index, 0.0)
            self.pagerank_scores[index] = pagerank_score

        self.avg_lengths["title"] = total_title_length / count if count > 0 else 0.0
        self.avg_lengths["body"] = total_body_length / count if count > 0 else 0.0

    def get_docs_with_query(self, term):
        count = sum(1 for doc in self.docs if term in doc["BODY_COUNT"] or term in doc["TITLE"].lower().split())
        return count

    def get_num_of_docs(self):
        return self.total_number_of_docs
    
    def get_idf(self, term):
        docs_containing_term = self.get_docs_with_query(term)
        if docs_containing_term <= 0:
            return 1.0
        idf = math.log(self.get_num_of_docs() / docs_containing_term)
        if idf <= 0:
            idf = 1.0
        return idf

    def get_net_score(self, tfs, query, tf_query, doc):
        score = 0.0
        for term in query.query_words:
            Wf = self.title_weight if term in tfs.get("title", {}) else self.body_weight
            ftf = tfs.get("title", {}).get(term, 0.0) + tfs.get("body", {}).get(term, 0.0)
            idf = self.get_idf(term)

            if ftf > 0:
                pagerank_score = math.log(1 + self.pagerank_scores.get(doc, 0.0))
                score += (Wf * ftf) / (self.k1 + ftf * Wf) * idf + self.pageRank_lambda * pagerank_score
            #print(f"Term: {term}, Wf: {Wf}, ftf: {ftf}, idf: {idf}, Score: {score}")
        return score

    def normalize_tfs(self, tfs, doc, query):
        for tf_type in ["title", "body"]:
            length = self.lengths[doc][tf_type]
            avg_length = self.avg_lengths[tf_type]
            Bf = self.b25title if tf_type == "title" else self.b25body

            for term in tfs.get(tf_type, {}).keys():
                raw_tf = tfs[tf_type][term]
                normalized_tf = raw_tf / ((1 - Bf) + Bf * (length / avg_length))
                tfs[tf_type][term] = normalized_tf

    def score_documents(self):
        scored_docs = []
        tf_query = defaultdict(int)
    
        for term in self.query.query_words:
            tf_query[term] += 1

        for index, doc in enumerate(self.docs):
            term_frequencies = {
                "title": defaultdict(int),
                "body": doc["BODY_COUNT"]
            }
            for term in doc["TITLE"].lower().split():
                term_frequencies["title"][term] += 1
            
            self.normalize_tfs(term_frequencies, index, self.query)
            score = self.get_net_score(term_frequencies, self.query, tf_query, index)
            scored_docs.append((doc, score))
    
        return scored_docs
