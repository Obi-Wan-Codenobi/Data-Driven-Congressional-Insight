import os
import re
import math
from collections import defaultdict
from .document import Document
from .dumbyloader import Query
from utils.tftypes import TFTYPES

class BM25:
    def __init__(self, docs, docs_with_term, total_number_of_docs, query):
        self.docs = docs
        self.query = query
        self.docs_with_term = docs_with_term

        self.title_weight = 0.70905
        self.body_weight = 0.555551
        self.b25title = 0.46
        self.b25body = 0.55
        self.k1 = 1.5
        self.page_rank_lambda = 0.8
        self.page_rank_lambda_prime = 0.9
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
            title_length = doc.title_length
            body_length = doc.body_length

            self.lengths[doc] = {
                TFTYPES[0]: title_length,
                TFTYPES[1]: body_length
            }

            total_title_length += title_length
            total_body_length += body_length
            count += 1

            pagerank_score = self.get_pagerank_score(doc)
            self.pagerank_scores[index] = pagerank_score

        self.avg_lengths[TFTYPES[0]] = total_title_length / count if count > 0 else 0.0
        self.avg_lengths[TFTYPES[1]] = total_body_length / count if count > 0 else 0.0
    
    def get_pagerank_score(self, doc):
        path = doc.file_path
        file_type_regex = re.search(r'tmp\/BILLS-\d+([a-zA-Z]+).*?.txt', path)
        if file_type_regex is None:
            return 0.0
        
        last_group_index = file_type_regex.lastindex
        pagerank = file_type_regex.group(last_group_index)
        
        if pagerank =="s":
            return 8.0
        elif pagerank=="hr":
            return 7.0
        elif pagerank=="sres":
            return 6.0
        elif pagerank=="sconres":
            return 5.0
        elif pagerank=="sjres":
            return 4.0
        elif pagerank=="hres":
            return 3.0
        elif pagerank=="hconres":
            return 2.0
        elif pagerank=="hjres":
            return 1.0

        return 0.0
        

    def get_net_score(self, tfs, query, tf_query, doc):
        score = 0.0

        for term in query.query_words:
            score_title = tfs.get(TFTYPES[0], {}).get(term, 0.0)
            score_body = tfs.get(TFTYPES[1], {}).get(term, 0.0)
            query_weight = tf_query.get(term)

            docs_with_term = float(self.docs_with_term.get(term,0))
            idf = math.log(self.total_number_of_docs / (docs_with_term if docs_with_term > 0 else 1))

            norm_title = (score_title * self.title_weight) / (self.k1 + score_title)
            norm_body = (score_body * self.body_weight) / (self.k1 + score_body)

            if query_weight is not None:
                score += (norm_title + norm_body) * idf * query_weight

        score += (self.page_rank_lambda * (self.pagerank_scores.get(doc,0.0) / (self.page_rank_lambda_prime + self.pagerank_scores.get(doc, 0.0))))

        return score


    def normalize_tfs(self, tfs, doc):
        for tf_type in TFTYPES:
            length = self.lengths[doc][tf_type]
            avg_length = self.avg_lengths[tf_type]
            Bf = self.b25title if tf_type == "title" else self.b25body

            for term in tfs.get(tf_type, {}).keys():
                raw_tf = tfs[tf_type][term]
                normalized_tf = raw_tf / ((1 - Bf) + Bf * (length / avg_length))
                tfs[tf_type][term] = normalized_tf

    def get_query_freq(self, q):
        tf_query = defaultdict(float)

        #raw term frequencies
        for word in q.query_words:
            tf_query[word.lower()] += 1

        # Weight each of the terms using the IDF value
        for key, tf in tf_query.items():
            docs_with_term_count = float(self.docs_with_term.get(key, 0))
            idf = math.log((self.total_number_of_docs if docs_with_term_count > 0 else 1) / (docs_with_term_count if docs_with_term_count > 0 else 1))

            tf_query[key] = tf * idf if idf > 0 else tf

        return dict(tf_query) 
    
    def get_title_map(self, d: Document) -> dict:
        title_map = {}

        if d.title is not None:
            title_words = d.title.lower().split()
            for title_word in title_words:
                title_map[title_word] = title_map.get(title_word, 0) + 1

        return title_map


    def get_doc_term_freqs(self, d: Document, q: Query) -> dict:
        tfs = {TFTYPES[0]: {}, TFTYPES[1]: {}}
        title_map = self.get_title_map(d)

        for query_word in q.query_words:
            word = query_word.lower()
            
            if d.body_hits is None:
                d.debug_str = "body_hits is null"
            else:
                word_positions = d.body_hits.get(word)
                prev_word_count = tfs[TFTYPES[1]].get(word)
                if word_positions is not None:
                    tfs[TFTYPES[1]][word] = len(word_positions) + (prev_word_count if prev_word_count is not None else 0)

            title_count = title_map.get(word)
            if title_count is not None:
                tfs[TFTYPES[0]][word] = float(title_count)

        return tfs
        
    def score_documents(self):
        scored_docs = []
        tf_query = self.get_query_freq(self.query)
        
        for doc in self.docs:
            tfs = self.get_doc_term_freqs(doc, self.query)
            self.normalize_tfs(tfs, doc)
            score = self.get_net_score(tfs, self.query, tf_query, doc)
            scored_docs.append((doc, score))
    
        return scored_docs
